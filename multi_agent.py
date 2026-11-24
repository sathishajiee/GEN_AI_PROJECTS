import dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent

dotenv.load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.2)


def fruit_info(fruit_name: str) -> str:
    """Look up info about a fruit."""
    facts = {
        "tomato": "Botanically a fruit (it develops from a flower and has seeds), "
        "but commonly treated as a vegetable in cooking.",
        "apple": "A pome fruit, related to roses. High in fiber and vitamin C.",
    }
    return facts.get(fruit_name.lower(), f"No specific info found for {fruit_name}.")


def veggie_info(veggie_name: str) -> str:
    """Look up info about a vegetable."""
    facts = {
        "carrot": "A root vegetable, high in beta-carotene (vitamin A).",
        "potato": "A starchy tuber vegetable, a staple food in many cuisines.",
    }
    return facts.get(veggie_name.lower(), f"No specific info found for {veggie_name}.")


fruit_agent = create_agent(
    model=llm,
    tools=[fruit_info],
    system_prompt='You are a fruit expert. Respond in one sentence.'
)

veggie_agent = create_agent(
    model=llm,
    tools=[veggie_info],
    system_prompt='You are a veggie expert. Respond in one sentence.'
)

def ask_fruit_expert(question: str) -> str:
    '''Ask the fruit expert. Use for ALL fruit questions'''
    response = fruit_agent.invoke({'messages': [{'role': 'user', 'content': question}]})
    return response['messages'][-1].content

def ask_veggie_expert(question: str) -> str:
    '''Ask the veggie expert. Use for ALL veggie questions'''
    response = veggie_agent.invoke({'messages': [{'role': 'user', 'content': question}]})
    return response['messages'][-1].content

main_agent = create_agent(
    model=llm,
    tools=[ask_fruit_expert, ask_veggie_expert],
    system_prompt='You have two experts: ask_fruit_expert and ask_veggie_expert.'
    'always delegate questions to the appropriate expert.'
)

response = main_agent.invoke({'messages': [{'role': 'user', 'content': 'Is a tomato a fruit?'}]})
print(response['messages'][-1].content)