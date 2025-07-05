from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx
import json
import asyncio

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:latest"

@app.post("/stream")
async def stream_response(request: Request):
    body = await request.json()
    prompt = body.get("prompt")
    if not prompt:
        return {"error": "Missing 'prompt' in request"}

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True
    }

    async def event_generator():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", OLLAMA_URL, json=payload) as response:
                async for line in response.aiter_lines():
                    if line:
                        # Ollama streams JSON lines (NDJSON)
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        done = data.get("done", False)
                        yield chunk
                        if done:
                            break
                    await asyncio.sleep(0)  # yield control

    return StreamingResponse(event_generator(), media_type="text/plain")
