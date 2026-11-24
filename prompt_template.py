import os
import dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

dotenv.load_dotenv()

class User(BaseModel):
    name: str = Field(description='the name of the user')
    age: int= Field(description='the age of the user')
    companies: list[str] = Field(description='the companies associated with the user')
    net_worth: str = Field(description='the net worth of the user')


class Agent:
    def __init__(self):
        self.llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.1)

    def chat(self):
        structured_llm = self.llm.with_structured_output(User, method='json_schema')
        response = structured_llm.invoke('Elon Reeve Musk (/ˈiːlɒn/ ⓘ EE-lon; born June 28, 1971) is a businessman and former public official who is the CEO and largest shareholder of Tesla and SpaceX. Musk has been the wealthiest person in the world since 2025, and briefly became the only trillionaire (in terms of US dollars) in June 2026; as of August 14, 2026, Forbes estimates his net worth to be US$864 billion.')

        print(response)





        

        
        


        
        
        


def main():

    agent = Agent()
    agent.chat()


if __name__ == '__main__':
    main()
