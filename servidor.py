    # servidor.py
from flask import Flask, request, jsonify, send_file
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
    ganho = data['ganho']
    sinais = data['sinais']

    start_time = time.time()

    f,iteracoes = algoritmos.cgnr()
    
    # Simulando geração de imagem (matriz convertida em imagem)
    matriz = np.random.rand(128, 128) * 255
    imagem = Image.fromarray(matriz.astype('uint8'))

    img_bytes = io.BytesIO()
    imagem.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    response = {
        'usuario': usuario,
        'modelo': modelo,
        'iteracoes': iteracoes,
        'tempo': time.time() - start_time
    }

    return send_file(img_bytes, mimetype='image/png',
                     download_name='reconstruida.png',
                     headers={
                         'X-Usuario': usuario,
                         'X-Iteracoes': str(iteracoes),
                         'X-Tempo': str(response['tempo'])
                     })

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
