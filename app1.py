import streamlit as st
import pandas as pd
from langchain_ollama import ChatOllama
from langchain_experimental.agents import create_pandas_dataframe_agent


st.title("AI Powered Knowledge Engine for Smart Support and Ticket_Resolution")

uploaded_file=st.file_uploader("Upload knowledge base CSV",type=["csv"])
if uploaded_file:
    kb=pd.read_csv(uploaded_file)
    st.success("Knowledge base loaded successfully")
    st.write("File_name:",uploaded_file.name)
    st.write("FileType:",uploaded_file.type)
    st.write("Filesize:",uploaded_file.size)
    
else:
    st.info("No file uploaded using default sample knowledge base")
    kb=pd.read_csv("knowledge_base_sample.csv")



llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0
    )

agent = create_pandas_dataframe_agent(
    llm,
    kb,
    verbose=True,
    agent_executor_kwargs={"handle_parsing_errors": True},
    allow_dangerous_code=True
)

question = st.text_input(
    "Ask a question about the knowledge base:",
    # value="What are the top 2 articles related to password reset issues?"
)
if st.button("Ask"):
    with st.spinner("Thinking... "):
        response = agent.invoke({"input": question})

    st.subheader("Answer")
    st.write(response)
    
    