def main():
    st.set_page_config(page_title="Protection Visa Eligibility Assistant", page_icon="🛡️", layout="wide")
    st.title("🛡️ Protection Visa Eligibility Assistant")

    if 'vector_db' not in st.session_state:
        st.session_state.vector_db = VectorDatabase()

    if 'openai_interface' not in st.session_state:
        st.session_state.openai_interface = OpenAIInterface()

    if 'eligibility_data' not in st.session_state:
        st.session_state.eligibility_data = {}

    # User Input Section
    st.header("Step 1: Provide Information")
    st.subheader("Eligibility Questionnaire")

    # Step 1: Basic Protection Questions
    question1 = st.radio(
        "1. Are you a refugee or at risk of significant harm if you return to your home country?",
        ["Yes", "No"]
    )
    question2 = st.radio(
        "2. Can you legally settle in another country where you will be safe?",
        ["Yes", "No"]
    )
    question3 = st.radio(
        "3. Do you fear persecution for reasons such as race, religion, nationality, or political opinion?",
        ["Yes", "No"]
    )

    # Step 2: Additional Details
    st.subheader("Additional Information")
    persecution_details = st.text_area("Describe the risks you face in your home country.")
    uploaded_file = st.file_uploader("Upload any supporting documents (optional)", type=["txt", "docx"])

    # Store data
    st.session_state.eligibility_data = {
        "question1": question1,
        "question2": question2,
        "question3": question3,
        "persecution_details": persecution_details,
    }

    # Document Processing (if uploaded)
    if uploaded_file:
        if uploaded_file.type == "text/plain":
            document = uploaded_file.getvalue().decode("utf-8")
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            document = read_docx(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a .txt or .docx file.")
            return

        chunks = chunk_document(document)
        st.session_state.vector_db.add_documents(chunks)
        st.success(f"✅ {uploaded_file.name} processed and added to vector database!")

    # Analysis and Output
    if st.button("Analyze Eligibility"):
        with st.spinner("Analyzing your eligibility..."):
            # Combine user input and optional document context
            context = st.session_state.eligibility_data["persecution_details"]
            if uploaded_file:
                relevant_chunks = st.session_state.vector_db.search(context)
                context += "\n".join(relevant_chunks)

            # Generate AI analysis
            prompt = f"""
            Context: {context}
            Questionnaire Responses:
            1. Are you a refugee or at risk? {question1}
            2. Can you legally settle in another country? {question2}
            3. Do you fear persecution for specific reasons? {question3}

            Based on this information, provide an analysis of the individual's eligibility for a protection visa.
            """
            conversation = [
                {"role": "system", "content": "You are an AI assistant analyzing eligibility for a protection visa based on the user's input and provided context."},
                {"role": "user", "content": prompt}
            ]
            response = st.session_state.openai_interface.generate_chat_response(conversation)

            # Display response
            st.subheader("Eligibility Analysis Result")
            st.markdown(response)

if __name__ == "__main__":
    main()
