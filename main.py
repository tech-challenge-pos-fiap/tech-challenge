from typing import Union
from app.adapters.api.routes.product_routes import router as produto_router
from app.adapters.api.routes.payment_routes import router as payment_routes
from fastapi import FastAPI

app = FastAPI()

app.include_router(payment_routes)
app.include_router(produto_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}