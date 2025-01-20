from fastapi import APIRouter
router = APIRouter()

menu = [
    {"item": "pizza", "price": 10},
    {"item": "burger", "price": 5},
    {"item": "coke", "price": 2},
    {"item": "fries", "price": 3},
]


@router.get("/")
async def get_menu():
    return menu


@router.get("/item/{item}")
async def get_item(item: str):
    for i in menu:
        if i["item"] == item:
            return i
    return {"item": "not found"}

@router.post("/order")
async def order(item: str):
    for i in menu:
        if i["item"] == item:
            return {"order": item, "price": i["price"], "payment": "cash on delivery"}
    return {"order": "not found"}

@router.put("/order/bulk")
async def order_bulk(items: list):
    total = 0
    for item in items:
        for i in menu:
            if i["item"] == item:
                total += i["price"]
    return {"items":items, "total": total, "payment": "cash on delivery"}
