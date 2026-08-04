import os
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import Fernet

    # Генерация масте-хеша для проверки мастер-пароля
def generate_master_hash(master_password: str, salt: bytes = None):
    if salt is None:    # Если это первый вход, то сгенерирует salt
        salt = os.urandom(16)
    
    kdf = Scrypt(
        length = 32,  # Желаемая длинна производного ключа 
        salt = salt,
        n=2**14,      # Стоимость памяти, в большинсттве случаях достаточно 2**14. Для более конфиденциальных данных можно 2**20, но время обработки возрастёт
        r=8,          # Размер блока (рекомендуется r=8)
        p=1           # Параллелизм (рекомендуется p=1)
    )
    
    master_hash = kdf.derive(master_password.encode())
    return master_hash, salt

 # Шифрование данных
def get_encryption_key(master_password: str, salt: bytes):
    kdf = Scrypt(
            length = 32,  # Желаемая длинна производного ключа 
            salt = salt,
            n = 2**14,      # Стоимость памяти, в большинсттве случаях достаточно 2**14. Для более конфиденциальных данных можно 2**20, но время обработки возрастёт
            r = 8,          # Размер блока (рекомендуется r=8)
            p = 1           # Параллелизм (рекомендуется p=1)
        )
    
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

salt = os.urandom(16)
password = "78hjy1!"

key = get_encryption_key(password, salt)
f = Fernet(key)

encrypted_text = f.encrypt("Hello".encode('utf-8'))
print(encrypted_text)
decrypted_text = f.decrypt(encrypted_text).decode('utf-8')
print(decrypted_text)
