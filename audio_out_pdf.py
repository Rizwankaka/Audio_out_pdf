import streamlit as st
from PyPDF2 import PdfReader
from gtts import gTTS
import tempfile

# Function to extract text from PDF
@st.cache_data
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + '\n'
    return text

# App Title
st.title('Listen to Your Text/Books 📚')

# Dropdown for selecting accent
accent = st.selectbox("Select an accent for the voice:", 
                      ['en-us', 'en-uk', 'en-au', 'en-in', 'en-ca'])

# File Upload
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)

    if text:
        # Convert text to speech with selected accent
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts = gTTS(text, lang=accent)
            tts.save(fp.name)
            st.audio(fp.name)
    else:
        st.error("Failed to extract text from the PDF. Please try a different file.")
