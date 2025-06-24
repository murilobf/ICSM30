import socket
import pickle
import random
import time
import os
import psutil
import threading
import numpy as np
from datetime import datetime
from PIL import Image

# Configurações
SERVER_HOST = os.environ.get('SERVER_HOST', 'server')
SERVER_PORT = int(os.environ.get('SERVER_PORT', 5001))
DATA_DIR = 'Data'
USERS = ['alice', 'bob', 'carol', 'dave']
MODELS = [
    {'H': 'H-1.csv', 'signals': ['G-1.csv', 'G-2.csv', 'A-60x60-1.csv'], 'size': 60},
    {'H': 'H-2.csv', 'signals': ['g-30x30-1.csv', 'g-30x30-2.csv', 'A-30x30-1.csv'], 'size': 30}
]

relatorio_imgs = []

# Função para monitorar desempenho
performance_log = []
def monitor_performance(interval=1, duration=30):
    for _ in range(duration):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        performance_log.append({'timestamp': datetime.now(), 'cpu': cpu, 'mem': mem})
        time.sleep(interval)

# Thread para monitorar desempenho
perf_thread = threading.Thread(target=monitor_performance)
perf_thread.start()

for i in range(3):
    user = random.choice(USERS)
    gain = random.uniform(0.8, 1.2)
    model = random.choice(MODELS)
    H = np.loadtxt(os.path.join(DATA_DIR, model['H']), delimiter=',')
    signal_file = random.choice(model['signals'])
    g = np.loadtxt(os.path.join(DATA_DIR, signal_file), delimiter=',') * gain
    payload = {
        'user': user,
        'gain': gain,
        'model': model['H'],
        'signal_file': signal_file,
        'g': g,
        'H': H,
        'size': model['size'],
        'algoritmo': 'CGNR'
    }
    t0 = datetime.now()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        s.sendall(pickle.dumps(payload))
        data = b''
        while True:
            part = s.recv(4096)
            if not part:
                break
            data += part
    result = pickle.loads(data)
    t1 = datetime.now()
    img_array = result['imagem']
    iters = result['iteracoes']
    start = result['inicio']
    end = result['fim']
    img = Image.fromarray((img_array * 255 / np.max(img_array)).astype(np.uint8))
    img_name = f"img_{i+1}_{user}.png"
    img.save(img_name)
    relatorio_imgs.append({
        'imagem': img_name,
        'usuario': user,
        'iteracoes': iters,
        'inicio': start,
        'fim': end,
        'tamanho': img_array.shape,
        'algoritmo': 'CGNR',
        'tempo_reconstrucao': (t1-t0).total_seconds()
    })
    time.sleep(random.uniform(1, 3))

perf_thread.join()

# Relatório de imagens
with open('relatorio_imagens.txt', 'w') as f:
    for r in relatorio_imgs:
        f.write(str(r) + '\n')

# Relatório de desempenho
with open('relatorio_desempenho.txt', 'w') as f:
    for p in performance_log:
        f.write(str(p) + '\n')
