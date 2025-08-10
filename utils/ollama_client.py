
import os
import streamlit as st

try:
    import ollama
except ImportError:
    ollama = None

def ensure_client():
    if ollama is None:
        st.error("The 'ollama' package is not installed. Run: pip install ollama")
        st.stop()

def chat_call(model, messages, stream=True, options=None):
    ensure_client()
    base_url = os.getenv("OLLAMA_HOST") or os.getenv("OLLAMA_BASE_URL")
    if base_url:
        client = ollama.Client(host=base_url)
    else:
        client = ollama
    try:
        return client.chat(model=model, messages=messages, stream=stream, options=options or {})
    except ollama.ResponseError as e:
        st.error(f"Ollama error: {e.error}")
        st.info("Is the model you're trying to use pulled? Quick test in a terminal: `ollama run {model} 'hello'`")
        st.stop()
    except Exception as e:
        st.error(f"Error: Could not connect to Ollama. Please ensure it is running.")
        st.info(f"Tip: set OLLAMA_HOST to point at a remote server, for example http://localhost:11434. Details: {e}")
        st.stop()

def stream_response(events, container):
    text = ""
    for event in events:
        chunk = event.get("message", {}).get("content", "") or event.get("content", "") or ""
        if chunk:
            text += chunk
            container.write(text)
    return text
