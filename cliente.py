# cliente.py
import requests
import random
import time

USUARIOS = ['Alice', 'José', 'Carol', 'Daniel','Murilo','Maria','Ana','Leonardo','Eduarda','Lucas']
MODELOS = ['Dados/H-1.csv', 'Dados/H-2.csv']
SINAIS60 = ['Dados/G-1.csv', 'Dados/G-2.csv', 'Dados/A-60x60-1.csv']
SINAIS30 = ['Dados/g-30x30-1.csv','Dados/g-30x30-2.csv','Dados/A-30x30-1.csv']

def enviar_sinal(usuario):
    
    #modelo = random.choice(MODELOS)
    modelo = random.choice(MODELOS)

    # Hardcoded demais pro ideal mas como temos poucos arquivos dá pra ser assim mesmo
    if(modelo == 'Dados/H-1.csv'):
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

#Função para simular a criação de vários clientes diferentes, cada um com uma quantidade de sinais pedido diferente
def simula_clientes():
    quantidade_clientes = random.randint(1,5)

    for i in range(quantidade_clientes):
        quantidade_sinais = random.randint(1,10)
        usuario = random.choice(USUARIOS)

        for j in range(quantidade_sinais):
            enviar_sinal(usuario)

if __name__ == '__main__':
    for _ in range(5):  # Envia 5 sinais
        enviar_sinal()
        time.sleep(random.uniform(1, 3))  # Intervalos aleatórios

    coletar_desempenho()
