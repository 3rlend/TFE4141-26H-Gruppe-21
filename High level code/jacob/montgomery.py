from math import log, ceil

def RSA(M: int, e: int, n: int) -> int:
    M_inv = M * r % n
    x_inv = 1 * r % n
    for i in range (k - 1, -1, -1):
        x_inv = MonPro(x_inv, x_inv)
        if (e >> i) & 1:
            x_inv = MonPro(x_inv, M_inv)
    return MonPro(x_inv, 1)

def MonPro(A: int, B: int) -> int:
    t = A * B
    m = (t * n_inv) & (r - 1)
    u = (t + m * n) >> k
    if u >= n:
        return u - n
    return u

def compute_n_prime(n: int) -> int:
    R = 1 << k
    n_prime = 1

    for _ in range(k - 1):
        n_prime = (n_prime * (2 - n * n_prime)) & (r - 1)
    return (-n_prime) & (r - 1)

n = 3233
plaintext = 90
e_key = 17
d_key = 413

k = int(ceil(log(n,2)))
r = 1 << k

n_inv = compute_n_prime(n)


cypher_result = RSA(plaintext, e_key, n)

print("C =",cypher_result)

plaintext_result = RSA(cypher_result, d_key, n)

print("M =",plaintext_result)



print()
print("Verified with simple RSA")
cypher_result = pow(plaintext, e_key, n)
print("C =",cypher_result)
plaintext_result = pow(cypher_result, d_key, n) 
print("M =",plaintext_result)

    
