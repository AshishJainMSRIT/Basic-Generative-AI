from time import time, sleep

import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Now we can instantiate our model object and generate chat completions:
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0, # this controls the randomness of the output, 0 means deterministic output
    max_tokens=None, # this controls the maximum number of tokens in the output, None means no limit
    timeout=None, # this controls the maximum time to wait for a response, None means no limit
    max_retries=2,
)

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a chatbot"),
        ("human","Question:{question}")
    ]
)



st.title('Langchain Demo With Gemini')
input_text=st.text_input("Enter your question here")


output_parser=StrOutputParser()

chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))



# To run this code, run cmd-  streamlit run gemini_chat_bot.py
