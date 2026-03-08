import httpx
from fastapi import FastAPI, Request
from fastapi.responses import Response

app = FastAPI()

# Anthropic proxy
@app.post("/v1/messages")
async def proxy_anthropic(request: Request):
    body = await request.body()
    headers = {
        "content-type": "application/json",
        "x-api-key": request.headers.get("x-api-key", ""),
        "anthropic-version": request.headers.get("anthropic-version", "2023-06-01"),
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post("https://api.anthropic.com/v1/messages", content=body, headers=headers)
    return Response(content=r.content, status_code=r.status_code, media_type="application/json")

# OpenAI proxy
@app.post("/openai/v1/{path:path}")
async def proxy_openai(request: Request, path: str):
    body = await request.body()
    headers = {
        "content-type": "application/json",
        "authorization": request.headers.get("authorization", ""),
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"https://api.openai.com/v1/{path}", content=body, headers=headers)
    return Response(content=r.content, status_code=r.status_code, media_type="application/json")

@app.get("/")
async def health():
    return {"status": "ok"}
