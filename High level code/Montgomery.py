"""
High-level model of RSA modular exponentiation using Montgomery multiplication.
 
Structure (each function corresponds to a hardware block):
  compute_r2() -> precompute unit (or CPU): r^2 mod n, once per key
  RSA()        -> exponentiation core (exp_core + its FSM)
  MonPro()     -> Montgomery product unit (radix-2, bit-serial datapath)
 
Only additions, shifts, comparisons and subtractions are used inside RSA()
and MonPro(): no multiplication and no division/modulo by n. This is what
makes the algorithm suitable for a simple hardware implementation.
 
References:
  C. K. Koc, "RSA Hardware Implementation", RSA Laboratories, 1995, Sec. 7.4
  (bit-serial Montgomery product)
  C. K. Koc, "High-Speed RSA Implementation", RSA Laboratories, 1994
  (left-to-right binary exponentiation with Montgomery products)
"""
 
import random
 
# Operand width in bits. Fixed to 256 to match the hardware (256-bit keys).
k = 256
 
 
def compute_r2(n: int) -> int:
    """
    Compute r^2 mod n = 2^(2k) mod n without any division.
 
    r^2 mod n is needed to convert the message into the Montgomery domain:
        MonPro(M, r^2) = M * r^2 * r^-1 = M * r  (mod n)
 
    Method: start with 1 and double it 2k times. After each doubling, subtract
    n once if the value has become >= n. One subtraction is always enough,
    because if r2 < n before doubling, then 2*r2 < 2n after doubling.
 
    Depends only on n (the key), so it is computed once per key, not per message.
    Hardware: register + left shift (wiring) + subtractor + 2:1 mux + counter,
    about 2k = 512 clock cycles.
    """
    r2 = 1
    for i in range(2 * k):
        r2 <<= 1            # double the value (left shift by one bit)
        if r2 >= n:         # keep the value in the range [0, n)
            r2 -= n
    return r2
 
 
def RSA(M: int, e: int, n: int, r2: int) -> int:
    """
    Compute M^e mod n with left-to-right binary exponentiation
    (square-and-multiply), using Montgomery products for every multiplication.
 
    Encryption and decryption are the same computation:
        encryption: C = M^e mod n   (exponent e, public key)
        decryption: M = C^d mod n   (exponent d, private key)
 
    All intermediate values are kept in the Montgomery domain (x_bar = x * r mod n),
    so the extra factor r^-1 introduced by each MonPro cancels out.
    """
 
    # Convert the message into the Montgomery domain: M_bar = M * r mod n.
    M_bar = MonPro(M, r2, n)
 
    # The most significant 1-bit of e gives x = M, so the accumulator can start
    # directly at M_bar. This also skips all leading zero bits of e
    # (e.g. e = 65537 needs about 19 MonPro calls instead of about 257).
    x_bar = M_bar
 
    # Process the remaining bits of e from the most significant to bit 0.
    # bit_length() - 2 because the top bit has already been handled above.
    for i in range(e.bit_length() - 2, -1, -1):
        x_bar = MonPro(x_bar, x_bar, n)        # square (every bit)
        if (e >> i) & 1:                       # bit i of e is 1:
            x_bar = MonPro(x_bar, M_bar, n)    # multiply by M_bar
 
    # Convert back to the normal domain: x_bar * 1 * r^-1 = x mod n.
    return MonPro(x_bar, 1, n)
 
 
def MonPro(A: int, B: int, n: int) -> int:
    """
    Montgomery product: returns A * B * r^-1 mod n, with r = 2^k.
    Requires A, B < n and n odd.
 
    Radix-2 (bit-serial) version, Koc 1995 Sec. 7.4:
      - One bit of A is processed per iteration (radix 2^1 = 2).
      - Each iteration divides the partial sum by 2 (a 1-bit right shift).
      - After k = 256 iterations the sum has been divided by 2^k = r.
 
    Why it works: n is added whenever the partial sum would be odd. This does
    not change the value modulo n, but makes the sum even so the division by 2
    is exact. With radix 2 this decision is a single bit (q_i), so no
    precomputed n' = -n^-1 mod r is needed.
 
    One loop iteration corresponds to one clock cycle in hardware.
    """
    S = 0                           # partial sum (S register in hardware)
 
    # Precompute B + n once per MonPro (PREP state in hardware).
    # Then each iteration needs only ONE addition: add 0, B, n or B+n,
    # selected by a 4:1 mux. Without BN, adding both B and n would need
    # two additions per bit.
    BN = B + n
 
    for i in range(k):              # k = 256 iterations, one per bit of A
        a_i = (A >> i) & 1          # current bit of A: radix 2 means 1 bit per step
 
        # q_i = 1 if the sum S + a_i*B would be odd. Computed BEFORE the addition:
        # only the lowest bits are needed (in hardware: S0 XOR (a_i AND b0)).
        q_i = (S + a_i * B) & 1
 
        # 4:1 mux selecting what to add, controlled by (a_i, q_i):
        if a_i and q_i:
            S += BN                 # (1, 1): add B + n
        elif a_i:
            S += B                  # (1, 0): add B
        elif q_i:
            S += n                  # (0, 1): add n
                                    # (0, 0): add 0
 
        S >>= 1                     # exact division by 2 (sum is always even here)
 
    # S is now in [0, 2n). One conditional subtraction brings it into [0, n).
    # Hardware: subtractor (S - n) + 2:1 mux selected by the borrow bit.
    if S >= n:
        S -= n
    return S
 
 
# ---------------------------------------------------------------------------
# Small test with textbook-sized numbers
# ---------------------------------------------------------------------------
n = 3233          # modulus (n = p * q = 61 * 53)
plaintext = 90
e = 17            # public exponent
d = 413           # private exponent
 
r2 = compute_r2(n)    # once per key: shared by encryption and decryption
 
cypher_result = RSA(plaintext, e, n, r2)         # encryption: C = M^e mod n
 
print("RSA-test:")
print("C =", cypher_result)
plaintext_result = RSA(cypher_result, d, n, r2)  # decryption: M = C^d mod n
print("M =", plaintext_result)
 
print()
 
# Reference result using Python's built-in modular exponentiation
print("Verified with simple RSA")
cypher_result = pow(plaintext, e, n)
print("C =", cypher_result)
plaintext_result = pow(cypher_result, d, n)
print("M =", plaintext_result)
 
 
# ---------------------------------------------------------------------------
# Random 256-bit tests against Python's pow()
# ---------------------------------------------------------------------------
for _ in range(20):
    n_test = random.getrandbits(256) | 1 | (1 << 255)   # odd, exactly 256 bits
    M = random.randrange(n_test)                         # message M < n
    e_test = random.randrange(1, n_test)                 # exponent 1 <= e < n
    r2_test = compute_r2(n_test)                         # new n each round, so new r2
    assert RSA(M, e_test, n_test, r2_test) == pow(M, e_test, n_test)
