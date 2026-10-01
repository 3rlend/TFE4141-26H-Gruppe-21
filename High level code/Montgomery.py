import random
#Calculating r²mod n, without dividing by n
def compute_r2(n: int) -> int:
    r2 = 1
    for i in range(2 * k): #
        r2 <<= 1
        if r2 >= n:
            r2 -= n
    return r2


def RSA(M: int, e: int, n: int, r2: int) -> int:

    # prepares M and x for Montgomery Product
    M_bar = MonPro(M, r2, n)
    x_bar = M_bar
    # RSA loop with Montgomery Product
    for i in range (e.bit_length() -2, -1, -1):
        x_bar = MonPro(x_bar, x_bar, n)
        if (e >> i) & 1:
            x_bar = MonPro(x_bar, M_bar, n)
    return MonPro(x_bar, 1, n)

def MonPro(A: int, B: int, n: int) -> int:
    S = 0
    BN = B + n                      # regnes ut én gang per MonPro (PREP-tilstand)
    for i in range(k):              # én iterasjon = én klokkesyklus i HW, 256 iterasjoner
        a_i = (A >> i) & 1          # 1 bit av A per runde → radix 2¹ = 2
        q_i = (S + a_i * B) & 1     # gjør summen partall
        if a_i and q_i:
            S += BN
        elif a_i:
            S += B
        elif q_i:
            S += n
        S >>= 1                     # dele på 2
    if S >= n:                      # én sluttsubtraksjon
        S -= n
    return S

n = 3233
plaintext = 90
e = 17
d = 413

# fjernet k = int(ceil(log(n, 2))) fordi k er konstant 256
k = 256
# brukes ikke r = 1 << k

r2 = compute_r2(n)

cypher_result = RSA(plaintext, e, n, r2)

print("RSA-test:")
print("C =",cypher_result)
plaintext_result = RSA(cypher_result, d, n, r2)
print("M =",plaintext_result)

print()

print("Verified with simple RSA")
cypher_result = pow(plaintext, e, n)
print("C =",cypher_result)
plaintext_result = pow(cypher_result, d, n) 
print("M =",plaintext_result)


#256 bit test
for _ in range(20):
    n_test = random.getrandbits(256) | 1 | (1 << 255)   # odde, 256 bit
    M = random.randrange(n_test)
    e_test = random.randrange(1, n_test)
    r2_test = compute_r2(n_test)                         # ny n i hver runde, så ny r2
    assert RSA(M, e_test, n_test, r2_test) == pow(M, e_test, n_test)
print("256-bit tester OK")