# # Assignment 1:

# import streamlit as st
# import os
# from typing import List, Dict
# import requests
# from dotenv import load_dotenv
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np
# from docx import Document

# load_dotenv()

# OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY not found in environment variables")

# class VectorDatabase:
#     def __init__(self):
#         self.vectorizer = TfidfVectorizer()
#         self.documents = []
#         self.vectors = None

#     def add_documents(self, documents: List[str]):
#         self.documents = documents
#         self.vectors = self.vectorizer.fit_transform(documents)

#     def search(self, query: str, k: int = 2) -> List[str]:
#         query_vector = self.vectorizer.transform([query])
#         similarities = cosine_similarity(query_vector, self.vectors)[0]
#         top_k_indices = np.argsort(similarities)[-k:][::-1]
#         return [self.documents[i] for i in top_k_indices]

# class OpenAIInterface:
#     def __init__(self):
#         self.api_key = OPENAI_API_KEY
#         self.base_url = "https://api.openai.com/v1"
#         self.headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json"
#         }

#     def generate_chat_response(self, conversation: List[Dict[str, str]]) -> str:
#         payload = {
#             "model": "gpt-3.5-turbo",
#             "messages": conversation
#         }
#         response = requests.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload)
#         response.raise_for_status()
#         return response.json()['choices'][0]['message']['content']

# def chunk_document(text: str, chunk_size: int = 200) -> List[str]:
#     words = text.split()
#     return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# def read_docx(file):
#     doc = Document(file)
#     return " ".join([paragraph.text for paragraph in doc.paragraphs])

# def main():
#     st.set_page_config(page_title="Legal Assistant", page_icon="⚖️", layout="wide")
#     st.title("🤖 Your AI Legal Assistant")

#     if 'vector_db' not in st.session_state:
#         st.session_state.vector_db = VectorDatabase()

#     if 'openai_interface' not in st.session_state:
#         st.session_state.openai_interface = OpenAIInterface()

#     if 'document_processed' not in st.session_state:
#         st.session_state.document_processed = False

#     if 'chat_history' not in st.session_state:
#         st.session_state.chat_history = []

#     uploaded_file = st.file_uploader("Upload a legal document", type=["txt", "docx"])

#     if uploaded_file and not st.session_state.document_processed:
#         if uploaded_file.type == "text/plain":
#             document = uploaded_file.getvalue().decode("utf-8")
#         elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#             document = read_docx(uploaded_file)
#         else:
#             st.error("Unsupported file type. Please upload a .txt or .docx file.")
#             return

#         chunks = chunk_document(document)
#         st.session_state.vector_db.add_documents(chunks)
#         st.session_state.document_processed = True
#         st.success(f"✅ {uploaded_file.name} processed and added to vector database!")

#     if st.session_state.document_processed:
#         st.subheader("💬 Chat with Your Legal Assistant")
#         for message in st.session_state.chat_history:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])

#         question = st.chat_input("Ask a question about the legal document...")

#         if question:
#             st.session_state.chat_history.append({"role": "user", "content": question})
#             with st.chat_message("user"):
#                 st.markdown(question)

#             with st.spinner("Searching document and generating response..."):
#                 relevant_chunks = st.session_state.vector_db.search(question)
#                 context = "\n".join(relevant_chunks)
#                 prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
#                 conversation = [
#                     {"role": "system", "content": "You are a helpful legal assistant. Provide clear and concise answers based on the given context."},
#                     {"role": "user", "content": prompt}
#                 ]
#                 response = st.session_state.openai_interface.generate_chat_response(conversation)

#             with st.chat_message("assistant"):
#                 st.markdown(response)
#                 st.session_state.chat_history.append({"role": "assistant", "content": response})

# if __name__ == "__main__":
#     main()



import streamlit as st
import os
from typing import List, Dict
import requests
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

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

def ask_openai(question: str, context: str) -> str:
    interface = st.session_state.openai_interface
    conversation = [
        {"role": "system", "content": "You are a legal assistant for Australian protection visas."},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
    ]
    return interface.generate_chat_response(conversation)

def main():
    st.set_page_config(page_title="Protection Visa Assistant", page_icon="🛡️", layout="wide")
    st.title("🛡️ Australian Protection Visa Assistant")

    # Initialize OpenAI Interface
    if 'openai_interface' not in st.session_state:
        st.session_state.openai_interface = OpenAIInterface()

    # Step 1: Input user details
    st.header("Step 1: Provide Your Details")
    is_refugee = st.radio("Are you a refugee or facing significant harm in your home country?", ["Yes", "No"])
    can_live_elsewhere = st.radio("Can you legally settle in another safe country?", ["Yes", "No"])

    # Step 2: Assess refugee qualifications
    if is_refugee == "Yes":
        st.header("Step 2: Refugee Qualification Assessment")
        has_persecution_reasons = st.radio(
            "Do you fear persecution for reasons of race, religion, nationality, political opinion, or membership in a particular social group?",
            ["Yes", "No"]
        )
        if has_persecution_reasons == "Yes":
            context = "Applicant fears persecution for reasons of race, religion, nationality, political opinion, or social group."
            st.write("Assessing eligibility...")
            ai_response = ask_openai("Is the applicant eligible for refugee status?", context)
            st.write(f"AI Response: {ai_response}")

    # Step 3: Evaluate significant harm
    if is_refugee == "No" or can_live_elsewhere == "No":
        st.header("Step 3: Significant Harm Assessment")
        significant_harm = st.radio("Do you face significant harm such as torture or cruel treatment?", ["Yes", "No"])
        if significant_harm == "Yes":
            context = "Applicant faces significant harm such as torture or inhumane treatment."
            ai_response = ask_openai("Can the applicant qualify for protection visa under significant harm risk?", context)
            st.write(f"AI Response: {ai_response}")

    # Final decision
    st.header("Final Decision")
    st.write("Based on your inputs, the AI will assess your overall eligibility for protection visa.")
    context = "Collect all provided information and evaluate protection visa eligibility."
    final_response = ask_openai("What is the applicant's overall eligibility for a protection visa?", context)
    st.write(f"AI Response: {final_response}")

if __name__ == "__main__":
    main()
