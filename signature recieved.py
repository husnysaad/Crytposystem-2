
def square_and_multiply(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def hash_function(message):
    # Hashing function
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

def rsa_sign(message_hash, d, n):#alice would sign using her private key
    message_hash_numeric = int(message_hash, 16)
    signature = square_and_multiply(message_hash_numeric, d, n)
    return signature

def rsa_verify(signature, e, n, original_message_hash):
    decrypted_hash = square_and_multiply(signature, e, n)
    original_message_hash_numeric = int(original_message_hash, 16)
    return decrypted_hash == original_message_hash_numeric

def rsa_encrypt(message, e, n):#alice would encrypt with bobs public key
    message_numeric = int(message.encode().hex(), 16)  # Convert message to numeric
    ciphertext = square_and_multiply(message_numeric, e, n)
    return ciphertext

def rsa_decrypt(ciphertext, d, n):#bob would decrypt with alices ppublic key
    decrypted_numeric = square_and_multiply(ciphertext, d, n)
    decrypted_message_hex = hex(decrypted_numeric)[2:]  # Convert to hex and strip '0x'
    return bytes.fromhex(decrypted_message_hex).decode()  # Convert hex back to string

# Alice's RSA key setup
p_a = 1313416836674735187140116209725943102937238644133
q_a = 1038734841305824333585135750546863280513918895879
n_a = p_a * q_a
phi_n_a = (p_a - 1) * (q_a - 1)

e_a = 65537
d_a = pow(e_a, -1, phi_n_a)

# Bob's RSA key setup
p_b = 70679880538383312502071352291856443545915428455819811944250026371670838470319
q_b = 115103074580370081613695071598840503525162509721316244662542820653816484667741
n_b = p_b * q_b
e_b = 7
d_b = pow(e_b, -1, (p_b - 1) * (q_b - 1))

# Message input by Alice
original_message = "Exams are on red USB drive in JO 18.103. Password is CaKe314."

# Encrypt the message using Bob's public key
ciphertext = rsa_encrypt(original_message, e_b, n_b)


# Hash the message
message_hash = hash_function(original_message)

# Sign the message hash with Alice's private key
signature = rsa_sign(message_hash, d_a, n_a)

# Output the message hash and signature
print("Message Hash:", message_hash)
print("Signature:", signature)

# Bob receives the ciphertext and signature
# Decrypt the ciphertext to retrieve the original message
decrypted_message = rsa_decrypt(ciphertext, d_b, n_b)
print("Decrypted Message:", decrypted_message)

# Input for received values from Bob
received_message_hash = input("Enter the received message hash (in hex): ")
received_signature_hash = input("Enter the received signature hash (in hex): ")

# Verify the signature using Alice's public key
is_valid = rsa_verify(signature, e_a, n_a, received_message_hash)

# Output the results
print("Received Message Hash:", received_message_hash)
print("Received Signature Hash:", hex(signature)[2:].upper())
print("Signature valid?", is_valid)

