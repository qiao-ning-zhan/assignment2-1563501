# =============================================
# =========     Version 1     =================
# =============================================

# import streamlit as st
# import os
# from typing import List, Dict
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY not found in environment variables")

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

# def ask_openai(question: str, context: str) -> str:
#     interface = st.session_state.openai_interface
#     conversation = [
#         {"role": "system", "content": "You are a legal assistant for Australian protection visas."},
#         {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
#     ]
#     return interface.generate_chat_response(conversation)

# def main():
#     st.set_page_config(page_title="Protection Visa Assistant", page_icon="🛡️", layout="wide")
#     st.title("🛡️ Australian Protection Visa Assistant")

#     # Initialize OpenAI Interface
#     if 'openai_interface' not in st.session_state:
#         st.session_state.openai_interface = OpenAIInterface()

#     # Step 1: Input user details
#     st.header("Step 1: Provide Your Details")
#     is_refugee = st.radio("Are you a refugee or facing significant harm in your home country?", ["Yes", "No"])
#     can_live_elsewhere = st.radio("Can you legally settle in another safe country?", ["Yes", "No"])

#     # Step 2: Assess refugee qualifications
#     if is_refugee == "Yes":
#         st.header("Step 2: Refugee Qualification Assessment")
#         has_persecution_reasons = st.radio(
#             "Do you fear persecution for reasons of race, religion, nationality, political opinion, or membership in a particular social group?",
#             ["Yes", "No"]
#         )
#         if has_persecution_reasons == "Yes":
#             context = "Applicant fears persecution for reasons of race, religion, nationality, political opinion, or social group."
#             st.write("Assessing eligibility...")
#             ai_response = ask_openai("Is the applicant eligible for refugee status?", context)
#             st.write(f"AI Response: {ai_response}")

#     # Step 3: Evaluate significant harm
#     if is_refugee == "No" or can_live_elsewhere == "No":
#         st.header("Step 3: Significant Harm Assessment")
#         significant_harm = st.radio("Do you face significant harm such as torture or cruel treatment?", ["Yes", "No"])
#         if significant_harm == "Yes":
#             context = "Applicant faces significant harm such as torture or inhumane treatment."
#             ai_response = ask_openai("Can the applicant qualify for protection visa under significant harm risk?", context)
#             st.write(f"AI Response: {ai_response}")

#     # Final decision
#     st.header("Final Decision")
#     st.write("Based on your inputs, the AI will assess your overall eligibility for protection visa.")
#     context = "Collect all provided information and evaluate protection visa eligibility."
#     final_response = ask_openai("What is the applicant's overall eligibility for a protection visa?", context)
#     st.write(f"AI Response: {final_response}")

# if __name__ == "__main__":
#     main()



# =============================================
# =========     Version 2     =================
# =============================================


# import streamlit as st
# from typing import List, Dict
# import requests
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Load OpenAI API Key
# OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY not found in environment variables")

# # OpenAI interface
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

# def ask_openai(question: str, context: str) -> str:
#     interface = st.session_state.openai_interface
#     conversation = [
#         {"role": "system", "content": "You are a legal assistant specializing in Australian protection visa cases. Use the provided context and respond based on legal eligibility criteria."},
#         {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
#     ]
#     return interface.generate_chat_response(conversation)

# # Streamlit application
# def main():
#     st.set_page_config(page_title="Protection Visa Assistant", page_icon="🛡️", layout="wide")
#     st.title("🛡️ Australian Protection Visa Assistant")

#     # Initialize OpenAI interface
#     if 'openai_interface' not in st.session_state:
#         st.session_state.openai_interface = OpenAIInterface()

#     # Predefined legal guidance
#     st.subheader("Guidance for Australian Protection Visa")
#     st.write("""
#     Protection visas apply to individuals who need protection in Australia because they face real risks of significant harm or persecution if they return to their home country. Please answer the following questions to determine your eligibility for a protection visa.
#     """)

#     # User inputs for 12 options
#     st.subheader("Step 1: Answer the Eligibility Questions")
#     responses = {}

#     # List all options with Yes/No choices
#     questions = [
#         "Are you a refugee or at risk of significant harm if you return to your home country?",
#         "Can you legally settle in another country (not your home country) with safety guaranteed?",
#         "Do you have a well-founded fear of persecution, making you unable or unwilling to return to your home country?",
#         "Do you fear persecution based on race, religion, nationality, membership in a particular social group, or political opinion?",
#         "Does persecution involve serious harm or systematic, discriminatory conduct?",
#         "Do you face real risk of persecution in all areas of your home country?",
#         "Does serious harm include threats to life or freedom?",
#         "Does serious harm include severe physical harassment or abuse?",
#         "Does serious harm include severe economic hardship threatening survival?",
#         "Does serious harm require you to alter or hide your beliefs, identity, or practices (e.g., religion, sexuality)?",
#         "Can your home country's government or any controlling group protect you from persecution?",
#         "Does significant harm risk include torture, inhumane treatment, or punishment?"
#     ]

#     # Collect responses
#     for idx, question in enumerate(questions, 1):
#         responses[f"option_{idx}"] = st.radio(f"{idx}. {question}", ["Yes", "No"], key=f"option_{idx}")

#     # Submit button
#     if st.button("Submit"):
#         # Ensure all questions are answered
#         if all(value != "" for value in responses.values()):
#             # Compile context for OpenAI API
#             context = "\n".join([f"Q{idx}: {q} | Answer: {responses[f'option_{idx}']}" for idx, q in enumerate(questions, 1)])
#             st.subheader("Results")
#             with st.spinner("Analyzing your responses..."):
#                 result = ask_openai("Based on the responses, what is the applicant's eligibility for a protection visa?", context)
#                 st.success("Analysis complete!")
#                 st.write(result)
#         else:
#             st.error("Please answer all questions before submitting.")

# if __name__ == "__main__":
#     main()



# =============================================
# =========     Version 3     =================
# =============================================

# import streamlit as st
# from typing import List, Dict
# import requests
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Load OpenAI API Key
# OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY not found in environment variables")

# # OpenAI interface
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

# def ask_openai(question: str, context: str) -> str:
#     interface = st.session_state.openai_interface
#     conversation = [
#         {"role": "system", "content": "You are a legal assistant specializing in Australian protection visa cases. Use the provided context and respond with probability estimates."},
#         {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
#     ]
#     return interface.generate_chat_response(conversation)

# # Streamlit application
# def main():
#     st.set_page_config(page_title="Protection Visa Assistant", page_icon="🛡️", layout="wide")
#     st.title("🛡️ Australian Protection Visa Assistant")

#     # Initialize OpenAI interface
#     if 'openai_interface' not in st.session_state:
#         st.session_state.openai_interface = OpenAIInterface()

#     # Initialize session state
#     if 'responses' not in st.session_state:
#         st.session_state.responses = {}
#     if 'step' not in st.session_state:
#         st.session_state.step = 1
#     if 'probabilities' not in st.session_state:
#         st.session_state.probabilities = {}

#     # Predefined legal guidance
#     st.subheader("Guidance for Australian Protection Visa")
#     st.write("""
#     Protection visas apply to individuals who need protection in Australia because they face real risks of significant harm or persecution if they return to their home country. Answer the questions below to determine your eligibility.
#     """)

#     # Questions split into groups
#     questions_group = {
#         1: [
#             "Are you a refugee or at risk of significant harm if you return to your home country?",
#             "Can you legally settle in another country (not your home country) with safety guaranteed?",
#             "Do you have a well-founded fear of persecution, making you unable or unwilling to return to your home country?",
#             "Do you fear persecution based on race, religion, nationality, membership in a particular social group, or political opinion?"
#         ],
#         2: [
#             "Does persecution involve serious harm or systematic, discriminatory conduct?",
#             "Do you face real risk of persecution in all areas of your home country?",
#             "Does serious harm include threats to life or freedom?",
#             "Does serious harm include severe physical harassment or abuse?"
#         ],
#         3: [
#             "Does serious harm include severe economic hardship threatening survival?",
#             "Does serious harm require you to alter or hide your beliefs, identity, or practices (e.g., religion, sexuality)?",
#             "Can your home country's government or any controlling group protect you from persecution?",
#             "Does significant harm risk include torture, inhumane treatment, or punishment?"
#         ]
#     }

#     # Current step
#     step = st.session_state.step
#     current_questions = questions_group[step]

#     # Display questions for the current step
#     st.subheader(f"Step {step}: Questions")
#     for idx, question in enumerate(current_questions, 1):
#         key = f"step_{step}_q{idx}"
#         st.session_state.responses[key] = st.radio(f"{idx}. {question}", ["Yes", "No"], key=key)

#     # Submit button for current step
#     if st.button(f"Submit Step {step}"):
#         # Ensure all questions are answered
#         if all(st.session_state.responses[f"step_{step}_q{idx}"] != "" for idx in range(1, len(current_questions) + 1)):
#             # Compile context for current step
#             context = "\n".join([f"{q} | Answer: {st.session_state.responses[f'step_{step}_q{idx}']}" for idx, q in enumerate(current_questions, 1)])
#             with st.spinner("Analyzing your responses..."):
#                 result = ask_openai("Based on these responses, what is the probability of meeting protection visa requirements?", context)
#             st.session_state.probabilities[f"step_{step}"] = result

#             # Display result with progress visualization
#             st.success("Analysis complete!")
#             st.write(result)

#             # Visualize the probability (mock visualization)
#             import random
#             percentage = random.randint(50, 100)  # Replace this with actual parsing of result from OpenAI
#             st.progress(percentage)

#             # Unlock next step
#             if step < 3:
#                 st.session_state.step += 1
#         else:
#             st.error("Please answer all questions before submitting.")

#     # Final result
#     if step == 3 and all(f"step_{i}" in st.session_state.probabilities for i in range(1, 4)):
#         st.subheader("Final Result")
#         st.write("Based on your answers to all questions, here is the final analysis:")
#         final_context = "\n".join([f"Step {i}: {st.session_state.probabilities[f'step_{i}']}" for i in range(1, 4)])
#         final_result = ask_openai("Provide a final analysis of the applicant's eligibility for a protection visa based on all steps.", final_context)
#         st.write(final_result)

# if __name__ == "__main__":
#     main()





# =============================================
# =========     Version 4     =================
# =============================================

# import streamlit as st
# from typing import List, Dict
# import requests
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Load OpenAI API Key
# OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY not found in environment variables")

# # OpenAI interface
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

# def ask_openai(question: str, context: str) -> str:
#     interface = st.session_state.openai_interface
#     conversation = [
#         {"role": "system", "content": "You are a legal assistant specializing in Australian protection visa cases. Use the provided context and respond with probability estimates."},
#         {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
#     ]
#     return interface.generate_chat_response(conversation)

# # Streamlit application
# def main():
#     st.set_page_config(page_title="Protection Visa Assistant", page_icon="🛡️", layout="wide")
#     st.title("🛡️ Australian Protection Visa Assistant")

#     # Initialize OpenAI interface
#     if 'openai_interface' not in st.session_state:
#         st.session_state.openai_interface = OpenAIInterface()

#     # Initialize session state
#     if 'responses' not in st.session_state:
#         st.session_state.responses = {}
#     if 'step' not in st.session_state:
#         st.session_state.step = 1
#     if 'progress' not in st.session_state:
#         st.session_state.progress = 0
#     if 'next_group_unlocked' not in st.session_state:
#         st.session_state.next_group_unlocked = False

#     # Predefined legal guidance
#     st.subheader("Guidance for Australian Protection Visa")
#     st.write("""
#     Protection visas apply to individuals who need protection in Australia because they face real risks of significant harm or persecution if they return to their home country. Answer the questions below to determine your eligibility.
#     """)

#     # Questions split into groups
#     questions_group = {
#         1: [
#             "Are you a refugee or at risk of significant harm if you return to your home country?",
#             "Can you legally settle in another country (not your home country) with safety guaranteed?",
#             "Do you have a well-founded fear of persecution, making you unable or unwilling to return to your home country?",
#             "Do you fear persecution based on race, religion, nationality, membership in a particular social group, or political opinion?"
#         ],
#         2: [
#             "Does persecution involve serious harm or systematic, discriminatory conduct?",
#             "Do you face real risk of persecution in all areas of your home country?",
#             "Does serious harm include threats to life or freedom?",
#             "Does serious harm include severe physical harassment or abuse?"
#         ],
#         3: [
#             "Does serious harm include severe economic hardship threatening survival?",
#             "Does serious harm require you to alter or hide your beliefs, identity, or practices (e.g., religion, sexuality)?",
#             "Can your home country's government or any controlling group protect you from persecution?",
#             "Does significant harm risk include torture, inhumane treatment, or punishment?"
#         ]
#     }

#     # Sidebar progress bar
#     total_questions = sum(len(questions) for questions in questions_group.values())
#     progress_percentage = int((st.session_state.progress / total_questions) * 100)
#     st.sidebar.header("Progress")
#     st.sidebar.progress(progress_percentage)

#     # Current step
#     step = st.session_state.step
#     current_questions = questions_group[step]

#     # Display questions for the current step
#     st.subheader(f"Step {step}: Questions")
#     for idx, question in enumerate(current_questions, 1):
#         key = f"step_{step}_q{idx}"
#         # Set default option to None
#         if key not in st.session_state.responses:
#             st.session_state.responses[key] = None
#         st.session_state.responses[key] = st.radio(f"{idx}. {question}", ["Select an option", "Yes", "No"], key=key, index=0)

#     # Submit button for current step
#     if st.button(f"Submit Step {step}"):
#         # Ensure all questions are answered
#         if all(st.session_state.responses[f"step_{step}_q{idx}"] not in [None, "Select an option"] for idx in range(1, len(current_questions) + 1)):
#             # Compile context for current step
#             context = "\n".join([f"{q} | Answer: {st.session_state.responses[f'step_{step}_q{idx}']}" for idx, q in enumerate(current_questions, 1)])
#             with st.spinner("Analyzing your responses..."):
#                 result = ask_openai("Based on these responses, what is the probability of meeting protection visa requirements?", context)
#             st.success("Analysis complete!")
#             st.write(result)

#             # Update progress
#             st.session_state.progress += len(current_questions)
#             st.session_state.next_group_unlocked = True
#         else:
#             st.error("Please answer all questions before submitting.")

#     # Next group button
#     if st.session_state.next_group_unlocked and step < 3:
#         if st.button("Next Group"):
#             st.session_state.step += 1
#             st.session_state.next_group_unlocked = False

#     # Final result
#     if step == 3 and st.session_state.progress == total_questions:
#         st.subheader("Final Result")
#         st.write("Based on your answers to all questions, here is the final analysis:")
#         final_context = "\n".join([f"Step {i}: {', '.join([f'Q{j}: {st.session_state.responses[f'step_{i}_q{j}']}' for j in range(1, 5)])}" for i in range(1, 4)])
#         final_result = ask_openai("Provide a final analysis of the applicant's eligibility for a protection visa based on all steps.", final_context)
#         st.write(final_result)

# if __name__ == "__main__":
#     main()




# # ======
# import streamlit as st
# from typing import List, Dict
# import requests
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Load OpenAI API Key
# OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY not found in environment variables")

# # OpenAI interface
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

# def ask_openai(question: str, context: str) -> str:
#     interface = st.session_state.openai_interface
#     conversation = [
#         {"role": "system", "content": "You are a legal assistant specializing in Australian protection visa cases. Use the provided context and respond with probability estimates."},
#         {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
#     ]
#     return interface.generate_chat_response(conversation)

# # Streamlit application
# def main():
#     st.set_page_config(page_title="Protection Visa Assistant", page_icon="🛡️", layout="wide")
#     st.title("🛡️ Australian Protection Visa Assistant")

#     # Initialize OpenAI interface
#     if 'openai_interface' not in st.session_state:
#         st.session_state.openai_interface = OpenAIInterface()

#     # Initialize session state
#     if 'responses' not in st.session_state:
#         st.session_state.responses = {}
#     if 'step' not in st.session_state:
#         st.session_state.step = 1
#     if 'progress' not in st.session_state:
#         st.session_state.progress = 0
#     if 'next_group_unlocked' not in st.session_state:
#         st.session_state.next_group_unlocked = False

#     # Predefined legal guidance
#     st.subheader("Guidance for Australian Protection Visa")
#     st.write("""
#     Protection visas apply to individuals who need protection in Australia because they face real risks of significant harm or persecution if they return to their home country. Answer the questions below to determine your eligibility.
#     """)

#     # Questions split into groups
#     questions_group = {
#         1: [
#             "Are you a refugee or at risk of significant harm if you return to your home country?",
#             "Can you legally settle in another country (not your home country) with safety guaranteed?",
#             "Do you have a well-founded fear of persecution, making you unable or unwilling to return to your home country?",
#             "Do you fear persecution based on race, religion, nationality, membership in a particular social group, or political opinion?"
#         ],
#         2: [
#             "Does persecution involve serious harm or systematic, discriminatory conduct?",
#             "Do you face real risk of persecution in all areas of your home country?",
#             "Does serious harm include threats to life or freedom?",
#             "Does serious harm include severe physical harassment or abuse?"
#         ],
#         3: [
#             "Does serious harm include severe economic hardship threatening survival?",
#             "Does serious harm require you to alter or hide your beliefs, identity, or practices (e.g., religion, sexuality)?",
#             "Can your home country's government or any controlling group protect you from persecution?",
#             "Does significant harm risk include torture, inhumane treatment, or punishment?"
#         ]
#     }

#     # Sidebar progress bar
#     total_questions = sum(len(questions) for questions in questions_group.values())
#     progress_percentage = int((st.session_state.progress / total_questions) * 100)
#     st.sidebar.header("Progress")
#     st.sidebar.progress(progress_percentage)

#     # Define function to go to next group
#     def next_group():
#         st.session_state.step += 1
#         st.session_state.next_group_unlocked = False

#     # Next group button
#     if st.session_state.next_group_unlocked and st.session_state.step < 3:
#         st.button("Next Group", on_click=next_group)

#     # Current step
#     step = st.session_state.step
#     current_questions = questions_group[step]

#     # Display questions for the current step
#     st.subheader(f"Step {step}: Questions")
#     for idx, question in enumerate(current_questions, 1):
#         key = f"step_{step}_q{idx}"
#         # Set default option to "Select an option"
#         if key not in st.session_state.responses:
#             st.session_state.responses[key] = "Select an option"
#         options = ["Select an option", "Yes", "No"]
#         current_value = st.session_state.responses[key]
#         index = options.index(current_value) if current_value in options else 0
#         st.session_state.responses[key] = st.radio(f"{idx}. {question}", options, key=key, index=index)

#     # Submit button for current step
#     if st.button(f"Submit Step {step}"):
#         # Ensure all questions are answered
#         if all(st.session_state.responses[f"step_{step}_q{idx}"] != "Select an option" for idx in range(1, len(current_questions) + 1)):
#             # Compile context for current step
#             context = "\n".join([f"{q} | Answer: {st.session_state.responses[f'step_{step}_q{idx}']}" for idx, q in enumerate(current_questions, 1)])
#             with st.spinner("Analyzing your responses..."):
#                 result = ask_openai("Based on these responses, what is the probability of meeting protection visa requirements?", context)
#             st.success("Analysis complete!")
#             st.write(result)

#             # Update progress
#             st.session_state.progress += len(current_questions)
#             st.session_state.next_group_unlocked = True
#         else:
#             st.error("Please answer all questions before submitting.")

#     # Final result
#     if step == 3 and st.session_state.progress == total_questions:
#         st.subheader("Final Result")
#         st.write("Based on your answers to all questions, here is the final analysis:")
#         final_context = "\n".join([
#             f"Step {i}: " + ", ".join([
#                 f"Q{j}: {st.session_state.responses[f'step_{i}_q{j}']}"
#                 for j in range(1, len(questions_group[i]) + 1)
#             ])
#             for i in range(1, 4)
#         ])
#         final_result = ask_openai(
#             "Provide a final analysis of the applicant's eligibility for a protection visa based on all steps.",
#             final_context
#         )
#         st.write(final_result)

# if __name__ == "__main__":
#     main()


# ====================


# import streamlit as st
# import time  # Import the time module
# from typing import List, Dict
# import requests
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Load OpenAI API key
# OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY not found in environment variables")

# # OpenAI API Interface
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

# def ask_openai(question: str, context: str) -> str:
#     interface = st.session_state.openai_interface
#     conversation = [
#         {"role": "system", "content": "You are a legal assistant specializing in Australian protection visa cases. Use the provided context and respond with probability estimates."},
#         {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
#     ]
#     return interface.generate_chat_response(conversation)

# # Streamlit application
# def main():
#     st.set_page_config(page_title="Protection Visa Assistant", page_icon="🛡️", layout="wide")
#     st.title("🛡️ Australian Protection Visa Assistant")

#     # Initialize the OpenAI interface
#     if 'openai_interface' not in st.session_state:
#         st.session_state.openai_interface = OpenAIInterface()

#     # Initialize session state
#     if 'responses' not in st.session_state:
#         st.session_state.responses = {}
#     if 'step' not in st.session_state:
#         st.session_state.step = 1
#     if 'progress' not in st.session_state:
#         st.session_state.progress = 0
#     if 'next_group_unlocked' not in st.session_state:
#         st.session_state.next_group_unlocked = False
#     if 'analysis_complete_time' not in st.session_state:
#         st.session_state.analysis_complete_time = None

#     # Predefined legal guidance
#     st.subheader("Guidance for Australian Protection Visa")
#     st.write("""
#     Protection visas apply to individuals who need protection in Australia because they face real risks of significant harm or persecution if they return to their home country. Answer the questions below to determine your eligibility.
#     """)

#     # Question groups
#     questions_group = {
#         1: [
#             "Are you a refugee or at risk of significant harm if you return to your home country?",
#             "Can you legally settle in another country (not your home country) with safety guaranteed?",
#             "Do you have a well-founded fear of persecution, making you unable or unwilling to return to your home country?",
#             "Do you fear persecution based on race, religion, nationality, membership in a particular social group, or political opinion?"
#         ],
#         2: [
#             "Does persecution involve serious harm or systematic, discriminatory conduct?",
#             "Do you face real risk of persecution in all areas of your home country?",
#             "Does serious harm include threats to life or freedom?",
#             "Does serious harm include severe physical harassment or abuse?"
#         ],
#         3: [
#             "Does serious harm include severe economic hardship threatening survival?",
#             "Does serious harm require you to alter or hide your beliefs, identity, or practices (e.g., religion, sexuality)?",
#             "Can your home country's government or any controlling group protect you from persecution?",
#             "Does significant harm risk include torture, inhumane treatment, or punishment?"
#         ]
#     }

#     # Sidebar progress bar
#     total_questions = sum(len(questions) for questions in questions_group.values())
#     progress_percentage = int((st.session_state.progress / total_questions) * 100)
#     st.sidebar.header("Progress")
#     st.sidebar.progress(progress_percentage)

#     # Function to proceed to the next group
#     def next_group():
#         st.session_state.step += 1
#         st.session_state.next_group_unlocked = False
#         st.session_state.analysis_complete_time = None  # Reset the analysis completion time

#     # Current step
#     step = st.session_state.step
#     current_questions = questions_group[step]

#     # Display the current step questions
#     st.subheader(f"Step {step}: Questions")
#     for idx, question in enumerate(current_questions, 1):
#         key = f"step_{step}_q{idx}"
#         # Set the default option to "Select an option"
#         if key not in st.session_state.responses:
#             st.session_state.responses[key] = "Select an option"
#         options = ["Select an option", "Yes", "No"]
#         current_value = st.session_state.responses[key]
#         index = options.index(current_value) if current_value in options else 0
#         st.session_state.responses[key] = st.radio(f"{idx}. {question}", options, key=key, index=index)

#     # Submit button for the current step
#     if st.button(f"Submit Step {step}"):
#         # Ensure all questions are answered
#         if all(st.session_state.responses[f"step_{step}_q{idx}"] != "Select an option" for idx in range(1, len(current_questions) + 1)):
#             # Compile the context for the current step
#             context = "\n".join([f"{q} | Answer: {st.session_state.responses[f'step_{step}_q{idx}']}" for idx, q in enumerate(current_questions, 1)])
#             with st.spinner("Analyzing your responses..."):
#                 result = ask_openai("Based on these responses, what is the probability of meeting protection visa requirements?", context)
#             st.success("Analysis complete!")
#             st.write(result)

#             # Update progress
#             st.session_state.progress += len(current_questions)
#             st.session_state.analysis_complete_time = time.time()
#             # Do not set next_group_unlocked here
#         else:
#             st.error("Please answer all questions before submitting.")

#     # Check if 3 seconds have passed to unlock the next group
#     if st.session_state.analysis_complete_time and step < 3:
#         elapsed_time = time.time() - st.session_state.analysis_complete_time
#         if elapsed_time >= 3:
#             st.session_state.next_group_unlocked = True

#     # Display the "Next Group" button
#     if st.session_state.next_group_unlocked and st.session_state.step < 3:
#         st.button("Next Group", on_click=next_group)

#     # Final result
#     if step == 3 and st.session_state.progress == total_questions:
#         st.subheader("Final Result")
#         st.write("Based on your answers to all questions, here is the final analysis:")
#         final_context = "\n".join([
#             f"Step {i}: " + ", ".join([
#                 f"Q{j}: {st.session_state.responses[f'step_{i}_q{j}']}"
#                 for j in range(1, len(questions_group[i]) + 1)
#             ])
#             for i in range(1, 4)
#         ])
#         final_result = ask_openai(
#             "Provide a final analysis of the applicant's eligibility for a protection visa based on all steps.",
#             final_context
#         )
#         st.write(final_result)

# if __name__ == "__main__":
#     main()


# Good Version

# import streamlit as st
# from typing import List, Dict
# import requests
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Load OpenAI API Key
# OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY not found in environment variables")

# # OpenAI interface
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

# def ask_openai(question: str, context: str) -> str:
#     interface = st.session_state.openai_interface
#     conversation = [
#         {"role": "system", "content": "You are a legal assistant specializing in Australian protection visa cases. Use the provided context and respond with probability estimates."},
#         {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
#     ]
#     return interface.generate_chat_response(conversation)

# # Streamlit application
# def main():
#     st.set_page_config(page_title="Protection Visa Assistant", page_icon="🛡️", layout="wide")
#     st.title("🛡️ Australian Protection Visa Assistant")

#     # Initialize OpenAI interface
#     if 'openai_interface' not in st.session_state:
#         st.session_state.openai_interface = OpenAIInterface()

#     # Initialize session state
#     if 'responses' not in st.session_state:
#         st.session_state.responses = {}
#     if 'progress' not in st.session_state:
#         st.session_state.progress = 0
#     if 'analysis' not in st.session_state:
#         st.session_state.analysis = {}
#     if 'current_step' not in st.session_state:
#         st.session_state.current_step = 1  # Start from step 1

#     # Predefined legal guidance
#     st.subheader("Guidance for Australian Protection Visa")
#     st.write("""
#     Protection visas apply to individuals who need protection in Australia because they face real risks of significant harm or persecution if they return to their home country. Answer the questions below to determine your eligibility.
#     """)

#     # Questions split into groups
#     questions_group = {
#         1: [
#             "Are you a refugee or at risk of significant harm if you return to your home country?",
#             "Can you legally settle in another country (not your home country) with safety guaranteed?",
#             "Do you have a well-founded fear of persecution, making you unable or unwilling to return to your home country?",
#             "Do you fear persecution based on race, religion, nationality, membership in a particular social group, or political opinion?"
#         ],
#         2: [
#             "Does persecution involve serious harm or systematic, discriminatory conduct?",
#             "Do you face real risk of persecution in all areas of your home country?",
#             "Does serious harm include threats to life or freedom?",
#             "Does serious harm include severe physical harassment or abuse?"
#         ],
#         3: [
#             "Does serious harm include severe economic hardship threatening survival?",
#             "Does serious harm require you to alter or hide your beliefs, identity, or practices (e.g., religion, sexuality)?",
#             "Can your home country's government or any controlling group protect you from persecution?",
#             "Does significant harm risk include torture, inhumane treatment, or punishment?"
#         ]
#     }

#     # Sidebar progress bar
#     total_questions = sum(len(questions) for questions in questions_group.values())
#     progress_percentage = int((st.session_state.progress / total_questions) * 100)
#     st.sidebar.header("Progress")
#     st.sidebar.progress(progress_percentage)

#     # Display questions and handle submissions for each group
#     for step in range(1, 4):
#         st.subheader(f"Step {step}: Questions")

#         # Disable the group if the previous group has not been submitted
#         group_disabled = step > st.session_state.current_step

#         # Container for the group's questions
#         with st.container():
#             # Display questions for the current group
#             for idx, question in enumerate(questions_group[step], 1):
#                 key = f"step_{step}_q{idx}"
#                 if key not in st.session_state.responses:
#                     st.session_state.responses[key] = "Select an option"

#                 options = ["Select an option", "Yes", "No"]
#                 current_value = st.session_state.responses[key]
#                 index = options.index(current_value) if current_value in options else 0

#                 # Disable the input if the group is disabled
#                 st.session_state.responses[key] = st.radio(
#                     f"{idx}. {question}",
#                     options,
#                     key=key,
#                     index=index,
#                     disabled=group_disabled
#                 )

#             # Submit button for the current group
#             submit_button_key = f"submit_step_{step}"
#             if group_disabled:
#                 # Display a disabled submit button
#                 st.button(f"Submit Step {step}", key=submit_button_key, disabled=True)
#             else:
#                 if st.button(f"Submit Step {step}", key=submit_button_key):
#                     # Ensure all questions are answered
#                     if all(
#                         st.session_state.responses[f"step_{step}_q{idx}"] != "Select an option"
#                         for idx in range(1, len(questions_group[step]) + 1)
#                     ):
#                         # Compile context for current step
#                         context = "\n".join([
#                             f"{question} | Answer: {st.session_state.responses[f'step_{step}_q{idx}']}"
#                             for idx, question in enumerate(questions_group[step], 1)
#                         ])
#                         with st.spinner("Analyzing your responses..."):
#                             result = ask_openai(
#                                 "Based on these responses, what is the probability of meeting protection visa requirements?",
#                                 context
#                             )
#                         st.success("Analysis complete!")
#                         st.write(result)

#                         # Save analysis result
#                         st.session_state.analysis[step] = result

#                         # Update progress and current step
#                         st.session_state.progress += len(questions_group[step])
#                         st.session_state.current_step += 1  # Allow next group to be filled
#                     else:
#                         st.error("Please answer all questions before submitting.")

#         # Display the analysis result if available
#         if step in st.session_state.analysis:
#             st.markdown(f"**Analysis for Step {step}:**")
#             st.write(st.session_state.analysis[step])

#     # Final result after all steps are completed
#     if st.session_state.current_step > 3:
#         st.subheader("Final Result")
#         st.write("Based on your answers to all questions, here is the final analysis:")
#         final_context = "\n".join([
#             f"Step {i}: " + ", ".join([
#                 f"Q{j}: {st.session_state.responses[f'step_{i}_q{j}']}"
#                 for j in range(1, len(questions_group[i]) + 1)
#             ])
#             for i in range(1, 4)
#         ])
#         final_result = ask_openai(
#             "Provide a final analysis of the applicant's eligibility for a protection visa based on all steps.",
#             final_context
#         )
#         st.write(final_result)

# if __name__ == "__main__":
#     main()


# ============ New version with text input
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

def ask_openai(question: str, context: str = "") -> str:
    # Helper function to interact with OpenAI
    interface = st.session_state.openai_interface
    conversation = [
        {"role": "system", "content": "You are a legal assistant specializing in Australian protection visa cases."},
    ]
    if context:
        conversation.append({"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"})
    else:
        conversation.append({"role": "user", "content": f"Question: {question}"})
    return interface.generate_chat_response(conversation)

# Main Streamlit application
def main():
    st.set_page_config(page_title="Protection Visa Assistant", page_icon="🛡️", layout="wide")
    st.title("🛡️ Australian Protection Visa Assistant")

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

    # Initial AI explanation (additional AI call)
    if 'initial_explanation' not in st.session_state:
        with st.spinner("Preparing assistant..."):
            explanation = ask_openai("Explain the purpose of this assistant and how it works.")
        st.write(explanation)
        st.session_state.initial_explanation = explanation  # Store to prevent re-calling

    # Questions split into groups
    questions_group = {
        1: [
            "Are you a refugee or at risk of significant harm if you return to your home country?",
            "Can you legally settle in another country (not your home country) with safety guaranteed?",
            "Do you have a well-founded fear of persecution, making you unable or unwilling to return to your home country?",
            "Do you fear persecution based on race, religion, nationality, membership in a particular social group, or political opinion?"
        ],
        2: [
            "Does persecution involve serious harm or systematic, discriminatory conduct?",
            "Do you face real risk of persecution in all areas of your home country?",
            "Does serious harm include threats to life or freedom?",
            "Does serious harm include severe physical harassment or abuse?"
        ],
        3: [
            "Does serious harm include severe economic hardship threatening survival?",
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
    for step in range(1, 4):
        st.subheader(f"Step {step}: Questions")

        # Disable the group if the previous group has not been submitted
        group_disabled = step > st.session_state.current_step

        # Container for the group's questions
        with st.container():
            # Display questions for the current group
            for idx, question in enumerate(questions_group[step], 1):
                key = f"step_{step}_q{idx}"
                if key not in st.session_state.responses:
                    st.session_state.responses[key] = "Select an option"

                options = ["Select an option", "Yes", "No"]
                current_value = st.session_state.responses[key]
                index = options.index(current_value) if current_value in options else 0

                # Disable the input if the group is disabled
                st.session_state.responses[key] = st.radio(
                    f"{idx}. {question}",
                    options,
                    key=key,
                    index=index,
                    disabled=group_disabled
                )

            # Submit button for the current group
            submit_button_key = f"submit_step_{step}"
            if group_disabled:
                # Display a disabled submit button
                st.button(f"Submit Step {step}", key=submit_button_key, disabled=True)
            else:
                if st.button(f"Submit Step {step}", key=submit_button_key):
                    # Ensure all questions are answered
                    if all(
                        st.session_state.responses[f"step_{step}_q{idx}"] != "Select an option"
                        for idx in range(1, len(questions_group[step]) + 1)
                    ):
                        # Compile context for current step
                        context = "\n".join([
                            f"{question} | Answer: {st.session_state.responses[f'step_{step}_q{idx}']}"
                            for idx, question in enumerate(questions_group[step], 1)
                        ])
                        with st.spinner("Analyzing your responses..."):
                            result = ask_openai(
                                "Based on these responses, what is the probability of meeting protection visa requirements?",
                                context
                            )
                        st.success("Analysis complete!")
                        st.write(result)

                        # Save analysis result
                        st.session_state.analysis[step] = result

                        # Update progress and current step
                        st.session_state.progress += len(questions_group[step])
                        st.session_state.current_step += 1  # Allow next group to be filled
                    else:
                        st.error("Please answer all questions before submitting.")

        # Display the analysis result if available
        if step in st.session_state.analysis:
            st.markdown(f"**Analysis for Step {step}:**")
            st.write(st.session_state.analysis[step])

    # After all steps are completed, optional text input and final analysis
    if st.session_state.current_step > 3:
        st.subheader("Additional Information (Optional)")
        user_story = st.text_area("Please provide any additional details about your circumstances that may be relevant to your protection visa application. (Optional)", "")

        # Add a button to submit the final analysis
        if st.button("Get Final Analysis"):
            # Compile the full context
            final_context = "\n".join([
                f"Step {i}: " + ", ".join([
                    f"Q{j}: {st.session_state.responses[f'step_{i}_q{j}']}"
                    for j in range(1, len(questions_group[i]) + 1)
                ])
                for i in range(1, 4)
            ])
            if user_story.strip():
                final_context += f"\n\nAdditional Information:\n{user_story}"

            st.subheader("Final Result")
            st.write("Based on your answers to all questions and the additional information provided, here is the final analysis:")

            with st.spinner("Generating final analysis..."):
                final_result = ask_openai(
                    "Provide a comprehensive analysis of the applicant's eligibility for a protection visa based on all steps and the additional information.",
                    final_context
                )
            st.write(final_result)

            # Store the final result
            st.session_state.final_result = final_result

    # Display the final result if already generated
    if 'final_result' in st.session_state:
        st.subheader("Final Result")
        st.write(st.session_state.final_result)

if __name__ == "__main__":
    main()
