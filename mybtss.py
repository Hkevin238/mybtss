st.markdown("""
<style>

/* ==========================================
   EACH MESSAGE = SEPARATE FULL-WIDTH ROW
   ========================================== */

[data-testid="stChatMessage"] {
    width: 100% !important;
    display: flex !important;
    clear: both !important;
    margin-bottom: 24px !important;
    padding: 0 !important;
    background: transparent !important;
}


/* ==========================================
   AI MESSAGE
   LEFT
   ========================================== */

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

    max-width: 75% !important;

    margin-left: 0 !important;
    margin-right: auto !important;

    text-align: left !important;

    background: transparent !important;

    padding: 8px 12px !important;
}


/* ==========================================
   USER MESSAGE
   RIGHT
   ========================================== */

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarUser"]
) {
    justify-content: flex-end !important;
    flex-direction: row !important;
}


/* User content */

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarUser"]
) [data-testid="stChatMessageContent"] {

    max-width: 65% !important;

    margin-left: 0 !important;
    margin-right: 0 !important;

    text-align: left !important;

    background: #303030 !important;

    padding: 10px 16px !important;

    border-radius: 18px !important;
}


/* ==========================================
   USER AVATAR
   ========================================== */

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarUser"]
) [data-testid="stChatMessageAvatarUser"] {

    margin-left: 10px !important;
}


/* ==========================================
   AI AVATAR
   ========================================== */

[data-testid="stChatMessage"]:has(
    [data-testid="stChatMessageAvatarAssistant"]
) [data-testid="stChatMessageAvatarAssistant"] {

    margin-right: 10px !important;
}

</style>
""", unsafe_allow_html=True)
