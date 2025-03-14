import streamlit as st
import uuid
from agent import perform_analysis

# Set page configuration
st.set_page_config(page_title="Legal AI Assistant", layout="wide")

# Title and header
st.title("⚖️ Lexi: Legal AI Assistant")

# Initialize session state variables if they don't exist
if "sessions" not in st.session_state:
    st.session_state.sessions = {}  # Maps session names to session IDs
if "current_session" not in st.session_state:
    st.session_state.current_session = None  # Holds the active session ID
if "session_data" not in st.session_state:
    st.session_state.session_data = {}  # Stores conversation history for each session

# Sidebar: Session management
st.sidebar.header("Chat Sessions")

# Form to create a new session (chat instance)
with st.sidebar.form(key="new_session_form"):
    new_session_name = st.text_input("New session name:", "")
    submit_new_session = st.form_submit_button("New Chat")
    if submit_new_session and new_session_name:
        new_session_id = str(uuid.uuid4())
        st.session_state.sessions[new_session_name] = new_session_id
        st.session_state.session_data[new_session_id] = []  # Initialize conversation history for new session
        st.session_state.current_session = new_session_id
        # Instead of st.experimental_rerun(), we rely on session state update

# List existing sessions as buttons to switch between them
for session_name, session_id in st.session_state.sessions.items():
    if st.sidebar.button(session_name):
        st.session_state.current_session = session_id

# If no session is active, initialize a default session
if st.session_state.current_session is None:
    default_session_id = str(uuid.uuid4())
    st.session_state.current_session = default_session_id
    st.session_state.sessions["Chat 1"] = default_session_id
    st.session_state.session_data[default_session_id] = []

# Display the chat history for the active session
chat_history = st.session_state.session_data.get(st.session_state.current_session, [])
if chat_history:
    st.write("### Chat History")
    for message in chat_history:
        st.markdown(message)

# Main chat input area
user_input = st.text_area("Enter your legal query or http link for analysis", height=200)

if st.button("Submit", key="submit_button"):
    if user_input:
        with st.spinner("Analyzing..."):
            response = perform_analysis(st.session_state.current_session, user_input)
            st.markdown("### Response:")
            if response and "response" in response:
                main_content = response["response"]
                st.markdown(main_content)
                # Save the conversation to session history (with formatting to differentiate speakers)
                st.session_state.session_data[st.session_state.current_session].append(f"**User:** {user_input}")
                st.session_state.session_data[st.session_state.current_session].append(f"**Lexi:** {main_content}")
            else:
                st.error("No valid response received.")
    else:
        st.warning("Please enter a legal query")

st.markdown("---")
st.markdown("Made with ❤️ by Nielay Shintre")
