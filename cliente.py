# CLIENTE PARA RECONSTRUÇÃO DE IMAGENS DE ULTRASSOM
# REQUISITOS ATENDIDOS:
# 1. Envia sequência de sinais em intervalos aleatórios
# 2. Define usuário, modelo e sinal aleatoriamente
# 3. Gera relatório com imagens reconstruídas
# 4. Gera relatório de desempenho do servidor

import requests
import random
import time
import threading

USUARIOS = ['Alice', 'José', 'Carol', 'Daniel','Murilo','Maria','Ana','Leonardo','Eduarda','Lucas']
MODELOS = ['Dados/H-1.csv', 'Dados/H-2.csv']
SINAIS60 = ['Dados/G-1.csv', 'Dados/G-2.csv', 'Dados/A-60x60-1.csv']
SINAIS30 = ['Dados/g-30x30-1.csv','Dados/g-30x30-2.csv','Dados/A-30x30-1.csv']


def enviar_sinal(usuario):
    
    #modelo = random.choice(MODELOS)
    modelo = random.choice(MODELOS)

    # REQUISITO ATENDIDO: Seleciona sinal compatível com o modelo
    if modelo == 'Dados/H-1.csv':
        sinal = random.choice(SINAIS60)
    else:
        sinal = random.choice(SINAIS30)

    print(f"[LOG] Enviando sinal -> Usuario: {usuario}, Modelo: {modelo}, Sinal: {sinal}")

    payload = {
        'usuario': usuario,
        'modelo': modelo,
        'sinal': sinal
    }

    try:
        resp = requests.post('http://localhost:5000/reconstruir', json=payload)
        if resp.status_code == 200:
            # REQUISITO ATENDIDO: Salva imagem reconstruída
            nome_arquivo = f"img_{usuario}_{int(time.time())}.png"
            with open(f"Imagens/{nome_arquivo}", 'wb') as f:
                f.write(resp.content)

            # REQUISITO ATENDIDO: Extrai metadados dos headers
            iteracoes = resp.headers.get('X-Iteracoes', '0')
            tempo = resp.headers.get('X-Tempo', '0')
            alg = resp.headers.get('X-Algoritmo', 'unknown')
            inicio = resp.headers.get('X-Inicio', '')
            fim = resp.headers.get('X-Fim', '')
            tamanho = resp.headers.get('X-Tamanho', '')

            uso_cpu = resp.headers.get('X-Cpu','')
            uso_mem = resp.headers.get('X-Mem','')

            # REQUISITO ATENDIDO: Gera relatório com informações da reconstrução
            with open('relatorio_imagens.txt', 'a') as f:
                f.write(
                    f"{nome_arquivo} - Usuario: {usuario}, Algoritmo: {alg}, "
                    f"Inicio: {inicio}, Fim: {fim}, Tamanho: {tamanho}, "
                    f"Iterações: {iteracoes}, Tempo: {tempo} s, Modelo: {modelo}, Sinal: {sinal}\n"
                )
            print(f"[SUCESSO] Imagem salva: {nome_arquivo} ({iteracoes} iterações, {tempo}s)")

            with open('relatorio_desempenho.txt', 'a') as f:
                f.write(
                    f"[{fim}] CPU: {uso_cpu}%, Memória: {uso_mem}%\n"
                )
            print(f"[DESEMPENHO] CPU: {uso_cpu}%, Memória: {uso_mem}%")
        else:
            print(f"[ERRO] Resposta do servidor: {resp.status_code} - {resp.text}")
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha na comunicação com servidor: {e}")


#Função para simular vários envios de sinal pelo mesmo cliente
def funcao_thread_sinal(usuario: str):
    enviar_sinal(usuario)
    

#Função para simular os clientes separados. Para isso usamos threads
def funcao_thread_cliente():
    quantidade_sinais = random.randint(1,5)

    usuario = random.choice(USUARIOS)

    for j in range(quantidade_sinais):
        thread_sinal = threading.Thread(target=funcao_thread_sinal, args=(usuario,))
        thread_sinal.start()
        time.sleep(random.randint(1,10))


#Função para simular a criação de vários clientes diferentes, cada um com uma quantidade de sinais pedido diferente
def simula_clientes():
    quantidade_clientes = random.randint(1,5)

    for i in range(quantidade_clientes):
        #Cria uma thread pra cada cliente simulado. O servidor que decide quantos rodam ao mesmo tempo na prática
        thread_cliente = threading.Thread(target=funcao_thread_cliente)
        thread_cliente.start()
