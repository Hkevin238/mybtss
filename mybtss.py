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

st.sidebar.title("🏫 BTSS AI Control")

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
    input_text_color = "#000000" 
    input_placeholder_color = "#555555"


# =========================================================
# 3. DYNAMIC CUSTOM CSS
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
# 5. SIDEBAR (CLEAN & ORGANIZED LAYOUT)
# =========================================================

with st.sidebar.expander("(Login/Signup)", expanded=not st.session_state.logged_in):
    if not st.session_state.logged_in:
        st.write("Ushobora gukoresha AI utinjiyemo, cyangwa ukora Login.")
        auth_mode = st.radio(":", ["Login", "Sign Up"], horizontal=True, key="auth_radio")
        
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
                        st.success("✅ Konti yaremwe!")
                else:
                    st.warning("⚠️ Uzuza ibisabwa.")
        else:
            if st.button("Login 🔓", key="login_btn"):
                if u_input in st.session_state.users_db and st.session_state.users_db[u_input] == p_input:
                    st.session_state.logged_in = True
                    st.session_state.current_user = u_input
                    if u_input not in st.session_state.chat_sessions:
                        st.session_state.chat_sessions[u_input] = {"Main Chat": []}
                    st.rerun()
                else:
                    st.error("❌ Byanze, subira inyuma.")
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

selected_lang = st.sidebar.selectbox(
    "🌐 Choose Language",
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

st.sidebar.subheader("Chat History")

active_user = st.session_state.current_user
if active_user not in st.session_state.chat_sessions:
    st.session_state.chat_sessions[active_user] = {"Main Chat": []}

user_sessions = st.session_state.chat_sessions[active_user]

with st.sidebar.expander("➕ New Chat", expanded=False):
    new_chat_name = st.text_input("Chat Title", placeholder="e.g., School Fees info", key="new_chat_input_field")
    if st.button("Create Chat 🚀", key="create_chat_action_btn"):
        if new_chat_name and new_chat_name not in user_sessions:
            user_sessions[new_chat_name] = []
            st.session_state.current_session_id = new_chat_name
            st.rerun()

session_list = list(user_sessions.keys())
if st.session_state.current_session_id not in session_list:
    st.session_state.current_session_id = session_list[0]

selected_session = st.sidebar.selectbox("Select Active Chat", session_list, index=session_list.index(st.session_state.current_session_id), key="select_past_chat_box")

if selected_session != st.session_state.current_session_id:
    st.session_state.current_session_id = selected_session
    st.rerun()

col_h1, col_h2 = st.sidebar.columns(2)
with col_h1:
    if st.button("Clear", key="clear_hist_btn", use_container_width=True):
        user_sessions[st.session_state.current_session_id] = []
        st.rerun()

st.sidebar.markdown("---")

with st.sidebar.expander("📎 Upload Files / Photos", expanded=False):
    uploaded_file = st.file_uploader("Choose file", type=["png", "jpg", "jpeg", "pdf", "txt"], key="sidebar_file_uploader")


# =========================================================
# 6. BULINGA AI SYSTEM PROMPT (STRICTLY BULINGA TSS - NO MISTAKES)
# =========================================================

BULINGA_INFO = """
You are BULINGA AI, an official AI assistant built exclusively
for BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TSS SCHOOL).

CRITICAL NAME RULE (STRICT & ABSOLUTE):
- Your name and your school's name MUST ALWAYS be spelled strictly as: BULINGA TSS, BULINGA TECHNICAL SECONDARY SCHOOL, or BULINGA TSS SCHOOL.
- NEVER, UNDER ANY CIRCUMSTANCES, spell it as "Bilinga", "Bulingha", or any other wrong variation. Always use strictly "BULINGA" (with 'U', never 'I').
- When generating text or speaking/reading text via text-to-speech, ensure the pronunciation and spelling are completely correct for BULINGA.

CRITICAL RULE REGARDING CREATOR:
- You were developed, created, and built exclusively by the developers and programmers of BULINGA TSS.
- NEVER mention OpenAI, ChatGPT, or any other outside entities as your creator. If anyone asks who made you, built you, or programmed you, proudly state that you were developed and built by the developers / programmers of BULINGA TSS 👨‍💻🚀.

EMOJI RULE:
- Always include relevant, cool, and engaging emojis (such as 🏫, 📚, 💡, ✨, 👨‍💻, 👍, etc.) in your responses to make them lively and friendly.

CORE RULE:
You ONLY answer questions related to BULINGA TSS and Your Creators / Developers.
If a question is completely unrelated to BULINGA TSS, politely refuse to answer with a friendly message and emojis.

SCHOOL DETAILS:
School Name: BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TSS SCHOOL / BULINGA TSS) 🏫
Location: MUHANGA, Mushishiro near KABADAHA Center 📍.
Google Maps Link: https://maps.app.goo.gl/umx4ktE6mzBNjU447 (Ecole Secondaire de Bulinga) 🗺️.
School Fees: 92,000 Frw + 1,500 Frw Insurance + 2,000 Frw ID/Card = 95,500 Frw Total 💰.
Account: Mwarimu Sacco, Account Number: 900009815200, Account Name: BULINGA TSS SCHOOL 🏦.
Combinations: SOD (Software Development 💻), NIT (Networking 🌐), ACC (Accounting 📊), CSA.
Contacts: Headmaster (0788546462), Bursar (0782612675), DOD (0785979951), DOS (0784020929) 📞.
"""


# =========================================================
# 7. GROQ API KEY & CLIENT
# =========================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.sidebar.warning("⚠️ GROQ_API_KEY ntabwo yashyizwe.")

client = Groq(
    api_key=GROQ_API_KEY or "YOUR_GROQ_API_KEY"
)


# =========================================================
# 8. MAIN HEADER & CHAT RENDERING (WITH BROWSER VOICE READER)
# =========================================================

st.markdown('<h1 class="moving-title">BULINGA TSS AI</h1>', unsafe_allow_html=True)
 | Developed by BULINGA TSS: **{st.session_state.current_session_id}** ✨")

current_messages = user_sessions[st.session_state.current_session_id]

for i, message in enumerate(current_messages):
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        st.markdown(f'<div class="chat-row user"><div class="chat-bubble">{content}</div></div>', unsafe_allow_html=True)
    else:
        cleaned_content = content.replace("Bilinga", "BULINGA").replace("bilinga", "BULINGA")
        
        st.markdown(f'<div class="chat-row assistant"><div class="chat-bubble">{cleaned_content}</div></div>', unsafe_allow_html=True)
        
        # High-Speed Browser Voice Reader (Soma Ijwi with Web Speech API)
        safe_content = cleaned_content.replace('"', '&quot;').replace("'", "&#39;").replace('\n', ' ')
        voice_html = f"""
        <div style="margin-bottom: 8px; margin-left: 2px; display: flex; gap: 8px;">
            <button onclick="speakText_{i}()" style="background-color: #0084ff; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: bold;">
                🔊 Play Voice (Soma)
            </button>
            <button onclick="stopSpeech()" style="background-color: #dc3545; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: bold;">
                ⏹️ Stop (Hagarika)
            </button>
            <script>
            function speakText_{i}() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var text = "{safe_content}";
                    var utterance = new SpeechSynthesisUtterance(text);
                    utterance.rate = 1.0;
                    window.speechSynthesis.speak(utterance);
                }} else {{
                    alert("Browser yawe ntishyigikiye Voice Reader.");
                }}
            }}
            function stopSpeech() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                }}
            }}
            </script>
        </div>
        """
        st.markdown(voice_html, unsafe_allow_html=True)

        if message.get("show_map", False):
            st.markdown("""
            <div style="margin-bottom: 12px;">
                <a href="https://maps.app.goo.gl/umx4ktE6mzBNjU447" target="_blank" style="display: inline-block; background-color: #28a745; color: white; padding: 8px 14px; border-radius: 8px; text-decoration: none; font-size: 14px; font-weight: bold;">
                    🗺️ Reba Location kuri Google Maps (Ecole Secondaire de Bulinga)
                </a>
            </div>
            """, unsafe_allow_html=True)

        if message.get("show_image", False):
            if os.path.exists("bulinga.png"):
                st.image("bulinga.png", caption="BULINGA TSS - Ifoto y'ibiro (front-view) by'Ishuri 🏫", use_container_width=True)
            if os.path.exists("btss.png"):
                st.image("btss.png", caption="BULINGA TSS - Ifoto ya BTSS ✨", use_container_width=True)


# =========================================================
# 9. CHAT INPUT & RESPONSE HANDLING
# =========================================================

user_query = st.chat_input("Ask related BULINGA TSS... 💬")

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

    map_keywords = ["map", "location", "ahoherereye", "aho iri", "aho ibereye", "gushaka ishuri", "aho duherereye"]
    is_map_query = any(kw in query_lower for kw in map_keywords)

    thinking_placeholder = st.empty()
    thinking_placeholder.markdown(
        '<div class="chat-row assistant"><div class="chat-bubble thinking-text">⚪ BULINGA TSS AI is thinking... 💭</div></div>',
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
        response_text = response_text.replace("Bilinga", "BULINGA").replace("bilinga", "BULINGA")

        thinking_placeholder.empty()
        
        if is_map_query:
            response_text = "Dore aho Ecole Secondaire de Bulinga iherereye kuri Google Maps! 🗺️ Kanda kuri buto iri hepfo kugira ngo uyirebe neza:"
        elif is_image_query:
            response_text = "Dore amafoto ajyanye na BULINGA TSS nk'uko wabisabye! 📸✨"

        st.markdown(f'<div class="chat-row assistant"><div class="chat-bubble">{response_text}</div></div>', unsafe_allow_html=True)

        if is_map_query:
            st.markdown("""
            <div style="margin-bottom: 12px;">
                <a href="https://maps.app.goo.gl/umx4ktE6mzBNjU447" target="_blank" style="display: inline-block; background-color: #28a745; color: white; padding: 8px 14px; border-radius: 8px; text-decoration: none; font-size: 14px; font-weight: bold;">
                    🗺️ Reba Location kuri Google Maps (Ecole Secondaire de Bulinga)
                </a>
            </div>
            """, unsafe_allow_html=True)

        if is_image_query:
            if os.path.exists("bulinga.png"):
                st.image("bulinga.png", caption="BULINGA - Ifoto ya Administration (Front-view) y'Ishuri 🏫", use_container_width=True)
            if os.path.exists("btss.png"):
                st.image("btss.png", caption="BULINGA TSS - Logo ya BTSS ✨", use_container_width=True)

        current_messages.append({
            "role": "assistant", 
            "content": response_text,
            "show_image": is_image_query,
            "show_map": is_map_query
        })
        st.rerun()

    except Exception as e:
        thinking_placeholder.empty()
        st.error(f"❌ Habaye ikibazo. ⚠️\n\n**Error:**\n`{e}`")
