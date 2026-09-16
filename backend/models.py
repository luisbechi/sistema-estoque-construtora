from pydantic import BaseModel, Field
from typing import Literal


class Produto(BaseModel):
    nome: str
    categoria_id: int
    unidade: str
    estoque_minimo: float = 0


class Categoria(BaseModel):
    nome: str
    descricao: str | None = None


class Movimentacao(BaseModel):
    produto_id: int
    usuario_id: int
    obra_id: int | None = None
    tipo: Literal["entrada", "saida"]
    quantidade: float = Field(gt=0)
    observacao: str | None = None