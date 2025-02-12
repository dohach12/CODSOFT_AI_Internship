import streamlit as st
import re

def get_chatbot_response(user_input: str) -> str:
    """
    Generate a chatbot response based on the user input using rule-based matching.
    
    Args:
        user_input (str): The input text from the user.
    
    Returns:
        str: The chatbot's response.
    """
    # List of (pattern, response) tuples for rule-based matching.
    rules = [
        (r'\b(hi|hello|hey)\b', "Hello! How can I help you today?"),
        (r"your name", "I'm MayaBot, your virtual assistant!"),
        (r"help", "Sure! Let me know what you need help with."),
        (r"weather", "I can't check live weather, but you can visit a weather website like weather.com!"),
        (r"python", "Python is a powerful programming language used in web development, AI, and more!"),
        (r"streamlit", "Streamlit is a Python framework for building interactive web applications easily."),
    ]
    
    # Iterate over rules to find a matching pattern.
    for pattern, response in rules:
        if re.search(pattern, user_input, re.IGNORECASE):
            return response
    return "I'm not sure about that. Can you rephrase?"

def display_chat_history(chat_history):
    """
    Display the chat history with styled chat bubbles.
    
    Args:
        chat_history (list of tuple): List containing tuples with speaker and message.
    """
    for speaker, message in chat_history:
        if speaker == "You":
            # Right-align user messages.
            st.markdown(
                f"<div style='text-align: right; background-color: #DCF8C6; padding: 8px; border-radius: 8px; margin-bottom: 5px; max-width: 80%; margin-left: auto;'>{message}</div>",
                unsafe_allow_html=True
            )
        else:
            # Left-align chatbot messages.
            st.markdown(
                f"<div style='text-align: left; background-color: #F1F0F0; padding: 8px; border-radius: 8px; margin-bottom: 5px; max-width: 80%;'>{message}</div>",
                unsafe_allow_html=True
            )

# Initialize chat history in session state if it doesn't exist.
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.title("🤖 Rule-Based Chatbot with Streamlit")
st.write("Ask me anything! Type 'exit' to stop.")

# Sidebar for additional controls.
st.sidebar.header("Options")
if st.sidebar.button("Clear Chat History"):
    st.session_state["chat_history"] = []
    # Check if experimental_rerun is available.
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# Create a form for user input to provide a clear submission flow.
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("You: ")
    submit_button = st.form_submit_button(label="Send")

# Process the user input when the form is submitted.
if submit_button and user_input:
    if user_input.lower() == "exit":
        st.stop()  # Stop the app if the user types 'exit'.
    
    # Generate the chatbot response using the rule-based function.
    response = get_chatbot_response(user_input)
    
    # Append the user input and chatbot response to the chat history.
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Chatbot", response))

# Display the chat history with styled chat bubbles.
display_chat_history(st.session_state.chat_history)
