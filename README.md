# 🤖 AI Support Agent

A multi-agent customer support system built with **LangGraph**, **FastAPI**, and **Streamlit**. This agent intelligently routes queries between a **PostgreSQL** customer database and a **ChromaDB** vector store.

## 🚀 Features
- **Smart Routing**: Uses LLMs to decide between structured SQL data and unstructured knowledge base lookups.
- **Dual-Database Support**: Integrated with PostgreSQL and ChromaDB.
- **Modern UI**: A clean, interactive chat interface built with Streamlit.
- **FastAPI Backend**: Robust API layer for handling agent logic.

## 🛠️ Setup
1. **Clone the repo**: `git clone <your-repo-link>`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure Environment**: Create a `.env` file with your `GROQ_API_KEY`.
4. **Run the App**: 
   - Backend: `python main.py`
   - Frontend: `streamlit run UI.py`
