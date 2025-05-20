from pydantic import BaseModel

class ProdutoDTO(BaseModel):
    nome: str
    descricao: str
    preco: float
    categoria: str