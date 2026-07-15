import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

try:
    from langchain_mistralai import ChatMistralAI
except Exception:  # pragma: no cover - graceful fallback for deployment issues
    ChatMistralAI = None

load_dotenv()

st.set_page_config(page_title="ROBO Chat", page_icon="🤖", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stSidebar"] {
        background: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "mood" not in st.session_state:
    st.session_state.mood = "friendly"

moods = ["friendly", "professional", "sarcastic", "funny", "romantic", "sad", "angry", "confused", "excited", "bored"]

st.title("🤖 ROBO Chat")
st.write("✨ created by Raman Yadav.")

with st.sidebar:
    st.header("🎭 Conversation Style")
    selected_mood = st.selectbox("Select mood", moods, index=moods.index(st.session_state.mood))
    st.session_state.mood = selected_mood

    st.divider()
    if st.button("🧹 Clear chat"):
        st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "🧑" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(f"{avatar} {message['content']}")

prompt = st.chat_input("💬 Type your message here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(f"🧑 {prompt}")

    def get_api_key():
        api_key = os.getenv("MISTRAL_API_KEY")
        if api_key:
            return api_key
        try:
            secrets = st.secrets
            if hasattr(secrets, "get"):
                value = secrets.get("MISTRAL_API_KEY")
                if value:
                    return str(value)
        except Exception:
            pass
        return ""

    api_key = get_api_key()

    if not api_key:
        reply = (
            "Live AI is currently unavailable because MISTRAL_API_KEY is not set. "
            "Add it in your hosting platform environment variables or in Streamlit Cloud Secrets as 'MISTRAL_API_KEY'."
        )
    elif ChatMistralAI is None:
        reply = "The chat model package is not available in this deployment environment."
    else:
        try:
            model = ChatMistralAI(api_key=api_key, model="mistral-large-latest", temperature=0.7, max_retries=2)
            system_prompt = f"You are a helpful assistant. Your conversation mood is {st.session_state.mood}."
            response = model.invoke([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
            reply = getattr(response, "content", str(response))
        except Exception as exc:
            reply = f"Sorry, I could not generate a reply right now: {exc}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(f"🤖 {reply}")

