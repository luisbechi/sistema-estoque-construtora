from fastapi import APIRouter, HTTPException 
from backend.database import conectar_banco
from backend.models import Movimentacao

router = APIRouter(
    prefix="/movimentacoes",
    tags=["movimentacoes"]
)


@router.post("")
def criar_movimentacao(movimentacao: Movimentacao):
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)


    try:
        sql_estoque = """
            select sum(
            case when tipo = 'entrada' then quantidade
            when tipo = 'saida' then -quantidade
            else 0
            end
        ) as estoque_atual
        from movimentacoes
            where produto_id = %s
        """


        cursor.execute(sql_estoque, (movimentacao.produto_id,))
        resultado = cursor.fetchone()
        estoque_atual = resultado["estoque_atual"] or 0

        if movimentacao.tipo == "saida" and estoque_atual < movimentacao.quantidade:
            raise HTTPException(
                status_code=400,
                detail="Estoque insuficiente"
            )

        sql = """
            INSERT INTO movimentacoes
            (produto_id, usuario_id, obra_id, tipo, quantidade, observacao)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = (
            movimentacao.produto_id,
            movimentacao.usuario_id,
            movimentacao.obra_id,
            movimentacao.tipo,
            movimentacao.quantidade,
            movimentacao.observacao
        )

        cursor.execute(sql, valores)
        conexao.commit()

        movimentacao_id = cursor.lastrowid

        return {
            "message": "Movimentação criada com sucesso!",
            "movimentacao_id": movimentacao_id
        }


    finally:
        cursor.close()
        conexao.close()


@router.get("")
def listar_movimentacoes():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        sql = """
            select
            m.id,
            m.tipo,
            m.quantidade,
            m.observacao,
            m.criado_em,
            p.nome as produto,
            u.nome as usuario,
            o.nome as obra
        from movimentacoes m
        join produtos p on m.produto_id = p.id
        join usuarios u on m.usuario_id = u.id
        left join obras o on m.obra_id = o.id
        order by m.criado_em desc
        """

        cursor.execute(sql)
        movimentacoes = cursor.fetchall()   


        return movimentacoes


    finally:
        cursor.close()
        conexao.close()


@router.get("/{movimentacao_id}")
def buscar_movimentacao(movimentacao_id: int):
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        sql = """
            SELECT
                m.id,
                m.tipo,
                m.quantidade,
                m.observacao,
                m.criado_em,
                p.nome AS produto,
                u.nome AS usuario,
                o.nome AS obra
            FROM movimentacoes m
            JOIN produtos p ON m.produto_id = p.id
            JOIN usuarios u ON m.usuario_id = u.id
            LEFT JOIN obras o ON m.obra_id = o.id
            WHERE m.id = %s
        """

        cursor.execute(sql, (movimentacao_id,))
        movimentacao = cursor.fetchone()

        if movimentacao is None:
            raise HTTPException(
                status_code=404,
                detail="Movimentação não encontrada"
            )

        return movimentacao

    finally:
        cursor.close()
        conexao.close()


