from services.langchain.agents import load_plan_and_execute
from dotenv import load_dotenv

load_dotenv()


with open("markdown/sample.md") as f:
    SAMPLE_DOCUMENT = f.read()

agent = load_plan_and_execute(context=SAMPLE_DOCUMENT, verbose=True)
output = agent.run({ "input": SAMPLE_DOCUMENT })

print(output)