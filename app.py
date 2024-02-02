import os
import streamlit as st
import textwrap
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

def load_image_from_file_uploader(uploaded_file):
    image_bytes = uploaded_file.getvalue()
    image_part = {
        'mime_type': uploaded_file.type,
        'data': image_bytes
    }
    return image_part

def main():
    st.title("Gemini AI Explorer")

    model_names = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    default_model_index = 1 if len(model_names) > 1 else 0 
    model_name = st.selectbox("Choose a model", model_names, index=default_model_index)
    model = genai.GenerativeModel(model_name)

    is_vision_model = model_name == "models/gemini-pro-vision"

    prompt_label = "Describe these images:" if is_vision_model else "Enter a prompt for the model:"
    prompt = st.text_input("Enter a prompt for the model:", prompt_label)

    images = None
    if is_vision_model:
        images = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if st.button("Generate"):
        with st.spinner("Generating content..."):
            if is_vision_model and images:
                parts = []
                for image in images:
                    image_part = load_image_from_file_uploader(image)
                    parts.append({'inline_data': image_part})
                
                parts.append({'text': prompt})
                content = {'parts': parts}
            else:
                content = prompt

            response = model.generate_content(content)

            with st.expander(prompt, expanded=True):
                st.markdown(to_markdown(response.text), unsafe_allow_html=True)

if __name__ == "__main__":
    main()