import os

import requests
import streamlit as st

# Ensure your API URL and key are securely stored
API_URL = "https://api.x.ai/v1/chat/completions"  # The actual endpoint
API_KEY = os.environ.get(
    "XAI_API_KEY"
)  # Ensure your XAI API key is set in your environment


# Function to send a message to the backend and return the response
def send_message(message):
    # Prepare the payload with the user message, following the cURL example from docs
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "Be a chill, observant chatbot inspired by Oreki Houtarou from 'Hyouka.' Respond with insightful yet laid-back answers, using modern English and Gen Z slang. Encourage users to think outside the box while reminding them to keep it simple and relaxed.",
            },
            {"role": "user", "content": message},
        ],
        "model": "grok-beta",  # The model you're using (could change depending on the API docs)
        "stream": False,  # Set to False as per the docs (no streaming)
        "temperature": 0,  # Set temperature (0 for deterministic responses)
    }

    # Headers as per cURL request
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    try:
        # Send the POST request to the x.ai API
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Check if request was successful (status code 200)

        # Parse the response
        data = response.json()

        # Extract the assistant's response from the API
        if "choices" in data and len(data["choices"]) > 0:
            return {"response": data["choices"][0]["message"]["content"]}
        else:
            return {"error": "No response from the assistant."}
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {str(e)}"}


# Streamlit app UI setup
st.title("Groovy Chatbot")

# Initialize session state for storing messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input and response handling
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send the message to the backend and get the response
    response = send_message(prompt)

    # Display the response from the assistant (if available)
    if "error" in response:
        st.error(f"Error: {response['error']}")
    else:
        assistant_response = response.get("response", "")
        if assistant_response:
            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_response}
            )
            with st.chat_message("assistant"):
                st.markdown(assistant_response)
        else:
            st.error("Received an empty response from the assistant.")
