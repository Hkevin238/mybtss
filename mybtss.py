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
# 2. CUSTOM CSS (STRICT CHAT ALIGNMENT FIX + ✨ MOVING SPARKLES)
# =========================================================

st.markdown("""
<style>

/* =====================================================
   MOVING SPARKLES BACKGROUND ANIMATION
   ===================================================== */

@keyframes moveSparkles {
    0% {
        background-position: 0 0, 0 0;
    }
    100% {
        background-position: -10000px 5000px, 5000px -10000px;
    }
}

.stApp {
    background-color: #111b21 !important;
    background-image: 
        radial-gradient(6px 6px at 20px 30px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(8px 8px at 40px 70px, #ffd700, rgba(0,0,0,0)),
        radial-gradient(5px 5px at 90px 40px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(7px 7px at 160px 120px, #fff8dc, rgba(0,0,0,0)),
        radial-gradient(6px 6px at 230px 180px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(8px 8px at 350px 250px, #ffd700, rgba(0,0,0,0)),
        radial-gradient(6px 6px at 450px 350px, #ffffff, rgba(0,0,0,0)) !important;
    background-repeat: repeat !important;
    background-size: 500px 500px !important;
    animation: moveSparkles 90s linear infinite !important;
    color: #e9edef !important;
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
   STRICT CHAT MESSAGE ALIGNMENT FIX (WHATSAPP STYLE)
   ===================================================== */

/* Force layout row for all chat messages */
[data-testid="stChatMessage"] {
    display: flex !important;
    width: 100% !important;
    margin-top: 10px !important;
    margin-bottom: 10px !important;
}

/* AI MESSAGE (Left Side) */
[data-testid="stChatMessage"][aria-label*="assistant"],
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    flex-direction: row !important;
    justify-content: flex-start !important;
    text-align: left !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {
    background-color: #202c33 !important;
    color: #e9edef !important;
    border-radius: 0px 12px 12px 12px !important;
    margin-right: auto !important;
    margin-left: 0 !important;
    max-width: 75% !important;
}

/* USER MESSAGE (Right Side) */
[data-testid="stChatMessage"][aria-label*="user"],
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse !important;
    justify-content: flex-start !important;
    text-align: left !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
    background-color: #005c4b !important;
    color: #e9edef !important;
    border-radius: 12px 0px 12px 12px !important;
    margin-left: auto !important;
    margin-right: 0 !important;
    max-width: 75% !important;
}


/* Chat Input Container Styling */
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

section[data-testid="stSidebar"] {
    background-color: #111b21 !important;
}

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
# 4. LIGHT MODE CONFIG
# =========================================================

if theme_mode == "Light Mode":
    st.markdown("""
    <style>
    .stApp {
        background-color: #efeae2 !important;
        background-image: none !important;
        color: #111b21 !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {
        background-color: #ffffff !important;
        color: #111b21 !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
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
# 5. CUSTOM THEME CONFIG
# =========================================================

elif theme_mode == "Custom Theme":
    st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a !important;
        background-image: none !important;
        color: #38bdf8 !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
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

You can answer questions about:
- School programs
- School fees
- School rules
- School location
- School schedule
- School religion
- School staff
- School contacts
- School combinations
- School meals
- School payment
- Student life
- School administration
- School Photos and Image Searches (Amafoto y'ikigo)

If a question is completely unrelated to BULINGA TVET SCHOOL,
politely refuse to answer.

=========================================================
SCHOOL PHOTOS & IMAGE SEARCH LINK
=========================================================
When a user asks for photos, pictures, or images of BULINGA TVET SCHOOL 
(e.g., "Nshaka amafoto ya bulinga", "show me school pictures"), you must 
provide them with the direct Google Image Search link using Markdown:

👉 [Reba amafoto ya Bulinga TVET School hano](https://www.google.com/search?q=bulinga+school+image)

=========================================================
SCHOOL DETAILS
=========================================================
School Name: BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TVET SCHOOL)
Location: MUHANGA, Mushishiro near KABADAHA Center.
Travel Time: Car (2 hours), Motorcycle (30 mins), On foot (3 hours).
School Fees: 92,000 Frw + 1,500 Frw Insurance + 2,000 Frw ID/Card = 95,500 Frw Total.
Account: Mwarimu Sacco, Account Number: 900009815200, Account Name: BULINGA TVET SCHOOL.
Combinations: SOD (Software Development), NIT (Networking), ACC (Accounting), CSA.
Contacts: Headmaster (0788546462), Bursar (0782612675), DOD (0785979951), DOS (0784020929).
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
# 8. AVATARS & SIDEBAR LOGO
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
st.sidebar.markdown(
    """
### 🤖 BULINGA AI
**Official AI Assistant**
Developed for: **BULINGA TECHNICAL SECONDARY SCHOOL**
Developers: **BULINGA Developers Team**
"""
)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# =========================================================
# 9. MAIN HEADER & SESSION STATE
# =========================================================

st.markdown('<h1 class="moving-title">🤖 BULINGA AI Assistant</h1>', unsafe_allow_html=True)
st.caption("Your Assistant guider for BULINGA Technical Secondary School")

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# 10. DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:
    role = message["role"]
    current_avatar = avatar_img if role == "assistant" else user_avatar
    
    with st.chat_message(role, avatar=current_avatar):
        st.markdown(message["content"])


# =========================================================
# 11. CHAT INPUT & RESPONSE HANDLING
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
            thinking_thinking_placeholder = locals().get('thinking_placeholder')
            if thinking_placeholder:
                thinking_placeholder.empty()
            st.error(f"❌ Habaye ikibazo.\n\n**Error:**\n`{e}`")
