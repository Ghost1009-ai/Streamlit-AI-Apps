import streamlit as st
import requests

# Hugging Face API configuration
API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-es"
headers = {"Authorization": "Bearer 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"}

# Query function to interact with the Hugging Face API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Encapsulated page function
def translation_page():
    st.title("Hugging Face Translation App")

    # Input from the user
    input_text = st.text_area("Enter the text to translate:")

    # Trigger translation
    if st.button("Translate"):
        if input_text:
            with st.spinner("Translating..."):
                output = query({"inputs": input_text})
                if output and "translation_text" in output[0]:
                    st.success("Translation completed!")
                    st.text_area("Translated text:", value=output[0]["translation_text"], height=200)
                else:
                    st.error("Translation failed. Please check the input or API key.")
        else:
            st.warning("Please enter text to translate.")
