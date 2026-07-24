from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
# from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

# below is used for langgraph workflow
import operator
from typing_extensions import TypedDict, Annotated

from langchain_groq import ChatGroq


load_dotenv()

# model = ChatGoogleGenerativeAI(
#         model="gemini-3.1-flash-lite",
#         temperature=0.4
#     )

# LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature= 0
)

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    SystemMessage,
    AIMessage
)

class MessageState(TypedDict) :
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

def chatbotNode(state: MessageState):
    print("Agent is responding...")
    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a helpful AI assistant. "
                    "Use conversation memory properly " \
                    "and answer based on previous messages."
                )
            )
        ]
        + state["messages"]
    )

    # return only updates
    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

builder = StateGraph(MessageState)

builder.add_node("chatbot", chatbotNode)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)


#short term memory
# memory = InMemorySaver()

# long term memory
DATABASE_URL="postgresql://postgres:AdinathJi%4019@localhost:5432/postgres"


with PostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
    checkpointer.setup()

    app = builder.compile(checkpointer=checkpointer)

    config = {
        "configurable" : {
            "thread_id": "user_1"
        }
    }
    result = app.invoke(
        {
            "messages": [
                HumanMessage("what is my name?"   )
            ],
            "llm_calls": 0
        },
        config=config
    )

    print("AI response")
    print(result["messages"][-1].content)

    # result = app.invoke(
    #     {
    #         "messages": [
    #             HumanMessage("What is my name?")
    #         ],
    #         "llm_calls": 0
    #     },
    #     config=config
    # )

    # print("AI response")
    # print(result["messages"][-1].content)
