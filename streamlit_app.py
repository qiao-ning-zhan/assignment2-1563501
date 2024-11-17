# import streamlit as st
# from utils import read_docx, chunk_document  # Ensure these functions are defined in utils.py
# from vector_database import VectorDatabase   # Ensure this class is defined in vector_database.py
# from openai_interface import OpenAIInterface  # Ensure this class is defined in openai_interface.py

# def main():
#     st.set_page_config(page_title="Protection Visa Eligibility Assistant", page_icon="🛡️", layout="wide")
#     st.title("🛡️ Protection Visa Eligibility Assistant")

#     if 'vector_db' not in st.session_state:
#         st.session_state.vector_db = VectorDatabase()

#     if 'openai_interface' not in st.session_state:
#         st.session_state.openai_interface = OpenAIInterface()

#     if 'eligibility_data' not in st.session_state:
#         st.session_state.eligibility_data = {}

#     # User Input Section
#     st.header("Step 1: Provide Information")
#     st.subheader("Eligibility Questionnaire")

#     # Step 1: Basic Protection Questions
#     question1 = st.radio(
#         "1. Are you a refugee or at risk of significant harm if you return to your home country?",
#         ["Yes", "No"]
#     )
#     question2 = st.radio(
#         "2. Can you legally settle in another country where you will be safe?",
#         ["Yes", "No"]
#     )
#     question3 = st.radio(
#         "3. Do you fear persecution for reasons such as race, religion, nationality, or political opinion?",
#         ["Yes", "No"]
#     )

#     # Step 2: Additional Details
#     st.subheader("Additional Information")
#     persecution_details = st.text_area("Describe the risks you face in your home country.")
#     uploaded_file = st.file_uploader("Upload any supporting documents (optional)", type=["txt", "docx"])

#     # Store data
#     st.session_state.eligibility_data = {
#         "question1": question1,
#         "question2": question2,
#         "question3": question3,
#         "persecution_details": persecution_details,
#     }

#     # Document Processing (if uploaded)
#     if uploaded_file:
#         if uploaded_file.type == "text/plain":
#             document = uploaded_file.getvalue().decode("utf-8")
#         elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#             document = read_docx(uploaded_file)
#         else:
#             st.error("Unsupported file type. Please upload a .txt or .docx file.")
#             return

#         chunks = chunk_document(document)
#         st.session_state.vector_db.add_documents(chunks)
#         st.success(f"✅ {uploaded_file.name} processed and added to vector database!")

#     # Analysis and Output
#     if st.button("Analyze Eligibility"):
#         with st.spinner("Analyzing your eligibility..."):
#             # Combine user input and optional document context
#             context = st.session_state.eligibility_data["persecution_details"]
#             if uploaded_file:
#                 relevant_chunks = st.session_state.vector_db.search(context)
#                 context += "\n" + "\n".join(relevant_chunks)

#             # Generate AI analysis
#             prompt = f"""
# Context: {context}
# Questionnaire Responses:
# 1. Are you a refugee or at risk? {question1}
# 2. Can you legally settle in another country? {question2}
# 3. Do you fear persecution for specific reasons? {question3}

# Based on this information, provide an analysis of the individual's eligibility for a protection visa.
#             """
#             conversation = [
#                 {"role": "system", "content": "You are an AI assistant analyzing eligibility for a protection visa based on the user's input and provided context."},
#                 {"role": "user", "content": prompt}
#             ]
#             response = st.session_state.openai_interface.generate_chat_response(conversation)

#             # Display response
#             st.subheader("Eligibility Analysis Result")
#             st.markdown(response)

# if __name__ == "__main__":
#     main()




import streamlit as st
import os
from typing import List, Dict
import requests
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from docx import Document

load_dotenv()

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

class VectorDatabase:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.documents = []
        self.vectors = None

    def add_documents(self, documents: List[str]):
        self.documents = documents
        self.vectors = self.vectorizer.fit_transform(documents)

    def search(self, query: str, k: int = 2) -> List[str]:
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.vectors)[0]
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        return [self.documents[i] for i in top_k_indices]

class OpenAIInterface:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_chat_response(self, conversation: List[Dict[str, str]]) -> str:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": conversation
        }
        response = requests.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

def chunk_document(text: str, chunk_size: int = 200) -> List[str]:
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def read_docx(file):
    doc = Document(file)
    return " ".join([paragraph.text for paragraph in doc.paragraphs])

def main():
    st.set_page_config(page_title="Legal Assistant", page_icon="⚖️", layout="wide")
    st.title("🤖 Your AI Legal Assistant")

    if 'vector_db' not in st.session_state:
        st.session_state.vector_db = VectorDatabase()

    if 'openai_interface' not in st.session_state:
        st.session_state.openai_interface = OpenAIInterface()

    if 'document_processed' not in st.session_state:
        st.session_state.document_processed = False

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    uploaded_file = st.file_uploader("Upload a legal document", type=["txt", "docx"])

    if uploaded_file and not st.session_state.document_processed:
        if uploaded_file.type == "text/plain":
            document = uploaded_file.getvalue().decode("utf-8")
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            document = read_docx(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a .txt or .docx file.")
            return

        chunks = chunk_document(document)
        st.session_state.vector_db.add_documents(chunks)
        st.session_state.document_processed = True
        st.success(f"✅ {uploaded_file.name} processed and added to vector database!")

    if st.session_state.document_processed:
        st.subheader("💬 Chat with Your Legal Assistant")
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("Ask a question about the legal document...")

        if question:
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            with st.spinner("Searching document and generating response..."):
                relevant_chunks = st.session_state.vector_db.search(question)
                context = "\n".join(relevant_chunks)
                prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
                conversation = [
                    {"role": "system", "content": "You are a helpful legal assistant. Provide clear and concise answers based on the given context."},
                    {"role": "user", "content": prompt}
                ]
                response = st.session_state.openai_interface.generate_chat_response(conversation)

            with st.chat_message("assistant"):
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
