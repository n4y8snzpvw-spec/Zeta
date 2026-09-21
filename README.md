# Zeta

Zeta is a small, responsive AI chat app with a FastAPI backend and a zero-build browser UI.

## Run locally

```bash
python -m pip install -e .
export OPENAI_API_KEY="your-api-key"  # optional: without it, demo mode is used
python -m zeta.cli
```

Open <http://127.0.0.1:8000>. The app uses the OpenAI-compatible Chat Completions API. Configure a compatible provider with `OPENAI_BASE_URL` and select a model with `ZETA_MODEL`.

### Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | unset | Enables live model responses |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | OpenAI-compatible API endpoint |
| `ZETA_MODEL` | `gpt-4o-mini` | Model name |

The API key is read only by the server and is never sent to the browser.

## API

- `GET /health` — reports whether the app is in `demo` or `live` mode.
- `POST /api/chat` — accepts `{ "messages": [{ "role": "user", "content": "..." }] }`.
