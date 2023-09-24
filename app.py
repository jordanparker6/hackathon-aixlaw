import streamlit as st
import fitz  # PyMuPDF
import tempfile
import structlog
from dotenv import load_dotenv    
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from services.langchain.chains import load_critisim_planner, load_redrafting_chain, load_reconstruction_chain
from langchain.chat_models import ChatOpenAI
from rich import print

load_dotenv()

log = structlog.get_logger("app.main")

def pdf_to_markdown(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
    doc = fitz.open(pdf_file)
    print(doc)
    markdown_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        markdown_text += page.get_text("text")
    return markdown_text

#st.set_page_config(page_title="404 Not Found", page_icon="🦜")
st.title("404")
st.subheader(":red[Not] Found")
st.markdown("Reviewing your organisations ICT Security Policy for compliance review and recommendations")
st.markdown("SEC Regulation S-K Item 106 - Information Security Controls")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")


pdf_file = st.file_uploader("Upload your organisations ICT Security Policy for compliance review and recommendations", type=["pdf"])
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    chat_memory=msgs, return_messages=True, memory_key="chat_history", output_key="output"
)

if len(msgs.messages) == 0 or st.sidebar.button("Reset chat history"):
    msgs.clear()
    st.session_state.steps = {}

if pdf_file is not None:

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    #markdown_text = pdf_to_markdown(pdf_file)
    with open("markdown/sample.md") as f:
        markdown_text = f.read()

    llm = ChatOpenAI(model_name="gpt-4")
    planner = load_critisim_planner(llm=llm)
    drafter = load_redrafting_chain(llm=llm)
    reconstruct = load_reconstruction_chain(llm=llm)
    with st.status(label="**Reviewing Document and Formulating Critisim**", state="running"):
        plan = planner.plan({ "input": markdown_text })
    print("Critisim Complete")

    revisions = []

    for plan in plan.steps:
        with st.status(label=f"**Critisim**: {plan.value}", state="running") as status:
            output = drafter({ "critisim": plan.value, "context": markdown_text })
            revision = output["text"]
            revisions.append(revision)
            status.write(f"Revised Text \n\n {revision}")
        
    with st.status(label="**Reconstructing Document**", state="running"):
        revision = "\n\n".join(revisions)
        reconstruction = reconstruct({ "revision": revisions, "context": markdown_text })
        st.write(reconstruction["output"])
