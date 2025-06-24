# Dockerfile para rodar tanto cliente quanto servidor
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install numpy matplotlib pillow psutil
EXPOSE 5001
CMD ["bash"]
# Para rodar o servidor: python server.py
# Para rodar o cliente: python client.py
