# Gemini Chat Bot Setup

## Create and activate the Python environment

```powershell
python -m venv myenv
.\myenv\Scripts\activate
```

## Install dependencies

```powershell
python -m pip install --upgrade pip
pip install --upgrade --quiet langchain-google-genai pillow
pip install streamlit
pip install python-dotenv
```

## Verify installation

```powershell
pip show langchain-google-genai
```

## Run the app

```powershell
streamlit run gemini_chat_bot.py
```
