import psycopg2
import chromadb
from chromadb.utils import embedding_functions

# --- 1. Setup PostgreSQL Data ---
def seed_postgres():
    print("Seeding PostgreSQL...")
    conn = psycopg2.connect(
        host="localhost",
        database="support_db",
        user="user",
        password="password",
        port="5432"
    )
    cur = conn.cursor()

    # Create Tables
    cur.execute("DROP TABLE IF EXISTS tickets;")
    cur.execute("DROP TABLE IF EXISTS customers;")
    
    # Corrected Table Creation: Added 'email' column
    cur.execute("""
        CREATE TABLE customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            city VARCHAR(50)
        );
    """)
    cur.execute("""
        CREATE TABLE tickets (
            id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(id),
            issue TEXT,
            status VARCHAR(20)
        );
    """)

    # Corrected Insert Statements: Added email data
    cur.execute("""
        INSERT INTO customers (name, email, city) VALUES 
        ('Alice Smith', 'alice.smith@example.com', 'New York'), 
        ('Bob Jones', 'bob.jones@example.com', 'London');
    """)
    cur.execute("""
        INSERT INTO tickets (customer_id, issue, status) VALUES 
        (1, 'Login error on mobile', 'Open'), 
        (2, 'Payment failed', 'Closed');
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("PostgreSQL seeded successfully!")

# --- 2. Setup ChromaDB Data ---
def seed_chroma():
    print("Seeding ChromaDB...")
    client = chromadb.HttpClient(host='localhost', port=8000)
    
    # Use a simple default embedding function (no API key needed for this part)
    emb_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(name="support_articles", embedding_function=emb_fn)

    articles = [
        "Refund Policy: You can return any item within 30 days of purchase with a valid receipt.",
        "Password Reset: To reset your password, click the 'Forgot Password' link on the login page and follow the email instructions.",
        "Shipping Info: Standard shipping takes 3-5 business days. Express shipping takes 1-2 business days."
    ]
    ids = ["art1", "art2", "art3"]

    collection.add(documents=articles, ids=ids)
    print("ChromaDB seeded successfully!")

if __name__ == "__main__":
    seed_postgres()
    seed_chroma()