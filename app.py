import streamlit as st
import fitz  # PyMuPDF
import tempfile
import structlog
from services.langchain.agents import load_plan_and_execute
from dotenv import load_dotenv    
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from services.langchain.chains import load_critisim_planner, load_redrafting_chain
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

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")


pdf_file = st.file_uploader("404 Not Found", type=["pdf"])
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    chat_memory=msgs, return_messages=True, memory_key="chat_history", output_key="output"
)

if len(msgs.messages) == 0 or st.sidebar.button("Reset chat history"):
    msgs.clear()
    st.session_state.steps = {}

# avatars = {"human": "user", "ai": "assistant"}
# for idx, msg in enumerate(msgs.messages):
#     with st.chat_message(avatars[msg.type]):
#         # Render intermediate steps if any were saved
#         for step in st.session_state.steps.get(str(idx), []):
#             log.info("step", step=step)
#             if step[0].tool == "_Exception":
#                 continue
#             query = step[0].tool_input["query"]
#             with st.status(label=f"**Critisim**: {query}", state="running"):
#                  st.write("running")
#             with st.status(label=f"**Critisim**: {query}", expanded=True, state="complete"):
#                 st.write(step)
#                 # st.write(step[0].log)
#                 # if step[1].get("completion"):
#                 #     st.write(step[1]["completion"])
#                 # else:
#                 #     st.write(step[1])
#         print(msg.content)
#         st.write(msg.content)

if pdf_file is not None:
    # st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    #markdown_text = pdf_to_markdown(pdf_file)
    with open("markdown/sample.md") as f:
        markdown_text = f.read()

    # agent = load_plan_and_execute(context=markdown_text, model_name="gpt-3.5-turbo-16k", verbose=False)

    llm = ChatOpenAI(model_name="gpt-4")
    planner = load_critisim_planner(llm=llm)
    drafter = load_redrafting_chain(llm=llm)
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
