# cliente.py
import requests
import random
import time

USUARIOS = ['Alice', 'José', 'Carol', 'Daniel']
MODELOS = ['Dados/H-1.csv', 'Dados/H-2.csv']
SINAIS60 = ['Dados/G-1.csv', 'Dados/G-2.csv']
SINAIS30 = ['Dados/g-30x30-1.csv', 'Dados/g-30x30-2.csv']

def enviar_sinal():
    usuario = random.choice(USUARIOS)
    modelo = random.choice(MODELOS)
    print("teste")

    # Hardcoded demais pro ideal mas como temos poucos arquivos dá pra ser assim mesmo
    if(modelo == 'Dados/H-1'):
        sinal = random.choice(SINAIS60)
    else:
        sinal = random.choice(SINAIS30)

    payload = {
        'usuario': usuario,
        'modelo': modelo,
        'sinal': sinal
    }

    resp = requests.post('http://localhost:5000/reconstruir', json=payload)

    # Salva imagem e metadados se a requisiçãp for bem sucedida
    if resp.status_code == 200:
        nome_arquivo = f"img_{usuario}_{int(time.time())}.png"
        with open(nome_arquivo, 'wb') as f:
            f.write(resp.content)
        print("testecliente\n")

        iteracoes = resp.headers.get('X-Iteracoes', '0')
        tempo = resp.headers.get('X-Tempo', '0')

        with open('relatorio_imagens.txt', 'a') as f:
            f.write(f"{nome_arquivo} - Usuario: {usuario}, Iterações: {iteracoes}, Tempo: {tempo} s\n")

    else:
        print("Erro ao abrir")

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
