# Custom MCP Using LangGraph

A small example showing how to run a custom MCP server alongside a LangGraph-based client.

## Features

- Example custom MCP server (local development)
- Client integration using LangGraph to call the MCP tool

## Prerequisites

- Python 3.11+ and `pip`
- (Recommended) a virtual environment

## Setup

1. Install the MCP helper package:

```bash
pip install fastmcp
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/Scripts/activate    # Windows: .venv\Scripts\activate
```

## Running

Open two terminals:

- In the first terminal, start the custom MCP server. This depends on how your server is implemented; for example you might run:

```bash
# example: run the server module or script for your custom MCP
python CustomMCPUsingLangGraph/custom_mcp_server.py
```

- In the second terminal, run the LangGraph client that connects to the MCP server:

```bash
python CustomMCPUsingLangGraph/mcp_client_langgraph.py
```

Adjust the commands above if your server entry point or filenames differ. If the server is provided as a console script by `fastmcp`, follow that package's instructions instead.

## Troubleshooting

- If the client cannot connect, ensure the server is running and check the host/port or transport settings used by the client.
- If you see import errors, confirm the virtual environment is activated and dependencies are installed.
