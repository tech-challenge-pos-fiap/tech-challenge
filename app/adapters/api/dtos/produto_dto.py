from pydantic import Basemodel


class ProdutoDTO(Basemodel):
    nome: str
    descricao: str
    preco: float
    categoria: str