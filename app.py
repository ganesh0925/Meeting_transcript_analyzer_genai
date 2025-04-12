import os
import streamlit as st
import PyPDF2
import google.generativeai as genai

# Set up Google Gemini API Key
GEMINI_API_KEY = "AIzaSyAgO5I6sN-2euuM_ZeomQG-ZVZ2EYqEOA4"
genai.configure(api_key=GEMINI_API_KEY)

# Streamlit UI Config
st.set_page_config(page_title="AI Meeting Transcript Analyzer", page_icon="🧠", layout="wide")

# Custom CSS Styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 34px;
        font-weight: bold;
        color: #1E88E5;
        text-shadow: 2px 2px 5px rgba(30, 136, 229, 0.3);
    }
    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #bbb;
        margin-bottom: 20px;
    }
    .stButton button {
        background: linear-gradient(to right, #1E88E5, #1565C0);
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background: linear-gradient(to right, #1565C0, #0D47A1);
    }
    .result-card {
        background: rgba(33, 150, 243, 0.1);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0px 2px 8px rgba(33, 150, 243, 0.2);
    }
    .success-banner {
        background: linear-gradient(to right, #1565C0, #0D47A1);
        color: white;
        padding: 15px;
        font-size: 18px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-top: 15px;
        box-shadow: 0px 2px 8px rgba(33, 150, 243, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Instructions
st.sidebar.title("📘 How to Use")
st.sidebar.write("- Upload a PDF containing a meeting transcript.")
st.sidebar.write("- The AI will extract, summarize, and analyze the meeting.")
st.sidebar.write("- Get key takeaways, action items, and sentiment insights.")

st.markdown('<h1 class="main-title">🧠 AI-Powered Meeting Transcript Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Upload your meeting transcript PDF for AI-generated summaries and action items</p>', unsafe_allow_html=True)

# Upload PDF File
uploaded_file = st.file_uploader("📂 Upload Transcript PDF", type=["pdf"], help="Only PDF files are supported")

def extract_text_from_pdf(file_path):
    """Extracts text from the uploaded PDF file."""
    text = ""
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def analyze_meeting_transcript(text):
    """Uses Google Gemini to analyze the meeting transcript."""
    model = genai.GenerativeModel("learnlm-1.5-pro-experimental")
    prompt = f"""
    Analyze the following meeting transcript and provide a detailed summary including:
    - **Meeting Summary**: Key points discussed
    - **Action Items**: List of assigned tasks with responsible persons (if available)
    - **Sentiment Analysis**: General tone and emotional context
    - **Highlights**: Important decisions or ideas
    - **Follow-ups**: Anything needing attention or future discussion
    Transcript:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response else "⚠️ Error analyzing the transcript."

if uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ File uploaded successfully!")

    with st.spinner("📄 Extracting text from PDF..."):
        extracted_text = extract_text_from_pdf(file_path)

    if not extracted_text:
        st.error("⚠️ No text found. The document might be a scanned image.")
    else:
        progress_bar = st.progress(0)
        with st.spinner("🧠 Analyzing transcript with AI..."):
            insights = analyze_meeting_transcript(extracted_text)
        progress_bar.progress(100)

        st.subheader("📊 Meeting Analysis Report")
        st.markdown(f'<div class="result-card"><b>📄 Summary for {uploaded_file.name}</b></div>', unsafe_allow_html=True)
        st.write(insights)
        st.markdown('<div class="success-banner">✅ Analysis Complete! Use this to align your team and follow up effectively. 🚀</div>', unsafe_allow_html=True)
        st.balloons()

    os.remove(file_path)
