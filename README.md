# Ultrassom Inverso - Reconstrução de Imagens via CGNR

Este projeto implementa um sistema cliente-servidor para reconstrução de imagens de ultrassom utilizando métodos baseados em problemas inversos, especificamente o algoritmo CGNR. O sistema é composto por um servidor responsável pela reconstrução das imagens e um cliente que envia sinais e recebe as imagens reconstruídas, gerando relatórios de desempenho e resultados.

## Estrutura dos Arquivos

- **cgnr.py**: Implementa o algoritmo CGNR para reconstrução de imagens a partir dos sinais e da matriz do modelo. [Ver código](./cgnr.py)
- **server.py**: Implementa o servidor que recebe os dados do cliente, executa a reconstrução usando o CGNR e retorna a imagem reconstruída junto com metadados. [Ver código](./server.py)
- **client.py**: Implementa o cliente que seleciona aleatoriamente sinais, usuário, ganho e modelo, envia ao servidor, recebe a imagem reconstruída e gera relatórios. [Ver código](./client.py)
- **Dockerfile**: Permite a criação de containers Docker para rodar tanto o cliente quanto o servidor.
- **Data/**: Pasta contendo os arquivos CSV de sinais e matrizes modelo para os testes.

## Funcionamento do Sistema

### 1. Algoritmo CGNR ([cgnr.py](./cgnr.py))
O arquivo `cgnr.py` define a função `cgnr(g, H, iter_max, tol)` que resolve o problema inverso de reconstrução de imagem a partir do sinal `g` e da matriz do modelo `H`. O algoritmo itera até que o erro seja menor que o tolerado ou até atingir o número máximo de iterações, retornando a imagem reconstruída e o número de iterações executadas.

### 2. Servidor ([server.py](./server.py))
O servidor escuta conexões TCP, recebe os dados do cliente (usuário, sinal, matriz modelo, parâmetros), executa a reconstrução de imagem usando o CGNR e retorna ao cliente a imagem reconstruída e metadados como usuário, algoritmo, datas de início/fim, tamanho e número de iterações. O servidor pode ser executado em container Docker.

### 3. Cliente ([client.py](./client.py))
O cliente seleciona aleatoriamente usuário, ganho de sinal, modelo e sinal, envia ao servidor, recebe a imagem reconstruída, salva a imagem em arquivo PNG e gera dois relatórios:
- `relatorio_imagens.txt`: informações de cada imagem reconstruída (usuário, algoritmo, tempo, iterações, etc).
- `relatorio_desempenho.txt`: log de uso de CPU e memória durante a execução.
O cliente também pode ser executado em container Docker.

## Como Utilizar

### Pré-requisitos
- Docker instalado
- Pasta `Data/` com os arquivos CSV necessários (H-1.csv, G-1.csv, etc.) no mesmo diretório do código

### 1. Build da Imagem Docker
Abra o terminal na pasta do projeto e execute:
```bash
docker build -t ultrassom-cgnr .
```

### 2. Rodar o Servidor
```bash
docker run --rm -it --name servidor -p 5001:5001 -v "$PWD/Data:/app/Data" ultrassom-cgnr python server.py
```

### 3. Rodar o Cliente (em outro terminal)
```bash
docker run --rm -it --name cliente --network host -v "$PWD/Data:/app/Data" ultrassom-cgnr python client.py
```
Obs: Se não estiver usando Linux, ajuste a opção de rede conforme necessário (ex: `--network=host` pode não funcionar no Windows/Mac, use o IP do host).

### 4. Resultados
- Imagens reconstruídas serão salvas como PNG no diretório do container (mapeado para o host se usar `-v`).
- Relatórios `relatorio_imagens.txt` e `relatorio_desempenho.txt` serão gerados no mesmo diretório.

## Observações
- O servidor aceita múltiplas conexões sequenciais.
- O cliente envia três sinais aleatórios por execução.
- O código pode ser adaptado para outros algoritmos de reconstrução, bastando alterar a chamada no `server.py`.

## Referências de Código
- Algoritmo CGNR: [cgnr.py](./cgnr.py)
- Servidor: [server.py](./server.py)
- Cliente: [client.py](./client.py)

---

Dúvidas ou sugestões? Abra uma issue!
