import streamlit as st
import ollama
from ollama._types import ResponseError
import base64

st.set_page_config(page_title="Mental support chatbot")

def get_base64(background):
    try:
        with open(background, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""  # Return empty string if file not found

bin_str = get_base64("HEALTH/background.jpg")

st.markdown(f"""
        <style>
            .main {{
                  background-image: url("data:image/jpeg;base64,{bin_str}");
                  background-size: cover;
                  background-position: center;
                  background-repeat: no-repeat;
            }}
        </style>
""", unsafe_allow_html=True)

st.session_state.setdefault('conversation_history', [])

def generate_response(user_input):
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})
    try:
        response = ollama.chat(
            model="tinyllama:latest",
            messages=st.session_state['conversation_history']
        )
        ai_response = response['message']['content']
    except ResponseError as e:
        ai_response = "Sorry, I couldn't process your request at the moment."
        st.error(f"Ollama API error: {e}")
    except Exception as e:
        ai_response = "An unexpected error occurred."
        st.error(f"Unexpected error: {e}")

    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})
    return ai_response

def generative_affirmation():
    prompt = "Generate a positive affirmation to encourage someone who is stressed or overwhelmed."
    try:
        response = ollama.chat(
            model="tinyllama:latest",  
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
    except Exception:
        return "Sorry, I couldn't generate an affirmation right now."

def generate_meditation_guide():
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce anxiety."
    try:
        response = ollama.chat(
            model="tinyllama:latest",  
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
    except Exception:
        return "Sorry, I couldn't generate a meditation guide right now."

st.title("Mental Health Support Chatbot")

# Display conversation history
for message in st.session_state['conversation_history']:
    role = "You" if message['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {message['content']}")

user_message = st.text_input("How can I help you today?")
if user_message:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

col1, col2 = st.columns(2)  
with col1:
    if st.button("Generate Affirmation"):
        affirmation = generative_affirmation()
        st.markdown(f"**Affirmation:** {affirmation}")     

with col2:
    if st.button("Meditation Guide"):
        meditation_guide = generate_meditation_guide()
        st.markdown(f"**Meditation:** {meditation_guide}")
