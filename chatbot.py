import streamlit as st
import time
from google import genai # Correct import

# Configure the page
st.set_page_config(
    page_title="Gemini Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set up Gemini API key
API_KEY = ""
client=genai.Client(api_key=API_KEY)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Custom CSS
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #1f77b4;
    margin-bottom: 2rem;
}
.chat-container {
    max-height: 600px;
    overflow-y: auto;
}
.stButton > button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>🤖 Chat Bot</h1>", unsafe_allow_html=True)
st.markdown("---")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_prompt := st.chat_input("💭 Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                response = client.models.generate_content(model="gemini-2.0-flash", contents=user_prompt)
                gemini_reply = response.text
            except Exception as e:
                gemini_reply = f"❌ Error: {e}"

        # Simulate streaming
        placeholder = st.empty()
        full_response = ""
        for word in gemini_reply.split():
            full_response += word + " "
            placeholder.markdown(full_response + "▌")
            time.sleep(0.03)
        placeholder.markdown(full_response)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": gemini_reply})

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em; padding: 1rem;'>
        🚀 Built by Soham Chavan
    </div>
    """,
    unsafe_allow_html=True
)
