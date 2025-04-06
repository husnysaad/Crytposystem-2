
def string_to_ascii(message):
    """Convert a string message to a list of ASCII values."""
    return [ord(char) for char in message]

def pad_message(ascii_values):
    """Pad the message to make its length a multiple of 16 bytes."""
    length = len(ascii_values)
    padding_length = (16 - (length % 16)) % 16  # Calculate how much to pad
    padded_message = ascii_values + [0] * padding_length
    return padded_message

def split_into_blocks(padded_message):
    """Split the padded message into 16-byte blocks."""
    return [padded_message[i:i + 16] for i in range(0, len(padded_message), 16)]

def initialize_hash_values():
    """Initialize the hash values."""
    return [
        0x12345678,  # H0
        0x9ABCDEF0,  # H1
        0xFEDCBA98,  # H2
        0x76543210   # H3
    ]

def process_block(block, hash_values):
    """Process a 16-byte block and update hash values."""
    W0 = (block[0] + (block[1] << 8) + (block[2] << 16) + (block[3] << 24))
    W1 = (block[4] + (block[5] << 8) + (block[6] << 16) + (block[7] << 24))
    W2 = (block[8] + (block[9] << 8) + (block[10] << 16) + (block[11] << 24))
    W3 = (block[12] + (block[13] << 8) + (block[14] << 16) + (block[15] << 24))

    hash_values[0] = (hash_values[0] + W0) ^ (W1 >> 3)
    hash_values[1] = (hash_values[1] + W1) ^ (W2 << 5)
    hash_values[2] = (hash_values[2] + W2) ^ (W3 >> 7)
    hash_values[3] = (hash_values[3] + W3) ^ (W0 << 11)

def hash_function(message):
    """Main hash function to produce a hash digest."""
    ascii_values = string_to_ascii(message)
    padded_message = pad_message(ascii_values)
    blocks = split_into_blocks(padded_message)
    
    hash_values = initialize_hash_values()
    
    for block in blocks:
        process_block(block, hash_values)

    # Combine hash values to produce the final hash output
    final_hash = ''.join(f'{h:08X}' for h in hash_values)  # Convert to hex format
    return final_hash

# Example usage
message = "Exams are on red USB drive in JO 18.103. password is CaKe314."
digest = hash_function(message)
print("Message Digest (Hash):", digest)


