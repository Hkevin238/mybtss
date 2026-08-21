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
# 2. CUSTOM CSS (WHATSAPP STYLE CHAT)
# =========================================================

st.markdown("""
<style>

/* =====================================================
   MAIN APP BACKGROUND (WhatsApp Dark Theme vibe)
   ===================================================== */

.stApp {
    background-color: #111b21;
    color: #e9edef;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* =====================================================
   SLOW UP AND DOWN ANIMATION FOR TITLE
   ===================================================== */

@keyframes bounceSlow {
    0% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-8px);
    }
    100% {
        transform: translateY(0px);
    }
}

.moving-title {
    display: inline-block;
    animation: bounceSlow 3s ease-in-out infinite;
}


/* =====================================================
   CHAT MESSAGE ROW CONTAINER
   ===================================================== */

[data-testid="stChatMessage"] {
    width: 100% !important;
    display: flex !important;
    clear: both !important;
    position: relative !important;
    margin-top: 8px !important;
    margin-bottom: 8px !important;
    padding: 0 !important;
    background: transparent !important;
}


/* =====================================================
   AI MESSAGE (LEFT SIDE - WHATSAPP STYLE)
   ===================================================== */

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarAssistant"]
) {
    width: 100% !important;
    justify-content: flex-start !important;
    flex-direction: row !important;
    text-align: left !important;
}

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarAssistant"]
) [data-testid="stChatMessageContent"] {
    max-width: 75% !important;
    margin-left: 0 !important;
    margin-right: auto !important;
    text-align: left !important;
    background-color: #202c33 !important;
    color: #e9edef !important;
    padding: 10px 14px !important;
    border-radius: 0px 12px 12px 12px !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}


/* =====================================================
   USER MESSAGE (RIGHT SIDE - WHATSAPP STYLE)
   ===================================================== */

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarUser"]
) {
    width: 100% !important;
    justify-content: flex-end !important;
    flex-direction: row-reverse !important;
    text-align: right !important;
}

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarUser"]
) [data-testid="stChatMessageContent"] {
    max-width: 75% !important;
    margin-left: auto !important;
    margin-right: 0 !important;
    text-align: left !important;
    background-color: #005c4b !important;
    color: #e9edef !important;
    padding: 10px 14px !important;
    border-radius: 12px 0px 12px 12px !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}


/* =====================================================
   AVATARS SPACING
   ===================================================== */

[data-testid="stChatMessageAvatarAssistant"] {
    margin-right: 8px !important;
    flex-shrink: 0 !important;
}

[data-testid="stChatMessageAvatarUser"] {
    margin-left: 8px !important;
    flex-shrink: 0 !important;
}


/* =====================================================
   CHAT INPUT (WHATSAPP BAR STYLE)
   ===================================================== */

.stChatInputContainer {
    background-color: #202c33 !important;
    border-radius: 24px !important;
    border: none !important;
    padding: 6px 14px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
}

.stChatInputContainer textarea {
    color: #e9edef !important;
    font-size: 16px !important;
}

.stChatInputContainer textarea::placeholder {
    color: #8696a0 !important;
}


/* =====================================================
   THINKING ANIMATION
   ===================================================== */

.thinking-text {
    font-style: italic;
    color: #8696a0;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { opacity: 0.4; }
    50% { opacity: 1; }
    100% { opacity: 0.4; }
}


/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {
    background-color: #111b21 !important;
}


/* =====================================================
   BUTTON
   ===================================================== */

.stButton button {
    border-radius: 10px !important;
    border: none !important;
    background-color: #202c33 !important;
    color: #e9edef !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. SIDEBAR
# =========================================================

st.sidebar.title("Settings & Control")

theme_mode = st.sidebar.selectbox(
    "Select Theme / Imiterere",
    [
        "Dark Mode",
        "Light Mode",
        "Custom Theme"
    ]
)

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
# 4. LIGHT MODE
# =========================================================

if theme_mode == "Light Mode":

    st.markdown("""
    <style>
    .stApp {
        background-color: #efeae2 !important;
        color: #111b21 !important;
    }
    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarAssistant"]
    ) [data-testid="stChatMessageContent"] {
        background-color: #ffffff !important;
        color: #111b21 !important;
    }
    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) [data-testid="stChatMessageContent"] {
        background-color: #d9fdd3 !important;
        color: #111b21 !important;
    }
    .stChatInputContainer {
        background-color: #f0f2f5 !important;
    }
    .stChatInputContainer textarea {
        color: #111b21 !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)


# =========================================================
# 5. CUSTOM THEME
# =========================================================

elif theme_mode == "Custom Theme":

    st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a !important;
        color: #38bdf8 !important;
    }
    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) [data-testid="stChatMessageContent"] {
        background-color: #1e293b !important;
        color: #e0f2fe !important;
    }
    </style>
    """, unsafe_allow_html=True)


# =========================================================
# 6. BULINGA AI SYSTEM PROMPT
# =========================================================

BULINGA_INFO = """
You are BULINGA AI, an official AI assistant built exclusively
for BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TVET SCHOOL).
You were developed exclusively by Developer Kevin.
If anyone asks who created you, say:
"I was created by BULINGA Developers Team for BULINGA TVET SCHOOL."

=========================================================
CORE RULE
=========================================================
You ONLY answer questions related to BULINGA TVET SCHOOL.
If a question is completely unrelated, politely refuse to answer.

=========================================================
SCHOOL DETAILS
=========================================================
School Name: BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TVET SCHOOL)
Location: MUHANGA, Mushishiro near KABADAHA Center.
School Fees Total: 95,500 Frw
Payment Account: Mwarimu Sacco (900009815200)
"""


# =========================================================
# 7. GROQ API KEY
# =========================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.sidebar.warning("⚠️ GROQ_API_KEY ntabwo yashyizwe muri Environment Variables.")

client = Groq(
    api_key=GROQ_API_KEY or "YOUR_GROQ_API_KEY"
)


# =========================================================
# 8. AVATARS
# =========================================================

avatar_img = None
if os.path.exists("btss.png"):
    avatar_img = "btss.png"

user_avatar = "👤"


# =========================================================
# 9. SIDEBAR LOGO
# =========================================================

if avatar_img:
    try:
        logo_img = Image.open(avatar_img)
        st.sidebar.image(
            logo_img,
            caption="BULINGA TVET SCHOOL",
            use_container_width=True
        )
    except Exception:
        st.sidebar.warning("btss.png ntishobora gufunguka.")


# =========================================================
# 10. SIDEBAR INFORMATION
# =========================================================

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
### 🤖 BULINGA AI
**Official AI Assistant**
Developed for:
**BULINGA TECHNICAL SECONDARY SCHOOL**
Developers:
**BULINGA Developers Team**
"""
)


# =========================================================
# 11. CLEAR CHAT
# =========================================================

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# =========================================================
# 12. MAIN HEADER
# =========================================================

st.markdown('<h1 class="moving-title">🤖 BULINGA AI Assistant</h1>', unsafe_allow_html=True)
st.caption("Your Assistant guider for BULINGA Technical Secondary School")


# =========================================================
# 13. SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# 14. DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:
    role = message["role"]
    current_avatar = avatar_img if role == "assistant" else user_avatar

    with st.chat_message(role, avatar=current_avatar):
        st.markdown(message["content"])


# =========================================================
# 15. CHAT INPUT
# =========================================================

user_query = st.chat_input("Ask related BULINGA TVET SCHOOL...")


# =========================================================
# 16. USER MESSAGE + AI RESPONSE
# =========================================================

if user_query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

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
                    "content": BULINGA_INFO + f"\n\nCURRENT PREFERRED LANGUAGE: {selected_lang}"
                }
            ]

            for message in st.session_state.messages:
                messages_payload.append(
                    {
                        "role": message["role"],
                        "content": message["content"]
                    }
                )

            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages_payload,
                temperature=0.7,
                max_tokens=1024
            )

            response_text = completion.choices[0].message.content

            thinking_placeholder.empty()
            st.markdown(response_text)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response_text
                }
            )

        except Exception as e:
            thinking_placeholder.empty()
            st.error(f"❌ Habaye ikibazo.\n\n**Error:** `{e}`")
