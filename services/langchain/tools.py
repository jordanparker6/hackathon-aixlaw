from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from services.langchain.chains import load_redrafting_chain


def load_tools():

    chain = load_redrafting_chain(ChatOpenAI(model_name="gpt-4", verbose=True))
    
    return [
        Tool.from_function(
            func=chain.run,
            name="Draft",
            description="useful for when you need to redraft a document in reponse to critism"
        )
    ]
