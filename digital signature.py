
# Function to check if a number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Square-and-Multiply algorithm for efficient modular exponentiation
def square_and_multiply(base, exponent, modulus):
    result = 1
    base = base % modulus  # Ensure base is within the modulus
    while exponent > 0:
        if exponent % 2 == 1:  # If the exponent is odd, multiply result by base
            result = (result * base) % modulus
        base = (base * base) % modulus  # Square the base
        exponent //= 2  # Shift exponent right by 1 (i.e., divide by 2)
    return result

# Custom hash function
def hash_function(message):
    def string_to_ascii(msg):
        return [ord(char) for char in msg]

    def pad_message(ascii_vals):
        length = len(ascii_vals)
        padding_length = (16 - (length % 16)) % 16
        return ascii_vals + [0] * padding_length

    def split_into_blocks(padded_msg):
        return [padded_msg[i:i + 16] for i in range(0, len(padded_msg), 16)]

    def initialize_hash_values():
        return [0x12345678, 0x9ABCDEF0, 0xFEDCBA98, 0x76543210]

    def process_block(block, hash_vals):
        W0 = (block[0] + (block[1] << 8) + (block[2] << 16) + (block[3] << 24))
        W1 = (block[4] + (block[5] << 8) + (block[6] << 16) + (block[7] << 24))
        W2 = (block[8] + (block[9] << 8) + (block[10] << 16) + (block[11] << 24))
        W3 = (block[12] + (block[13] << 8) + (block[14] << 16) + (block[15] << 24))

        hash_vals[0] = (hash_vals[0] + W0) ^ (W1 >> 3)
        hash_vals[1] = (hash_vals[1] + W1) ^ (W2 << 5)
        hash_vals[2] = (hash_vals[2] + W2) ^ (W3 >> 7)
        hash_vals[3] = (hash_vals[3] + W3) ^ (W0 << 11)

    ascii_vals = string_to_ascii(message)
    padded_msg = pad_message(ascii_vals)
    blocks = split_into_blocks(padded_msg)
    
    hash_vals = initialize_hash_values()
    
    for block in blocks:
        process_block(block, hash_vals)

    return ''.join(f'{h:08X}' for h in hash_vals)

# RSA signing and verification
def rsa_sign(message_hash, d, n):
    message_hash_numeric = int(message_hash, 16)
    signature = square_and_multiply(message_hash_numeric, d, n)
    return signature

def rsa_verify(signature, e, n, original_message_hash):
    decrypted_hash = square_and_multiply(signature, e, n)
    original_message_hash_numeric = int(original_message_hash, 16)
    return decrypted_hash == original_message_hash_numeric

# Example RSA key setup
p = 1313416836674735187140116209725943102937238644133  # Large prime 1
q = 1038734841305824333585135750546863280513918895879  # Large prime 2
n = p * q  # RSA modulus
phi_n = (p - 1) * (q - 1)  # Euler's totient function phi(n)

e = 65537  # Commonly used public exponent
d = pow(e, -1, phi_n)  # Private key

# Message
message = "Exams are on red USB drive in JO 18.103. Password is CaKe314."

# Hash the message
message_hash = hash_function(message)

# Sign the message hash
signature = rsa_sign(message_hash, d, n)

# Debug information
print("Message Hash:", message_hash)
print("Signature:", signature)

# Verify the signature
is_valid = rsa_verify(signature, e, n, message_hash)
print("Signature valid?", is_valid)

# Debug output to check values
decrypted_hash = square_and_multiply(signature, e, n)
print("Decrypted Hash:", f"{decrypted_hash:X}")
print("Original Hash:", message_hash)


