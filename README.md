# Autogen Sandbox

Based on Autogen Getting Started: https://microsoft.github.io/autogen/docs/Getting-Started
and
https://www.youtube.com/watch?v=V2qZ_lgxTzg&list=PLp9pLaqAQbY2vUjGEVgz8yAOdJlyy3AQb

## Setup

```bash
conda create -n autogen python=3.11.4
conda activate autogen
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and populate variables

## IMPORTANT

Make sure Proxyman is running if `OPENAI_BASE_URL` in `.env` is set up to proxy through Proxyman.
