import os
import streamlit as st
from PIL import Image
from groq import Groq


st.set_page_config(
    page_title="BULINGA TSS AI",
    page_icon="btss.png",
    layout="centered",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>

/* ================================
   GENERAL
   ================================ */

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


/* ================================
   EVERY MESSAGE HAS ITS OWN ROW
   ================================ */

[data-testid="stChatMessage"] {
    width: 100% !important;
    display: flex !important;
    clear: both !important;
    padding: 0 !important;
    margin-top: 8px !important;
    margin-bottom: 28px !important;
    background: transparent !important;
}


/* ================================
   AI = LEFT
   ================================ */

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarAssistant"]
) {
    justify-content: flex-start !important;
    flex-direction: row !important;
}


/* AI CONTENT */

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarAssistant"]
) [data-testid="stChatMessageContent"] {
    max-width: 75% !important;
    margin-left: 0 !important;
    margin-right: auto !important;
    text-align: left !important;
    background: transparent !important;
    padding: 8px 12px !important;
}


/* ================================
   USER = RIGHT
   ================================ */

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarUser"]
) {
    justify-content: flex-end !important;
    flex-direction: row !important;
}


/* USER CONTENT */

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarUser"]
) [data-testid="stChatMessageContent"] {
    max-width: 65% !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    text-align: left !important;
    background-color: #303030 !important;
    padding: 10px 16px !important;
    border-radius: 18px !important;
}


/* ================================
   AVATARS
   ================================ */

[data-testid="stChatMessageAvatarAssistant"] {
    margin-right: 10px !important;
}

[data-testid="stChatMessageAvatarUser"] {
    margin-left: 10px !important;
}


/* ================================
   CHAT INPUT
   ================================ */

.stChatInputContainer {
    background-color: #2f2f3f !important;
    border-radius: 28px !important;
    border: 1px solid #424255 !important;
    padding: 6px 14px !important;
}


/* ================================
   THINKING
   ================================ */

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

</style>
""", unsafe_allow_html=True)
