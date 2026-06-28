import streamlit as st
import html as html_module
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage


# ---------------- MODEL ----------------
model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)


# ---------------- PAGE ----------------
st.set_page_config(
    page_title="MoodVerse AI",
    page_icon="🤖",
    layout="centered"
)


# ---------------- CUSTOM CSS / ANIMATIONS ----------------
st.markdown("""
<style>
    /* ====== IMPORTS ====== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* ====== ROOT VARIABLES ====== */
    :root {
        --primary-blue: #4285f4;
        --primary-purple: #a855f7;
        --primary-cyan: #06b6d4;
        --primary-pink: #ec4899;
        --glass-bg: rgba(15, 15, 30, 0.65);
        --glass-border: rgba(255, 255, 255, 0.08);
        --text-primary: #f0f0ff;
        --text-secondary: rgba(200, 200, 230, 0.7);
        --dark-bg: #06060e;
    }

    /* ====== ANIMATED BACKGROUND ====== */
    .stApp {
        background: var(--dark-bg) !important;
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: 0;
        pointer-events: none;
        background:
            radial-gradient(ellipse 80% 50% at 20% 20%, rgba(66, 133, 244, 0.15) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 30%, rgba(168, 85, 247, 0.12) 0%, transparent 55%),
            radial-gradient(ellipse 70% 50% at 50% 80%, rgba(6, 182, 212, 0.10) 0%, transparent 60%),
            radial-gradient(ellipse 50% 30% at 70% 60%, rgba(236, 72, 153, 0.08) 0%, transparent 50%);
        animation: auroraShift 12s ease-in-out infinite alternate;
    }

    @keyframes auroraShift {
        0% {
            background:
                radial-gradient(ellipse 80% 50% at 20% 20%, rgba(66, 133, 244, 0.15) 0%, transparent 60%),
                radial-gradient(ellipse 60% 40% at 80% 30%, rgba(168, 85, 247, 0.12) 0%, transparent 55%),
                radial-gradient(ellipse 70% 50% at 50% 80%, rgba(6, 182, 212, 0.10) 0%, transparent 60%),
                radial-gradient(ellipse 50% 30% at 70% 60%, rgba(236, 72, 153, 0.08) 0%, transparent 50%);
        }
        50% {
            background:
                radial-gradient(ellipse 70% 45% at 60% 15%, rgba(168, 85, 247, 0.18) 0%, transparent 60%),
                radial-gradient(ellipse 65% 50% at 25% 50%, rgba(6, 182, 212, 0.14) 0%, transparent 55%),
                radial-gradient(ellipse 80% 40% at 75% 75%, rgba(66, 133, 244, 0.10) 0%, transparent 60%),
                radial-gradient(ellipse 55% 35% at 40% 30%, rgba(236, 72, 153, 0.10) 0%, transparent 50%);
        }
        100% {
            background:
                radial-gradient(ellipse 85% 50% at 50% 30%, rgba(66, 133, 244, 0.17) 0%, transparent 60%),
                radial-gradient(ellipse 55% 45% at 30% 60%, rgba(168, 85, 247, 0.14) 0%, transparent 55%),
                radial-gradient(ellipse 70% 40% at 80% 50%, rgba(6, 182, 212, 0.12) 0%, transparent 60%),
                radial-gradient(ellipse 60% 35% at 20% 80%, rgba(236, 72, 153, 0.09) 0%, transparent 50%);
        }
    }

    /* ====== FLOATING PARTICLES ====== */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: 0;
        pointer-events: none;
        background-image:
            radial-gradient(2px 2px at 10% 15%, rgba(168, 85, 247, 0.5), transparent),
            radial-gradient(2px 2px at 20% 35%, rgba(66, 133, 244, 0.4), transparent),
            radial-gradient(1.5px 1.5px at 35% 55%, rgba(6, 182, 212, 0.5), transparent),
            radial-gradient(2px 2px at 45% 10%, rgba(236, 72, 153, 0.3), transparent),
            radial-gradient(1.5px 1.5px at 55% 75%, rgba(168, 85, 247, 0.4), transparent),
            radial-gradient(2px 2px at 65% 25%, rgba(6, 182, 212, 0.35), transparent),
            radial-gradient(1.5px 1.5px at 75% 65%, rgba(66, 133, 244, 0.45), transparent),
            radial-gradient(2px 2px at 85% 45%, rgba(236, 72, 153, 0.4), transparent),
            radial-gradient(1px 1px at 90% 85%, rgba(168, 85, 247, 0.5), transparent),
            radial-gradient(1.5px 1.5px at 30% 80%, rgba(66, 133, 244, 0.35), transparent);
        animation: particleDrift 25s linear infinite;
    }

    @keyframes particleDrift {
        0%   { transform: translateY(0px) translateX(0px); }
        50%  { transform: translateY(-12px) translateX(8px); }
        100% { transform: translateY(0px) translateX(0px); }
    }

    /* ====== Z-INDEX ====== */
    .stMainBlockContainer { position: relative; z-index: 1; }

    /* ====== HIDE STREAMLIT CHROME ====== */
    #MainMenu, footer, .stDeployButton { visibility: hidden; display: none; }
    header { visibility: hidden !important; }

    /* ====== GLOBAL TYPOGRAPHY ====== */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* ====== MAIN CONTAINER ====== */
    .stMainBlockContainer > div {
        max-width: 860px;
        margin: 0 auto;
        padding: 2rem 2.5rem 5rem !important;
    }

    /* ====== PREVENT UNNECESSARY SCROLL ====== */
    .stApp, html, body { overflow-x: hidden !important; }

    /* ====== HERO HEADER ====== */
    .hero-header {
        text-align: center;
        padding: 2rem 1rem 1.5rem;
        margin-bottom: 0.5rem;
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #4285f4 0%, #a855f7 40%, #ec4899 70%, #06b6d4 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientText 5s ease-in-out infinite;
        margin: 0 0 0.3rem 0 !important;
        padding: 0 !important;
        letter-spacing: -0.02em;
        line-height: 1.2 !important;
        display: block;
    }

    @keyframes gradientText {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    .hero-header .subtitle {
        font-size: 0.95rem;
        color: var(--text-secondary);
        font-weight: 400;
        letter-spacing: 0.03em;
        margin-top: 0.2rem;
    }

    .hero-header .divider-line {
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, #4285f4, #a855f7, #06b6d4);
        border-radius: 2px;
        margin: 1rem auto 0;
        animation: dividerGlow 3s ease-in-out infinite alternate;
    }

    @keyframes dividerGlow {
        0% { box-shadow: 0 0 8px rgba(66, 133, 244, 0.4); width: 80px; }
        100% { box-shadow: 0 0 16px rgba(168, 85, 247, 0.5); width: 120px; }
    }

    /* ====== SECTION LABEL ====== */
    .section-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: var(--text-secondary);
        margin-bottom: 0.6rem;
        text-align: center;
    }

    /* ====== MODE BUTTONS ====== */
    div[data-testid="stColumns"] .stButton > button {
        width: 100% !important;
        padding: 1rem 0.8rem !important;
        border-radius: 16px !important;
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        line-height: 1.6 !important;
        min-height: 90px !important;
    }

    div[data-testid="stColumns"] .stButton > button:hover {
        transform: translateY(-4px) !important;
        border-color: rgba(255, 255, 255, 0.18) !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35) !important;
    }

    div[data-testid="stColumns"] .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }

    /* ====== HIDE DEFAULT CHAT MESSAGES ====== */
    .stChatMessage { display: none !important; }

    /* ====== CUSTOM CHAT AREA ====== */
    .chat-area {
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        padding: 0.5rem 0;
        margin-bottom: 1rem;
    }

    .chat-bubble {
        max-width: 75%;
        padding: 0.85rem 1.2rem;
        font-size: 0.95rem;
        line-height: 1.55;
        color: var(--text-primary);
        word-wrap: break-word;
        animation: bubbleIn 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    }

    @keyframes bubbleIn {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* User bubble — dark, right */
    .chat-bubble.user-bubble {
        background: rgba(12, 12, 20, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 20px 20px 4px 20px;
        align-self: flex-end;
        backdrop-filter: blur(12px);
    }

    .chat-bubble.user-bubble:hover {
        border-color: rgba(255, 255, 255, 0.14);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }

    /* AI bubble — gradient, left */
    .chat-bubble.ai-bubble {
        background: linear-gradient(135deg, rgba(55, 65, 160, 0.3), rgba(168, 85, 247, 0.2) 45%, rgba(6, 182, 212, 0.15));
        border: 1px solid rgba(168, 85, 247, 0.18);
        border-radius: 20px 20px 20px 4px;
        align-self: flex-start;
        backdrop-filter: blur(12px);
    }

    .chat-bubble.ai-bubble:hover {
        border-color: rgba(168, 85, 247, 0.35);
        box-shadow: 0 4px 24px rgba(168, 85, 247, 0.12);
    }

    /* Empty state */
    .chat-empty {
        text-align: center;
        padding: 3rem 1rem;
        color: var(--text-secondary);
    }
    .chat-empty .empty-icon { font-size: 2.5rem; display: block; margin-bottom: 0.6rem; opacity: 0.5; }
    .chat-empty p { font-size: 0.9rem; margin: 0; }

    /* ====== BOTTOM BAR ====== */
    [data-testid="stBottom"] {
        background: transparent !important;
        border: none !important;
    }

    [data-testid="stBottom"] > div {
        background: transparent !important;
    }

    /* ====== CHAT INPUT ====== */
    .stChatInput { border-radius: 16px !important; overflow: hidden; }

    .stChatInput > div {
        background: rgba(15, 15, 30, 0.7) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        transition: all 0.3s ease;
    }

    .stChatInput > div:focus-within {
        border-color: rgba(168, 85, 247, 0.4) !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.1), 0 0 40px rgba(66, 133, 244, 0.05) !important;
    }

    .stChatInput textarea {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
    }

    .stChatInput textarea::placeholder { color: var(--text-secondary) !important; }

    .stChatInput button {
        background: linear-gradient(135deg, #4285f4, #a855f7) !important;
        border: none !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }

    .stChatInput button:hover {
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.4) !important;
        transform: scale(1.05);
    }

    /* ====== HIDE DIVIDERS ====== */
    .stHorizontalRule, hr { display: none !important; }

    /* ====== PENCIL (NEW CHAT) BUTTON — styled as an icon, aligned via JS ====== */
    button[kind="primary"][data-testid="stBaseButton-primary"] {
        width: 46px !important;
        height: 46px !important;
        min-width: 46px !important;
        min-height: 46px !important;
        border-radius: 16px !important;
        background: rgba(15, 15, 30, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        padding: 0 !important;
        font-size: 0 !important;
        color: transparent !important;
        overflow: hidden !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    button[kind="primary"][data-testid="stBaseButton-primary"]:hover {
        background: rgba(168, 85, 247, 0.15) !important;
        border-color: rgba(168, 85, 247, 0.3) !important;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.15) !important;
        transform: translateY(-2px) !important;
    }

    button[kind="primary"][data-testid="stBaseButton-primary"]::after {
        content: '✎';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 1.2rem;
        color: rgba(200, 200, 230, 0.7);
    }

    button[kind="primary"][data-testid="stBaseButton-primary"]:hover::after {
        color: #f0f0ff;
    }

    /* ====== ACTIVE MODE BADGE ====== */
    .active-mode-badge {
        text-align: center;
        margin: 0.8rem 0 1.5rem;
    }

    .active-mode-badge span {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--text-secondary);
        background: rgba(168, 85, 247, 0.1);
        border: 1px solid rgba(168, 85, 247, 0.2);
        padding: 0.35rem 1rem;
        border-radius: 20px;
        letter-spacing: 0.03em;
    }

    /* ====== WARNING ====== */
    .stAlert {
        background: rgba(234, 179, 8, 0.1) !important;
        border: 1px solid rgba(234, 179, 8, 0.25) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(16px) !important;
    }

    /* ====== SCROLLBAR ====== */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(168, 85, 247, 0.25); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(168, 85, 247, 0.4); }

    /* ====== RESPONSIVE ====== */
    @media (max-width: 640px) {
        .hero-title { font-size: 2rem !important; }
        div[data-testid="stColumns"] .stButton > button {
            min-height: 75px !important;
            padding: 0.7rem 0.5rem !important;
            font-size: 0.8rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown("""
<div class="hero-header">
    <span class="hero-title">MoodVerse AI</span>
    <p class="subtitle">Experience AI with Personality — Choose a Mood, Start a Conversation</p>
    <div class="divider-line"></div>
</div>
""", unsafe_allow_html=True)


# ---------------- MODE SELECTION ----------------
st.markdown('<p class="section-label">⚡ Select AI Personality</p>', unsafe_allow_html=True)

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "😂 Funny"

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    if st.button("😡\nAngry\n_Aggressive & fierce_", use_container_width=True):
        st.session_state.selected_mode = "😡 Angry"
        st.rerun()

with col2:
    if st.button("😂\nFunny\n_Humorous & witty_", use_container_width=True):
        st.session_state.selected_mode = "😂 Funny"
        st.rerun()

with col3:
    if st.button("😢\nSad\n_Emotional & deep_", use_container_width=True):
        st.session_state.selected_mode = "😢 Sad"
        st.rerun()

mode_choice = st.session_state.selected_mode

st.markdown(f"""
<div class="active-mode-badge">
    <span>Currently: {mode_choice}</span>
</div>
""", unsafe_allow_html=True)


# ---------------- MAP MODE ----------------
if mode_choice == "😡 Angry":
    mode = "You are an angry AI agent. You respond aggressively and impatiently."
elif mode_choice == "😂 Funny":
    mode = "You are a very funny AI agent. You respond with humor and jokes."
else:
    mode = "You are a very sad AI agent. You respond in a depressed and emotional tone."


# ---------------- SESSION MEMORY ----------------
if "messages" not in st.session_state or st.session_state.get("current_mode") != mode:
    st.session_state.current_mode = mode
    st.session_state.messages = [SystemMessage(content=mode)]


# ---------------- DISPLAY CHAT ----------------
chat_html_parts = []
has_chat = False

for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        has_chat = True
        escaped = html_module.escape(msg.content)
        chat_html_parts.append(f'<div class="chat-bubble user-bubble">{escaped}</div>')
    elif isinstance(msg, AIMessage):
        has_chat = True
        escaped = html_module.escape(msg.content)
        chat_html_parts.append(f'<div class="chat-bubble ai-bubble">{escaped}</div>')

if has_chat:
    st.markdown('<div class="chat-area">' + ''.join(chat_html_parts) + '</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="chat-empty">
        <span class="empty-icon">💬</span>
        <p>Start a conversation — type a message below!</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------- USER INPUT ----------------
user_input = st.chat_input("Type your message here...")

if user_input:
    if user_input == "0":
        st.warning("Conversation ended. Refresh page to start again.")
        st.stop()

    st.session_state.messages.append(HumanMessage(content=user_input))
    response = model.invoke(st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=response.content))
    st.rerun()


# ---------------- NEW CHAT (PENCIL) BUTTON ----------------
if st.button("reset", key="new_chat_btn", type="primary"):
    st.session_state.messages = [SystemMessage(content=mode)]
    st.rerun()

# ---------------- PERFECT ALIGNMENT VIA JS ----------------
import streamlit.components.v1 as components

components.html("""
<script>
    // Access the parent document since this runs in an iframe
    const parentDoc = window.parent.document;
    
    // Find the pencil button and the chat input
    const button = parentDoc.querySelector('button[kind="primary"][data-testid="stBaseButton-primary"]');
    const chatInput = parentDoc.querySelector('.stChatInput');
    
    if (button && chatInput) {
        // If not already wrapped, wrap them together!
        let wrapper = parentDoc.querySelector('.chat-input-flex-wrapper');
        if (!wrapper) {
            // Create flex wrapper
            wrapper = parentDoc.createElement('div');
            wrapper.className = 'chat-input-flex-wrapper';
            wrapper.style.display = 'flex';
            wrapper.style.alignItems = 'center';
            wrapper.style.gap = '12px';
            wrapper.style.width = '100%';
            
            // Insert wrapper where chat input was
            chatInput.parentNode.insertBefore(wrapper, chatInput);
            
            // Move chat input into wrapper
            wrapper.appendChild(chatInput);
            chatInput.style.flex = '1';
            
            // Move pencil button into wrapper
            wrapper.appendChild(button);
        }
    }
</script>
""", height=0, width=0)