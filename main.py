# # main.py
# import cliente
# import servidor
# import time
# import random
# import threading

# def iniciar_servidor():
#     servidor.app.run(port=5000)

# # Inicia o servidor em uma thread separada (precisa pois o app.run é bloqueante )
# thread_servidor = threading.Thread(target=iniciar_servidor, daemon=True)
# thread_servidor.start()

# # Aguarda um pouco para o servidor iniciar
# time.sleep(1)

# # Envia sinais
# for _ in range(5):
#     cliente.enviar_sinal()
#     time.sleep(random.uniform(1, 3))
