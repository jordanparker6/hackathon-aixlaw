from typing import List
import re
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.pydantic_v1 import BaseModel, Field, validator
from services.langchain.templates import SYSTEM_PROMPT
#from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser
from langchain.output_parsers import PydanticOutputParser
from langchain_experimental.plan_and_execute.schema import Plan, PlanOutputParser

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema.language_model import BaseLanguageModel
from langchain.schema.messages import SystemMessage

from langchain_experimental.plan_and_execute.planners.base import LLMPlanner
from langchain_experimental.plan_and_execute.schema import (
    Plan,
    PlanOutputParser,
    Step,
)




class Critisim(BaseModel):
    """
    A critisim of a security policy document.
    """

    critisim: str = Field(..., description="The critisim of the policy document in reference to context from the document. This should be in answer to the system prompt")
    context: List[str] = Field(
        ...,
        description=(
            "The context for the critisim."
        ),
    )

class PlanningOutputParser(PlanOutputParser):
    """Planning output parser."""

    def parse(self, text: str) -> Plan:
        steps = [Step(value=v) for v in re.split("\n\s*\d+\. ", text)[1:]]
        return Plan(steps=steps)



def load_critisim_chain(verbose=True):
    """Loads a critizim chat chain."""
    messages = [
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
    prompt = ChatPromptTemplate.from_messages(messages)
    # output_parser = PydanticOutputParser(pydantic_object=CritisimList)
    return LLMChain(
        llm=ChatOpenAI(model_name="gpt-4", verbose=verbose), 
        prompt=prompt, 
        output_key="output", 
        verbose=verbose,
        # output_parser=output_parser,
    )

def load_chat_planner(
    llm: BaseLanguageModel, system_prompt: str = SYSTEM_PROMPT
) -> LLMPlanner:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt_template)
    return LLMPlanner(
        llm_chain=llm_chain,
        output_parser=PlanningOutputParser(),
        stop=["<END_OF_PLAN>"],
    )

def load_action_chain():
    """Load an action chain."""




    
