from services.langchain.chains import load_chain
from dotenv import load_dotenv

load_dotenv()

chain = load_chain()
with open("markdown/sample.md") as f:
    SAMPLE_DOCUMENT = f.read()

output = chain.run(SAMPLE_DOCUMENT)


print(output)