import matplotlib.pyplot as plt
import numpy as np
import random

p = 170141183460469231731687303716007562651
q = 170141183460469231731687303716871760241
n = p*q
phi = (p-1)*(q-1)
e = 65537
d = pow(e, -1, phi)
k = n.bit_length()
 
# def compute_r2(n: int) -> int:
#     r2 = 1
#     for i in range(2 * k):
#         r2 <<= 1            # double the value (left shift by one bit)
#         if r2 >= n:         # keep the value in the range [0, n)
#             r2 -= n
#     return r2
#
#
# def RSA(M: int, e: int, n: int, r2: int) -> int:
#     M_bar = MonPro(M, r2, n)
#     x_bar = M_bar
#     for i in range(e.bit_length() - 2, -1, -1):
#         x_bar = MonPro(x_bar, x_bar, n)        # square (every bit)
#         if (e >> i) & 1:                       # bit i of e is 1:
#             x_bar = MonPro(x_bar, M_bar, n)    # multiply by M_bar
#     return MonPro(x_bar, 1, n)
#
#
# def MonPro(A: int, B: int, n: int) -> int:
#     S = 0                           # partial sum (S register in hardware)
#     BN = B + n
#
#     for i in range(k):              # k = 256 iterations, one per bit of A
#         a_i = (A >> i) & 1          # current bit of A: radix 2 means 1 bit per step
#         q_i = (S + a_i * B) & 1
#
#         # 4:1 mux selecting what to add, controlled by (a_i, q_i):
#         if a_i and q_i:
#             S += BN                 # (1, 1): add B + n
#         elif a_i:
#             S += B                  # (1, 0): add B
#         elif q_i:
#             S += n                  # (0, 1): add n
#         S >>= 1                     # exact division by 2 (sum is always even here)
#     if S >= n:
#         S -= n
#     return S
 
 

def compute_r2(n: int) -> (int, int):
    cycle = 0
    r2 = 1
    for i in range(2 * k):
        r2 <<= 1            
        cycle = cycle + 1
        if r2 >= n:         
            r2 -= n
            cycle = cycle + 8
    return r2, cycle

def RSA(M: int, e: int, n: int, r2: int) -> (int, int):
    addr = 0
    M_bar, addr_temp = MonPro(M, r2, n)
    addr = addr + addr_temp
    x_bar = M_bar
    for i in range(e.bit_length() - 2, -1, -1):
        x_bar, addr_temp = MonPro(x_bar, x_bar, n)        
        addr = addr + addr_temp
        if (e >> i) & 1:                       
            x_bar, addr_temp = MonPro(x_bar, M_bar, n)    
            addr = addr + addr_temp
    x_bar, addr_temp = MonPro(x_bar, 1, n)
    addr = addr + addr_temp
    return (x_bar, addr)

def MonPro(A: int, B: int, n: int) -> (int, int):
    S = 0                       
    BN = B + n
    addr = 8;
    for i in range(k):           
        a_i = (A >> i) & 1        
        q_i = (S + a_i * B) & 1
        if a_i and q_i:
            addr = addr + 8
            S += BN                
        elif a_i:
            addr = addr + 8
            S += B                  
        elif q_i:
            addr = addr + 8
            S += n                 
        S >>= 1                     
        addr = addr + 1
    if S >= n:
        addr = addr + 8
        S -= n
    return (S, addr)


def mean(arr):
    return sum(arr) // len(arr)
        



AMOUNT_OF_MESSAGES = 100

msg_src = []
msg_enc = []
addr_enc = []
msg_dec = []
addr_dec = []

 
r2, r2_cycles = compute_r2(n)    # once per key: shared by encryption and decryption

 
n_minus_one = n - 1

for i in range(AMOUNT_OF_MESSAGES):
    num = random.randint(0, n_minus_one)
    enc, addr = RSA(num,e,n,r2)
    msg_enc.append(enc)
    addr_enc.append(addr)
    dec, addr = RSA(enc,d,n,r2)
    msg_dec.append(dec)
    addr_dec.append(addr)
    print(i,"/",AMOUNT_OF_MESSAGES)
    assert num == dec

addr_dec.sort()
addr_enc.sort()


print()

e_b = bin(e)
d_b = bin(d)

print(e_b)
print(d_b)

print()
print("############################################")


print("Max for encoding =", max(addr_enc))
print("Snitt for encoding =", mean(addr_enc))
print("Min for encoding =", min(addr_enc))

print()
print("Max for decoding =", max(addr_dec))
print("Snitt for decoding =", mean(addr_dec))
print("Min for decoding =", min(addr_dec))
print()
print("for R^2 % n",r2_cycles)
print("############################################")



prev = 0
unique_amnt = -1
normal_dist_x = []
normal_dist_y = []
for i in addr_enc:
    if i != prev:
        prev = i
        unique_amnt = unique_amnt + 1
        normal_dist_x.append(i)
        normal_dist_y.append(1)
    else:
        normal_dist_y[unique_amnt] += 1
    
    
plt.plot(normal_dist_x, normal_dist_y)
plt.xlabel("Cycles")
plt.ylabel("Occurences")
plt.title("Normal distribution of cycle amount")
plt.grid(True)
plt.show()



prev = 0
unique_amnt = -1
normal_dist_x = []
normal_dist_y = []
for i in addr_dec:
    if i != prev:
        prev = i
        unique_amnt = unique_amnt + 1
        normal_dist_x.append(i)
        normal_dist_y.append(1)
    else:
        normal_dist_y[unique_amnt] += 1
    
    
plt.plot(normal_dist_x, normal_dist_y)
plt.xlabel("Cycles")
plt.ylabel("Occurences")
plt.title("Normal distribution of cycle amount")
plt.grid(True)
plt.show()









