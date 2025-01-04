import streamlit as st
import os
import shutil
from PIL import Image
import base64
from openai import OpenAI 
import os

## Set the API key and model name
MODEL="gpt-4o-mini"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Temporary directory for uploaded files
TMP_DIR = "tmp"
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

# Clear temporary folder on app start or rerun
def clear_tmp_directory():
    for file in os.listdir(TMP_DIR):
        file_path = os.path.join(TMP_DIR, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            st.error(f"Error clearing temporary files: {e}")

clear_tmp_directory()  # Call this at the start of the script

def save_uploaded_file(uploaded_file):
    """Save uploaded file to the tmp directory."""
    file_path = os.path.join(TMP_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def encode_image(image_path):
    """Encode image as a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

st.title("Math Operations from Images")

# File uploader
uploaded_file = st.file_uploader("Upload an image for math operations", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    # Save the uploaded file
    file_path = save_uploaded_file(uploaded_file)

    # Display the uploaded image
    st.image(file_path, caption="Uploaded Image", use_container_width=True)

    # Input for instructions
    instructions = st.text_area("Enter instructions for the operation")

    if st.button("Process Image"):
        if instructions.strip():
            # Encode image as base64
            base64_image = encode_image(file_path)

            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that responds in Markdown. Help me with my math homework!"},
                    {"role": "user", "content": [
                        {"type": "text", "text": "{instructions}"},
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"}
                        }
                    ]}
                ],
                temperature=0.0,
            )

            st.markdown(response.choices[0].message.content)
       
        else:
            st.warning("Please enter instructions for the operation.")
