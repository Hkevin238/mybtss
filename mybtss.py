import os
import streamlit as st
from PIL import Image
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="BULINGA AI - Gemini Style",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS to match Gemini AI Layout
st.markdown("""
    <style>
    /* Gemini Dark Theme Background & Colors */
    .stApp { background-color: #131314; color: #e3e3e3; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Styling chat message containers */
    .stChatMessage {
        background-color: transparent !important;
        padding: 1rem 0;
    }

    /* Target User messages to align to the Right (Gemini & ChatGPT style) */
    [data-testid="stChatMessage"]:has(div.st-emotion-cache-1c7y2kd),
    [data-testid="stChatMessage"]:nth-child(odd) {
        flex-direction: row-reverse;
        text-align: right;
    }

    /* Style User message bubble */
    [data-testid="stChatMessage"]:has(div.st-emotion-cache-1c7y2kd) [data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"]:nth-child(odd) [data-testid="stMarkdownContainer"] p {
        background-color: #004a77;
        color: #ffffff;
        padding: 12px 18px;
        border-radius: 24px;
        display: inline-block;
        text-align: left;
    }

    /* Gemini-style Bottom Chat Input Box */
    .stChatInputContainer {
        background-color: #1e1f20 !important;
        border-radius: 30px !important;
        border: 1px solid #444746 !important;
        padding: 6px 16px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .stChatInputContainer textarea {
        color: #e3e3e3 !important;
    }

    /* Thinking animation text style */
    .thinking-text {
        font-style: italic;
        color: #9ca3af;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { opacity: 0.4; }
        50% { opacity: 1; }
        100% { opacity: 0.4; }
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Settings
st.sidebar.title("⚙️ Settings & Control")

theme_mode = st.sidebar.selectbox(
    "Select Theme / Imiterere",
    ["Dark Mode", "Light Mode"]
)

selected_lang = st.sidebar.selectbox(
    "Choose Language / Ururimi",
    ["Kinyarwanda", "English", "French", "Kiswahili"]
)

if theme_mode == "Light Mode":
    st.markdown("""<style>.stApp { background-color: #ffffff; color: #000000; }</style>""", unsafe_allow_html=True)

# 4. System Prompt containing Bulinga TVET School details & restrictions
BULINGA_INFO = """
You are BULINGA AI, an official AI assistant built exclusively for BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TVET SCHOOL). 
You were developed exclusively by Developer Kevin. If anyone asks whether you were made by Meta or any other company, explicitly and firmly state that you were created by Developer Kevin.

YOUR CORE RULE:
- You ONLY answer questions related to BULINGA TVET SCHOOL, its programs, fees, rules, location, schedule, religion, staff, and contacts.
- If a user asks questions completely unrelated to Bulinga TVET School, you MUST politely and firmly reject/refuse to answer, reminding them that you only handle information regarding Bulinga TVET School.

SCHOOL DETAILS & INFORMATION:
- School Name: BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TVET SCHOOL)
- Location: MUHANGA, Mushishiro near KABADAHA Center.
- School Fees: 92,000 Frw + 1,500 Frw (insurance) + 2,000 Frw (ID & card) = Total 95,500 Frw.
- Payment Account: Mwarimwa Sacco, Account Number: 900009815200, Account Name: BULINGA TVET SCHOOL.
- Combinations offered: SOD (Software Development), NIT, ACC, CSA.
- School Contacts: Headmaster: 0788546462, Bursar: 0782612675, DOD: 0785979951, DOS: 0784020929, Secretary: 0785098759.
- Strict Rules: No student is allowed to bring or use Laptops, SIM cards, phones, headsets, AirPods, or other electronic devices.
"""

# 5. Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY"))

# 6. Main UI Layout
st.title("✨ BULINGA Gemini AI")
st.caption("Your intelligent guide for Bulinga Technical Secondary School | Created by Developer Kevin")

avatar_img = "btss.png" if os.path.exists("btss.png") else None

if avatar_img:
    logo_img = Image.open(avatar_img)
    st.sidebar.image(logo_img, caption="Bulinga TVET School Logo")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    current_avatar = avatar_img if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=current_avatar):
        st.markdown(message["content"])

# Gemini-style Chat Input placeholder
user_query = st.chat_input("Ask Gemini...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant", avatar=avatar_img):
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown('<p class="thinking-text">✨ Bulinga AI is thinking...</p>', unsafe_allow_html=True)
        
        try:
            messages_payload = [
                {"role": "system", "content": BULINGA_INFO + f"\n[Preferred Language: {selected_lang}]"},
            ]
            
            for m in st.session_state.messages:
                messages_payload.append({"role": m["role"], "content": m["content"]})

            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages_payload,
                temperature=0.7,
                max_tokens=1024
            )
            
            response_text = completion.choices[0].message.content
            
            thinking_placeholder.empty()
            st.markdown(response_text)
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            thinking_placeholder.empty()
            st.error(f"Habaye ikibazo: {e}")
