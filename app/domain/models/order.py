class Order:
    def __init__(self, client, products, status, total_price, order_date):
        self.client = client
        self.products = products
        self.status = status
        self.total_price = total_price
        self.order_date = order_date
