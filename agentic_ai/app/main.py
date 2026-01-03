import os
import sys
import webbrowser
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse

# Force imports to work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.agents import graph
from app.vector_store import index_document

@asynccontextmanager
async def lifespan(app: FastAPI):
    url = "http://127.0.0.1:8000/docs"
    print(f"🚀 OPENING SWAGGER: {url}")
    webbrowser.open(url)
    yield

# --- STEP 1: Enable DEBUG=True ---
app = FastAPI(title="Agentic AI Debugger", lifespan=lifespan, debug=True)

# --- STEP 2: Catch any hidden error and print it ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"❌ CRITICAL ERROR CAUGHT: {exc}")
    import traceback
    traceback.print_exc() # This prints the RED text in your terminal
    return JSONResponse(
        status_code=500,
        content={"message": "The server crashed!", "details": str(exc)},
    )

@app.post("/chat")
async def chat(query: str):
    # LangGraph call
    inputs = {"messages": [("user", query)]}
    result = graph.invoke(inputs)
    return {"response": result["messages"][-1].content}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": index_document(file_path)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)