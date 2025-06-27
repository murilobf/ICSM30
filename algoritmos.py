import numpy as np


# Definições de constantes
# Estabelece o critério de parada para o algoritmo,
# conforme o requisito funcional de que o erro (ϵ) seja menor que 1e-4
TOLERANCIA_ERRO = 1e-4
# frequência com que o progresso da convergência é impresso no console
LOG_PROGRESSO_ITERACOES = 10

def cgnr(g: np.array, H: np.array, iter_max: int):
    """
    Implementa o algoritmo CGNR para reconstrução de imagens.
    
    Args:
        g: Vetor de sinais capturados
        H: Matriz modelo do sistema
        iter_max: Número máximo de iterações
    
    Returns:
        tuple: (f_reconstruido, num_iteracoes)
    """
    
    # Normalização z-score para g
    g_mean = np.mean(g)
    g_std = np.std(g)
    if g_std > 1e-12:
        g_norm = (g - g_mean) / g_std
    else:
        g_norm = g - g_mean
        print("Aviso: Desvio padrão de g muito pequeno, normalização parcial aplicada.")

    # Normalização z-score para H
    H_mean = np.mean(H)
    H_std = np.std(H)
    # Normaliza H apenas se o desvio padrão for significativo
    # Isso evita problemas numéricos com matrizes mal condicionadas
    # Se H_std for muito pequeno, não normaliza para evitar divisão por zero
    # e apenas subtrai a média
    if H_std > 1e-12:
        H_norm = (H - H_mean) / H_std
    else:
        H_norm = H - H_mean
        print("Aviso: Desvio padrão de H muito pequeno, normalização parcial aplicada.")

    # Dimensões do problema
    m, n = H_norm.shape
    print(f"Resolvendo sistema {m}x{n} com {iter_max} iterações máximas (normalização z-score)")

    # Inicialização do algoritmo CGNR
    # Inicializa o vetor de solução f que será a reconstrução da imagem
    f = np.zeros(n)
    # Inicializa o vetor de resíduos r (erro) como a diferença entre g normalizado e H normalizado aplicado a f
    r = g_norm - H_norm @ f
    # Inicializ o vetor z como o produto transposto de H normalizado e r
    z = H_norm.T @ r
    # Inicializa o vetor de direção p como uma cópia de z
    # Isso é necessário para o primeiro passo do algoritmo CGNR
    # p é a direção de descida do gradiente
    # e é atualizado a cada iteração
    p = z.copy()

    # Implementação do algoritmo CGNR
    for i in range(iter_max):
        # Calcula w = H*p (produto matriz-vetor)
        w = H_norm @ p
        
        # Calcula  (||w||²)
        # Usado para calcular o passo ótimo alpha
        w_norm_sq = np.linalg.norm(w, ord=2) ** 2
            
        # Calcula  (||z||²)
        z_norm_sq = np.linalg.norm(z, ord=2) ** 2
        
        # Calcula o tamanho do passo alpha = ||z||²/||w||²
        alpha = z_norm_sq / w_norm_sq
        
        # Atualiza a solução: f_next = f + alpha*p
        f_next = f + alpha * p
        
        # Atualiza o vetor resíduo: r_next = r - alpha*w
        r_next = r - alpha * w
        
        # Calcula o erro absoluto como a norma do resíduo atual
        error_absolute = np.linalg.norm(r_next, ord=2)
        
        # Calcula o erro relativo como a mudança na norma do resíduo
        error_relative = abs(error_absolute - np.linalg.norm(r, ord=2))
        
        # Verifica critério de convergência: se erro < tolerância, interrompe o loop
        # REQUISITO ATENDIDO: Executa o algoritmo de reconstrução até que o erro seja menor que 1e-4
        if error_absolute < TOLERANCIA_ERRO or error_relative < TOLERANCIA_ERRO:
            print(f"Convergência atingida na iteração {i+1}")
            print(f"Erro absoluto: {error_absolute:.2e}, Erro relativo: {error_relative:.2e}")
            f = f_next
            break
            
        # Calcula z_next = H^T * r_next para a próxima iteração
        z_next = H_norm.T @ r_next
        z_next_norm_sq = np.linalg.norm(z_next, ord=2) ** 2
            
        # Calcula o parâmetro beta = ||z_next||²/||z||² para a próxima direção conjugada
        beta = z_next_norm_sq / z_norm_sq
        
        # Atualiza a direção de busca p para a próxima iteração
        # p_next = z_next + beta*p (fórmula de Fletcher-Reeves)
        p_next = z_next + beta * p
        
        # Atualiza as variáveis para a próxima iteração
        f = f_next
        r = r_next
        z = z_next
        p = p_next
        
        # Exibe progresso a cada LOG_PROGRESSO_ITERACOES iterações
        if (i + 1) % LOG_PROGRESSO_ITERACOES == 0:
            print(f"Iteração {i+1}: erro = {error_absolute:.2e}")

    # Reescalonamento do resultado
    # A normalização z-score alterou a escala do problema
    # Para obter a solução na escala original, precisamos reverter a normalização
    # Apenas o fator de escala é considerado importante para imagens
    if H_std > 1e-12:
        f_final = f * (g_std / H_std)
    else:
        f_final = f
        
    print(f"Reconstrução concluída em {i+1} iterações (z-score)")
    return f_final, i+1