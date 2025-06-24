import numpy as np

def cgnr(g: np.array, H: np.array, iter_max: int, tol: float = 1e-5):
    m, n = H.shape
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
        if (error < tol):
            return f_next, i+1
        z_next = np.matmul(np.transpose(H), r_next)
        beta = (np.linalg.norm(z_next))**2 / (np.linalg.norm(z))**2
        p_next = z_next + beta * p
        f = f_next
        r = r_next
        z = z_next
        p = p_next
    return f, i+1
