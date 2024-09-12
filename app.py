import streamlit as st
import requests

st.title("Medical Question Answering System")

question = st.text_input("Enter your medical question:")

if st.button("Get Answer"):
    if question:
        response = requests.post("http://localhost:8000/AnswerGenerator", json={"question": question})
        if response.status_code == 200:
            answer = response.json().get("answer", "No answer generated.")
            st.write(f"**Answer**: {answer}")
        else:
            st.write("Error in fetching the answer. Please try again.")
    else:
        st.write("Please enter a question.")
