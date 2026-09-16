from fastapi import FastAPI
from backend.routes.produtos import router as produtos_router
from backend.routes.categorias import router as categorias_router
from backend.routes.movimentacoes import router as movimentacoes_router

app = FastAPI()

app.include_router(produtos_router)
app.include_router(categorias_router)
app.include_router(movimentacoes_router)

@app.get("/")
def inicio():
    return {"message": "Sistema de Estoque - API funcionando!"}