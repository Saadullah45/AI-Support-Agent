import psycopg2
import chromadb
from langchain_core.tools import tool
from chromadb.utils import embedding_functions

# --- TOOL 1: PostgreSQL Search (Customer/Tickets) ---
@tool
def query_customer_info(sql_query: str):
    """
    Query the PostgreSQL database for customer, ticket, or account information.
    The input should be a valid SQL query.
    """
    try:
        # Use 'localhost' because we are running the script from our computer, 
        # but the DB is in Docker.
        conn = psycopg2.connect(
            host="localhost",
            database="support_db",
            user="user",
            password="password",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return str(rows)
    except Exception as e:
        return f"Error executing SQL: {e}"

# --- TOOL 2: ChromaDB Search (Knowledge Base) ---
@tool
def search_knowledge_base(query: str):
    """
    Search the vector database for support articles, FAQs, and company policies.
    """
    try:
        client = chromadb.HttpClient(host='localhost', port=8000)
        # Use the same default embedding function as your seed script
        emb_fn = embedding_functions.DefaultEmbeddingFunction()
        collection = client.get_collection(name="support_articles", embedding_function=emb_fn)
        
        results = collection.query(query_texts=[query], n_results=1)
        return results['documents'][0]
    except Exception as e:
        return f"Error searching vector DB: {e}"

# --- TOOL 3: External Mock API ---
@tool
def get_external_info(topic: str):
    """
    Fetch general information like weather or crypto prices for topics 
    not covered by company databases.
    """
    topic = topic.lower()
    if "weather" in topic:
        return "The weather in Karachi is currently 22°C and sunny."
    elif "crypto" in topic or "bitcoin" in topic:
        return "Bitcoin is currently trading at $95,000."
    else:
        return f"No external information found for {topic}."