import numpy as np
import matplotlib.pyplot as plt

H = np.loadtxt('Dados/H-2.csv', delimiter=',', dtype=np.float64)
g = np.loadtxt('Dados/g-30x30-2.csv', delimiter=',', dtype=np.float64)

#Função para cgnr
def cgnr(g: np.array, H: np.array, iter_max: int):
    
    #Pra pegar a quantidade de colunas de H pra usar no f
    m, n = H.shape

    #O código abaixo é uma "tradução" do cgnr dado pelo professor para código
    f = np.zeros(n)
    r = g - np.matmul(H, f)
    z = np.matmul(H.transpose(), r)
    p = z

    for i in range(iter_max):
        w = np.matmul(H, p)
        alpha = (np.linalg.norm(z, ord=2))**2 / (np.linalg.norm(w, ord=2))**2
        f_next = f + alpha * p
        r_next = r - alpha * w

        error = abs(np.linalg.norm(r_next, ord=2) - np.linalg.norm(r, ord=2))
        print ('Erro no ciclo ' + str(i) + ':')
        print (error)
        if (error < 0.00001):
            return f_next, i+1

        z_next = np.matmul(np.transpose(H), r_next)
        beta = (np.linalg.norm(z_next))**2 / (np.linalg.norm(z))**2
        p_next = z_next + beta * p

        f = f_next
        r = r_next
        z = z_next
        p = p_next

    return f, i+1

# Chama cgnr
f,residuos = cgnr(g, H, 1000)

# Transforma  f em imagem
lado = int(np.sqrt(len(f)))  # tentar fazer quadrada
imagem = f[:lado*lado].reshape((lado, lado), order='F')

# Salvar imagem
plt.imsave("teste.png", imagem, cmap='gray')
