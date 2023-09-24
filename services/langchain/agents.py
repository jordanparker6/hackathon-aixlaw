from langchain.chat_models import ChatOpenAI
from services.langchain.pande import PlanAndExecute
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor
from services.langchain.chains import load_critisim_planner
from services.langchain.tools import load_tools


def load_plan_and_execute(verbose=False):
    llm = ChatOpenAI(model_name="gpt-4", verbose=verbose)

    tools = load_tools()
    planner = load_critisim_planner(llm=llm)
    executor = load_agent_executor(llm, tools, verbose=True)

    agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
    return agent