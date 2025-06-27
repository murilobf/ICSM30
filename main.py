# main.py
import cliente
import servidor
import time
import threading
from waitress import serve

def iniciar_servidor():
    serve(servidor.app, host='0.0.0.0', port=5000, threads = 5)

# Inicia o servidor em uma thread separada (precisa pois o app.run é bloqueante )
thread_servidor = threading.Thread(target=iniciar_servidor, daemon=True)
thread_servidor.start()

# Aguarda um pouco para o servidor iniciar
time.sleep(10)

# Envia sinais
cliente.simula_clientes()