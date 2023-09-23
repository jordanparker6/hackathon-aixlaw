from services.langchain.agents import load_plan_and_execute
from dotenv import load_dotenv

load_dotenv()

agent = load_plan_and_execute(verbose=True)
with open("markdown/sample.md") as f:
    SAMPLE_DOCUMENT = f.read()

output = agent.run({ "input": SAMPLE_DOCUMENT })

print(output)