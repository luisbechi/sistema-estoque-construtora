import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv()

conexao = mysql.connector.connect(
    host=os.getenv("db_host"),
    user=os.getenv("db_user"),
    password=os.getenv("db_password"),
    database=os.getenv("db_name")
)
if conexao.is_connected():
    print("Conectado ao banco de dados MySQL")
    conexao.close()