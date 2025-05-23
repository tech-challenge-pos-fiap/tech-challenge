from fastapi import FastAPI

from app.adapters.api.routes.customer_routes import router as customer_routes
from app.adapters.api.routes.payment_routes import router as payment_routes
from app.adapters.api.routes.product_routes import router as product_routes
from app.adapters.api.routes.order_routes import router as order_routes

app = FastAPI()

app.include_router(customer_routes)
app.include_router(payment_routes)
app.include_router(product_routes)
app.include_router(order_routes)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
