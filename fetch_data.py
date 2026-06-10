import os
import requests
import pandas as pd


def fetch_and_save_data():

    BASE_URL = "https://api.vipunen.fi/api"

    resource = (
        "amm_opiskelijat_ja_tutkinnot_vuosi_tutkinto"
    )

    url = (
        f"{BASE_URL}/resources/{resource}/data"
    )

    response = requests.get(url)

    data = response.json()

    df = pd.DataFrame(data)

    df["tilastovuosi"] = pd.to_numeric(
        df["tilastovuosi"],
        errors="coerce"
    )

    df["opiskelijatLkm"] = pd.to_numeric(
        df["opiskelijatLkm"],
        errors="coerce"
    )

    df = df[df["tilastovuosi"] >= 2020]
    df = df[df["tilastovuosi"] <= 2025]


    df = df[
        df["tutkinto"] != "Tieto puuttuu"
    ]

    os.makedirs(
        "data",
        exist_ok=True
    )

    df.to_csv(
        "data/cleaned_data.csv",
        index=False
    )

    print("Data tallennettu.")


if __name__ == "__main__":
    fetch_and_save_data()