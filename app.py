import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Generative Model
# Consider using a more powerful model like "gemini-pro" for better conversational capabilities
model = genai.GenerativeModel("gemini-1.5-flash") 

# Set Streamlit page configuration
st.set_page_config(page_title=" AquaSathi-Clean Water & Sanitation Chatbott", page_icon="💧")
st.title("💧  AquaSathi-Clean Water & Sanitation Chatbots")
st.markdown("Ask me anything about hygiene, clean water, or sanitation tips!")

# --- Initialize chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle user input ---
user_input = st.chat_input("Type your question about water & sanitation...")
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message in chat bubble
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Define the prompt for the AI
                prompt = f"You are an expert health and water sanitation assistant. Provide simple and friendly answers.\n\nUser: {user_input}"
                
                # Generate content from the model
                response = model.generate_content(prompt)
                bot_reply = response.text
            except Exception as e:
                # Catch potential errors, e.g., API key issues, network problems
                bot_reply = f"❌ Error: Could not get a response. Please check your API key or internet connection. Details: {e}"
            
            # Display assistant's reply
            st.markdown(bot_reply)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
