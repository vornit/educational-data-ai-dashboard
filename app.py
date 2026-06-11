import os
import pandas as pd
import gradio as gr
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from openai import OpenAI

from fetch_data import fetch_and_save_data

if not os.getenv("OPENROUTER_API_KEY"):
    load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


if not os.path.exists(
    "data/cleaned_data.csv"
):

    print("Data not found.")
    print("Fetching data from Vipunen...")

    fetch_and_save_data()

    print("Data fetched.")


def load_data():

    df = pd.read_csv(
        "data/cleaned_data.csv"
    )

    return df


def get_top_5_fields(df, analysis_type):

    latest_year = df["tilastovuosi"].max()
    first_year = df["tilastovuosi"].min()

    latest_df = (
        df[df["tilastovuosi"] == latest_year]
        .groupby("tutkinto")["opiskelijatLkm"]
        .sum()
    )

    first_df = (
        df[df["tilastovuosi"] == first_year]
        .groupby("tutkinto")["opiskelijatLkm"]
        .sum()
    )

    if analysis_type == "Suosituimmat alat":

        result = (
            latest_df
            .sort_values(ascending=False)
            .head(5)
        )

    elif analysis_type == "Vähiten suositut alat":

        result = (
            latest_df
            .sort_values(ascending=True)
            .head(5)
        )

    elif analysis_type == "Nopeimmin kasvavat alat":

        combined = pd.DataFrame({
            "first": first_df,
            "latest": latest_df
        }).fillna(0)

        combined["change"] = (
            combined["latest"] - combined["first"]
        )

        result = (
            combined["change"]
            .sort_values(ascending=False)
            .head(5)
        )

    elif analysis_type == "Nopeimmin laskevat alat":

        combined = pd.DataFrame({
            "first": first_df,
            "latest": latest_df
        }).fillna(0)

        combined["change"] = (
            combined["latest"] - combined["first"]
        )

        result = (
            combined["change"]
            .sort_values(ascending=True)
            .head(5)
        )

    return result.index.tolist()


def prepare_dashboard(analysis_type):

    df = load_data()

    top_10_names = get_top_5_fields(
        df,
        analysis_type
    )

    trend_df = df[
        df["tutkinto"].isin(top_10_names)
    ]

    trend_df = (
        trend_df.groupby(
            ["tutkinto", "tilastovuosi"]
        )["opiskelijatLkm"]
        .sum()
        .reset_index()
    )

    pivot_df = (
        trend_df.pivot(
            index="tutkinto",
            columns="tilastovuosi",
            values="opiskelijatLkm"
        )
        .fillna(0)
        .astype(int)
        .reset_index()
    )

    pivot_df.columns = [
        "Tutkinto",
        *[
            f"Opiskelijamäärä ({year})"
            for year in pivot_df.columns[1:]
        ]
    ]

    fig, ax = plt.subplots(figsize=(12, 6))

    for tutkinto in top_10_names:

        temp = trend_df[
            trend_df["tutkinto"] == tutkinto
        ]

        ax.plot(
            temp["tilastovuosi"],
            temp["opiskelijatLkm"],
            marker="o",
            label=tutkinto
        )

    ax.set_title(analysis_type)

    ax.set_xlabel("Vuosi")
    ax.set_ylabel("Opiskelijamäärä")

    ax.set_xticks(
        sorted(trend_df["tilastovuosi"].unique())
    )

    ax.legend(
        bbox_to_anchor=(1.05, 1),
        loc="upper left"
    )

    plt.tight_layout()

    plt.close(fig)

    return pivot_df, fig


def generate_ai_analysis(analysis_type):

    df = load_data()

    top_5_names = get_top_5_fields(
        df,
        analysis_type
    )

    trend_df = df[
        df["tutkinto"].isin(top_5_names)
    ]

    summary = (
        trend_df.groupby(
            ["tutkinto", "tilastovuosi"]
        )["opiskelijatLkm"]
        .sum()
        .reset_index()
        .to_string(index=False)
    )

    prompt = f"""
    Olet koulutusalan data-analyytikko koulutuskuntayhtymä Gradia.

    Analysoi ammatillisen koulutuksen opiskelijamääriä vuosilta 2020–2025.

    Tarkasteltavana ovat top 5 {analysis_type.lower()}.

    Alat ovat tiedossa. Älä listaa niitä uudelleen.

    Kirjoita tiiviisti ja konkreettisesti.

    Kirjoita vastaukseen nämä osiot:

    - Tärkeimmät havainnot
    - Nosta esiin 2 tärkeintä muutosta opiskelijamäärissä.
    - Selityksen opiskelijamäärien muutoksiin.
    - Mainitse epävarmuus tarvittaessa.
    - Anna 2 konkreettista kehitysehdotusta johdolle.

    Pidä vastaus alle 300 sanassa.

    Data:
    {summary}
    """
    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENROUTER_MODEL"),
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Virhe AI-analyysin generoinnissa:\n\n{e}"

initial_analysis = "Suosituimmat alat"

initial_table, initial_chart = prepare_dashboard(
    initial_analysis
)


with gr.Blocks(title="Vipunen AI Dashboard") as app:

    gr.Markdown(
        """
        # Ammatillisten alojen opiskelijamäärät vuosilta 2020-2025
        """
    )

    analysis_dropdown = gr.Dropdown(
        choices=[
            "Suosituimmat alat",
            "Vähiten suositut alat",
            "Nopeimmin kasvavat alat",
            "Nopeimmin laskevat alat"
        ],
        value=initial_analysis,
        label="Analyysityyppi"
    )

    table_output = gr.Dataframe(
        value=initial_table,
        label="Opiskelijamäärät vuosittain"
    )

    chart_output = gr.Plot(
        value=initial_chart,
        label="Graafi"
    )

    analysis_dropdown.change(
        fn=prepare_dashboard,
        inputs=analysis_dropdown,
        outputs=[
            table_output,
            chart_output
        ]
    )

    gr.Markdown("## AI-analyysi")

    run_button = gr.Button(
        "Generoi AI-analyysi",
        variant="primary"
    )

    ai_output = gr.Markdown()

    def start_loading():
        return """
        <span style="font-size: 24px;">
        Generoidaan AI-analyysi...
        </span>
        """

    run_button.click(
        fn=start_loading,
        outputs=ai_output
    ).then(
        fn=generate_ai_analysis,
        inputs=analysis_dropdown,
        outputs=ai_output
    )


if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        auth=(
            os.getenv("APP_USERNAME"),
            os.getenv("APP_PASSWORD")
        )
    )