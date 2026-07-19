import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv

load_dotenv()

async def main():
    model = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0.4
    )

    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",  # Local subprocess communication
                "command": "python",
                "args": ["C:\\Users\\Adinath Ji\\Documents\\genAIApp\\CustomMCPUsingLangGraph\\custom_mcp_server.py"],
            },
        }
    )

    tools = await client.get_tools()
    model_with_tools = model.bind_tools(tools)

    tool_node = ToolNode(tools)

    def should_continue(state: MessagesState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    async def call_model(state: MessagesState):
        response = await model_with_tools.ainvoke(state["messages"])
        return {"messages": [response]}

    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "call_model")
    # builder.add_edge("call_model", "tools", condition=should_continue)
    builder.add_conditional_edges("call_model", should_continue)
    builder.add_edge("tools", "call_model")

    graph = builder.compile()

    result  = await graph.ainvoke({"messages":  "What is the sum of 5 and 7?" })
    print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
