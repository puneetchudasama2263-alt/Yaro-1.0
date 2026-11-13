
import os
import streamlit as st
from openai import OpenAI

# ==================================
# YARO 1.0 - AI ASSISTANT
# ==================================

st.set_page_config(
    page_title="YARO 1.0 - AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# API configuration
API_KEY = st.secrets.get("OPENAI_API_KEY", "")
MODEL = st.secrets.get("OPENAI_MODEL", "gpt-4.1-mini")

# ==================================
# ANIMATED DESIGN
# ==================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg, #080d1b, #111c35, #101020
    );
    color: white;
}

h1 {
    color: #70a5ff;
    text-align: center;
    font-size: 48px !important;
    font-weight: 900;
}

.subtitle {
    text-align: center;
    color: #aabbd8;
    font-size: 16px;
}

div.stButton > button {
    background: linear-gradient(
        90deg, #2563eb, #9333ea
    );
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-weight: bold;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 18px #397bff;
}

[data-testid="stChatMessage"] {
    border: 1px solid #344466;
    border-radius: 15px;
    padding: 12px;
    background: #15213b;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ==================================
# AI INSTRUCTIONS
# ==================================

SYSTEM_PROMPT = """
You are YARO 1.0, a helpful and intelligent AI assistant.

YOUR RESPONSIBILITIES:

1. Give accurate, clear and useful answers.
2. Explain difficult concepts from basic to advanced.
3. Solve mathematics and science problems step by step.
4. Help students understand concepts rather than
   simply memorizing answers.
5. For current facts, use web search.
6. Prefer official government websites, universities,
   scientific publications and other reputable sources.
7. Cross-check important claims when possible.
8. Never invent sources, statistics or quotations.
9. Provide source links when available.
10. Clearly distinguish verified facts from estimates.
11. If uncertain, admit that you are uncertain.
12. Never claim that you are 100% accurate.
13. Answer in the language requested by the user.
14. Use headings and examples when helpful.

IMPORTANT DISCLAIMER:
YARO is an AI assistant. It can make mistakes.
Verify important information independently.
"""

# ==================================
# HEADER
# ==================================

st.markdown("<h1>🤖 YARO 1.0</h1>",
            unsafe_allow_html=True)

st.markdown(
    '<p class="subtitle">'
    'YOUR AI • YOUR KNOWLEDGE • YOUR FUTURE'
    '</p>',
    unsafe_allow_html=True
)

st.divider()

# ==================================
# SIDEBAR
# ==================================

with st.sidebar:

    st.title("⚙️ YARO SETTINGS")

    st.write("Version: 1.0")
    st.write("AI Status: Ready")

    if st.button("🗑️ New Conversation"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("Features")

    st.write("🌐 Live Web Research")
    st.write("📚 Study Assistant")
    st.write("🧮 Mathematics")
    st.write("🔬 Science")
    st.write("💡 General Knowledge")

    st.divider()

    st.caption(
        "YARO is an AI and can make mistakes."
    )

# ==================================
# CHAT MEMORY
# ==================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ==================================
# WELCOME SCREEN
# ==================================

if not st.session_state.messages:

    st.markdown("### Welcome to YARO!")

    st.write(
        "I can help you research, learn, "
        "understand and solve problems."
    )

    st.info(
        "Ask any question below to begin."
    )

# ==================================
# USER INPUT
# ==================================

user_input = st.chat_input(
    "Ask YARO anything..."
)

# ==================================
# AI RESPONSE
# ==================================

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        if not API_KEY:

            st.error(
                "API key missing. Configure "
                "OPENAI_API_KEY before starting YARO."
            )

        else:

            try:

                client = OpenAI(api_key=API_KEY)

                with st.spinner(
                    "YARO is thinking and researching..."
                ):

                    # Keep recent conversation context
                    history = st.session_state.messages[-12:]

                    response = client.responses.create(

                        model=MODEL,

                        instructions=SYSTEM_PROMPT,

                        tools=[
                            {"type": "web_search"}
                        ],

                        input=history

                    )

                    answer = response.output_text

                    if not answer:
                        answer = (
                            "I could not generate an answer. "
                            "Please try again."
                        )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

        except Exception as error:

    st.error(
        f"YARO ERROR: {type(error).__name__}: {error}"
    )

    print("YARO ERROR:", repr(error))

# ==================================
# FOOTER
# ==================================

st.divider()

st.markdown(
    "<center>© 2026 YARO 1.0 | "
    "Powered by Artificial Intelligence</center>",
    unsafe_allow_html=True
)

st.caption(
    "Disclaimer: YARO is an AI assistant. "
    "It can make mistakes. Always verify "
    "important information using trusted sources."
)
