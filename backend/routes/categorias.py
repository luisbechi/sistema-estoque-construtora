from fastapi import APIRouter, HTTPException 
from backend.database import conectar_banco
from backend.models import Categoria 


router = APIRouter(
    prefix="/categorias",
    tags=["categorias"]
)


@router.get("")
def listar_categorias():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM categorias")
        categorias = cursor.fetchall()


        return categorias
    
    finally:
        cursor.close()
        conexao.close()


@router.get("/{categoria_id}")
def buscar_categoria(categoria_id: int):
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        sql = "SELECT * FROM categorias WHERE id = %s"
        valores = (categoria_id,)

        cursor.execute(sql, valores)

        categoria = cursor.fetchone()

        if categoria is None:
            raise HTTPException(
                status_code=404, 
                detail="Categoria não encontrada"
            )


        return categoria


    finally:
        cursor.close()
        conexao.close()


@router.post("")
def criar_categoria(categoria: Categoria):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        sql = """
            INSERT INTO categorias
            (nome, descricao)
            VALUES (%s, %s)
        """

        valores = (
            categoria.nome,
            categoria.descricao
        )


        cursor.execute(sql, valores)
        conexao.commit()


        categoria_id = cursor.lastrowid


        return {
            "message": "Categoria criada com sucesso!",
            "categoria_id": categoria_id
        }

    finally:
        cursor.close()
        conexao.close()


@router.put("/{categoria_id}")
def atualizar_categoria(categoria_id: int, categoria: Categoria):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        sql = """
            UPDATE categorias
            SET nome = %s, descricao = %s
            WHERE id = %s
        """

        valores = (
            categoria.nome,
            categoria.descricao,
            categoria_id
        )


        cursor.execute(sql, valores)
        conexao.commit()


        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, 
                detail="Categoria não encontrada"
            )


        return {"message": "Categoria atualizada com sucesso!"}

    finally:
        cursor.close()
        conexao.close()


@router.delete("/{categoria_id}")
def excluir_categoria(categoria_id: int):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        sql = "DELETE FROM categorias WHERE id = %s"
        valores = (categoria_id,)

        cursor.execute(sql, valores)
        conexao.commit()


        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, 
                detail="Categoria não encontrada"
            )


        return {"message": "Categoria excluída com sucesso!"}

    finally:
        cursor.close()
        conexao.close()


