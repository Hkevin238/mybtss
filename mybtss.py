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
# 2. CUSTOM CSS (MESSENGER / WHATSAPP STYLE ALIGNMENT)
# =========================================================

st.markdown("""
<style>

/* App Background */
.stApp {
    background-color: #121212 !important;
    color: #e4e6eb !important;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { background: transparent !important; }

@keyframes bounceSlow {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}

.moving-title {
    display: inline-block;
    animation: bounceSlow 3s ease-in-out infinite;
}


/* =====================================================
   MESSENGER CHAT BUBBLE ALIGNMENT FIX
   ===================================================== */

/* Base chat message container */
[data-testid="stChatMessage"] {
    display: flex !important;
    width: 100% !important;
    margin-top: 8px !important;
    margin-bottom: 8px !important;
}

/* 1. ASSISTANT MESSAGE (Left Side - Grey/Dark Bubble) */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    flex-direction: row !important;
    justify-content: flex-start !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {
    background-color: #3a3b3c !important;
    color: #e4e6eb !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 10px 14px !important;
    max-width: 75% !important;
    margin-right: auto !important;
    margin-left: 0 !important;
}

/* 2. USER MESSAGE (Right Side - Messenger Blue Bubble) */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse !important;
    justify-content: flex-start !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
    background-color: #0084ff !important;
    color: #ffffff !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 10px 14px !important;
    max-width: 75% !important;
    margin-left: auto !important;
    margin-right: 0 !important;
}


/* Chat Input Container Styling */
.stChatInputContainer {
    background-color: #242526 !important;
    border-radius: 24px !important;
    border: 1px solid #3a3b3c !important;
    padding: 4px 12px !important;
}

.stChatInputContainer textarea {
    color: #e4e6eb !important;
    font-size: 15px !important;
}

.stChatInputContainer textarea::placeholder {
    color: #b0b3b8 !important;
}

.thinking-text {
    font-style: italic;
    color: #b0b3b8;
}

section[data-testid="stSidebar"] {
    background-color: #18191a !important;
}

.stButton button {
    border-radius: 8px !important;
    border: none !important;
    background-color: #3a3b3c !important;
    color: #e4e6eb !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. SIDEBAR
# =========================================================

st.sidebar.title("Settings & Control")

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


# =========================================================
# 4. BULINGA AI SYSTEM PROMPT
# =========================================================

BULINGA_INFO = """
You are BULINGA AI, an official AI assistant built exclusively
for BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TVET SCHOOL).
You were developed exclusively by Developer Kevin.

CORE RULE:
You ONLY answer questions related to BULINGA TVET SCHOOL.
If a question is completely unrelated to BULINGA TVET SCHOOL, politely refuse to answer.

SCHOOL DETAILS:
School Name: BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TVET SCHOOL)
Location: MUHANGA, Mushishiro near KABADAHA Center.
School Fees: 92,000 Frw + 1,500 Frw Insurance + 2,000 Frw ID/Card = 95,500 Frw Total.
Account: Mwarimu Sacco, Account Number: 900009815200, Account Name: BULINGA TVET SCHOOL.
Combinations: SOD (Software Development), NIT (Networking), ACC (Accounting), CSA.
Contacts: Headmaster (0788546462), Bursar (0782612675), DOD (0785979951), DOS (0784020929).
"""


# =========================================================
# 5. GROQ API KEY
# =========================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.sidebar.warning("⚠️ GROQ_API_KEY ntabwo yashyizwe muri Environment Variables.")

client = Groq(
    api_key=GROQ_API_KEY or "YOUR_GROQ_API_KEY"
)


# =========================================================
# 6. AVATARS & SIDEBAR LOGO
# =========================================================

avatar_img = None
if os.path.exists("btss.png"):
    avatar_img = "btss.png"

user_avatar = "👤"

if avatar_img:
    try:
        logo_img = Image.open(avatar_img)
        st.sidebar.image(logo_img, caption="BULINGA TVET SCHOOL", use_container_width=True)
    except Exception:
        pass

st.sidebar.markdown("---")
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# =========================================================
# 7. MAIN HEADER & SESSION STATE
# =========================================================

st.markdown('<h1 class="moving-title">🤖 BULINGA AI Assistant</h1>', unsafe_allow_html=True)
st.caption("Your Assistant guider for BULINGA Technical Secondary School")

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# 8. DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:
    role = message["role"]
    current_avatar = avatar_img if role == "assistant" else user_avatar
    
    with st.chat_message(role, avatar=current_avatar):
        st.markdown(message["content"])


# =========================================================
# 9. CHAT INPUT & RESPONSE HANDLING
# =========================================================

user_query = st.chat_input("Ask related BULINGA TVET SCHOOL...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(user_query)

    with st.chat_message("assistant", avatar=avatar_img):
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown(
            '<p class="thinking-text">⚪ BULINGA AI thinking...</p>',
            unsafe_allow_html=True
        )

        try:
            messages_payload = [
                {
                    "role": "system",
                    "content": BULINGA_INFO + f"\n\nCURRENT PREFERRED LANGUAGE:\n{selected_lang}\nAnswer the user using this language."
                }
            ]

            for message in st.session_state.messages:
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
            st.markdown(response_text)

            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            if 'thinking_placeholder' in locals():
                thinking_placeholder.empty()
            st.error(f"❌ Habaye ikibazo.\n\n**Error:**\n`{e}`")
