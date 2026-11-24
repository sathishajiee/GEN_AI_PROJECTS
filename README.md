## Requirements

- Python 3.12
- [Pipenv](https://pipenv.pypa.io/)
- Git (for version control and publishing to GitHub)
- A Groq API key. Some scripts also need a Hugging Face token, a Tavily key, or Postgres.

## Setup

Install Pipenv if it is not already installed:

```bash
python -m pip install --user pipenv
```

Then, from the project directory:

```bash
pipenv sync
```

Copy `.env.example` to `.env` (`Copy-Item .env.example .env` in PowerShell) and
add the credentials needed by the scripts you want to run:

```
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_hugging_face_token
TAVILY_API_KEY=your_tavily_api_key
DATABASE_URL=your_postgres_connection_uri
```

`GROQ_API_KEY` is required by `agent.py`, `chat_bot.py`, `checkpointers.py`,
`graph.py`, `multi_agent.py`, `prompt_template.py`, and `rag.py`. `HF_TOKEN` is
needed by `chat_bot.py` to access the gated Llama tokenizer, `TAVILY_API_KEY` by
`agent.py`, and `DATABASE_URL` plus a reachable PostgreSQL server by
`checkpointers.py`. `sentiment_analysis.py`, `embedding.py`, and
`pydantic_validation.py` do not require API credentials. Scripts load `.env`
automatically. Hugging Face model files are downloaded the first time a model
is used.

The VS Code workspace recommends the Python and Pylance extensions. Python
debugging support is provided by the Python extension.

## Running

```bash
pipenv run python rag.py
```

Scripts with a `chat_loop` / `chat` REPL read from stdin — type `q` to exit.

## Publishing to GitHub

Create an empty repository on GitHub, then replace the URL below with its
repository URL:

```bash
git remote add origin https://github.com/<your-username>/<your-repository>.git
git add .
git commit -m "Prepare AI engineering tutorial project"
git push -u origin main
```

`.env`, virtual environments, and generated Chroma data are excluded by
`.gitignore`; do not commit API keys.

## Scripts

| File | What it does |
| --- | --- |
| `chat_bot.py` | Streaming chat bot over the Groq OpenAI-compatible API. Trims and periodically summarizes history, counts tokens with the Llama 3.1 tokenizer, enforces a prompt-length and daily token budget, and reports estimated cost. |
| `sentiment_analysis.py` | Zero-shot sentiment classification with a local `transformers` pipeline (`typeform/distilbert-base-uncased-mnli`) — no API calls. |
| `embedding.py` | Sentence embeddings with `sentence-transformers/all-MiniLM-L6-v2`; cosine similarity search over a list of sentences, both by hand and via `util.semantic_search`. |
| `rag.py` | Retrieval-augmented QA over `symptoms.pdf`. Splits pages with a tiktoken-aware splitter, embeds with MiniLM, persists to a Chroma store in `./chroma`, then answers questions with a source-citing, grounded-only system prompt. |
| `agent.py` | LangChain agent with two tools: a stub `get_weather` and Tavily web search. Keeps a running message list across turns. |
| `checkpointers.py` | Agent with a `PostgresSaver` checkpointer and `SummarizationMiddleware`. Two thread IDs demonstrate persistent, switchable sessions (`ch` toggles between them); prints final state on exit. |
| `graph.py` | LangGraph write → review loop. A draft node and a scoring node run until the score hits 10 or three revisions are used, with feedback fed back into the next draft. |
| `multi_agent.py` | Supervisor pattern: a main agent delegates to a fruit expert and a veggie expert, each exposed to it as a tool. |
| `prompt_template.py` | Structured output — a Pydantic `User` model extracted from a biography paragraph via `with_structured_output(..., method='json_schema')`. |
| `pydantic_validation.py` | Pydantic model validation and type coercion. |

## Notes

- Chunks in `rag.py` are keyed by an MD5 of their content, so re-running the script re-ingests
  the PDF idempotently rather than duplicating documents.
- `chroma/` and `.env` are gitignored — the vector store rebuilds itself on the next `rag.py` run.
