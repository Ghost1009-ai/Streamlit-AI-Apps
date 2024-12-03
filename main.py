import streamlit as st
from anime import anime_page
from home import home_page
from image_gen import flux_lora_page
from object_detect import detection_page
from spanish_translator import translation_page
from speech_recog import speech_to_text_page
# Import your class from the file

def main():
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home",
                                      "Anime",
                                      "Image Generation",
                                      "Object detection",
                                      "Spanish Translator",
                                      "Speech Recognition"
                                      ])

    # Adding custom CSS
    st.markdown("""
        <style>
            .big-font {
            font-size: 3rem;
            color: yellow;
            font-weight: 800;
            cursor: pointer;
            transition: 0.3s ease;
        }
        </style>
    """, unsafe_allow_html=True)

    # Load the appropriate page based on sidebar selection
    if page == "Home":
        st.markdown('<h1 class="big-font">Welcome to Home Page</h1>', unsafe_allow_html=True)
        home_page()

    elif page == "Anime":
        st.markdown('<h1 class="big-font">Anime</h1>', unsafe_allow_html=True)
        anime_page()


    elif page == "Image Generation":
        st.markdown('<h1 class="big-font">Image Generation</h1>', unsafe_allow_html=True)
        flux_lora_page()


    elif page == "Object detection":
        st.markdown('<h1 class="big-font">Object detection</h1>', unsafe_allow_html=True)
        detection_page()

    elif page == "Spanish Translator":
        st.markdown('<h1 class="big-font">Spanish Translator</h1>', unsafe_allow_html=True)
        translation_page()

    elif page == "Speech Recognition":
        st.markdown('<h1 class="big-font">Speech Recognition</h1>', unsafe_allow_html=True)
        speech_to_text_page()


if __name__ == "__main__":
    main()
