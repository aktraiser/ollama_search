import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "https://ollama.com/api")

if not OLLAMA_API_KEY:
    raise RuntimeError("Missing OLLAMA_API_KEY env var")

app = FastAPI(
    title="Ollama Web Search Proxy",
    description="OpenAPI proxy for Ollama's web_search and web_fetch endpoints",
    version="1.0.0",
)

class WebSearchIn(BaseModel):
    query: str
    max_results: Optional[int] = 5

class SearchResult(BaseModel):
    title: str
    url: str
    content: str

class WebSearchOut(BaseModel):
    results: List[SearchResult]

class WebFetchIn(BaseModel):
    url: str

class WebFetchOut(BaseModel):
    title: str
    content: str
    links: List[str]

headers = {
    "Authorization": f"Bearer {OLLAMA_API_KEY}",
    "Content-Type": "application/json",
}

@app.post("/web_search", response_model=WebSearchOut)
async def web_search(payload: WebSearchIn):
    url = f"{OLLAMA_BASE_URL}/web_search"
    data = {"query": payload.query}
    if payload.max_results is not None:
        data["max_results"] = payload.max_results

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url, headers=headers, json=data)
    if resp.status_code >= 400:
        raise HTTPException(resp.status_code, resp.text)
    
    result = resp.json()
    
    # Truncate content to manage context window (Ollama recommendation: 8000 chars)
    if "results" in result:
        for search_result in result["results"]:
            if "content" in search_result and search_result["content"]:
                content = search_result["content"]
                if len(content) > 8000:
                    search_result["content"] = content[:8000] + "..."
    
    return result

@app.post("/web_fetch", response_model=WebFetchOut)
async def web_fetch(payload: WebFetchIn):
    url = f"{OLLAMA_BASE_URL}/web_fetch"
    data = {"url": payload.url}

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url, headers=headers, json=data)
    if resp.status_code >= 400:
        raise HTTPException(resp.status_code, resp.text)
    
    result = resp.json()
    
    # Truncate content to manage context window (Ollama recommendation: 8000 chars)
    if "content" in result and result["content"]:
        content = result["content"]
        if len(content) > 8000:
            result["content"] = content[:8000] + "..."
    
    return result

@app.get("/")
async def root():
    return {
        "message": "Ollama Web Search Proxy",
        "endpoints": ["/web_search", "/web_fetch"],
        "docs": "/docs",
        "openapi": "/openapi.json"
    }