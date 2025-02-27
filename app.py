
import streamlit as st
from google import genai

# Initialize GenAI client
API_KEY = st.secrets["api_key"]
client = genai.Client(api_key="API_KEY")

# List of important biochemistry topics
biochem_topics = [
    "Enzyme Kinetics",
    "Metabolism and Bioenergetics",
    "Protein Structure and Function",
    "DNA Replication and Repair",
    "Lipid Metabolism",
    "Carbohydrate Metabolism",
    "Hormonal Regulation",
    "Cell Signaling Pathways",
    "Molecular Biology Techniques",
    "Biochemical Disorders"
]

# Custom CSS for better UI
def apply_custom_css():
    st.markdown(
        """
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                background: #f4f4f4;
                color: #333;
            }
            .stApp {
                padding: 20px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                height: 100vh;
            }
            .main-title {
                text-align: center;
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
            }
            .sidebar .sidebar-content {
                background: #2c3e50;
                color: white;
            }
            .topic-btn {
                background: #3498db;
                color: white;
                padding: 10px;
                border-radius: 8px;
                text-align: center;
                margin-bottom: 10px;
                cursor: pointer;
                transition: 0.3s;
            }
            .topic-btn:hover {
                background: #2980b9;
            }
            .response-container {
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                margin-top: 20px;
                flex-grow: 1;
                overflow-y: auto;
            }
            .input-container {
                position: fixed;
                bottom: 0;
                width: 100%;
                background: #fff;
                padding: 10px;
                box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Apply styles
apply_custom_css()

# Display title
st.markdown("<h1 class='main-title'>🔬 Biochemistry Query Solver</h1>", unsafe_allow_html=True)

# Sidebar with topic suggestions
st.sidebar.title("📌 Suggested Topics")
selected_topic = st.sidebar.radio("Choose a topic to explore:", biochem_topics)

# AI Response section appears first
# st.markdown("<div class='response-container'>", unsafe_allow_html=True)
if "response" in st.session_state:
    st.write(st.session_state.response)
st.markdown("</div>", unsafe_allow_html=True)

# User input field at the bottom
st.markdown("<div class='input-container'>", unsafe_allow_html=True)
prompt = st.text_input("Write your query related to biochemistry here...", selected_topic)
st.markdown("</div>", unsafe_allow_html=True)

if prompt:
    with st.spinner("Processing your query... 🔄"):
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=f"You are an expert in biochemistry. First, provide a concise yet informative explanation of the given topic: {prompt}. Then, generate 10 multiple-choice questions (MCQs) based on your explanation, each with four answer options. Finally, provide the correct answer for each question."
        )
    
    st.session_state.response = response.text
    st.rerun()
