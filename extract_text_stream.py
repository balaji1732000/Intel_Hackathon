# import streamlit as st
# import easyocr
# from PIL import Image
# from io import BytesIO

# def extract_text_from_image(image_bytes):
#     try:
#         # Initialize the OCR reader
#         reader = easyocr.Reader(['en'])

#         # Use EasyOCR to extract text from the image
#         result = reader.readtext(image_bytes)

#         # Extract and concatenate text from the result
#         text = ' '.join([item[1] for item in result])

#         return text
#     except Exception as e:
#         return str(e)

# def main():
#     st.title("Image Text Extractor with EasyOCR")

#     # File uploader
#     uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

#     if uploaded_file is not None:
#         # Display the uploaded image
#         st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

#         # Perform OCR and extract text
#         # Read the content of the uploaded file as bytes
#         image_bytes = uploaded_file.read()

#         text_result = extract_text_from_image(image_bytes)
#         print(text_result)

#         # Display the extracted text
#         st.header("Extracted Text:")
#         st.text(text_result)

# if __name__ == "__main__":
#     main()

import streamlit as st
import easyocr
from PIL import Image
from io import BytesIO

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

def main():
    st.title("Image Text Extractor with EasyOCR")

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

if __name__ == "__main__":
    main()
