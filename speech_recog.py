import streamlit as st
import requests
import sounddevice as sd
import numpy as np
import wave
import tempfile

# Define API URL and headers
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
headers = {"Authorization": "Bearer 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"}  # Replace with your token


# Function to send audio to Hugging Face API
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return {}


# Function to record audio using the microphone
def record_audio(duration=10, fs=16000):
    st.write("Recording... Please speak into your microphone.")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    st.write("Recording complete.")

    # Save the audio to a temporary WAV file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    with wave.open(temp_file, 'wb') as wf:
        wf.setnchannels(1)  # Mono audio
        wf.setsampwidth(2)  # 16-bit samples
        wf.setframerate(fs)
        wf.writeframes(audio_data.tobytes())

    return temp_file.name


# Encapsulated page function
def speech_to_text_page():
    st.title("Automatic Speech Recognition (Speech-to-Text)")
    st.write("You can record your voice or upload an audio file to transcribe its content.")

    # Option to upload an audio file
    uploaded_file = st.file_uploader("Upload an audio file:", type=["wav", "mp3", "flac"])

    if uploaded_file is not None:
        # Save uploaded file temporarily
        temp_uploaded_file = tempfile.NamedTemporaryFile(delete=False)
        with open(temp_uploaded_file.name, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Display uploaded audio and send it for transcription
        st.write(f"Uploaded file: {uploaded_file.name}")
        st.audio(uploaded_file, format="audio/wav")
        result = query(temp_uploaded_file.name)

        # Display transcription
        if 'text' in result:
            st.subheader("Transcription:")
            st.write(result['text'])
        else:
            st.error("Transcription failed. Please try again.")

    elif st.button("Record Audio"):
        # Record audio and save it to a file
        audio_file = record_audio()

        # Display recorded audio and send it for transcription
        with open(audio_file, 'rb') as f:
            st.audio(f.read(), format="audio/wav")
        st.write("Sending audio to Whisper API for transcription...")
        result = query(audio_file)

        # Display transcription
        if 'text' in result:
            st.subheader("Transcription:")
            st.write(result['text'])
        else:
            st.error("Transcription failed. Please try again.")
