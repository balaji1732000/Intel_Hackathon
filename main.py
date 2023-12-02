import streamlit as st
import winsound
import numpy as np
import time
import io
from PIL import Image
import pytesseract
import openai
import easyocr
from PyPDF2 import PdfReader
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os
# import asyncio
import textwrap
from datetime import datetime
from persist import persist, load_widget_state
from generate_response import response_function
from generate_response_azure import response_function_azure
from speech_func import Speech
# from speech_processing import Start_recording

# Create an instance of the Speech class
speech_functions = Speech()

load_dotenv()

azure_api_key = os.environ.get("AZURE_API_KEY")

# Initialize the OpenAI object with your API key
openai.api_type = "azure"
openai.api_base = "https://dwspoc.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = azure_api_key

# Define a persistent key for st.session_state.messages
messages_key = persist("messages")

# Initialize st.session_state.messages as a list if not already defined
st.session_state.messages = st.session_state.get(messages_key, [])


st.set_page_config(
    page_title="ByteZen Support",
    page_icon=":🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
    <style>
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


def main(stop_keyword="restart", exit_keyword="exit"):
      # Add a line break for extra space
    st.markdown("<h1 style='text-align: left;'>🖥️ IT Customer Support, Driven by Intel® Innovation.</h1>", unsafe_allow_html=True)
    # The rest of your code goes here
    #st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown("""
        <div style='position: absolute; z-index: -1; top: 0; left: 0; width: 100%; height: 100%;'>
            <img src='AI.jpg' style='object-fit: cover; width: 100%; height: 100%; opacity: 0.3;'/>
        </div>
    """, unsafe_allow_html=True)

    # Add a welcoming image or logo
    #st.image("AI.jpg")

    # Add a catchy headline
    st.header("Explore our AI IT Support Portal")

    # Add a brief description
    st.write(
    "Your gateway to expert assistance in IT technical support. Whether you have questions, face issues, or need help, our Intelligent Voice Assistant and Chat Assistance are here for you, available at your convenience.\n"
    "\nYou can ask our Intelligent Voice Assistant and Chat Assistance depending upon your convenience."
)
    #st.image("AI.jpg", caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")


    # # Display IT support-related content
    # st.subheader("Explore Our AI IT Support Services")

    # # Add content related to your IT services
    # st.markdown("Here's what AI Assistant offer to help you with your IT needs:")

    # # Service 1: Password Reset
    # st.markdown(
    #     "1. **Password Reset:** Forgot your password? No worries, Our Intelligent Virtual Assistant help you reset it."
    # )

    # # Service 2: Software Installation
    # st.markdown(
    #     "2. **Software Installation:** Need to install software on your computer? Intelligent Virtual Assistant will guide you through the process."
    # )

    # # Service 3: Network Troubleshooting
    # st.markdown(
    #     "3. **Network Troubleshooting:** Experiencing network issues? Our AI IT Expert will diagnose and fix the problem."
    # )

    # # Service 4: Hardware Support
    # st.markdown(
    #     "4. **Hardware Support:** Problems with your hardware? Let us know, and Our AI IT Expert provide solutions."
    # )

    # # Service 5: General IT Queries
    # st.markdown(
    #     "5. **General IT Queries:** Have questions about IT? Ask us anything, and Our IVA provide answers."
    # )

    # # Add a call-to-action or promotional content
    # st.subheader("Get Started Today!")

    # st.write(
    #     "Ready to get the IT support you need? Feel free to explore our Fully Functional AI IT Support and reach out to Our IVA Service whenever you're ready."
    # )

    # Add a button for users to take action
    if st.button("Contact Us"):
        # You can customize this action based on your application's needs
        st.write("Contact form or support contact information can go here.")


def Speech_support(stop_keyword="restart", exit_keyword="exit"):
    st.title("🤖 Intelligent Voice Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.sidebar.write("Settings")

    st.sidebar.selectbox("Choose Your Preferred Language", st.session_state["languages"], key=persist("language_name"))

    st.sidebar.write("Press the Start button and ask me a question. I will respond.")
    
    if st.sidebar.button("Start", key="speech_button"):
        st.session_state.should_exit = True

        st.sidebar.write(
            "Note:  You can start your question over by saying Restart during question input..."
        )  # Instruction section
        st.sidebar.write(
            "You can Stop the session by Clicking below 'Stop' Button"
        )  # Instruction section

        if st.sidebar.button("Stop", key="stop_button"):
            st.session_state.should_exit = True

        welcome_message = "Hi, I am MyLiva, How can I assist you today"

        st.markdown(
            f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; text-align: left; color: black;'>"
            f"{welcome_message}</div>",
            unsafe_allow_html=True,
        )

        speech_functions.text_to_speech_azure(welcome_message)
        # speech_functions.synthesize_and_play_speech(welcome_message)
        # speech_functions.text_to_speech_elevanlabs(welcome_message)
        
        output_folder = f'./Output/{datetime.now().strftime("%Y%m%d_%H%M%S")}/'
        os.makedirs(output_folder)

        while st.session_state.should_exit:
            st.text("🤖 Listening...")
            winsound.Beep(800, 200)  # Play a beep sound when ready for input

            # input_text = speech_functions.transcribe_audio()
            input_text = speech_functions.speech_to_text_azure()
            # input_text = await Start_recording(output_folder=output_folder)[0]['DisplayText']



            if not input_text:
                not_listening = "Your voice is not audible, can you say it again?"
                st.markdown(
                    f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; text-align: left; color: black;'>"
                    f"{not_listening}</div>",
                    unsafe_allow_html=True,
                )
                # speech_functions.synthesize_and_play_speech(not_listening)
                #speech_functions.text_to_speech_elevanlabs(not_listening)
                speech_functions.text_to_speech_azure(not_listening)
                continue
                
            wrapped_input = textwrap.fill(input_text, width=90)
            indented_input = "\n".join(
                [
                    "<div style='text-align: left;'>" + line + "</div>"
                    for line in wrapped_input.splitlines()
                ]
            )

            st.markdown(
                f"<div style='padding: 30px;'>"
                f"<div style='background-color: blue; padding: 10px; border-radius: 5px; color: white; text-align: left;'>"
                f"{indented_input}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

            if stop_keyword.lower() in input_text.lower():
                st.text("Restarting prompt...")
                st.session_state.messages = []
                continue

            # try:
            # response_text = response_function.generate_response(
            #     input_text, st.session_state.messages
            # )
            response_text = response_function_azure.generate_response_azure(
                input_text, st.session_state.messages
            )
            print(response_text)
            wrapped_response = textwrap.fill(response_text, width=70)
            indented_response = "\n".join(
                [
                    "<div style='text-align: left;'>" + line + "</div>"
                    for line in wrapped_response.splitlines()
                ]
            )

            st.markdown(
                f"<div style='background-color: #ADD8E6; padding: 10px; border-radius: 5px; text-align: left; color: black;'>"
                f"{indented_response}</div>",
                unsafe_allow_html=True,
            )

            speech_functions.text_to_speech_azure(response_text)
            # speech_functions.synthesize_and_play_speech(response_text)
            # speech_functions.text_to_speech_elevanlabs(response_text)
            st.session_state.messages.append(
                {"role": "user", "content": input_text}
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )

def image_upload_button():
    uploaded_image = None
    upload_button = st.button("📷 Upload Image")
    
    if upload_button:
        uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    return uploaded_image
    
def Chat_support():
    st.title("🤖 Intelligent Chat Support")

    st.sidebar.selectbox("Choose Your Preferred Language", st.session_state["languages"], key=persist("language_name"))

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("ai"):
            full_response = response_function_azure.generate_response_azure(
                prompt, st.session_state.messages
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

            # Implement letter-by-letter printing
            st.markdown(full_response)


def extract_text_from_image(image_bytes):
    try:
        # Initialize the OCR reader
        reader = easyocr.Reader(['en'])

        # Use EasyOCR to extract text from the image
        result = reader.readtext(image_bytes)

        # Extract and concatenate text from the result
        text = ' '.join([item[1] for item in result])

        return text
    except Exception as e:
        return str(e)


def image_support():
    st.title("📷 Image Support")

    # Image upload
    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

        # Perform OCR and extract text
        # Read the content of the uploaded file as bytes
        image_bytes = uploaded_file.read()

        text_result = extract_text_from_image(image_bytes)

        # Display the extracted text in a text area
        st.header("Extracted Text:")
        st.text_area("Text", text_result, height=200)


def automation_support():
    pass

def general_queries():
    st.sidebar.title("FAQ's")
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

    

if "page" not in st.session_state:
    # Initialize session state.
    st.session_state.update({
        # Default page.
        "page": "Home",

        "list": [],

        # Languages which you prefer
        "languages": ["English", "French", "Hindi", "Tamil"],
    })
    st.balloons()

page_names_to_funcs = {
    "Home": main,
    "🗣️SPEECH SUPPORT": Speech_support,
    "💬CHAT ASSIST": Chat_support,
    "📷IMAGE GUIDANCE": image_support,
    "❓GENERAL QUERIES": general_queries,
    "🤖AUTOMATION_SUPPORT": automation_support,
}

# Load widget state
load_widget_state()

demo_name = st.sidebar.selectbox("Choose Your Preference", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()


