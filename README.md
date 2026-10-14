# Multi-Agent Research System

**Discover → Extract → Synthesize → Review**

A basic Streamlit research assistant that searches the web with Tavily, extracts accessible pages with Requests and BeautifulSoup, drafts a report with a Groq chat model through LangChain, asks a separate critic call to review the draft, and attempts a separate revision call. It displays source URLs and lets users download the report.

## Deploy for free on Streamlit Community Cloud

1. Create a GitHub repository and put the project files at its root. Keep `.env` and API keys out of Git; `.gitignore` excludes `.env` and `.streamlit/secrets.toml`.
2. Sign in at [share.streamlit.io](https://share.streamlit.io) with GitHub, choose **Create app** → **Yup, I have an app**, then select your repository, branch, and `app.py` as the main file.
3. Open **Advanced settings** → **Secrets** and paste the TOML below, replacing the two key values with your own:

   ```toml
   GROQ_API_KEY = "your_groq_api_key"
   TAVILY_API_KEY = "your_tavily_api_key"
   GROQ_MODEL = "openai/gpt-oss-120b"
   ```

4. Save and deploy. Streamlit will provide a `*.streamlit.app` URL. The app reads keys from Cloud Secrets; locally it continues to read `.env`.

If you want the app publicly accessible but prefer not to publish the source code, use a **private GitHub repository** and change the app's visibility to public in its Sharing settings after deployment. Streamlit's documentation notes that private apps are invite-only and that an account can have only one private app at a time. If you make the repository public, the app is public by default. Never commit API keys.

Official guides: [Deploy an app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [Secrets management](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management), and [Share your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app).

## Run locally on Windows PowerShell

From the extracted project folder:

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
notepad .env
streamlit run app.py
```

In `.env`, set `GROQ_API_KEY`, `TAVILY_API_KEY`, and `GROQ_MODEL=openai/gpt-oss-120b`. Open the local URL printed by Streamlit (normally `http://localhost:8501`). Press **Ctrl+C** in PowerShell to stop the app.

## Requirements

- Python 3.10 or newer
- A [Groq API key](https://console.groq.com/keys)
- A [Tavily API key](https://app.tavily.com/)

## Workflow components

- **Search and Reader (`tools.py`)** — Tavily search plus Requests/BeautifulSoup extraction; inaccessible pages do not discard other sources.
- **Writer, Critic, and Revision (`agents.py`)** — separate LangChain/Groq calls for drafting, critique, and improvement.
- **Pipeline (`pipeline.py`)** — orchestrates the stages and preserves source URLs.
- **Frontend (`app.py`)** — shows progress, the report, critique, sources, and a Markdown download.
- **Configuration (`settings.py`)** — bridges local `.env` and Streamlit Community Cloud Secrets without printing credentials.

If extraction fails, the search snippet remains available and the source URL is preserved. If Tavily returns no usable results or an API key is missing, the app shows an error instead of inventing sources. Verify important claims against the linked sources.
