import os
import pandas as pd
import numpy as np
import streamlit as st
import faiss
import pickle
from sentence_transformers import SentenceTransformer

try:
    from openai import OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "sk-abc1234567890yourrealapikey"  
    USE_OPENAI = "sk-" in OPENAI_API_KEY
    if USE_OPENAI:
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        client = OpenAI()
except:
    USE_OPENAI = False
    client = None

DATASET_PATH = "Training Dataset.csv"
VECTOR_FILE = "vector_index.pkl"
MODEL_NAME = "all-MiniLM-L6-v2"

embedder = SentenceTransformer(MODEL_NAME)

@st.cache_data
def load_data():
    df = pd.read_csv(DATASET_PATH)
    df.fillna("Unknown", inplace=True)
    docs = []
    for _, row in df.iterrows():
        doc = " ".join([f"{col}: {row[col]}" for col in df.columns])
        docs.append(doc)
    return docs

def build_faiss_index(docs):
    embeddings = embedder.encode(docs, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    with open(VECTOR_FILE, "wb") as f:
        pickle.dump((index, docs), f)

def load_faiss_index():
    with open(VECTOR_FILE, "rb") as f:
        return pickle.load(f)

def retrieve_top_k(query, index, docs, k=3):
    query_vec = embedder.encode([query])
    D, I = index.search(np.array(query_vec), k)
    return [docs[i] for i in I[0]]

def generate_answer(prompt):
    if USE_OPENAI and client:
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful loan analysis assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"[ERROR: {e}]"
    else:
        return "OpenAI API key not found or invalid. Please set your key to get real AI responses."

st.set_page_config(page_title="📄 Loan Approval RAG Chatbot", layout="wide")
st.title("🤖 Loan Approval RAG Chatbot")

query = st.text_input("Ask a question about the loan dataset:")


if query:

    if not os.path.exists(VECTOR_FILE):
        with st.spinner("Building vector index..."):
            documents = load_data()
            build_faiss_index(documents)

    index, documents = load_faiss_index()
    retrieved = retrieve_top_k(query, index, documents)
    context = "\n".join(retrieved)

    final_prompt = f"""Use the following loan application data to answer the question:\n\n{context}\n\nQuestion: {query}"""
    answer = generate_answer(final_prompt)

    st.markdown("### 🔍 Retrieved Data Context")
    st.code(context)
    st.markdown("### 🤖 Answer")
    st.success(answer)
