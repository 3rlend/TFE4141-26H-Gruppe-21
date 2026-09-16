from math import log, ceil

def RSA(M: int, e: int, n: int) -> int:

    # prepares M and x for Montgomery Product
    M_bar = M * r % n
    x_bar = r % n 

    # RSA loop with Montgomery Prdoduct
    for i in range (k - 1, -1, -1):
        x_bar = MonPro(x_bar, x_bar)
        if (e >> i) & 1: # Check for odd
            x_bar = MonPro(x_bar, M_bar)
    return MonPro(x_bar, 1)

def MonPro(A: int, B: int) -> int:
    t = A * B
    # Black magic modulo hack for powers of two
    # x & [pow(2,n) - 1] == x [mod pow(2,n)]
    m = (t * n_prime) & (r - 1) 
    # Since r = 2^k can skip division by right-shifting bits a k-amount
    u = (t + m * n) >> k 
    if u >= n:
        return u - n
    return u


# Finding n_prime for the Montgomery Product
def compute_n_prime(n: int) -> int: 
    temp = 1
    for i in range(k - 1):
        temp = (temp * (2 - n * temp)) & (r - 1)
    return (-temp) & (r - 1)

n = 3233
plaintext = 90
e = 17
d = 413

k = int(ceil(log(n, 2)))
r = 1 << k

n_prime = compute_n_prime(n)

cypher_result = RSA(plaintext, e, n)

print("RSA-test:")
print("C =",cypher_result)
plaintext_result = RSA(cypher_result, d, n)
print("M =",plaintext_result)

print()

print("Verified with simple RSA")
cypher_result = pow(plaintext, e, n)
print("C =",cypher_result)
plaintext_result = pow(cypher_result, d, n) 
print("M =",plaintext_result)

