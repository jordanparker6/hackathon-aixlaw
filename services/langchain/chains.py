from typing import List
import re
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import HumanMessagePromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from services.langchain.templates import CRITISM_SYSTEM_PROMPT, DRAFTING_PROMPT, RECONSTRUCTION_PROMPT
from langchain_experimental.plan_and_execute.schema import Plan, PlanOutputParser

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
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



def load_critisim_planner(llm, verbose=False) -> LLMPlanner:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=CRITISM_SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt_template
    )
    return LLMPlanner(
        llm_chain=llm_chain,
        output_parser=PlanningOutputParser(),
        stop=["<END_OF_PLAN>"],
    )

    
def load_redrafting_chain(llm):
    prompt = PromptTemplate.from_template(DRAFTING_PROMPT)
    chain = LLMChain(
        llm=llm,
        prompt=prompt
    )
    return chain

def load_reconstruction_chain(llm):
    prompt = PromptTemplate.from_template(RECONSTRUCTION_PROMPT)
    chain = LLMChain(
        llm=llm,
        prompt=prompt
    )
    return chain