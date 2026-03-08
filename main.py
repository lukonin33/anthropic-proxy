import httpx
from fastapi import FastAPI, Request
from fastapi.responses import Response

app = FastAPI()

@app.post("/v1/messages")
async def proxy(request: Request):
    body = await request.body()
    headers = {
        "content-type": "application/json",
        "x-api-key": request.headers.get("x-api-key", ""),
        "anthropic-version": request.headers.get("anthropic-version", "2023-06-01"),
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post("https://api.anthropic.com/v1/messages", content=body, headers=headers)
    return Response(content=r.content, status_code=r.status_code, media_type="application/json")

@app.get("/")
async def health():
    return {"status": "ok"}
