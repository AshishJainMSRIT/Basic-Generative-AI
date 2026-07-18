import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import streamlit as st
from dotenv import load_dotenv
from operator import itemgetter

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

load_dotenv()

# ------------------------------
# Configuration
# ------------------------------

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
TOP_K = 5

PERSIST_DIRECTORY = "./chroma_db"

# ------------------------------
# Prompt
# ------------------------------

SYSTEM_PROMPT = """
You are an assistant for question-answering tasks.

Answer ONLY from the provided context.

If the answer is not available in the context,
reply with:

"I couldn't find that information in the provided documents."

Keep the answer concise (maximum 3 sentences).

Context:
{context}
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}")
    ]
)

# ------------------------------
# Helper Functions
# ------------------------------

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


@st.cache_resource
def create_vectorstore():

    embeddings =  GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview"
    )

    # Load existing vector DB if already persisted
    if os.path.exists(PERSIST_DIRECTORY):

        return Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=embeddings
        )

    # Otherwise create it

    docs = []
    loader = PyPDFLoader("yolov9_paper.pdf")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    splits = splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
    )

    return vectorstore


@st.cache_resource
def build_chain():

    vectorstore = create_vectorstore()

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0.4
    )

    chain = (
        {
            "context":
                itemgetter("input")
                | retriever
                | RunnableLambda(format_docs),

            "input":
                itemgetter("input"),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever


# ------------------------------
# Streamlit UI
# ------------------------------

st.set_page_config(page_title="RAG Demo")

st.title("📚 LangChain RAG Demo")

query = st.chat_input("Ask a question about the YOLOv9 paper...")

if query:

    rag_chain, retriever = build_chain()

    with st.spinner("Searching documents..."):

        answer = rag_chain.invoke(
            {
                "input": query
            }
        )

    st.subheader("Answer")

    st.write(answer)

    # --------------------------
    # Debug Section
    # --------------------------

    with st.expander("Retrieved Documents"):

        docs = retriever.invoke(query)

        for i, doc in enumerate(docs, start=1):

            st.markdown(f"### Chunk {i}")

            st.write(doc.page_content)

            st.caption(doc.metadata)


# Run this app using the command: streamlit run pdfChatBotUsingRAG.py
