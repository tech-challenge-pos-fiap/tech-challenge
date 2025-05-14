from config.db import SessionLocal
from adapters.persistence.models.produto_model import ProdutoModel

produtos = [
    {"nome": "X-Burger", "descricao": "Hambúrguer com queijo", "preco": 18.0, "categoria": "lanche"},
    {"nome": "Batata", "descricao": "Batata frita média", "preco": 9.0, "categoria": "acompanhamento"},
    {"nome": "Coca-Cola", "descricao": "Lata 350ml", "preco": 6.5, "categoria": "bebida"},
    {"nome": "Sorvete", "descricao": "Casquinha de baunilha", "preco": 5.0, "categoria": "sobremesa"},
]

db = SessionLocal()
for p in produtos:
    db.add(ProdutoModel(**p))
db.commit()