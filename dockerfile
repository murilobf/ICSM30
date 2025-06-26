# DOCKERFILE PARA SISTEMA DE RECONSTRUÇÃO DE IMAGENS DE ULTRASSOM
# Este container permite execução tanto do servidor quanto do cliente

FROM python:3.9-slim

# Atualiza pacotes e instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python necessárias para o projeto
RUN pip install --no-cache-dir \
    flask \
    requests \
    pillow \
    psutil \
    numpy \
    matplotlib

# Define diretório de trabalho
WORKDIR /app

# Copia todos os arquivos do projeto
COPY . /app

# Cria script de entrada
RUN echo '#!/bin/bash\n\
if [ "$1" = "servidor" ]; then\n\
    echo "Iniciando servidor..."\n\
    python servidor.py\n\
elif [ "$1" = "cliente" ]; then\n\
    echo "Iniciando cliente..."\n\
    python cliente.py\n\
else\n\
    echo "Uso: docker run <imagem> servidor|cliente"\n\
    echo "Exemplo para servidor: docker run -p 5000:5000 <imagem> servidor"\n\
    echo "Exemplo para cliente: docker run <imagem> cliente"\n\
fi' > /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Expõe a porta do servidor Flask
EXPOSE 5000

# Define o script de entrada
ENTRYPOINT ["/app/entrypoint.sh"]

# Por padrão, inicia o servidor
CMD ["servidor"]