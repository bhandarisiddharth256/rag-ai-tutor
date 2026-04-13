from fastapi import APIRouter
from pydantic import BaseModel

from services.rag_service import search
from services.llm_service import generate_answer

router = APIRouter()

class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
def chat(req: ChatRequest):
    query = req.query.strip()

    # 🔍 Step 1: search relevant chunks
    results = search(query)

    # ✅ handle no data
    if not results or results == ["No data available"]:
        return {
            "query": query,
            "answer": "No document data available. Please upload a file first."
        }

    # 🧠 Step 2: limit context (VERY IMPORTANT)
    top_chunks = results[:3]
    context = "\n\n".join(results[:2])

    # 🤖 Step 3: generate answer
    try:
        answer = generate_answer(query, context)
    except Exception as e:
        print("Chat Error:", e)
        answer = "Something went wrong while generating answer."

    return {
        "query": query,
        "answer": answer,
        "context_used": top_chunks   # 🔥 helpful for debugging
    }