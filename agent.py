import dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain.agents import create_agent
from langchain_tavily import TavilySearch

dotenv.load_dotenv()

search_tool = TavilySearch(max_results=1)


def get_weather(city):
    '''get the weather of a city. 
      Args:
        city: a city name
    '''
    return {'city': city, 'weather': 'sunny, 22C'}


class Agent:
    def __init__(self):
        self.llm = ChatGroq(model='openai/gpt-oss-20b', temperature=0.5)
        self.messages = [
            SystemMessage(
                'Answer the given questions, and use the provided tools whenever needed. provide concise answers.')
        ]
        self.agent = create_agent(
            model=self.llm,
            tools=[get_weather, search_tool]
        )

    def chat_loop(self):
        while True:
            user_input = input(
                'Ask something (type "q" to terminate): ').strip().lower()

            if user_input == 'q':
                print('Good Luck')
                break

            self.messages.append(HumanMessage(user_input))

            response = self.agent.invoke({'messages': self.messages})

            self.messages.append(response['messages'][-1])
            print(response['messages'][-1].content)


def main():
    agent = Agent()
    agent.chat_loop()


if __name__ == '__main__':
    main()
