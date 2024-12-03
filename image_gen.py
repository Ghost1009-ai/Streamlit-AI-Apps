import streamlit as st
import requests
import io
from PIL import Image, ImageEnhance

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/ginipick/flux-lora-eric-cat"
headers = {"Authorization": "Bearer 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"}

# Query function to interact with the Hugging Face API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None

# Encapsulated page function
def flux_lora_page():
    st.title("AI Image Generator with Live Enhancements")
    st.write("Generate an image and adjust brightness and contrast live.")

    # Input fields
    prompt = st.text_input("Enter your prompt:", "A serene landscape with mountains at sunset")
    generate_button = st.button("Generate Image")

    # Initialize session state to store the generated image
    if "original_image" not in st.session_state:
        st.session_state.original_image = None

    # Generate the image if the button is clicked
    if generate_button:
        with st.spinner("Generating image..."):
            image_bytes = query({"inputs": prompt})
            if image_bytes:
                st.session_state.original_image = Image.open(io.BytesIO(image_bytes))
                st.success("Image generated! Adjust brightness and contrast below.")

    # Display sliders and adjust the image live
    if st.session_state.original_image:
        st.subheader("Adjust Enhancements")

        # Brightness and contrast sliders
        brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
        contrast = st.slider("Contrast", 0.5, 2.0, 1.0)

        # Apply adjustments to the original image
        adjusted_image = st.session_state.original_image.copy()
        brightness_enhancer = ImageEnhance.Brightness(adjusted_image)
        adjusted_image = brightness_enhancer.enhance(brightness)
        contrast_enhancer = ImageEnhance.Contrast(adjusted_image)
        adjusted_image = contrast_enhancer.enhance(contrast)

        # Display the adjusted image
        st.image(adjusted_image, caption="Enhanced Image", use_container_width=True)
