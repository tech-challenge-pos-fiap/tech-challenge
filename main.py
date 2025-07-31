from fastapi import FastAPI

from app.infrastructure.routes.customer_routes import router as customer_routes
from app.infrastructure.routes.order_routes import router as order_routes
from app.infrastructure.routes.product_routes import router as product_routes
from app.infrastructure.routes.payment_routes import router as payment_routes

app = FastAPI()
ROUTES_PREFIX = '/api/v1'

app.include_router(customer_routes, prefix=ROUTES_PREFIX)
app.include_router(product_routes, prefix=ROUTES_PREFIX)
app.include_router(order_routes, prefix=ROUTES_PREFIX)
app.include_router(payment_routes, prefix=ROUTES_PREFIX)
