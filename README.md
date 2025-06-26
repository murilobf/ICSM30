# Sistema de Reconstrução de Imagens de Ultrassom

Este projeto implementa um sistema cliente-servidor para reconstrução de imagens de ultrassom usando algoritmos baseados em problemas inversos. O sistema utiliza o algoritmo CGNR (Conjugate Gradient Normal Residual) para resolver sistemas lineares mal-condicionados.

## Características do Sistema

### Servidor
- **Recebe dados para reconstrução**: Endpoint `/reconstruir` aceita dados JSON com modelo, sinal e usuário
- **Carrega modelo dinamicamente**: Suporte para modelos 30x30 e 60x60 pixels
- **Executa algoritmo CGNR**: Iterações até erro < 1e-4
- **Retorna imagem com metadados**: Todos os dados obrigatórios nos headers HTTP
- **Monitoramento de desempenho**: Endpoint `/desempenho` retorna CPU e memória

### Cliente
- **Envios aleatórios**: Intervalos de 1-3 segundos entre requisições
- **Seleção aleatória**: Usuários, modelos e sinais escolhidos automaticamente
- **Relatórios completos**: Informações de reconstrução e desempenho do servidor
- **Tratamento de erros**: Conexões robustas com timeouts

### Algoritmo CGNR Melhorado
- **Pré-condicionamento inteligente**: Detecta valores extremos (>1e6) e aplica escalonamento
- **Normalização robusta**: Proteção contra divisão por zero
- **Convergência rigorosa**: Critério de parada 1e-4 conforme especificação
- **Logs detalhados**: Progresso das iterações e diagnósticos

## Estrutura dos Dados

### Modelos Suportados
- **H-1.csv**: Matriz modelo para imagens 60x60 pixels
- **H-2.csv**: Matriz modelo para imagens 30x30 pixels

### Sinais de Teste
**Para 60x60 pixels:**
- G-1.csv, G-2.csv: Sinais padrão
- A-60x60-1.csv: Sinal com valores altos (requer pré-condicionamento)

**Para 30x30 pixels:**
- g-30x30-1.csv, g-30x30-2.csv: Sinais padrão
- A-30x30-1.csv: Sinal com valores altos (requer pré-condicionamento)

## Metadados das Imagens

Cada imagem reconstruída contém os seguintes metadados nos headers HTTP:

1. **X-Usuario**: Identificação do usuário
2. **X-Algoritmo**: Algoritmo utilizado (cgnr)
3. **X-Inicio**: Data/hora do início da reconstrução
4. **X-Fim**: Data/hora do término da reconstrução
5. **X-Tamanho**: Tamanho em pixels (ex: 60x60)
6. **X-Iteracoes**: Número de iterações executadas
7. **X-Tempo**: Tempo total de processamento em segundos

## Execução de Testes

### Teste Automático de Sinais
Para verificar se o sistema funciona corretamente com todos os sinais (incluindo os problemáticos A-30x30-1.csv e A-60x60-1.csv):

```bash
python teste_sinais.py
```

Este script testa todos os pares modelo-sinal e verifica:
- Carregamento correto dos dados
- Execução do algoritmo CGNR
- Convergência dentro dos parâmetros
- Ausência de valores inválidos (NaN/Inf)

### Teste Manual do Servidor

### Método 1: Execução Local

#### Pré-requisitos
```bash
pip install flask requests pillow psutil numpy matplotlib
```

#### Executar Servidor
```bash
python servidor.py
```
O servidor será iniciado em `http://localhost:5000`

#### Executar Cliente
```bash
python cliente.py
```

### Método 2: Docker (Recomendado)

#### Construir a imagem
```bash
docker build -t ultrassom-sistema .
```

#### Executar Servidor
```bash
docker run -p 5000:5000 ultrassom-sistema servidor
```

#### Executar Cliente (em outro terminal)
```bash
docker run --network="host" ultrassom-sistema cliente
```

### Método 3: Docker Compose
```yaml
version: '3.8'
services:
  servidor:
    build: .
    ports:
      - "5000:5000"
    command: servidor
    
  cliente:
    build: .
    depends_on:
      - servidor
    command: cliente
    network_mode: "host"
```

```bash
docker-compose up
```

## Endpoints da API

### POST /reconstruir
Reconstrói uma imagem a partir dos dados fornecidos.

**Payload:**
```json
{
    "usuario": "Alice",
    "modelo": "Dados/H-1.csv",
    "sinal": "Dados/G-1.csv"
}
```

**Resposta:**
- Imagem PNG no corpo da resposta
- Metadados nos headers HTTP

### GET /desempenho
Retorna informações de desempenho do servidor.

**Resposta:**
```json
{
    "cpu_percent": 15.2,
    "mem_percent": 45.8,
    "timestamp": "2024-12-19 10:30:45"
}
```

## Arquivos de Saída

### Imagens Reconstruídas
- **Formato**: PNG
- **Nomenclatura**: `img_{usuario}_{timestamp}.png`
- **Localização**: Diretório atual

### Relatórios

#### relatorio_imagens.txt
Contém informações detalhadas de cada reconstrução:
```
img_Alice_1703001234.png - Usuario: Alice, Algoritmo: cgnr, Inicio: 2024-12-19 10:30:45, Fim: 2024-12-19 10:30:47, Tamanho: 60x60, Iterações: 25, Tempo: 1.85 s, Modelo: Dados/H-1.csv, Sinal: Dados/G-1.csv
```

#### relatorio_desempenho.txt
Contém métricas de desempenho do servidor:
```
[2024-12-19 10:30:45] CPU: 15.2%, Memória: 45.8%
[2024-12-19 10:30:48] CPU: 22.1%, Memória: 47.2%
```

## Tratamento de Valores Extremos

O sistema detecta automaticamente sinais com valores muito altos (>1e6) como nos arquivos A-30x30-1.csv e A-60x60-1.csv e aplica:

1. **Pré-condicionamento**: Escalonamento baseado no valor máximo
2. **Normalização robusta**: Evita divisão por zero
3. **Reescalonamento**: Restaura escala original no resultado final

## Monitoramento e Logs

### Logs do Servidor
- Informações de inicialização
- Detalhes de processamento de cada requisição
- Métricas de convergência do algoritmo

### Logs do Cliente
- Status de cada envio
- Informações de resposta do servidor
- Dados de desempenho coletados

## Arquitetura

```
Cliente → HTTP POST → Servidor → Algoritmo CGNR → Imagem PNG
   ↓                    ↓
Relatórios         Monitoramento
```

## Requisitos Atendidos

✅ **Servidor:**
1. Recebe dados para reconstrução
2. Carrega modelo conforme parâmetros
3. Executa algoritmo de reconstrução
4. Executa até erro < 1e-4
5. Salva resultado com metadados

✅ **Cliente:**
1. Envia sinais em intervalos aleatórios
2. Parâmetros definidos aleatoriamente
3. Gera relatório de imagens
4. Gera relatório de desempenho

✅ **Metadados obrigatórios:**
1. Identificação do usuário
2. Identificação do algoritmo
3. Data/hora início
4. Data/hora término
5. Tamanho em pixels
6. Número de iterações

## Solução de Problemas

### Erro de Conexão
- Verifique se o servidor está rodando na porta 5000
- Confirme que não há firewall bloqueando a porta

### Valores Extremos
- O sistema automaticamente detecta e trata sinais com valores altos
- Logs indicarão quando pré-condicionamento for aplicado

### Performance
- Use o endpoint `/desempenho` para monitorar recursos
- Ajuste o número de iterações máximas conforme necessário

## Contribuição

Este sistema foi desenvolvido para atender especificamente os requisitos de reconstrução de imagens de ultrassom usando problemas inversos, com foco em robustez e facilidade de uso.