from langchain.tools import Tool
from langchain.tools.base import BaseTool
from langchain.chat_models import ChatOpenAI
from services.langchain.chains import load_redrafting_chain


def load_tools(context):

    chain = load_redrafting_chain(ChatOpenAI(model_name="gpt-4", verbose=True))

    class DraftingTool(BaseTool):
        name = "drafting_tool"
        description = "useful for when you need to redraft a document in reponse to critism"

        def _run(
            self, query: str, run_manager
        ) -> str:
            """Use the tool."""
            return chain({ "critisim": query, "context": context})
    
    return [
        DraftingTool()
    ]
