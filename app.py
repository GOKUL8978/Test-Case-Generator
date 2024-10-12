import streamlit as st
import os
import requests
from groq import Groq
import json

if 'response' not in st.session_state:
    st.session_state['response'] = ""
if 'json_input' not in st.session_state:
    st.session_state['json_input'] = ""

def generate_groq_test_cases(json_input,http_method,api_url):
    try:
        # This is a mock structure, adjust the client setup and call as per the real Groq API SDK
        client = Groq(
            api_key=os.os.environ.get('GROQ_API_KEY')
)
        
        # Send the JSON input to Groq to generate JavaScript test cases
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Generate JavaScript test cases that is compatible for postman for the following JSON data: {json_input} for api url {api_url} and http method : {http_method}""Output **only** the code without any explanation or comments.",
                }
            ],
            model="llama3-groq-70b-8192-tool-use-preview",  # Example model, adjust as necessary
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        
        # Extract and return the generated content
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        return f"Error generating test cases: {e}"


# Streamlit app title
st.title("API Request Tester")

# Input for API URL
api_url = st.text_input("Enter the API URL")

# Dropdown for selecting HTTP method
http_method = st.selectbox("Select HTTP Method", ["GET", "POST", "PUT", "DELETE"])

# Input for request body (for POST and PUT requests)
request_body = st.text_area("Enter the request body (for POST/PUT)", "", height=150)

# Send button
if st.button("Send"):
    try:
        # Perform the selected HTTP request
        if http_method == "GET":
            response = requests.get(api_url)
        elif http_method == "POST":
            response = requests.post(api_url, data=request_body)
        elif http_method == "PUT":
            response = requests.put(api_url, data=request_body)
        elif http_method == "DELETE":
            response = requests.delete(api_url)

        # Display the response in a text box
        json_input=st.text_area("Response", response.text, height=200)
        st.session_state['response'] = response.text
        st.session_state['json_input'] = response.text  # You can use this for further processing

        # Display the response in a text box
        st.text_area("Response", st.session_state['response'], height=200)

    except Exception as e:
        st.error(f"Error: {str(e)}")


json_input = st.session_state['json_input']
st.text_area("Response (for Test Case Generation)", json_input, height=200)

if st.button("Generate Test Cases"):
        with st.spinner("Generating test cases..."):
            test_cases = generate_groq_test_cases(json_input,http_method,api_url)
            st.success("Test cases generated successfully!")
            st.text_area("Generated JavaScript Test Cases", test_cases, height=300)

