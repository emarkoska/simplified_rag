import os, os.path
import shutil
import pathlib
import streamlit as st
from simplified_rag.RAG import generate_answer

st.title("Can AI replace the MPC?")
st.header("\n Probably not, but let's try.")

if 'selection' not in st.session_state:
    st.session_state.selection = ""

# clearing previously loaded pool of docs
target_folder = pathlib.Path().absolute()  / "docs/"

if target_folder.exists():
    shutil.rmtree(target_folder)
target_folder.mkdir(parents=True, exist_ok=True)

# activating selection box for user choice 
options = False
emp = st.empty()
vari = emp.selectbox(
    key = "Options",
    label = "Please select the option for query running:",
    options = ("Nov 2024 MPC Report", " ")
)

if st.button("Select"):
    choice = vari
    options = True


def research_choice() -> str:
    
    with st.form(key="doc_upload", clear_on_submit=False):

        uploaded_doc = st.file_uploader(
            label="Please upload your document",
            accept_multiple_files = False,
            type=['pdf']
        )
        research_query = st.text_input(
            label = "Input your question for the AI-MPC",
            max_chars = 256
        )
        submit_button1 = st.form_submit_button("Load Document")

    if submit_button1:
        with open(os.path.join(target_folder, uploaded_doc.name), 'wb') as f:
            f.write(uploaded_doc.getbuffer())
        return research_query


def main(selection):
    if selection == "Nov 2024 MPC Report":
        research_query = research_choice()

        if research_query is not None:
            with st.spinner("Processing your request..."):
                answer = generate_answer(selection, research_query)

                st.success("Data processing complete!")
                st.write(answer['result'])

if __name__ == "__main__":
    if options:
        st.session_state.selection = choice

    main(st.session_state.selection)
