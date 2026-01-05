# 🤖 AI Support Agent: Multi-Agent Customer Support System

A sophisticated **AI Support Agent** built with a multi-agent architecture to streamline customer service. This system intelligently orchestrates logic between structured customer data and unstructured knowledge bases using **LangGraph**, **FastAPI**, and **Streamlit**.

---

## 🏗️ System Architecture

The diagram below illustrates the flow of a user query through the various layers of the application, from the frontend interface to the reasoning engine and final data retrieval.

<p align="center">
  <img src="https://github.com/user-attachments/assets/03154372-75f3-46fb-8885-9667900e8b1a" alt="System Architecture Diagram" width="800">
</p>

### Architecture Breakdown:
* **Client Layer**: A responsive **Streamlit** UI for a seamless user chat experience.
* **Server Layer**: **FastAPI** gateway that manages API endpoints and request routing.
* **Orchestration Layer**: **LangGraph** framework that manages agent state and decision-making logic.
* **Reasoning Engine**: **Groq (Llama 3)** providing lightning-fast LLM inference.
* **Data Layer**: 
    * **PostgreSQL**: Stores structured customer profiles (e.g., Alice Smith).
    * **ChromaDB**: Vector Store containing the unstructured Knowledge Base/Docs.

---

## 🚀 Key Features

* **Smart Query Routing**: The agent uses LLMs to determine if a query requires a **SQL lookup** (for personal data) or a **Vector search** (for general support docs).
* **Agentic State Management**: Built with **LangGraph** to handle complex, multi-step reasoning loops.
* **High-Speed Inference**: Leveraging **Groq** for near-instant response times.
* **Scalable Design**: Backend and Frontend are decoupled, making it ready for cloud deployment.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/Saadullah45/AI-Support-Agent.git](https://github.com/Saadullah45/AI-Support-Agent.git)
cd AI-Support-Agent

```


### 2. Set Up Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

```

### 3. Configure Environment Variables
Create a .env file in the root directory:
```bash
GROQ_API_KEY=your_groq_api_key_here
# Replace with your local or cloud DB URL
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### 4. Initialize the Databases
Seed the initial customer data and knowledge base:
```bash
python seed_data.py
```


## Running the Application
You will need two terminal windows open to run the full stack.
### Terminal 1: Start the Backend (FastAPI)
```bash
python main.py
```

### Terminal 2: Start the Frontend (Streamlit)
```bash
streamlit run UI.py
```


## 🌐 Deployment

### ☁️ Streamlit Community Cloud (Frontend)
1. **Push your code**: Ensure your latest changes are committed and pushed to your GitHub repository.
2. **Connect to Streamlit**: Log into [share.streamlit.io](https://share.streamlit.io/) and select your repository.
3. **Configure Secrets**: 
   - Go to **Settings > Secrets**.
   - Add your credentials in TOML format:
     ```toml
     GROQ_API_KEY = "your_groq_key_here"
     API_URL = "[https://your-backend-service.onrender.com](https://your-backend-service.onrender.com)"
     ```

### 🚀 Render / Railway (Backend)
1. **Create Web Service**: Connect your GitHub repo to Render or Railway.
2. **Environment Variables**: Add the following in the dashboard:
   - `GROQ_API_KEY`: Your Groq API key.
   - `DATABASE_URL`: Your connection string (e.g., from Supabase or Neon).
3. **Deployment Settings**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## 📄 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
