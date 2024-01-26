import os
import streamlit as st
import textwrap
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

def main():
    st.title("Gemini AI Explorer")

    model_names = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = st.selectbox("Choose a model", model_names)
    model = genai.GenerativeModel(model_name)

    prompt = st.text_input("Enter a prompt for the model:", "What is the meaning of life?")

    if st.button("Generate"):
        with st.spinner("Generating content..."):
            response = model.generate_content(prompt)

            with st.expander(prompt, expanded=True):
                st.markdown(to_markdown(response.text), unsafe_allow_html=True)

if __name__ == "__main__":
    main()