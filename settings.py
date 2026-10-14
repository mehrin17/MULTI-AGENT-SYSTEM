"""Configuration bridge for local dotenv files and Streamlit Community Cloud secrets."""
from __future__ import annotations

import os
from collections.abc import Mapping

CONFIG_KEYS = ("GROQ_API_KEY", "TAVILY_API_KEY", "GROQ_MODEL")


def apply_streamlit_secrets(secrets: Mapping[str, object]) -> None:
    """Copy configured Streamlit secrets into missing environment variables only."""
    for name in CONFIG_KEYS:
        if os.getenv(name, "").strip():
            continue
        try:
            value = secrets.get(name)
        except Exception:
            continue
        if value is not None and str(value).strip():
            os.environ[name] = str(value).strip()


def load_streamlit_secrets() -> None:
    """Load Community Cloud secrets when available; local .env remains supported."""
    try:
        import streamlit as st
        secrets = st.secrets
    except Exception:
        # Locally, users normally configure .env; Streamlit may have no secrets.toml.
        return
    apply_streamlit_secrets(secrets)
