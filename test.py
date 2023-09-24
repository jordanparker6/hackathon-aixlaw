from services.langchain.chains import load_critisim_planner, load_redrafting_chain
from langchain.chat_models import ChatOpenAI
from rich import print

llm = ChatOpenAI(model_name="gpt-4")
planner = load_critisim_planner(llm=llm)
drafter = load_redrafting_chain(llm=llm)

with open("markdown/sample.md") as f:
    SAMPLE_DOCUMENT = f.read()

plan = planner.plan({ "input": SAMPLE_DOCUMENT })

for step in plan.steps:
    print("**Critisim:**", step.value)
    output = drafter({ "critisim": step.value, "context": SAMPLE_DOCUMENT })
    print("Revision:", output["text"])