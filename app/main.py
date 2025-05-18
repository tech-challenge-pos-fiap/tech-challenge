from typing import Union

#from app.adapters.api.routes.payment_routes import payment_routes
from fastapi import FastAPI

app = FastAPI()
#app.include_router(payment_routes.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
