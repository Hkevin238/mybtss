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
# 2. SIDEBAR & AUTOMATIC THEME DETECTION
# =========================================================

st.sidebar.title("🏫 BULINGA AI Control")

# Theme Switcher
theme_mode = st.sidebar.radio("Theme Mode", ["Dark Mode 🌙", "Light Mode ☀️"], horizontal=True)

# Dynamic Color Detection based on Selected Mode
if theme_mode == "Dark Mode 🌙":
    app_bg = "#121212"
    text_color = "#e4e6eb"
    sidebar_bg = "#18191a"
    chat_input_bg = "#242526"
    chat_input_border = "#3a3b3c"
    assistant_bubble_bg = "#3a3b3c"
    assistant_text = "#e4e6eb"
    button_bg = "#3a3b3c"
    button_text = "#e4e6eb"
    # Auto-detected input text color for Dark Mode
    input_text_color = "#ffffff" 
    input_placeholder_color = "#b0b3b8"
else:
    app_bg = "#f0f2f5"
    text_color = "#1c1e21"
    sidebar_bg = "#ffffff"
    chat_input_bg = "#ffffff"
    chat_input_border = "#ced4da"
    assistant_bubble_bg = "#e4e6eb"
    assistant_text = "#1c1e21"
    button_bg = "#e4e6eb"
    button_text = "#1c1e21"
    # Auto-detected input text color for Light Mode
    input_text_color = "#000000" 
    input_placeholder_color = "#555555"


# =========================================================
# 3. DYNAMIC CUSTOM CSS (AUTO-ADJUSTS PROMPT INPUT TEXT COLOR)
# =========================================================

st.markdown(f"""
<style>
@keyframes moveSparkles {{
    0% {{ background-position: 0 0, 0 0, 0 0; }}
    100% {{ background-position: -10000px 5000px, 5000px -10000px, -7500px -7500px; }}
}}

.stApp {{
    background-color: {app_bg} !important;
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

.chat-row.user .chat-bubble {{
    background-color: #0084ff;
    color: #ffffff;
    border-radius: 18px 18px 4px 18px;
}}

.chat-row.assistant .chat-bubble {{
    background-color: {assistant_bubble_bg};
    color: {assistant_text};
    border-radius: 18px 18px 18px 4px;
}}

.stChatInputContainer {{
    background-color: {chat_input_bg} !important;
    border-radius: 24px !important;
    border: 1px solid {chat_input_border} !important;
    padding: 4px 12px !important;
}}

/* Automatically detected and applied input text color based on active mode */
.stChatInputContainer textarea {{
    color: {input_text_color} !important;
    font-size: 15px !important;
    font-weight: 500 !important;
}}

.stChatInputContainer textarea::placeholder {{
    color: {input_placeholder_color} !important;
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
    background-color: {button_bg} !important;
    color: {button_text} !important;
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
    st.session_state.current_user = "Guest"

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {
        "Guest": {"Main Chat": []}
    }

if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = "Main Chat"


# =========================================================
# 5. SIDEBAR (ACCOUNT, LANGUAGE, HISTORY & UPLOAD)
# =========================================================

with st.sidebar.expander("🔐 Account (Optional Login/Signup)", expanded=not st.session_state.logged_in):
    if not st.session_state.logged_in:
        st.write("Ushobora gukoresha AI utinjiyemo, cyangwa ukora Login kugira ngo ubibike.")
        auth_mode = st.radio("Hitamo:", ["Login", "Sign Up"], horizontal=True, key="auth_radio")
        
        u_input = st.text_input("Username", key="auth_user")
        p_input = st.text_input("Password", type="password", key="auth_pass")
        
        if auth_mode == "Sign Up":
            if st.button("Create Account 🚀", key="signup_btn"):
                if u_input and p_input:
                    if u_input in st.session_state.users_db:
                        st.error("⚠️ Izina ryatwawe!")
                    else:
                        st.session_state.users_db[u_input] = p_input
                        st.session_state.chat_sessions[u_input] = {"Main Chat": []}
                        st.success("✅ Konti yaremwe! Kora Login.")
                else:
                    st.warning("⚠️ Uzuza ibisabwa byose.")
        else:
            if st.button("Login 🔓", key="login_btn"):
                if u_input in st.session_state.users_db and st.session_state.users_db[u_input] == p_input:
                    st.session_state.logged_in = True
                    st.session_state.current_user = u_input
                    if u_input not in st.session_state.chat_sessions:
                        st.session_state.chat_sessions[u_input] = {"Main Chat": []}
                    st.rerun()
                else:
                    st.error("❌ Username cyangwa Password bitari byo.")
    else:
        st.write(f"👤 Ufunguye nka: **{st.session_state.current_user}**")
        if st.button("Logout 🚪", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.current_user = "Guest"
            st.session_state.current_session_id = "Main Chat"
            if "Guest" not in st.session_state.chat_sessions:
                st.session_state.chat_sessions["Guest"] = {"Main Chat": []}
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Ururimi / Language")

selected_lang = st.sidebar.selectbox(
    "Choose Language",
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

active_user = st.session_state.current_user
if active_user not in st.session_state.chat_sessions:
    st.session_state.chat_sessions[active_user] = {"Main Chat": []}

user_sessions = st.session_state.chat_sessions[active_user]

new_chat_name = st.sidebar.text_input("New Chat Title", placeholder="e.g., School Fees info")
if st.sidebar.button("➕ Start New Chat", key="new_chat_btn"):
    if new_chat_name and new_chat_name not in user_sessions:
        user_sessions[new_chat_name] = []
        st.session_state.current_session_id = new_chat_name
        st.rerun()

session_list = list(user_sessions.keys())
if st.session_state.current_session_id not in session_list:
    st.session_state.current_session_id = session_list[0]

selected_session = st.sidebar.selectbox("Select Past Chat", session_list, index=session_list.index(st.session_state.current_session_id))

if selected_session != st.session_state.current_session_id:
    st.session_state.current_session_id = selected_session
    st.rerun()

if st.sidebar.button("🗑️ Clear Current History", key="clear_hist_btn"):
    user_sessions[st.session_state.current_session_id] = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📎 Upload Files / Photos")
uploaded_file = st.sidebar.file_uploader("Upload image or document", type=["png", "jpg", "jpeg", "pdf", "txt"])


# =========================================================
# 6. BULINGA AI SYSTEM PROMPT
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
# 7. GROQ API KEY & CLIENT
# =========================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.sidebar.warning("⚠️ GROQ_API_KEY ntabwo yashyizwe muri Environment Variables.")

client = Groq(
    api_key=GROQ_API_KEY or "YOUR_GROQ_API_KEY"
)


# =========================================================
# 8. MAIN HEADER & CHAT RENDERING
# =========================================================

st.markdown('<h1 class="moving-title">BULINGA AI Assistant</h1>', unsafe_allow_html=True)
st.caption(f"User: **{st.session_state.current_user}** | Active Chat: **{st.session_state.current_session_id}** ✨")

current_messages = user_sessions[st.session_state.current_session_id]

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
# 9. CHAT INPUT & RESPONSE HANDLING
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
