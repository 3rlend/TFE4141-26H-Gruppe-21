from math import log, ceil
import matplotlib.pyplot as plt


def RSA(M: int, e: int, n: int, k: int) -> (int, int):
    r = 1 << k 
    # R = 2^k
    r_mod_n = r - n
    additions = 1
    r2_mod_n = (1 << k) - n
    for i in range(k):
        r2_mod_n = r2_mod_n << 1
        if r2_mod_n >= n:
            r2_mod_n = r2_mod_n - n
            additions = additions + 1
    # prepares M and x for Montgomery Product
    # M_bar = (M * r_mod_n) % n
    M_bar, add_temp = MonPro(M, r2_mod_n, n, k, additions) 
    additions = additions + add_temp

    # RSA loop with Montgomery Prdoduct
    for i in range (k - 1, -1, -1):
        r_mod_n, add_temp = MonPro(r_mod_n, r_mod_n, n, k, additions)
        additions = additions + add_temp
        if (e >> i) & 1: # Check for odd
            r_mod_n, add_temp = MonPro(r_mod_n, M_bar, n, k, additions)
            additions = additions + add_temp
    r_mod_n, add_temp = MonPro(r_mod_n, 1, n, k, additions)
    additions = additions + add_temp
    return r_mod_n, additions

def MonPro(A: int, B: int, n: int, k: int, additions: int) -> (int, int):
    u = 0
    for i in range(k):
        A_i = A >> i & 1
        u = u + (B * A_i) # Allowed since A_i is either 1 or 0
        additions = additions + 1
        if u & 1: 
            u = u + n
            additions = additions + 1
        u = u >> 1
    if u >= n:
        u = u - n
        additions = additions + 1
    return u, additions


n = 3233
plaintext = 90
e = 17
d = 413

k = int(ceil(log(n, 2)))

cypher_result, additions = RSA(plaintext, e, n, k)

print("RSA-test:")
print("C =",cypher_result, "Additions =", additions)
additions = 0
plaintext_result, additions = RSA(cypher_result, d, n, k)
print("M =",plaintext_result, "Additions =", additions)

print()
cypher_result, additions = RSA(plaintext, e, n, k)
print("C =",cypher_result, "Additions =", additions)
additions = 0

print()

print("Verified with simple RSA")
cypher_result = pow(plaintext, e, n)
print("C =",cypher_result)
plaintext_result = pow(cypher_result, d, n) 
print("M =",plaintext_result)










