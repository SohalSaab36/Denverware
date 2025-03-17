import random

def gen_key():
    """Generate a random key mapping for encryption."""
    string = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    string_list = list(string)
    shuffled_list = string_list.copy()

    while True:
        random.shuffle(shuffled_list)
        if shuffled_list[-1] != ' ':  # Ensure whitespace is not the last character
            break

    key_mapping = dict(zip(string_list, shuffled_list))  # Create encryption dictionary
    return key_mapping

key = gen_key()  # Generate a key once

def encrypt(data, key):
    """Encrypt the input data using a key dictionary."""
    cipher_text = ''.join(key.get(char, char) for char in data)  # Encrypt with fallback
    key_str = ''.join(key.values())  # Convert key dictionary to a string for saving
    return cipher_text, key_str

def decrypt(data, key_str):
    """Decrypt the input data using a key string."""
    string = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    if len(key_str) != len(string):
        print('❌ Wrong key format!')
        return None

    # Create reverse mapping from the key string
    key_mapping = dict(zip(key_str, string))

    decrypted_text = ''.join(key_mapping.get(char, char) for char in data)  # Decrypt using the key
    return decrypted_text

# Example Usage
if __name__ == '__main__':
    data = "Hello, World!"
    encrypted_text, stored_key = encrypt(data, key)
    print(f"🔐 Encrypted: {encrypted_text}")
    print(f"🔑 Key: {stored_key}")

    decrypted_text = decrypt(encrypted_text, stored_key)
    print(f"🔓 Decrypted: {decrypted_text}")
