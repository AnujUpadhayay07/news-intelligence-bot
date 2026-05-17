from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.rag_chain import answer_question

import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/analyze")
async def analyze(request: QueryRequest):
    try:
        result = answer_question(request.question, top_k=request.top_k)
        return {
            "success": True,
            "answer": result["answer"],
            "sources": result["sources"],
            "articles_used": result["articles_used"],
            "contradictions": result.get("contradictions", {})
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)