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
# 2. CUSTOM CSS (WHATSAPP STYLE + ✨ LARGER MOVING SPARKLES BACKGROUND)
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

/* =====================================================
   MAIN APP BACKGROUND (Starry Moving Sparkles + Dark Vibe)
   ===================================================== */

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
    margin-top: 10px !important;
    margin-bottom: 10px !important;
    padding: 0 !important;
    background: transparent !important;
}


/* =====================================================
   AI MESSAGE (LEFT SIDE)
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
   CHAT INPUT
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
        background-image: none !important;
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
        background-image: none !important;
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
# 6. BULINGA AI SYSTEM PROMPT (INCLUDING GOOGLE IMAGE SEARCH LINK)
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

Example:

"Sorry, I am BULINGA AI and I am designed specifically to
provide information about BULINGA TVET SCHOOL."


=========================================================
SCHOOL PHOTOS & IMAGE SEARCH LINK
=========================================================

When a user asks for photos, pictures, or images of BULINGA TVET SCHOOL 
(e.g., "Nshaka amafoto ya bulinga", "show me school pictures"), you must 
provide them with the direct Google Image Search link using Markdown:

👉 [Reba amafoto ya Bulinga TVET School hano](https://www.google.com/search?q=bulinga+school+image)

Always include this link so the user can easily click and view all related pictures directly on Google.


=========================================================
SCHOOL DETAILS
=========================================================

School Name:

BULINGA TECHNICAL SECONDARY SCHOOL
(BULINGA TVET SCHOOL)


=========================================================
LOCATION
=========================================================

MUHANGA, Mushishiro near KABADAHA Center.

The road is a dirt road (umuhanda w'igitaka).


=========================================================
TRAVEL TIME FROM MUHANGA GARE
=========================================================

By Car / Coaster:

2 hours


By Motorcycle:

30 minutes


On foot:

3 hours


By Helicopter:

15 minutes


=========================================================
SCHOOL FEES
=========================================================

School Fees / Minerval:

92,000 Frw


Accident Insurance:

1,500 Frw


School ID and Behavior Card:

2,000 Frw


TOTAL:

95,500 Frw


=========================================================
PAYMENT ACCOUNT
=========================================================

Bank:

Mwarimu Sacco


Account Number:

900009815200


Account Name:

BULINGA TVET SCHOOL


=========================================================
PAYMENT METHODS
=========================================================

Method 1:

Go physically to Mwarimu Sacco and pay to the school account.


Method 2:

Mobile Money:

Dial:

*182*3*10*1*Student_SDMS_Code#

Then follow the instructions.


=========================================================
MEALS
=========================================================

Students receive balanced meals.

Examples include:

- Rice
- Meat
- Posho / Kawunga
- Sweet potatoes
- Isombe
- Porridge
- Ugali
- Other balanced foods


=========================================================
DAILY SCHOOL SCHEDULE
=========================================================

8:30 AM:

Morning arrival and classes start.


Morning study:

3 hours.


Morning break follows.


Next study session:

2 hours.


Lunch:

11:45 AM.


Afternoon classes:

1:10 PM - 4:00 PM.


Preparation for evening revision:

From 4:00 PM.


Evening classroom cleaning:

7:15 PM.


Dinner:

7:30 PM.


After dinner:

Resting / sleeping time.


=========================================================
STAFF
=========================================================

The school has approximately:

30 staff members.


=========================================================
COMBINATIONS
=========================================================

BULINGA TVET SCHOOL offers 4 combinations:

1. SOD - Software Development
2. NIT - Networking and Internet Technology
3. ACC - Accounting
4. CSA

Each combination has its own dedicated computer laboratory.


=========================================================
RELIGION
=========================================================

The school is non-denominational.

The school does not belong to one specific religion.

Students may practice different religions.

Examples:

- Islam
- La Paix
- Catholic
- Jehovah's Witnesses

Every Friday and Sunday, respective groups gather for worship.

The school is also near a Catholic church.


=========================================================
SCHOOL CONTACTS
=========================================================

Headmaster:

0788546462

Email:

munoel20@gmail.com


Bursar:

0782612675


Discipline Master / DOD:

0785979951


Director of Studies / DOS:

0784020929


Secretary:

0785098759


School Email:

bulingatvetschool@gmail.com


=========================================================
SCHOOL RULES
=========================================================

Students are not allowed to bring or use:

- Laptops
- SIM cards
- Phones
- Headsets
- AirPods
- Other electronic devices


=========================================================
LOGO
=========================================================

The official school logo is:

btss.png


=========================================================
LANGUAGE
=========================================================

Always respond using the language selected by the user.

The current selected language will be provided separately.

Always maintain the BULINGA AI persona.
"""


# =========================================================
# 7. GROQ API KEY
# =========================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


if not GROQ_API_KEY:

    st.sidebar.warning(
        "⚠️ GROQ_API_KEY ntabwo yashyizwe muri Environment Variables."
    )


client = Groq(
    api_key=GROQ_API_KEY or "YOUR_GROQ_API_KEY"
)


# =========================================================
# 8. AVATARS
# =========================================================

# AI avatar
avatar_img = None

if os.path.exists("btss.png"):

    avatar_img = "btss.png"


# USER AVATAR
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

        st.sidebar.warning(
            "btss.png ntishobora gufunguka."
        )


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
# 12. MAIN HEADER (WITH MOVING ANIMATION)
# =========================================================

st.markdown('<h1 class="moving-title">🤖 BULINGA AI Assistant</h1>', unsafe_allow_html=True)


st.caption(
    "Your Assistant guider for BULINGA Technical Secondary School"
)


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


    if role == "assistant":

        current_avatar = avatar_img

    else:

        current_avatar = user_avatar


    with st.chat_message(
        role,
        avatar=current_avatar
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# 15. CHAT INPUT
# =========================================================

user_query = st.chat_input(
    "Ask related BULINGA TVET SCHOOL..."
)


# =========================================================
# 16. USER MESSAGE + AI RESPONSE
# =========================================================

if user_query:


    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )


    # =====================================================
    # USER MESSAGE
    # RIGHT SIDE
    # =====================================================

    with st.chat_message(
        "user",
        avatar=user_avatar
    ):

        st.markdown(
            user_query
        )


    # =====================================================
    # AI MESSAGE
    # LEFT SIDE
    # =====================================================

    with st.chat_message(
        "assistant",
        avatar=avatar_img
    ):


        thinking_placeholder = st.empty()


        thinking_placeholder.markdown(
            """
            <p class="thinking-text">
            ⚪ BULINGA AI thinking...
            </p>
            """,
            unsafe_allow_html=True
        )


        try:


            # =================================================
            # BUILD MESSAGE PAYLOAD
            # =================================================

            messages_payload = [

                {
                    "role": "system",

                    "content":

                    BULINGA_INFO

                    +

                    f"""

=========================================================
CURRENT PREFERRED LANGUAGE
=========================================================

{selected_lang}

Answer the user using this language.
"""
                }

            ]


            # =================================================
            # ADD CONVERSATION HISTORY
            # =================================================

            for message in st.session_state.messages:

                messages_payload.append(
                    {
                        "role": message["role"],
                        "content": message["content"]
                    }
                )


            # =================================================
            # SEND REQUEST TO GROQ
            # =================================================

            completion = client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=messages_payload,

                temperature=0.7,

                max_tokens=1024
            )


            # =================================================
            # GET AI RESPONSE
            # =================================================

            response_text = (
                completion
                .choices[0]
                .message
                .content
            )


            # =================================================
            # REMOVE THINKING
            # =================================================

            thinking_placeholder.empty()


            # =================================================
            # DISPLAY AI RESPONSE
            # =================================================

            st.markdown(
                response_text
            )


            # =================================================
            # SAVE AI RESPONSE
            # =================================================

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response_text
                }
            )


        except Exception as e:


            thinking_placeholder.empty()


            st.error(
                f"""
❌ Habaye ikibazo.

**Error:**

`{e}`

Nyamuneka reba niba **GROQ_API_KEY** yawe yashyizwe neza.
"""
            )
