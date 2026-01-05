import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Support Dashboard", layout="wide")
st.title("🤖 Intelligent Support Desk")

# --- Sidebar Dashboard ---
st.sidebar.title("🛠️ Agent Inner Monologue")
debug_container = st.sidebar.container()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "debug_logs" not in st.session_state:
    st.session_state.debug_logs = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Connect to FastAPI backend
            with requests.post("http://localhost:8080/chat", 
                               json={"message": prompt}, 
                               stream=True) as r:
                for line in r.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith("data: "):
                            data = json.loads(decoded_line[6:])
                            node = data.get("node")
                            content = data.get("content")
                            
                            # Log tool calls to the Sidebar Dashboard
                            if node == "tools":
                                st.session_state.debug_logs.append(f"🔍 Tool Used: {content}")
                                with debug_container:
                                    st.info(f"Tool: {content}")
                            
                            # Update the final response if it's from the agent node
                            if node == "agent" and content != "Processing...":
                                full_response = content
                                response_placeholder.markdown(full_response)
                                
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Connection Error: {e}")