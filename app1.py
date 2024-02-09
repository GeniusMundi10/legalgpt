
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from retrying import retry

load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


st.set_page_config(page_title="Prototype Chatbot")
st.header("Indian Penal Code GPT")

@retry(stop_max_attempt_number=3,wait_fixed=1000)
def get_gemini_response(question):
	model=genai.GenerativeModel("gemini-pro")
	chat=model.start_chat(history=[])
	response = chat.send_message(question,stream=True)
	return {
		"chunks": [response] if isinstance(response, str) else [chunk.text for chunk in response]
	}


if 'chat_history' not in st.session_state:
	st.session_state['chat_history']=[]

input_question = st.text_input("Input: ",key="input")
submit_button = st.button("Ask the question")

if submit_button and input_question:
	response = get_gemini_response(input_question)
	st.session_state['chat_history'].append(("You: ",input_question))
	bot_response=' '.join(response["chunks"])

	st.subheader("The Response is")
	
	st.markdown(bot_response,unsafe_allow_html=True)
	st.session_state['chat_history'].append(("IPC-GPT: ",bot_response))

st.subheader("The Chat History is")

chat_history_text = ""
for role,text in st.session_state['chat_history']:
	chat_history_text += f"{role}: {text}\n"
st.text_area("Chat History", value=chat_history_text,height=400)
