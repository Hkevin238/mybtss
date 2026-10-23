import os
import base64
import uuid
import streamlit as st
from PIL import Image
from groq import Groq
from openai import OpenAI

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
    assistant_bubble_bg = "#e0e0fb"
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
