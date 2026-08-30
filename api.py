from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI(title="PyClima API")

# ========================================
# BANCO DE DADOS
# ========================================

def conectar_banco():
    return sqlite3.connect("pyclima.db")


def criar_banco():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura REAL NOT NULL,
            umidade REAL NOT NULL,
            chuva BOOLEAN NOT NULL,
            data_hora TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


# Criar banco/tabela ao iniciar a API
criar_banco()


# ========================================
# MODELO DOS DADOS
# ========================================

class DadosSensores(BaseModel):
    temperatura: float
    umidade: float
    chuva: bool


# ========================================
# ROTA PRINCIPAL
# ========================================

@app.get("/")
def inicio():
    return {
        "mensagem": "API do PyClima funcionando!"
    }


# ========================================
# RECEBER E SALVAR DADOS
# ========================================

@app.post("/sensores")
def receber_dados(dados: DadosSensores):

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO sensores
        (temperatura, umidade, chuva, data_hora)
        VALUES (?, ?, ?, ?)
    """, (
        dados.temperatura,
        dados.umidade,
        dados.chuva,
        data_hora
    ))

    conexao.commit()

    id_registro = cursor.lastrowid

    conexao.close()

    print("----------------------------------------")
    print("DADO SALVO NO BANCO")
    print("ID:", id_registro)
    print("Temperatura:", dados.temperatura)
    print("Umidade:", dados.umidade)
    print("Chuva:", dados.chuva)
    print("Data/Hora:", data_hora)
    print("----------------------------------------")

    return {
        "status": "sucesso",
        "mensagem": "Dados salvos no banco!",
        "id": id_registro,
        "data_hora": data_hora
    }


# ========================================
# CONSULTAR DADOS
# ========================================

@app.get("/sensores")
def consultar_dados():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, temperatura, umidade, chuva, data_hora
        FROM sensores
        ORDER BY id DESC
    """)

    registros = cursor.fetchall()

    conexao.close()

    dados = []

    for registro in registros:
        dados.append({
            "id": registro[0],
            "temperatura": registro[1],
            "umidade": registro[2],
            "chuva": bool(registro[3]),
            "data_hora": registro[4]
        })

    return dados