import socket
import pickle
import numpy as np
from datetime import datetime
from cgnr import cgnr

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen()
    print('Servidor aguardando conexões...')
    while True:
        conn, addr = s.accept()
        with conn:
            data = b''
            while True:
                part = conn.recv(4096)
                if not part:
                    break
                data += part
            payload = pickle.loads(data)
            user = payload['user']
            gain = payload['gain']
            model = payload['model']
            g = payload['g']
            H = payload['H']
            size = payload['size']
            algoritmo = payload['algoritmo']
            inicio = datetime.now().isoformat()
            f, iters = cgnr(g, H, 1000, tol=1e-4)
            fim = datetime.now().isoformat()
            imagem = f[:size*size].reshape((size, size), order='F')
            result = {
                'imagem': imagem,
                'usuario': user,
                'algoritmo': algoritmo,
                'inicio': inicio,
                'fim': fim,
                'tamanho': imagem.shape,
                'iteracoes': iters
            }
            conn.sendall(pickle.dumps(result))
