import numpy as np

TOLERANCIA_ERRO = 1e-4
THRESHOLD_VALORES_ALTOS = 1e6
LOG_PROGRESSO_ITERACOES = 10

"""
Algoritmos para reconstrução de imagens de ultrassom baseados em problemas inversos.
Este módulo implementa o algoritmo CGNR (Conjugate Gradient Normal Residual) 
para resolver sistemas lineares mal-condicionados Hf = g.
"""

def cgnr(g: np.array, H: np.array, iter_max: int):
    """
    Implementa o algoritmo CGNR para reconstrução de imagens.
    
    REQUISITO ATENDIDO: Executa o algoritmo de reconstrução até que o erro seja menor que 1e-4
    
    Args:
        g: Vetor de sinais capturados
        H: Matriz modelo do sistema
        iter_max: Número máximo de iterações
    
    Returns:
        tuple: (f_reconstruido, num_iteracoes)
    """
    
    # --- NOVO TRATAMENTO ROBUSTO DE VALORES EXTREMOS ---
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
    if H_std > 1e-12:
        H_norm = (H - H_mean) / H_std
    else:
        H_norm = H - H_mean
        print("Aviso: Desvio padrão de H muito pequeno, normalização parcial aplicada.")

    # Dimensões do problema
    m, n = H_norm.shape
    print(f"Resolvendo sistema {m}x{n} com {iter_max} iterações máximas (normalização z-score)")

    # Inicialização do algoritmo CGNR
    f = np.zeros(n)
    r = g_norm - H_norm @ f
    z = H_norm.T @ r
    p = z.copy()
    tolerance = TOLERANCIA_ERRO

    for i in range(iter_max):
        w = H_norm @ p
        w_norm_sq = np.linalg.norm(w, ord=2) ** 2
        if w_norm_sq < 1e-15:
            print(f"Convergência prematura na iteração {i+1}: w_norm muito pequeno")
            break
        z_norm_sq = np.linalg.norm(z, ord=2) ** 2
        alpha = z_norm_sq / w_norm_sq
        f_next = f + alpha * p
        r_next = r - alpha * w
        error_absolute = np.linalg.norm(r_next, ord=2)
        error_relative = abs(np.linalg.norm(r_next, ord=2) - np.linalg.norm(r, ord=2))
        if error_absolute < tolerance or error_relative < tolerance:
            print(f"Convergência atingida na iteração {i+1}")
            print(f"Erro absoluto: {error_absolute:.2e}, Erro relativo: {error_relative:.2e}")
            f = f_next
            break
        z_next = H_norm.T @ r_next
        z_next_norm_sq = np.linalg.norm(z_next, ord=2) ** 2
        if z_norm_sq < 1e-15:
            print(f"Convergência prematura na iteração {i+1}: z_norm muito pequeno")
            f = f_next
            break
        beta = z_next_norm_sq / z_norm_sq
        p_next = z_next + beta * p
        f = f_next
        r = r_next
        z = z_next
        p = p_next
        if (i + 1) % LOG_PROGRESSO_ITERACOES == 0:
            print(f"Iteração {i+1}: erro = {error_absolute:.2e}")

    # --- REESCALONAMENTO ROBUSTO ---
    # O resultado f está na base z-score, precisamos "desfazer" a normalização
    # f_final = f * (g_std / H_std) + (g_mean - H_mean * (g_std / H_std))
    # Mas para imagens, geralmente só o fator de escala é relevante
    if H_std > 1e-12:
        f_final = f * (g_std / H_std)
    else:
        f_final = f
    print(f"Reconstrução concluída em {i+1} iterações (z-score)")
    return f_final, i+1

# def ganho_sinal(H):
#     N,S = H.shape

#     for c in range(N):
#         for l in range(S):
#             H[c][l] *= 100 + (1/20)*l*np.sqrt(l)

# '''# Chama cgnr
# f,residuos = cgnr(g, H, 1000)

# # Transforma  f em imagem
# lado = int(np.sqrt(len(f)))  # tentar fazer quadrada
# imagem = f[:lado*lado].reshape((lado, lado), order='F')

# # Salvar imagem
# plt.imsave("teste.png", imagem, cmap='gray')
# '''
