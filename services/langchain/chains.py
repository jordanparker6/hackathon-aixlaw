from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from services.langchain.templates import SYSTEM_PROMPT

def load_chain(verbose=True):
    """Loads a vanila chat chain."""
    messages = [
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
    prompt = ChatPromptTemplate.from_messages(messages)
    return LLMChain(
        llm=ChatOpenAI(model_name="gpt-4", verbose=verbose), 
        prompt=prompt, 
        output_key="output", 
        verbose=verbose
    )