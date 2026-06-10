# Educational Data AI Dashboard

A lightweight AI-powered dashboard for analyzing Finnish vocational education data from the Vipunen API.

The application fetches student data, visualizes trends between years, and generates insights for decision-making using AI.

## Setup

Clone the repository:

```bash
git clone https://github.com/vornit/educational-data-ai-dashboard.git
cd educational-data-ai-dashboard
```


Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key
```

You can generate an API key at:

https://openrouter.ai/

## Running

### Running locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

The app will be available at:

```text
http://localhost:7860
```

### Running with Docker

Build the image:

```bash
docker build -t ai-dashboard .
```

Run the container:

```bash
docker run -p 7860:7860 --env-file .env ai-dashboard
```

The app will be available at:

```text
http://localhost:7860
```