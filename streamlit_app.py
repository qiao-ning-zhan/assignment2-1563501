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
