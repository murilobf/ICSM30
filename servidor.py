# SERVIDOR FLASK PARA RECONSTRUÇÃO DE IMAGENS DE ULTRASSOM
# REQUISITOS ATENDIDOS:
# 1. Recebe dados para reconstrução
# 2. Carrega modelo de acordo com parâmetros
# 3. Executa algoritmo de reconstrução  
# 4. Executa até erro < 1e-4
# 5. Salva resultado com metadados obrigatórios

import time
import numpy as np
import psutil
import io
from PIL import Image
import algoritmos
import matplotlib.pyplot as plt
import threading
import datetime
from flask import Flask, request, jsonify, send_file, make_response

app = Flask(__name__)
#Semáforos para determinar o número máximo de clientes e processos de reconstrução simultâneos
#Se passar do valor do parâmetro ele bloqueia a thread até estar liberado
semaforo_clientes = threading.Semaphore(2)
semaforo_processos = threading.Semaphore(5)

#Dicionario guardando os modelos já visitados
modelos = {}


@app.route('/reconstruir', methods=['POST'])
def reconstruir():
    """
    REQUISITO ATENDIDO: Fazer o atendimento de vários clientes ao mesmo tempo, qtde determinada por semaforo_clientes
    """
    with semaforo_clientes:
        """
        REQUISITO ATENDIDO: Recebe dados para reconstrução via POST
        Processa sinal usando algoritmo CGNR e retorna imagem com metadados
        """
        data = request.json
        usuario = data['usuario']  # REQUISITO: Identificação do usuário
        modelo = data['modelo']
        sinal = data['sinal']

        # REQUISITO ATENDIDO: Data e hora do início da reconstrução
        start_time = time.time()
        start_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        """
        REQUISITO ATENDIDO: Fazer vários processamentos ao mesmo tempo, qtde determinada por semaforo_processos
        """
        with semaforo_processos:
            try:
                # REQUISITO ATENDIDO: Carrega modelo de acordo com parâmetros recebidos
                # Já que demora bastante pra carregar os modelos maiores, salvamos ele na memória do servidor no formato de um dicionário {caminho - Matriz}
                if modelo in modelos:
                    H = modelos[modelo]
                else:
                    H = np.loadtxt(modelo, delimiter=',', dtype=np.float64)
                    modelos[modelo] = H

                g = np.loadtxt(sinal, delimiter=',', dtype=np.float64)

                # REQUISITO ATENDIDO: Executa algoritmo de reconstrução até erro < 1e-4
                f, iteracoes = algoritmos.cgnr(g, H, 100)  # Unpack all three return values

                """
                REQUISITO ATENDIDO: Monitoramento de desempenho do servidor
                Retorna informações de CPU e memória
                """
                mem = psutil.virtual_memory()
                cpu = psutil.cpu_percent(interval=1)

                # Normaliza para 0–255 com tratamento robusto
                f_min, f_max = f.min(), f.max()
                if f_max != f_min:
                    f_norm = (f - f_min) / (f_max - f_min) * 255
                else:
                    f_norm = np.full_like(f, 128)  # Valor médio se todos os pixels são iguais

                # REQUISITO ATENDIDO: Determina tamanho em pixels
                lado = int(np.sqrt(len(f)))
                imagem_array = f_norm[:lado*lado].reshape((lado, lado), order='F')
                
                # Garante que os valores estão no range válido para imagem
                imagem_array = np.clip(imagem_array, 0, 255)
                imagem = Image.fromarray(imagem_array.astype('uint8'))

                # Converte imagem para bytes
                img_bytes = io.BytesIO()
                imagem.save(img_bytes, format='PNG')
                img_bytes.seek(0)

                # REQUISITO ATENDIDO: Data e hora do término da reconstrução
                end_time = time.time()
                end_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # REQUISITO ATENDIDO: Resposta com todos os metadados obrigatórios
                response = make_response(send_file(img_bytes, mimetype='image/png', download_name='reconstruida.png'))
                response.headers['X-Usuario'] = usuario  # 1. Identificação do usuário
                response.headers['X-Algoritmo'] = "cgnr"  # 2. Identificação do algoritmo
                response.headers['X-Inicio'] = start_dt  # 3. Data/hora início
                response.headers['X-Fim'] = end_dt  # 4. Data/hora término  
                response.headers['X-Tamanho'] = f"{lado}x{lado}"  # 5. Tamanho em pixels
                response.headers['X-Iteracoes'] = str(iteracoes)  # 6. Número de iterações
                response.headers['X-Tempo'] = str(end_time - start_time) 
                response.headers['X-Cpu'] = str(cpu)
                response.headers['X-Mem'] = str(mem.percent)

                return response

            except Exception as e:
                return jsonify({'error': str(e)}), 500

#endpoint para verificar se o servidor ligou
@app.route('/ping', methods=["GET"])
def ping():
    return 'OK', 200


if __name__ == '__main__':
    print("Iniciando servidor de reconstrução de imagens...")
    print("Endpoints disponíveis:")
    print("  POST /reconstruir - Processa imagem")
    print("  GET /desempenho - Monitora recursos")
    app.run(host='0.0.0.0', port=5000, threaded=True)