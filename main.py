from fastapi import FastAPI

from app.adapters.api.routes.customer_routes import router as customer_routes
from app.adapters.api.routes.payment_routes import router as payment_routes
from app.adapters.api.routes.product_routes import router as product_routes

app = FastAPI()

app.include_router(customer_routes)
app.include_router(payment_routes)
app.include_router(product_routes)
