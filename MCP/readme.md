# MCP Example

This folder demonstrates a LangGraph application using two MCP tools:

- `calculator` via the Python `mcp-server-calculator` package
- `weather` via the `mcp-openweather` MCP server

## Prerequisites

- Python 3.11+ installed
- `pip` available on your PATH
- `git` installed to clone the weather MCP repo
- Go installed to build the weather MCP server binary
- OpenWeatherMap API key

## Setup

### 1. Install the calculator MCP server

```bash
pip install -U mcp-server-calculator
```

### 2. Build the weather MCP server

```bash
git clone https://github.com/mschneider82/mcp-openweather.git
cd mcp-openweather
go build -o mcp-weather.exe
```

If you already have `MCP/mcp-openweather/mcp-weather.exe`, you can skip moving it. Otherwise place the generated binary in `MCP/mcp-openweather` or update the path in `app.py`.

### 3. Configure environment variables

Create or update `.env` in the `MCP` folder with your keys:

```dotenv
OWM_API_KEY=your_openweathermap_api_key
GOOGLE_API_KEY=your_google_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
OPENAI_API_KEY=your_openai_api_key
```

> Only `OWM_API_KEY` is required to run the weather tool. The other keys are used by the application model configuration.

## Run the app

From the `MCP` folder:

```bash
python app.py
```

Then ask questions such as weather lookups or calculations.

Type `exit` or `quit` to stop the program.

## Notes

- `app.py` uses `MultiServerMCPClient` to launch both tools.
- If you change the location of `mcp-weather.exe`, update the `command` path in `app.py`.
- The calculator tool starts with:
  
```bash
python -m mcp_server_calculator
```

if it is installed correctly.
