import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
GEMINI_API_KEY = st.secrets["GEMINI"]["api_key"]
MODEL = st.secrets["GEMINI"]["model"]

def generate(prompt):
    client = genai.Client(api_key=GEMINI_API_KEY)
    model = MODEL
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
    ]
    generate_content_config = types.GenerateContentConfig(response_mime_type="text/plain")

    response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response += chunk.text
    return response

# Streamlit UI
st.set_page_config(page_title="Ingenuity Sumakses AI Chatbot", page_icon="💬", layout="centered")

st.title("Sumakses AI Chatbot")

def update_response():
    if st.session_state.user_input.strip():
        with st.spinner("Fetching data from universe..."):
            st.session_state.response = generate(st.session_state.user_input)

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# User input
user_input = st.text_input("Ask me anything:", key="user_input")
if user_input:
    st.session_state.messages.append({"role": "user", "avatar": "./logos/froggy.jpg", "content": user_input})
    with st.chat_message("user", avatar="./logos/froggy.jpg"):
        st.markdown(user_input)

    with st.spinner("Fetching data from universe..."):
        response = generate(user_input)

    st.session_state.messages.append({"role": "assistant", "avatar": "./logos/kit.gif", "content": response})
    with st.chat_message("assistant", avatar="./logos/kit.gif"):
        st.markdown(response)
        # st.image("./logos/froggy.jpg", caption="AI's response mood 😂")

st.caption("Powered by Niña's Brain Cells 🧠")
