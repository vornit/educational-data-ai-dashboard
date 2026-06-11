---
title: Educational Data AI Dashboard
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: gradio
app_file: app.py
pinned: false
---

# Educational Data AI Dashboard

A lightweight AI-powered dashboard for analyzing Finnish vocational education data from the Vipunen API.

The application fetches student data, visualizes trends between years, and generates insights for decision-making using AI.

## Live Demo

A running version of the application is available at:

https://vornit-educational-data-ai-dashboard.hf.space

## Setup

Clone the repository:

```bash
git clone https://github.com/vornit/educational-data-ai-dashboard.git
cd educational-data-ai-dashboard
```


Create a `.env` file and set the following environment variables:

```env
OPENROUTER_API_KEY=your_api_key
APP_USERNAME=user
APP_PASSWORD=password
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