from fastapi import FastAPI
import os
import uvicorn
from menu import router as menu_router
from webhook import router as webhook_router

app = FastAPI()
app.include_router(menu_router, prefix="/api/menu", tags=["menu"])
app.include_router(webhook_router, prefix="/webhooks", tags=["webhooks"])

@app.get("/")
async def read_root():
    return {"name": "HTTP Server"}


@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)