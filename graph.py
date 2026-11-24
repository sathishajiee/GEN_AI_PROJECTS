import dotenv
from typing import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph

dotenv.load_dotenv()


class ContentState(TypedDict):
    topic: str
    draft: str
    score: int
    feedback: str
    revision_count: int


llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.7)


def write_draft(state: ContentState):
    prompt = f"Write a short paragraph about: {state['topic']}"

    if state.get('feedback'):
        prompt += f"\n\nPrevious feedback to address: {state['feedback']}"

    response = llm.invoke(prompt)

    return {'draft': response.content, 'revision_count': state.get('revision_count', 0) + 1}


def review_draft(state: ContentState):
    prompt = f'''Rate this paragraph from 1-10 and give one sentence of feedback. be extremely strict.
    Paragraph: {state['draft']}
    
    Respond in exactly this format:
    Score: <number>
    Feedback: <text>'''

    response = llm.invoke(prompt)
    text = response.content

    score_line = [l for l in text.split('\n') if l.startswith('Score:')][0]
    feedback_line = [l for l in text.split(
        '\n') if l.startswith('Feedback:')][0]

    score = int(score_line.replace('Score:', '').strip())
    feedback = feedback_line.replace('Feedback:', '').strip()

    return {'score': score, 'feedback': feedback}


def should_revise(state: ContentState):
    if state['score'] >= 10:
        return END
    if state['revision_count'] >= 3:
        return END

    return 'write_draft'


builder = StateGraph(ContentState)

builder.add_node(write_draft)
builder.add_node(review_draft)

builder.add_edge(START, 'write_draft')
builder.add_edge('write_draft', 'review_draft')
builder.add_conditional_edges('review_draft', should_revise)

graph = builder.compile()

result = graph.invoke({
    'topic': 'why sleep matters for learning',
    'draft': '',
    'feedback': '',
    'score': 0,
    'revision_count': 0
})

print(f"Final draft ({result['revision_count']} revision(s)):\n")
print(result['draft'])
print(f"\nFinal Score: {result['score']}")
