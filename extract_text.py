import easyocr
from PIL import Image

# def extract_text_from_image(image_path):
#     # Open the image from the file path
#     image = Image.open(image_path)

#     # Convert the PIL Image to text using easyocr
#     reader = easyocr.Reader(['en'])  # Language code for English
#     results = reader.readtext(image_path)  # Use image_path instead of image

#     extracted_text = ""
#     for result in results:
#         extracted_text += result[1] + "\n"

#     return extracted_text.strip()

def extract_text_from_image(image):
    reader = easyocr.Reader(['en'])  # Language code for English
    results = reader.readtext(image)

    extracted_text = ""
    for result in results:
        extracted_text += result[1] + "\n"
        print(extracted_text)

    return extracted_text.strip()


# Example usage
image_path = "download (2).png"
text_result = extract_text_from_image(image_path)
print(text_result)
