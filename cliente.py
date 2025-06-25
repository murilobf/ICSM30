# cliente.py
import requests
import random
import time
import os
from PIL import Image
from io import BytesIO

USUARIOS = ['Alice', 'José', 'Carol', 'Daniel']
MODELOS = ['modelo1', 'modelo2', 'modelo3']

def enviar_sinal():
    usuario = random.choice(USUARIOS)
    modelo = random.choice(MODELOS)
    ganho = random.uniform(0.5, 2.0)
    sinais = [random.random() for _ in range(100)]

    payload = {
        'usuario': usuario,
        'modelo': modelo,
        'ganho': ganho,
        'sinais': sinais
    }

    resp = requests.post('http://localhost:5000/reconstruir', json=payload)

    # Salva imagem e metadados se a requisiçãp for bem sucedida
    if resp.status_code == 200:
        nome_arquivo = f"img_{usuario}_{int(time.time())}.png"
        with open(nome_arquivo, 'wb') as f:
            f.write(resp.content)

        iteracoes = resp.headers.get('X-Iteracoes', '0')
        tempo = resp.headers.get('X-Tempo', '0')

        with open('relatorio_imagens.txt', 'a') as f:
            f.write(f"{nome_arquivo} - Usuario: {usuario}, Iterações: {iteracoes}, Tempo: {tempo} s\n")

def coletar_desempenho():
    resp = requests.get('http://localhost:5000/desempenho')
    if resp.status_code == 200:
        dados = resp.json()
        with open('relatorio_desempenho.txt', 'a') as f:
            f.write(f"CPU: {dados['cpu_percent']}%, Memória: {dados['mem_percent']}%\n")

if __name__ == '__main__':
    for _ in range(5):  # Envia 5 sinais
        enviar_sinal()
        time.sleep(random.uniform(1, 3))  # Intervalos aleatórios

    coletar_desempenho()
