import os
import mysql.connector
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


load_dotenv()

app = FastAPI()
class Produto(BaseModel):
    nome: str
    categoria_id: int
    unidade: str
    estoque_minimo: float = 0


def conectar_banco():
    conexao = mysql.connector.connect(
        host=os.getenv("db_host"),
        user=os.getenv("db_user"),
        password=os.getenv("db_password"),
        database=os.getenv("db_name")
    )

    return conexao

@app.get("/")
def inicio():
        return {"message": "Sistema de Estoque - API funcionando!"}  

@app.get("/produtos")
def listar_produtos():
    conexao = conectar_banco()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produtos")

    produtos = cursor.fetchall()

    cursor.close()

    conexao.close()

    return produtos

@app.post("/produtos")
def criar_produto(produto: Produto):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO produtos
        (nome, categoria_id, unidade, estoque_minimo)
        VALUES (%s, %s, %s, %s)
    """

    valores = (
        produto.nome,
        produto.categoria_id,
        produto.unidade,
        produto.estoque_minimo
    )

    cursor.execute(sql, valores)
    conexao.commit()

    produto_id = cursor.lastrowid

    cursor.close()
    conexao.close()

    return {
        "message": "Produto criado com sucesso!",
        "produto_id": produto_id
    }

@app.get("/produtos/{produto_id}")
def buscar_produto(produto_id: int):
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    sql = "SELECT * FROM produtos WHERE id = %s"
    valores = (produto_id,)

    cursor.execute(sql, valores)

    produto = cursor.fetchone()

    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return produto

    cursor.close()
    conexao.close()

    
    return produto

@app.put("/produtos/{produto_id}")
def atualizar_produto(produto_id: int, produto: Produto):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        sql = """
            UPDATE produtos
            SET nome = %s, categoria_id = %s, unidade = %s, estoque_minimo = %s
            WHERE id = %s
        """

        valores = (
            produto.nome,
            produto.categoria_id,
            produto.unidade,
            produto.estoque_minimo,
            produto_id
        )

        cursor.execute(sql, valores)
        conexao.commit()

        linhas_alteradas = cursor.rowcount
    
        if linhas_alteradas == 0:
            raise HTTPException(status_code=404, detail="Produto não encontrado")


        return {"message": "Produto atualizado com sucesso!"}

    finally:
        cursor.close()
        conexao.close()

@app.delete("/produtos/{produto_id}")
def excluir_produto(produto_id: int):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        sql = "DELETE FROM produtos WHERE id = %s"
        valores = (produto_id,)

        cursor.execute(sql, valores)
        conexao.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        return {"message": "Produto excluído com sucesso!"}

    finally:
        cursor.close()
        conexao.close()