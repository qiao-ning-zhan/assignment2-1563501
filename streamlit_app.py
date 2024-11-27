import streamlit as st
from typing import List, Dict
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Attempt to load OpenAI API Key from secrets
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    OPENAI_API_KEY = None  # Will prompt user to enter API key

# OpenAI interface class
class OpenAIInterface:
    def __init__(self):
        # Initialize API key and headers
        self.api_key = OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "Content-Type": "application/json"
        }

    def generate_chat_response(self, conversation: List[Dict[str, str]]) -> str:
        # Check if API key is provided
        if not self.api_key:
            return "OpenAI API key is not provided."
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": conversation
        }
        # Make API request
        response = requests.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload)
        response.raise_for_status()
        # Return the assistant's reply
        return response.json()['choices'][0]['message']['content']

# Function to retrieve relevant context from the uploaded document
def retrieve_context(question: str, document_path: str) -> str:
    """
    Simple keyword-based retrieval to extract relevant paragraphs from a text document.
    """
    with open(document_path, "r", encoding="utf-8") as file:
        document_content = file.read()
    
    # Split document into paragraphs
    paragraphs = document_content.split("\n\n")  # Assuming paragraphs are separated by double newlines
    
    # Find paragraphs containing the question's keywords
    keywords = question.split()
    relevant_paragraphs = [
        para.strip() for para in paragraphs 
        if any(keyword.lower() in para.lower() for keyword in keywords)
    ]
    
    # Join the most relevant paragraphs (up to 3 for simplicity)
    return "\n\n".join(relevant_paragraphs[:3])  # Limit to 3 paragraphs

def ask_openai(question: str, context: str = "") -> str:
    # Helper function to interact with OpenAI
    interface = st.session_state.openai_interface
    conversation = [
        {
            "role": "system", 
            "content": (
                "You are an expert in Australian protection visa cases. "
                "Answer user questions based only on the provided context. "
                "If the context is insufficient, state that more information is needed."
            )
        },
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
    ]
    return interface.generate_chat_response(conversation)

# Main Streamlit application
def main():
    st.set_page_config(page_title="Protection Visa Assistant", page_icon="🛡️", layout="wide")
    st.title("🛡️ Australian Protection Visa Assistant 🛡️")

    # Initialize OpenAI interface
    if 'openai_interface' not in st.session_state:
        st.session_state.openai_interface = OpenAIInterface()

    # Initialize session state variables
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    if 'analysis' not in st.session_state:
        st.session_state.analysis = {}
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1  # Start from step 1

    # Predefined legal guidance
    st.subheader("Guidance for Australian Protection Visa")
    st.write("""
    Protection visas apply to individuals who need protection in Australia because they face real risks of significant harm or persecution if they return to their home country. Answer the questions below to determine your eligibility.
    """)

    # Path to the document
    document_path = "Australian_Protection_Visa_Information.txt"

    # Questions split into 4 groups of 3 questions each
    questions_group = {
        1: [
            "Are you a refugee or at risk of significant harm if you return to your home country?",
            "Can you legally settle in another country (not your home country) with safety guaranteed?",
            "Do you have a well-founded fear of persecution, making you unable or unwilling to return to your home country?"
        ],
        2: [
            "Do you fear persecution based on race, religion, nationality, membership in a particular social group, or political opinion?",
            "Does persecution involve serious harm or systematic, discriminatory conduct?",
            "Do you face real risk of persecution in all areas of your home country?"
        ],
        3: [
            "Does serious harm include threats to life or freedom?",
            "Does serious harm include severe physical harassment or abuse?",
            "Does serious harm include severe economic hardship threatening survival?"
        ],
        4: [
            "Does serious harm require you to alter or hide your beliefs, identity, or practices (e.g., religion, sexuality)?",
            "Can your home country's government or any controlling group protect you from persecution?",
            "Does significant harm risk include torture, inhumane treatment, or punishment?"
        ]
    }

    # Sidebar progress bar
    total_questions = sum(len(questions) for questions in questions_group.values())
    progress_percentage = int((st.session_state.progress / total_questions) * 100)
    st.sidebar.header("Progress")
    st.sidebar.progress(progress_percentage)

    # Display questions and handle submissions for each group
    for step in range(1, 5):
        st.subheader(f"Step {step}: Questions")
        group_disabled = step > st.session_state.current_step

        with st.container():
            for idx, question in enumerate(questions_group[step], 1):
                key = f"step_{step}_q{idx}"
                if key not in st.session_state.responses:
                    st.session_state.responses[key] = "Select an option"

                options = ["Select an option", "Yes", "No"]
                current_value = st.session_state.responses[key]
                index = options.index(current_value) if current_value in options else 0

                st.session_state.responses[key] = st.radio(
                    f"{idx}. {question}", options, key=key, index=index, disabled=group_disabled
                )

            submit_button_key = f"submit_step_{step}"
            if group_disabled:
                st.button(f"Submit Step {step}", key=submit_button_key, disabled=True)
            else:
                if st.button(f"Submit Step {step}", key=submit_button_key):
                    if all(
                        st.session_state.responses[f"step_{step}_q{idx}"] != "Select an option"
                        for idx in range(1, len(questions_group[step]) + 1)
                    ):
                        context = "\n".join([
                            f"{question} | Answer: {st.session_state.responses[f'step_{step}_q{idx}']}"
                            for idx, question in enumerate(questions_group[step], 1)
                        ])
                        retrieved_context = retrieve_context(context, document_path)
                        with st.spinner("Analyzing your responses..."):
                            analysis_result = ask_openai(
                                "Based on the responses, assess the likelihood of meeting protection visa requirements.",
                                retrieved_context
                            )
                            additional_info = ask_openai("Provide additional relevant guidance based on the context.", retrieved_context)
                        st.success("Analysis complete!")
                        analysis_result = analysis_result + additional_info
                        st.write(analysis_result)
                        # st.markdown(f"**Additional Guidance:**\n{additional_info}")
                        # st.write(additional_info)

                        st.session_state.analysis[step] = analysis_result
                        st.session_state.progress += len(questions_group[step])
                        st.session_state.current_step += 1
                    else:
                        st.error("Please answer all questions before submitting.")

        if step in st.session_state.analysis:
            st.markdown(f"**Analysis for Step {step}:**")
            st.write(st.session_state.analysis[step])

    if st.session_state.current_step > 4:
        st.subheader("Additional Information (Required For Final Analysis)")
        user_story = st.text_area(
            "Provide any additional details relevant to your application:", ""
        )
        if st.button("Get Final Analysis"):
            full_context = "\n".join([
                f"Step {i} Responses: " + ", ".join([
                    f"Q{j}: {st.session_state.responses[f'step_{i}_q{j}']}"
                    for j in range(1, len(questions_group[i]) + 1)
                ])
                for i in range(1, 5)
            ])
            if user_story.strip():
                full_context += f"\n\nAdditional Information:\n{user_story}"

            with st.spinner("Generating final analysis..."):
                final_result = ask_openai(
                    "Provide a comprehensive final assessment for the applicant.", full_context
                )
            # st.subheader("Final Result")
            # st.write(final_result)
            st.session_state.final_result = final_result

    if 'final_result' in st.session_state:
        st.subheader("Final Result")
        st.write(st.session_state.final_result)

if __name__ == "__main__":
    main()
