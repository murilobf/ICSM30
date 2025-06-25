    # servidor.py
from flask import Flask, request, jsonify, send_file, make_response
import time
import numpy as np
import psutil
import io
from PIL import Image
import algoritmos

app = Flask(__name__)

@app.route('/reconstruir', methods=['POST'])
def reconstruir():
    data = request.json
    usuario = data['usuario']
    modelo = data['modelo']
    sinal = data['sinal']

    start_time = time.time()

    print("testeH")
    H = np.loadtxt(modelo, delimiter=',', dtype=np.float64)
    print("testeg")
    g = np.loadtxt(sinal, delimiter=',', dtype=np.float64)
    print("testecgnr")
    f,iteracoes = algoritmos.cgnr(g,H,100)
    
    # Simulando geração de imagem (matriz convertida em imagem)
    lado = int(np.sqrt(len(f)))  # tentar fazer quadrada
    imagem = f[:lado*lado].reshape((lado, lado), order='F')


    '''lado = int(np.ceil(np.sqrt(len(f))))
    imagem = np.zeros((lado, lado))
    imagem.flat[:len(f)] = f  # Preenche imagem com os dados'''
    imagem = Image.fromarray(imagem.astype('uint8'))


    img_bytes = io.BytesIO()
    imagem.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    tempo = time.time() - start_time

    response = make_response(send_file(img_bytes, mimetype='image/png', download_name='reconstruida.png'))
    response.headers['X-Usuario'] = usuario
    response.headers['X-Iteracoes'] = str(iteracoes)
    response.headers['X-Tempo'] = str(tempo)
    
    return response

@app.route('/desempenho', methods=['GET'])
def desempenho():
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    return jsonify({
        'cpu_percent': cpu,
        'mem_percent': mem.percent
    })

if __name__ == '__main__':
    app.run(port=5000)
