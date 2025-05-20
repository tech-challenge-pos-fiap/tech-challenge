from typing import Union
from fastapi import FastAPI
from app.adapters.api.routes.product_routes import router as produto_router

app = FastAPI()

# Inclui o router dos produtos
app.include_router(produto_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}