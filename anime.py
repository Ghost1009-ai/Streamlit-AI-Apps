import streamlit as st
import requests
import io
from PIL import Image

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/strangerzonehf/Flux-Animex-v2-LoRA"
headers = {"Authorization": "Bearer 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"}

# Function to query the Hugging Face API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

# Encapsulated Streamlit page function
def anime_page():
    st.title("AI Image Generator")
    st.write("Generate images using a Hugging Face model!")

    # User input
    prompt = st.text_input("Enter your image prompt:", "Astronaut riding a horse")

    # Generate button
    if st.button("Generate Image"):
        st.write("Generating image...")
        image_bytes = query({"inputs": prompt})

        if image_bytes:
            # Display the image
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption=f"Generated Image: {prompt}", use_container_width=True)
        else:
            st.error("Failed to generate the image.")
