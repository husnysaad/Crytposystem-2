
import random

# Function to check if a number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Function to find a random prime of a specified bit length
def random_prime(bits):
    while True:
        num = random.getrandbits(bits)
        # Ensure the number is odd
        if num % 2 == 0:
            num += 1
        if is_prime(num):
            return num

# Generate two large primes of 256
p = random_prime(256)
q = random_prime(256)
n = p * q

print("Prime p:", p)
print("Prime q:", q)
print("Modulus n (p*q):", n)
print("Bit length of n:", n.bit_length())


