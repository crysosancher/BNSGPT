from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from rag_chain import ask_question_stream

app = FastAPI()

@app.post("/query")
async def query(request: Request):
    data = await request.json()
    question = data.get("question")
    if not question:
        return {"error": "Question is required"}
    return StreamingResponse(ask_question_stream(question), media_type="text/plain")
