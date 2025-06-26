# CLIENTE PARA RECONSTRUÇÃO DE IMAGENS DE ULTRASSOM
# REQUISITOS ATENDIDOS:
# 1. Envia sequência de sinais em intervalos aleatórios
# 2. Define usuário, modelo e sinal aleatoriamente
# 3. Gera relatório com imagens reconstruídas
# 4. Gera relatório de desempenho do servidor

import requests
import random
import time
import datetime
import os

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
        resp = requests.post('http://localhost:5000/reconstruir', json=payload, timeout=30)
        if resp.status_code == 200:
            # REQUISITO ATENDIDO: Salva imagem reconstruída
            nome_arquivo = f"img_{usuario}_{int(time.time())}.png"
            with open(nome_arquivo, 'wb') as f:
                f.write(resp.content)

            # REQUISITO ATENDIDO: Extrai metadados dos headers
            iteracoes = resp.headers.get('X-Iteracoes', '0')
            tempo = resp.headers.get('X-Tempo', '0')
            alg = resp.headers.get('X-Algoritmo', 'unknown')
            inicio = resp.headers.get('X-Inicio', '')
            fim = resp.headers.get('X-Fim', '')
            tamanho = resp.headers.get('X-Tamanho', '')

            # REQUISITO ATENDIDO: Gera relatório com informações da reconstrução
            with open('relatorio_imagens.txt', 'a') as f:
                f.write(
                    f"{nome_arquivo} - Usuario: {usuario}, Algoritmo: {alg}, "
                    f"Inicio: {inicio}, Fim: {fim}, Tamanho: {tamanho}, "
                    f"Iterações: {iteracoes}, Tempo: {tempo} s, Modelo: {modelo}, Sinal: {sinal}\n"
                )
            print(f"[SUCESSO] Imagem salva: {nome_arquivo} ({iteracoes} iterações, {tempo}s)")
        else:
            print(f"[ERRO] Resposta do servidor: {resp.status_code} - {resp.text}")
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha na comunicação com servidor: {e}")

def coletar_desempenho():
    """
    REQUISITO ATENDIDO: Coleta dados de desempenho do servidor
    """
    try:
        resp = requests.get('http://localhost:5000/desempenho', timeout=10)
        if resp.status_code == 200:
            dados = resp.json()
            timestamp = dados.get('timestamp', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            # REQUISITO ATENDIDO: Gera relatório de desempenho
            with open('relatorio_desempenho.txt', 'a') as f:
                f.write(
                    f"[{timestamp}] CPU: {dados['cpu_percent']}%, Memória: {dados['mem_percent']}%\n"
                )
            print(f"[DESEMPENHO] CPU: {dados['cpu_percent']}%, Memória: {dados['mem_percent']}%")
        else:
            print(f"[ERRO] Falha ao coletar desempenho: {resp.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha ao conectar servidor de desempenho: {e}")

def executar_cliente(num_sinais=5):
    """
    REQUISITO ATENDIDO: Executa cliente com envio de sinais em intervalos aleatórios
    """
    print("=== CLIENTE DE RECONSTRUÇÃO DE IMAGENS DE ULTRASSOM ===")
    print(f"Enviando {num_sinais} sinais com intervalos aleatórios...")
    
    # Limpa relatórios anteriores
    for arquivo in ['relatorio_imagens.txt', 'relatorio_desempenho.txt']:
        if os.path.exists(arquivo):
            os.remove(arquivo)
    
    # REQUISITO ATENDIDO: Cabeçalhos dos relatórios
    with open('relatorio_imagens.txt', 'w') as f:
        f.write("=== RELATÓRIO DE IMAGENS RECONSTRUÍDAS ===\n")
        f.write(f"Gerado em: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    with open('relatorio_desempenho.txt', 'w') as f:
        f.write("=== RELATÓRIO DE DESEMPENHO DO SERVIDOR ===\n")
        f.write(f"Gerado em: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    for i in range(num_sinais):
        print(f"\n--- Enviando sinal {i+1}/{num_sinais} ---")
        
        # REQUISITO ATENDIDO: Envia sinal para reconstrução
        enviar_sinal()
        
        # Coleta desempenho após cada envio
        coletar_desempenho()
        
        # REQUISITO ATENDIDO: Intervalo aleatório entre envios (1-3 segundos)
        if i < num_sinais - 1:  # Não espera após o último envio
            intervalo = random.uniform(1, 3)
            print(f"[INTERVALO] Aguardando {intervalo:.1f}s...")
            time.sleep(intervalo)

    print("\n=== EXECUÇÃO CONCLUÍDA ===")
    print("Arquivos gerados:")
    print("- relatorio_imagens.txt: Relatório das imagens reconstruídas")
    print("- relatorio_desempenho.txt: Relatório de desempenho do servidor")
    print("- img_*.png: Imagens reconstruídas")

#Função para simular a criação de vários clientes diferentes, cada um com uma quantidade de sinais pedido diferente
def simula_clientes():
    quantidade_clientes = random.randint(1,5)

    for i in range(quantidade_clientes):
        quantidade_sinais = random.randint(1,10)
        usuario = random.choice(USUARIOS)

        for j in range(quantidade_sinais):
            enviar_sinal(usuario)

if __name__ == '__main__':
    executar_cliente(10)