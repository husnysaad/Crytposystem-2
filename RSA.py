

# RSA encryption and decryption using modular exponentiation with a string as the key

# Step 1: Define the primes and calculate n, phi(n)
p = 70679880538383312502071352291856443545915428455819811944250026371670838470319   # Prime number p > 20
q = 115103074580370081613695071598840503525162509721316244662542820653816484667741   # Prime number q > 20
n = p * q  # RSA modulus n
phi_n = (p - 1) * (q - 1)  # Euler's totient function phi(n)

# Step 2: Choose the public exponent e
e = 17  # Public exponent e must be coprime with phi(n)

# Step 3: Calculate the private key d (modular inverse of e mod phi_n)
d = pow(e, -1, phi_n)

# Step 4: Convert the string "CAKE" to a numeric representation
message = "CAKE"
# Convert each character to its ASCII value and concatenate them
K = int(''.join([str(ord(char)).zfill(3) for char in message]))

# Square and Multiply Algorithm for Modular Exponentiation
def square_and_multiply(base, exponent, modulus):
    result = 1
    base = base % modulus  # Ensure base is within modulus
    while exponent > 0:
        # If exponent is odd, multiply the base with the result
        if (exponent % 2) == 1:
            result = (result * base) % modulus
        # Square the base
        base = (base * base) % modulus
        exponent //= 2  # Divide exponent by 2
    return result

# Step 5: Encrypt K using RSA: C = K^e mod n
C = square_and_multiply(K, e, n)

# Step 6: Decrypt C using RSA: K_decrypted = C^d mod n
K_decrypted = square_and_multiply(C, d, n)

# Step 7: Convert the decrypted numeric value back to the string
# Split the decrypted integer into its ASCII components (each 3 digits)
K_decrypted_str = ''.join([chr(int(str(K_decrypted)[i:i+3])) for i in range(0, len(str(K_decrypted)), 3)])

# Output the results
print("Public Key (n, e):", (n, e))
print("Private Key d:", d)
print("Original Symmetric Key (String):", message)
print("Original Symmetric Key (Numeric K):", K)
print("Encrypted Ciphertext C:", C)
print("Decrypted Symmetric Key (Numeric):", K_decrypted)

