from fastapi import FastAPI
import os
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
    return {"name": "HTTP Server"}


@app.get("/health")
async def health():
    return {"status": "ok"}

menu = [
    {"item": "pizza", "price": 10},
    {"item": "burger", "price": 5},
    {"item": "coke", "price": 2},
    {"item": "fries", "price": 3},
]

@app.get("/menu")
async def get_menu():
    return menu


@app.get("/menu/{item}")
async def get_item(item: str):
    for i in menu:
        if i["item"] == item:
            return i
    return {"item": "not found"}

@app.post("/order")
async def order(item: str):
    for i in menu:
        if i["item"] == item:
            return {"order": item, "price": i["price"], "payment": "cash on delivery"}
    return {"order": "not found"}

@app.put("/order/bulk")
async def order_bulk(items: list):
    total = 0
    for item in items:
        for i in menu:
            if i["item"] == item:
                total += i["price"]
    return {"items":items, "total": total, "payment": "cash on delivery"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)