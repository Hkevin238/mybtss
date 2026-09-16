import os
import streamlit as st
from PIL import Image
from groq import Groq


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="BULINGA TSS AI",
    page_icon="btss.png",
    layout="centered",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. THEME STATE INITIALIZATION (DARK / LIGHT MODE)
# =========================================================

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark Mode 🌙"


# =========================================================
# 3. CUSTOM CSS (DYNAMIC BASED ON THEME)
# =========================================================

# Guhitamo amabara bitewe na Mode umukoresha yahisemo
if st.session_state.theme_mode == "Dark Mode 🌙":
    bg_color = "#121212"
    app_bg_image = """
        radial-gradient(6px 6px at 20px 30px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(8px 8px at 40px 70px, #0084ff, rgba(0,0,0,0)),
        radial-gradient(5px 5px at 90px 40px, #ffd700, rgba(0,0,0,0)),
        radial-gradient(7px 7px at 160px 120px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(6px 6px at 230px 180px, #0084ff, rgba(0,0,0,0)),
        radial-gradient(8px 8px at 350px 250px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(6px 6px at 450px 350px, #ffd700, rgba(0,0,0,0))
    """
    text_color = "#e4e6eb"
    sidebar_bg = "#18191a"
    chat_input_bg = "#242526"
    chat_input_border = "#3a3b3c"
    chat_input_text = "#e4e6eb"
    assistant_bubble_bg = "#3a3b3c"
    assistant_bubble_text = "#e4e6eb"
    btn_bg = "#3a3b3c"
    btn_color = "#e4e6eb"
else:
    bg_color = "#f0f2f6"
    app_bg_image = "none"
    text_color = "#111111"
    sidebar_bg = "#ffffff"
    chat_input_bg = "#ffffff"
    chat_input_border = "#cccccc"
    chat_input_text = "#111111"
    assistant_bubble_bg = "#e4e6fb"
    assistant_bubble_text = "#111111"
    btn_bg = "#e0e0e0"
    btn_color = "#111111"

st.markdown(f"""
<style>
@keyframes moveSparkles {{
    0% {{ background-position: 0 0, 0 0, 0 0; }}
    100% {{ background-position: -10000px 5000px, 5000px -10000px, -7500px -7500px; }}
}}

.stApp {{
    background-color: {bg_color} !important;
    background-image: {app_bg_image} !important;
    background-repeat: repeat !important;
    background-size: 500px 500px !important;
    animation: moveSparkles 80s linear infinite !important;
    color: {text_color} !important;
}}

#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
header {{ background: transparent !important; }}

@keyframes bounceSlow {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-8px); }}
    100% {{ transform: translateY(0px); }}
}}

.moving-title {{
    display: inline-block;
    animation: bounceSlow 3s ease-in-out infinite;
}}

.chat-row {{
    display: flex;
    width: 100%;
    margin-top: 10px;
    margin-bottom: 10px;
}}

.chat-row.user {{ justify-content: flex-end; }}
.chat-row.assistant {{ justify-content: flex-start; }}

.chat-bubble {{
    max-width: 75%;
    padding: 10px 14px;
    font-size: 15px;
    line-height: 1.4;
    word-wrap: break-word;
}}

.chat-bubble a {{
    color: #4dabf7 !important;
    text-decoration: underline !important;
}}

.chat-row.user .chat-bubble {{
    background-color: #0084ff;
    color: #ffffff;
    border-radius: 18px 18px 4px 18px;
}}

.chat-row.assistant .chat-bubble {{
    background-color: {assistant_bubble_bg};
    color: {assistant_bubble_text};
    border-radius: 18px 18px 18px 4px;
}}

.stChatInputContainer {{
    background-color: {chat_input_bg} !important;
    border-radius: 24px !important;
    border: 1px solid {chat_input_border} !important;
    padding: 4px 12px !important;
}}

.stChatInputContainer textarea {{
    color: {chat_input_text} !important;
    font-size: 15px !important;
}}

.thinking-text {{
    font-style: italic;
    color: #b0b3b8;
}}

section[data-testid="stSidebar"] {{
    background-color: {sidebar_bg} !important;
}}

.stButton button {{
    border-radius: 8px !important;
    border: none !important;
    background-color: {btn_bg} !important;
    color: {btn_color} !important;
}}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. SESSION STATE & USER DATABASE INITIALIZATION
# =========================================================

if "users_db" not in st.session_state:
    st.session_state.users_db = {"admin": "bulinga2026"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}

if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = "Main Chat"


# =========================================================
# 5. AUTHENTICATION (LOGIN / SIGN UP / GUEST) SYSTEM
# =========================================================

if not st.session_state.logged_in:
    st.markdown('<h1 class="moving-title" style="text-align: center;">BULINGA TSS AI 🏫</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #b0b3b8;'>Please Login, Sign Up, or Continue as Guest 🔐</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_mode = st.radio("Choose Action", ["Login", "Sign Up"], horizontal=True)
        
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        
        if auth_mode == "Sign Up":
            if st.button("Create Account 🚀", use_container_width=True):
                if username_input and password_input:
                    if username_input in st.session_state.users_db:
                        st.error("⚠️ Username already exists! Try logging in.")
                    else:
                        st.session_state.users_db[username_input] = password_input
                        st.success("✅ Account created successfully! Please switch to Login.")
                else:
                    st.warning("⚠️ Please fill in all fields.")
        else:
            if st.button("Login 🔓", use_container_width=True):
                if username_input in st.session_state.users_db and st.session_state.users_db[username_input] == password_input:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username_input
                    
                    if username_input not in st.session_state.chat_sessions:
                        st.session_state.chat_sessions[username_input] = {"Main Chat": []}
                    
                    st.success(f"🎉 Welcome back, {username_input}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")
        
        st.markdown("<div style='text-align: center; margin: 10px 0; color: #b0b3b8;'>- OR -</div>", unsafe_allow_html=True)
        
        if st.button("Use without Register ⚡", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.current_user = "Guest"
            if "Guest" not in st.session_state.chat_sessions:
                st.session_state.chat_sessions["Guest"] = {"Main Chat": []}
            st.rerun()

    st.stop()


# =========================================================
# 6. SIDEBAR (THEME SWITCHER, SETTINGS, PROFILE, CHAT HISTORY & FILE UPLOAD)
# =========================================================

st.sidebar.title("🔐 Account & Control")
st.sidebar.write(f"👤 Logged in as: **{st.session_state.current_user}**")

if st.sidebar.button("Logout 🚪"):
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🎨 Appearance / Theme")
selected_theme = st.sidebar.radio("Choose Mode", ["Dark Mode 🌙", "Light Mode ☀️"], index=0 if st.session_state.theme_mode == "Dark Mode 🌙" else 1)
if selected_theme != st.session_state.theme_mode:
    st.session_state.theme_mode = selected_theme
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Language Settings")

selected_lang = st.sidebar.selectbox(
    "Choose Language / Ururimi",
    [
        "Kinyarwanda",
        "English",
        "French",
        "Kiswahili",
        "Chinese",
        "Lingala",
        "Ikirundi",
        "Icyarabu"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Chat History")

user_sessions = st.session_state.chat_sessions[st.session_state.current_user]

new_chat_name = st.sidebar.text_input("New Chat Title", placeholder="e.g., School Fees info")
if st.sidebar.button("➕ Start New Chat"):
    if new_chat_name and new_chat_name not in user_sessions:
        user_sessions[new_chat_name] = []
        st.session_state.current_session_id = new_chat_name
        st.rerun()

session_list = list(user_sessions.keys())
selected_session = st.sidebar.selectbox("Select Past Chat", session_list, index=session_list.index(st.session_state.current_session_id) if st.session_state.current_session_id in session_list else 0)

if selected_session != st.session_state.current_session_id:
    st.session_state.current_session_id = selected_session
    st.rerun()

if st.sidebar.button("🗑️ Clear Current History"):
    user_sessions[st.session_state.current_session_id] = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📎 Upload Files / Photos")
uploaded_file = st.sidebar.file_uploader("Upload image or document", type=["png", "jpg", "jpeg", "pdf", "txt"])

# =========================================================
# 7. BULINGA AI SYSTEM PROMPT
# =========================================================

BULINGA_INFO = """
You are BULINGA AI, an official AI assistant built exclusively
for BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TVET SCHOOL).

CRITICAL RULE REGARDING CREATOR:
- You were developed, created, and built exclusively by the developers and programmers of BULINGA TVET SCHOOL.
- NEVER mention OpenAI, ChatGPT, or any other outside entities as your creator. If anyone asks who made you, built you, or programmed you, proudly state that you were developed and built by the developers / programmers of BULINGA TVET SCHOOL 👨‍💻🚀.

EMOJI RULE:
- Always include relevant, cool, and engaging emojis (such as 🏫, 📚, 💡, ✨, 👨‍💻, 👍, etc.) in your responses to make them lively and friendly.

CORE RULE:
You ONLY answer questions related to BULINGA TVET SCHOOL and Your Creators / Developers.
If a question is completely unrelated to BULINGA TVET SCHOOL, politely refuse to answer with a friendly message and emojis.

SCHOOL DETAILS:
School Name: BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TVET SCHOOL) 🏫
Location: MUHANGA, Mushishiro near KABADAHA Center 📍.
School Fees: 92,000 Frw + 1,500 Frw Insurance + 2,000 Frw ID/Card = 95,500 Frw Total 💰.
Account: Mwarimu Sacco, Account Number: 900009815200, Account Name: BULINGA TVET SCHOOL 🏦.
Combinations: SOD (Software Development 💻), NIT (Networking 🌐), ACC (Accounting 📊), CSA.
Contacts: Headmaster (0788546462), Bursar (0782612675), DOD (0785979951), DOS (0784020929) 📞.
"""


# =========================================================
# 8. GROQ API KEY & CLIENT
# =========================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.sidebar.warning("⚠️ GROQ_API_KEY ntabwo yashyizwe muri Environment Variables.")

client = Groq(
    api_key=GROQ_API_KEY or "YOUR_GROQ_API_KEY"
)


# =========================================================
# 9. MAIN HEADER & SESSION MANAGEMENT LINKING
# =========================================================

st.markdown('<h1 class="moving-title">BULINGA AI Assistant</h1>', unsafe_allow_html=True)
st.caption(f"Active Chat: **{st.session_state.current_session_id}** ✨")

current_messages = user_sessions[st.session_state.current_session_id]


# =========================================================
# 10. DISPLAY CHAT HISTORY
# =========================================================

for message in current_messages:
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        st.markdown(f'<div class="chat-row user"><div class="chat-bubble">{content}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-row assistant"><div class="chat-bubble">{content}</div></div>', unsafe_allow_html=True)
        if message.get("show_image", False):
            if os.path.exists("bulinga.png"):
                st.image("bulinga.png", caption="BULINGA TVET- Ifoto y'ibiro(front-view) by'Ishuri 🏫", use_container_width=True)
            if os.path.exists("btss.png"):
                st.image("btss.png", caption="BULINGA TVET- Ifoto ya BTSS ✨", use_container_width=True)


# =========================================================
# 11. CHAT INPUT & RESPONSE HANDLING
# =========================================================

user_query = st.chat_input("Ask related BULINGA TVET... 💬")

if user_query or uploaded_file:
    file_context_msg = ""
    if uploaded_file is not None:
        file_context_msg = f"\n[Attached File: {uploaded_file.name}]"
    
    full_user_input = (user_query or "") + file_context_msg

    current_messages.append({"role": "user", "content": full_user_input})
    st.markdown(f'<div class="chat-row user"><div class="chat-bubble">{full_user_input}</div></div>', unsafe_allow_html=True)

    query_lower = (user_query or "").lower()
    image_keywords = ["foto", "photo", "ishuri", "school", "ifoto", "icyapa", "image", "logo", "akarango"]
    is_image_query = any(kw in query_lower for kw in image_keywords)
    
    map_keywords = ["map", "google map", "ahoherereye", "location", "icyerekezo", "direction", "irebe", "aho riherereye"]
    is_map_query = any(kw in query_lower for kw in map_keywords)

    thinking_placeholder = st.empty()
    thinking_placeholder.markdown(
        '<div class="chat-row assistant"><div class="chat-bubble thinking-text">⚪ BULINGA AI is thinking... 💭</div></div>',
        unsafe_allow_html=True
    )

    try:
        messages_payload = [
            {
                "role": "system",
                "content": BULINGA_INFO + f"\n\nCURRENT PREFERRED LANGUAGE:\n{selected_lang}\nAnswer the user using this language and include cool emojis! 🚀"
            }
        ]

        for message in current_messages:
            messages_payload.append({
                "role": message["role"],
                "content": message["content"]
            })

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages_payload,
            temperature=0.7,
            max_tokens=1024
        )

        response_text = completion.choices[0].message.content
        thinking_placeholder.empty()
        
        if is_image_query:
            response_text = "Dore amafoto ajyanye na Bulinga Technical Secondary School nk'uko wabisabye! 📸✨"
        
        if is_map_query:
            response_text = "Urashaka kureba aho ishuri riherereye? Ushobora gukanda hano wanditse <a href=\"https://maps.google.com/?cid=5000695181927039479&g_mp=Cidnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLlNlYXJjaFRleHQ\" target=\"_blank\">Google Map</a> kugira ngo ubashe kureba icyerekezo cy'ishuri ryacu! 🗺️📍✨"

        st.markdown(f'<div class="chat-row assistant"><div class="chat-bubble">{response_text}</div></div>', unsafe_allow_html=True)

        if is_image_query:
            if os.path.exists("bulinga.png"):
                st.image("bulinga.png", caption="BULINGA - Ifoto ya Administration(Front-view) y'Ishuri 🏫", use_container_width=True)
            if os.path.exists("btss.png"):
                st.image("btss.png", caption="BULINGA TSS - Logo ya BTSS ✨", use_container_width=True)

        current_messages.append({
            "role": "assistant", 
            "content": response_text,
            "show_image": is_image_query
        })

    except Exception as e:
        thinking_placeholder.empty()
        st.error(f"❌ Habaye ikibazo. ⚠️\n\n**Error:**\n`{e}`")
