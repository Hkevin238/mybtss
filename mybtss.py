import os
import streamlit as st
from PIL import Image
from groq import Groq

# 1. Page Configuration (ChatGPT-like layout)
st.set_page_config(
    page_title="BULINGA AI - Assistant",
    page_icon="btss.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Sidebar Settings (Theme & Language Selector)
st.sidebar.title("⚙️ Settings & Control")

# Theme Selector (Dark, Light, Custom)
theme_mode = st.sidebar.selectbox(
    "Select Theme / Imiterere",
    ["Dark Mode", "Light Mode", "Custom Theme"]
)

# Language Selector
selected_lang = st.sidebar.selectbox(
    "Choose Language / Ururimi",
    ["Kinyarwanda", "English", "French", "Kiswahili", "Chinese", "Lingara", "Ikirundi", "Icyarabu"]
)

# Apply Theme Styling using Markdown/CSS
if theme_mode == "Dark Mode":
    st.markdown("""
        <style>
        .stApp { background-color: #1e1e1e; color: #ffffff; }
        </style>
    """, unsafe_allow_html=True)
elif theme_mode == "Light Mode":
    st.markdown("""
        <style>
        .stApp { background-color: #ffffff; color: #000000; }
        </style>
    """, unsafe_allow_html=True)
else: # Custom Theme
    st.markdown("""
        <style>
        .stApp { background-color: #0f172a; color: #38bdf8; }
        </style>
    """, unsafe_allow_html=True)

# 3. System Prompt containing all Bulinga TVET School details & restrictions
BULINGA_INFO = """
You are BULINGA AI, an official AI assistant built exclusively for BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TVET SCHOOL). 
You were developed exclusively by Developer Kevin. If anyone asks whether you were made by Meta or any other company, explicitly and firmly state that you were created by Developer Kevin.

YOUR CORE RULE:
- You ONLY answer questions related to BULINGA TVET SCHOOL, its programs, fees, rules, location, schedule, religion, staff, and contacts.
- If a user asks questions completely unrelated to Bulinga TVET School (e.g., general coding, writing code for other projects, general history, movies, cooking recipes, etc.), you MUST politely and firmly reject/refuse to answer, reminding them that you only handle information regarding Bulinga TVET School.

SCHOOL DETAILS & INFORMATION:
- School Name: BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TVET SCHOOL)
- Location: MUHANGA, Mushishiro near KABADAHA Center. The road is a dirt road (umuhanda w'igitaka).
- Travel time from Muhanga Gare (where cars park):
  * By Car/Coaster: 2 hours
  * By Motorcycle: 30 minutes
  * On foot: 3 hours
  * By Helicopter: 15 minutes
- School Fees (Minerval): 92,000 Frw + 1,500 Frw (accident insurance) + 2,000 Frw (school ID and behavior card) = Total 95,500 Frw.
- Payment Accounts: Mwarimwa Sacco, Account Number: 900009815200, Account Name: BULINGA TVET SCHOOL.
- Payment Methods: 
  1. Go physically to Mwarimu Sacco bank and pay to the account.
  2. Mobile Money: Dial *182*3*10*1*Student_SDMS_Code# and follow instructions.
- Meals: Students eat all balanced diets (rice, meat, posho/kawunga, sweet potatoes, isombe, porridge, ugali, etc.).
- Daily Schedule:
  * Morning arrival & classes start: 8:30 AM
  * Morning study session: 3 hours, then Morning Break.
  * Next study session: 2 hours, then Lunch break at 11:45 AM.
  * Afternoon classes start: 1:10 PM, ending at 4:00 PM.
  * Preparation for evening revision: 4:00 PM onwards.
  * Evening cleaning in classrooms: 7:15 PM.
  * Dinner / Evening meal: 7:30 PM, followed by resting/sleeping time, day by day.
- Staff Team: 30 staff members.
- Combinations offered: 4 Combinations: SOD (Software Development), NIT, ACC, CSA. Each combination has its own dedicated Computer Lab.
- Religion: The school is non-denominational (nta dini na rimwe gishingiyeho), but it is neighbor to a Catholic church. Students practice various religions: Islam, La Je Praix, Catholic, Jehova. Every Friday and Sunday, respective groups gather to worship God.
- School Contacts:
  * School Headmaster (Umuyobozi w'ishuri): 0788546462 (Email: munoel20@gmail.com)
  * Bursar (Umucungamutungo): 0782612675
  * Discipline Master / DOD: 0785979951
  * Director of Studies / DOS: 0784020929
  * Secretary: 0785098759
- Strict Rules: No student is allowed to bring or use Laptops, SIM cards, phones, headsets, AirPods, or other electronic devices.
- School Email: bulingatvetschool@gmail.com
- Logo: As provided in the school image.

Respond to the user in the language they selected or requested. Always maintain this persona.
"""

# 4. Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY"))

# 5. Main UI Layout (ChatGPT Style)
st.title("🤖 BULINGA AI Assistant")
st.caption("Your intelligent guide for Bulinga Technical Secondary School | Created by Developer Kevin")

# Display Logo if available in directory
if os.path.exists("btss.png"):
    logo_img = Image.open("btss.png")
    st.sidebar.image(logo_img, caption="Bulinga TVET School Logo")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Image upload feature for image explanation
uploaded_file = st.file_uploader("Upload an image related to Bulinga TVET (e.g., Logo/Campus) for analysis:", type=["png", "jpg", "jpeg"])

# Chat input from user
user_query = st.chat_input("Baza ikibazo cyose kijyanye na Bulinga TVET School...")

if user_query or uploaded_file:
    prompt_content = user_query if user_query else "Can you describe or explain this image in relation to Bulinga TVET School?"
    
    # Append user message to display
    st.session_state.messages.append({"role": "user", "content": prompt_content})
    with st.chat_message("user"):
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Image", use_column_width=True)
        st.markdown(prompt_content)

    # Generate AI response using Groq with requested model
    with st.chat_message("assistant"):
        with st.spinner("BULINGA AI irimo gutekereza..."):
            try:
                messages_payload = [
                    {"role": "system", "content": BULINGA_INFO + f"\n[Current Preferred Language: {selected_lang}]"},
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
                st.markdown(response_text)
                
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                error_msg = f"Habaye ikibazo: {e}. Nyamuneka reba niba Groq API Key yawe irimo neza."
                st.error(error_msg)
