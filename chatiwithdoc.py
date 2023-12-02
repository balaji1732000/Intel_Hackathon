import os
import streamlit as st
import pickle
import time
from PyPDF2 import PdfReader
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.vectorstores import FAISS

import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

azure_api_key = os.environ.get("AZURE_API_KEY")

# Initialize the OpenAI object with your API key
openai.api_type = "azure"
openai.api_base = "https://dwspoc.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = azure_api_key

# Streamlit UI
st.title("DocBot: Chat with PDF and URL 📈")

# Sidebar for PDF upload
st.sidebar.title("Upload PDF Document")
document = st.sidebar.file_uploader("Select a PDF Document", type=["pdf"])

# Chat history for the document chat
chat_history = []

if document:
    # Handle PDF document
    pdf_reader = PdfReader(document)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

st.subheader("Chat with Document")
user_message = st.text_input("Question:", "")

if user_message and document:
    conversation = []

    for message in chat_history:
        conversation.append({"role": "system", "content": "You: " + message["user_message"]})
        conversation.append({"role": "assistant", "content": "Document:\n" + text})
        response = openai.ChatCompletion.create(
            engine="GPT4",
            messages=conversation,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        ai_responses.append(response.choices[0].message["content"])

    # Add the new user message to the chat history
    conversation.append({"role": "system", "content": "You: " + user_message})
    conversation.append({"role": "assistant", "content": "Document:\n" + text})
    response = openai.ChatCompletion.create(
        engine="GPT4",
        messages=conversation,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    ai_response = response.choices[0].message["content"]

    # Add the new user message to the chat history
    chat_history.append({"user_message": user_message})

    # Display AI response directly below the input field
    st.subheader("AI Response:")
    st.write(ai_response)
