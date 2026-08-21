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
# 2. CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* ==============================
       MAIN APPLICATION
       ============================== */

    .stApp {
        background-color: #212121;
        color: #ececec;
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


    /* ==============================
       CHAT AREA
       ============================== */

    [data-testid="stChatMessage"] {
        width: 100% !important;
        display: flex !important;
        margin-bottom: 18px !important;
        padding: 0 !important;
        background: transparent !important;
    }


    /* ==============================
       AI MESSAGE - LEFT
       ============================== */

    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarAssistant"]
    ) {
        justify-content: flex-start !important;
        flex-direction: row !important;
    }


    /* AI content */

    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarAssistant"]
    ) [data-testid="stChatMessageContent"] {

        text-align: left !important;
        background: transparent !important;
        color: #ececec !important;
        max-width: 80% !important;
        padding: 8px 12px !important;
    }


    /* ==============================
       USER MESSAGE - RIGHT
       ============================== */

    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) {
        justify-content: flex-end !important;
        flex-direction: row-reverse !important;
    }


    /* User content */

    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) [data-testid="stChatMessageContent"] {

        text-align: left !important;
        background-color: #303030 !important;
        color: #ffffff !important;

        max-width: 75% !important;

        padding: 10px 16px !important;

        border-radius: 18px !important;

        margin-left: auto !important;
        margin-right: 0 !important;
    }


    /* ==============================
       AVATARS
       ============================== */

    [data-testid="stChatMessageAvatarAssistant"] {
        margin-right: 10px !important;
    }

    [data-testid="stChatMessageAvatarUser"] {
        margin-left: 10px !important;
    }


    /* ==============================
       CHAT INPUT
       ============================== */

    .stChatInputContainer {

        background-color: #2f2f3f !important;

        border-radius: 28px !important;

        border: 1px solid #424255 !important;

        padding: 6px 14px !important;

        box-shadow:
            0 4px 15px rgba(0,0,0,0.4);
    }


    .stChatInputContainer textarea {

        color: #ffffff !important;

        font-size: 16px !important;
    }


    .stChatInputContainer textarea::placeholder {

        color: #9a9aa5 !important;
    }


    /* ==============================
       THINKING ANIMATION
       ============================== */

    .thinking-text {

        font-style: italic;

        color: #8e8ea0;

        animation: pulse 1.5s infinite;
    }


    @keyframes pulse {

        0% {
            opacity: 0.4;
        }

        50% {
            opacity: 1;
        }

        100% {
            opacity: 0.4;
        }
    }


    /* ==============================
       SIDEBAR
       ============================== */

    section[data-testid="stSidebar"] {

        background-color: #171717 !important;
    }


    /* ==============================
       BUTTONS
       ============================== */

    .stButton button {

        border-radius: 10px;

        border: 1px solid #424255;

        background-color: #2f2f3f;

        color: white;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Settings & Control")


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
# 4. THEMES
# =========================================================

if theme_mode == "Light Mode":

    st.markdown("""
    <style>

    .stApp {
        background-color: #ffffff !important;
        color: #111111 !important;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarUser"]
    ) [data-testid="stChatMessageContent"] {

        background-color: #eeeeee !important;
        color: #111111 !important;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="stChatMessageAvatarAssistant"]
    ) [data-testid="stChatMessageContent"] {

        color: #111111 !important;
    }

    </style>
    """, unsafe_allow_html=True)


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
# 5. BULINGA SCHOOL INFORMATION / SYSTEM PROMPT
# =========================================================

BULINGA_INFO = """

You are BULINGA AI, an official AI assistant built exclusively
for BULINGA TECHNICAL SECONDARY SCHOOL (BULINGA TVET SCHOOL).

You were developed exclusively by Developer Kevin.

If anyone asks who created you, say:

"I was created by Developer Kevin for BULINGA TVET SCHOOL."

=========================================================
CORE RULE
=========================================================

You ONLY answer questions related to:

- BULINGA TVET SCHOOL
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
- Student life at BULINGA TVET SCHOOL

If a question is completely unrelated to BULINGA TVET SCHOOL,
politely refuse to answer.

Example:

"Sorry, I am BULINGA AI and I am designed specifically to
provide information about BULINGA TVET SCHOOL."

=========================================================
SCHOOL INFORMATION
=========================================================

School Name:

BULINGA TECHNICAL SECONDARY SCHOOL
(BULINGA TVET SCHOOL)

Location:

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

Total:

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
- La Jeunesse / La Paix
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

If the selected language is Kinyarwanda,
answer in Kinyarwanda.

If the selected language is English,
answer in English.

If the selected language is French,
answer in French.

And so on.

Always maintain the BULINGA AI persona.
"""


# =========================================================
# 6. GROQ CLIENT
# =========================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


if not GROQ_API_KEY:

    st.sidebar.error(
        "⚠️ GROQ_API_KEY ntabwo yashyizwe muri environment variables."
    )


client = Groq(
    api_key=GROQ_API_KEY or "YOUR_GROQ_API_KEY"
)


# =========================================================
# 7. LOGO
# =========================================================

avatar_img = None


if os.path.exists("btss.png"):

    avatar_img = "btss.png"

    try:

        logo_img = Image.open("btss.png")

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
# 8. SIDEBAR INFORMATION
# =========================================================

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    ### 🤖 BULINGA AI

    **Official AI Assistant**

    Developed for:

    **BULINGA TECHNICAL SECONDARY SCHOOL**

    Developer:

    **Kevin**
    """
)


# =========================================================
# 9. CLEAR CHAT BUTTON
# =========================================================

if st.sidebar.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()


# =========================================================
# 10. MAIN HEADER
# =========================================================

st.title("🤖 BULINGA AI Assistant")

st.caption(
    "Your intelligent guide for "
    "BULINGA Technical Secondary School"
)


# =========================================================
# 11. SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# 12. DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    role = message["role"]

    if role == "assistant":

        current_avatar = avatar_img

    else:

        current_avatar = None

    with st.chat_message(
        role,
        avatar=current_avatar
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# 13. CHAT INPUT
# =========================================================

user_query = st.chat_input(
    "Ask about BULINGA TVET SCHOOL..."
)


# =========================================================
# 14. PROCESS USER MESSAGE
# =========================================================

if user_query:

    # -----------------------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )


    # -----------------------------------------------
    # DISPLAY USER MESSAGE
    # RIGHT SIDE
    # -----------------------------------------------

    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_query
        )


    # -----------------------------------------------
    # AI RESPONSE
    # LEFT SIDE
    # -----------------------------------------------

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

            # ---------------------------------------
            # BUILD MESSAGES
            # ---------------------------------------

            messages_payload = [

                {
                    "role": "system",
                    "content":
                        BULINGA_INFO
                        +
                        f"""

Current Preferred Language:
{selected_lang}
"""
                }

            ]


            # Add conversation history

            for message in st.session_state.messages:

                messages_payload.append(
                    {
                        "role": message["role"],
                        "content": message["content"]
                    }
                )


            # ---------------------------------------
            # GROQ REQUEST
            # ---------------------------------------

            completion = client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=messages_payload,

                temperature=0.7,

                max_tokens=1024
            )


            # ---------------------------------------
            # GET AI RESPONSE
            # ---------------------------------------

            response_text = (
                completion
                .choices[0]
                .message
                .content
            )


            # ---------------------------------------
            # REMOVE THINKING
            # ---------------------------------------

            thinking_placeholder.empty()


            # ---------------------------------------
            # DISPLAY AI RESPONSE
            # ---------------------------------------

            st.markdown(
                response_text
            )


            # ---------------------------------------
            # SAVE AI RESPONSE
            # ---------------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response_text
                }
            )


        except Exception as e:

            thinking_placeholder.empty()

            error_msg = f"""
Habaye ikibazo ❌

**Error:**
`{e}`

Nyamuneka reba niba **GROQ_API_KEY** yawe yashyizwe neza.
"""

            st.error(
                error_msg
            )
