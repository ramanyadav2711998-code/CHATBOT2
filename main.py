from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

model=ChatMistralAI( model="mistral-large-latest",
    temperature=0.7,                
    max_retries=2,)
message = [
    SystemMessage("You are a helpful assistant."),
    HumanMessage("who is virat kholi"),
]
response = model.invoke(message)

print(response.content)