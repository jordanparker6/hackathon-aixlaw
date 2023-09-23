# ICT Security Policy Compliance App
# ---------------------
# This app uses the HelpMeFindLaw API to build an AutoGPT style agent the 
# completes legal research prior to attempting to draft any clauses for
# a end user.

# ---- app ------------

from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

SYSTEM_PROMPT = """
Using the following examples please provide a criticism of my current cybersecurity policy :
```
RESPONSIBILITIES
The following are the principal recurring responsibilities of the Cybersecurity Committee. 
1. Information Technology and Network Systems. The Cybersecurity Committee shall oversee
the quality and effectiveness of the Company’s policies and procedures with respect to its
information technology and network systems, including encryption, network security and data
security, as well as access to such systems.
2. IT/Engineering Security Funding. The Cybersecurity Committee shall oversee the Company’s
information technology senior management team relating to budgetary priorities based, in part, on
assessing risk associated with various perceived threats.
3. Incident Response. The Cybersecurity Committee shall review and provide oversight on the
policies and procedures of the Company in preparation for responding to any data security
incidents.
4. Disaster Recovery. The Cybersecurity Committee shall review periodically with management the
Company’s disaster recovery, business continuity, and business resiliency capabilities.
5. Compliance Risks and Audits. The Cybersecurity Committee shall oversee the Company’s
management of internal and external risks related to its information technology systems and 
processes, including encryption, network security, data security, risk management frameworks,
and any internal or third party audits of such systems and processes.
6. Access Controls. The Cybersecurity Committee shall review with management the quality and
effectiveness of IT systems and processes that relate to the Company’s internal access control
systems, including physical, organizational, and technical security.
7. Cyber Insurance. The Cybersecurity Committee shall review the Company’s cyber insurance
policies to ensure appropriate coverage.
8. Product Security. The Cybersecurity Committee shall review periodically with management the
risks related to the security of and access to customer data through use of the Company’s products
and services.



The Committee shall be responsible for the following: 
1. Data Governance – To provide oversight of policies, procedures, plans, and execution intended to provide security, confidentiality, availability, and integrity of the information. 
2. Information Technology Systems – To oversee the quality and effectiveness of the Company’s policies and procedures with respect to its information technology systems, including privacy, network security and data security. 
3. Incident Response – To review and provide oversight on the policies and procedures of the Company in preparation for responding to any material incidents. 
4. Disaster Recovery – To review periodically with management the Company’s disaster recovery capabilities. 
5. Compliance Risks and Internal Audits – To oversee the Company’s management of risks related to its information technology systems and processes, including privacy, network security and data security, and any internal audits of such systems and processes. 
6. Periodic and Annual Reports – To review and oversee the preparation of the Company’s disclosures in its reports filed with the Securities and Exchange Commission relating to the Company’s information technology systems, including privacy, network security, and data security. 
7. IT/Engineering Security Budget – To oversee the Company’s information technology senior management team relating to budgetary priorities based, in part, on assessing risk associated with various perceived threats. 
8. Advisory Role – To review the Company’s information technology strategy or programs relating to new technologies, applications, and systems. 
9. General Authority – To perform such other functions and to have such powers as may be necessary or appropriate in the efficient and lawful discharge of the foregoing.


The Cybersecurity Subcommittee (the “Subcommittee”) of the Audit Committee (the “Committee”) of the Board of Directors of UMH Properties, Inc. (the “Company”) is established to assist the Committee in
fulfilling its oversight responsibilities with respect to the Company’s cybersecurity risks. Company
management is responsible for the preparation, presentation, and self-assessment of the Company’s
cybersecurity policies and practices. The Subcommittee shall be comprised of at least two independent
directors. The Subcommittee shall review and provide high level guidance on cybersecurity-related issues of importance to the Company, including but not limited to:
1. the Company’s cybersecurity policies, procedures, plans, and execution intended to provide
security, confidentiality, availability, and integrity of the information;
2. the Company’s cybersecurity risks, controls and procedures, including high level review of the
threat landscape facing the Company and the Company’s strategy to mitigate cybersecurity risks
and potential breaches, and to ensure legal and regulatory compliance;
3. the recovery and communication plans for any unplanned outage or security breach;
4. data management systems and processes, including security of the Company’s data repositories,
encryption practices, and third-party use of the Company’s customers’ data;
5. periodic reports to the Committee regarding Company systems and processes relating to
cybersecurity; and
6. periodic review of the Company’s IT staffing and cybersecurity employee training plan.


THE COMMITTEE SHALL Review and provide high level guidance on technology related issues of importance to the Company, including but not limited to: 
1. The Company’s technology landscape, competitive assessment and roadmap for future development. 2. The Company’s cybersecurity and other information technology (IT) risks, controls and procedures, including high level review of the threat landscape facing the Company and the Company’s strategy to mitigate cybersecurity risks and potential breaches. The Committee shall also review the recovery and communication plans for any unplanned outage or security breach. 
3. The Company’s technology planning processes to support its growth objectives as well as acquisitions and the system integrations required in support of such activities. 
4. The integrity of the Company’s IT Systems’ operational controls to ensure legal and regulatory compliance. 
5. Data Management Systems & Processes, including security of the Company’s data repositories (US and EU), encryption practices, and third party use of the Company’s customers’ data. 
6. Review the Company’s Cyber insurance policies, if applicable, to ensure appropriate coverage and that all insurance terms and conditions are being met. 
7. With the assistance of Company management, provide an IT Risk Assessment Report to the Board on an annual basis, including systems and processes relating to cybersecurity.
 8. Review the Company’s development and training plan for critical IT staff as well as succession planning and employee training of cybersecurity risks. The Committee shall have the authority to retain outside technical consultants or other appropriate advisors. The Company shall provide for appropriate funding, as determined by the Committee, for payment of compensation to such consultants. The Committee shall review and reassess the adequacy of this Charter periodically and recommend any proposed changes to the Board for approval.
```
"""

MESSAGE_PROMPT = """
My Policy Document: 
{input}
"""

def load_chain(verbose=True):
    """Loads a vanila chat chain."""
    messages = [
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template(MESSAGE_PROMPT),
    ]
    prompt = ChatPromptTemplate.from_messages(messages)
    return LLMChain(
        llm=ChatOpenAI(model_name="gpt-4", verbose=verbose), 
        prompt=prompt, 
        output_key="output", 
        verbose=verbose
    )

# ----- Streamlit -----

from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.tools import DuckDuckGoSearchRun
import streamlit as st

def handle_output(output):
    if isinstance(output, str):
        return output
    elif isinstance(output, dict):
        if output.get("completion"):
            return output["completion"]
    return output

st.set_page_config(page_title="HelpMeFindLaw\n\n BabyAGI For Contract Drafting", page_icon="🦜")
st.title("HelpMeFindLaw x Langchain 🦜")
st.subheader("AutoGPT For Contract Drafting")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    chat_memory=msgs, return_messages=True, memory_key="chat_history", output_key="output"
)
if len(msgs.messages) == 0 or st.sidebar.button("Reset chat history"):
    msgs.clear()
    msgs.add_ai_message("How can I help you?")
    st.session_state.steps = {}

avatars = {"human": "user", "ai": "assistant"}
for idx, msg in enumerate(msgs.messages):
    with st.chat_message(avatars[msg.type]):
        # Render intermediate steps if any were saved
        for step in st.session_state.steps.get(str(idx), []):
            if step[0].tool == "_Exception":
                continue
            with st.status(f"**{step[0].tool}**: {step[0].tool_input}", state="complete"):
                st.write(step)
                # st.write(step[0].log)
                # if step[1].get("completion"):
                #     st.write(step[1]["completion"])
                # else:
                #     st.write(step[1])
        st.write(msg.content)

if prompt := st.chat_input(placeholder="Draft a non-compete clause for an employment contract in Texas"):
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    model = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key, streaming=True)
    tools = [
        DuckDuckGoSearchRun(name="Search"),
        HelpMeFindlLawCompletionTool(client=client)
    ]
    planner = load_chat_planner(llm=model)
    executor = load_agent_executor(llm=model, tools=tools)
    agent = PlanAndExecute(planner=planner, executor=executor)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
        response = agent({ "input": prompt }, callbacks=[st_cb])

        output = response["output"]
        if isinstance(output, str):
            st.write(output)
        else:
            st.write(output["action_input"])
        if response.get("intermediate_steps"):
            st.session_state.steps[str(len(msgs.messages) - 1)] = response["intermediate_steps"]