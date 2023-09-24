import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os
import base64
from services.langchain.chains import load_critisim_chain
from dotenv import load_dotenv    
load_dotenv()

def pdf_to_markdown(pdf_file):
    doc = fitz.open(pdf_file)
    print(doc)
    markdown_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        markdown_text += page.get_text("text")

    return markdown_text

st.markdown("## 404 Not[:red] Found")

# Upload a PDF file
pdf_file = st.file_uploader("404 Not Found", type=["pdf"])

if pdf_file is not None:
    # Display the uploaded PDF
    # st.subheader("Uploaded PDF:")
    # st.write(pdf_file)

    # Create a temporary file for the uploaded PDF
    pdf_temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_temp_file.write(pdf_file.read())
    pdf_temp_file.close()

    # Process the PDF file
    markdown_text = pdf_to_markdown(pdf_temp_file.name)

    # Display the Markdown text
    st.subheader("Markdown Output:")
    st.text(markdown_text)


    chain = load_critisim_chain()
    output = chain.run(markdown_text)

    critisims = output.split("\n\n")

    for critism in critisims:
        st.write(critism)

    # Provide a download link for the uploaded PDF
    # st.markdown("### Download Uploaded PDF")
    # st.markdown(f"Download the uploaded PDF [here](data:application/pdf;base64,{base64.b64encode(open(pdf_temp_file.name, 'rb').read()).decode()})")

    # Create a temporary file for the generated Markdown
    markdown_temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".md")
    markdown_temp_file.write(markdown_text.encode())
    markdown_temp_file.close()

    # Provide a download link for the generated Markdown
    # st.markdown("### Download Markdown")
    # st.markdown(f"Download the generated Markdown [here](data:file/md;base64,{base64.b64encode(open(markdown_temp_file.name, 'rb').read()).decode()})")

    # Remove the temporary files
    os.unlink(pdf_temp_file.name)
    os.unlink(markdown_temp_file.name)
