from fastapi import APIRouter, HTTPException 
from backend.database import conectar_banco
from backend.models import Produto

router = APIRouter(
    prefix="/produtos",
    tags=["produtos"]
)


@router.get("")
def listar_produtos():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()


        return produtos
    
    finally:
        cursor.close()
        conexao.close()


@router.post("")
def criar_produto(produto: Produto):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
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


        return {
            "message": "Produto criado com sucesso!",
            "produto_id": produto_id
        }

    finally:
        cursor.close()
        conexao.close()


@router.get("/{produto_id}")
def buscar_produto(produto_id: int):
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        sql = "SELECT * FROM produtos WHERE id = %s"
        valores = (produto_id,)

        cursor.execute(sql, valores)

        produto = cursor.fetchone()

        if produto is None:
            raise HTTPException(
                status_code=404, 
                detail="Produto não encontrado"
            )


        return produto


    finally:
        cursor.close()
        conexao.close()


@router.put("/{produto_id}")
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

@router.delete("/{produto_id}")
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