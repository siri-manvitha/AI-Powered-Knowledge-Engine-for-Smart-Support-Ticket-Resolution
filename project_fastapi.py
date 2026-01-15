from fastapi import FastAPI, UploadFile, File, Form
import pandas as pd
from langchain_ollama import ChatOllama
from langchain_experimental.agents import create_pandas_dataframe_agent
import tempfile

app = FastAPI(
    title="AI Powered Knowledge Engine for Smart Support and Ticket Resolution"
)

# Initialize LLM once
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

@app.post("/ask")
async def ask_question(
    question: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Upload a CSV knowledge base and ask a question about it.
    """

    # Save uploaded CSV temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(await file.read())
        csv_path = tmp.name

    # Load CSV
    kb = pd.read_csv(csv_path)

    # Create agent
    agent = create_pandas_dataframe_agent(
        llm,
        kb,
        verbose=False,
        agent_executor_kwargs={"handle_parsing_errors": True},
        allow_dangerous_code=True
    )

    # Invoke agent
    response = agent.invoke({"input": question})

    return {
        # "question": question,
        "answer": response
    }
