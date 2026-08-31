import os
import base64

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import Fernet


#   Генерация масте-хеша для проверки мастер-пароля
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
    master_hash = kdf.derive(master_password.encode("utf-8"))
    return master_hash, salt


#   Проверка введёного пароля с master_hash
class Authentication:
    def __init__(self, master_hash: str, password: str, salt: bytes):
        self.master_hash = master_hash
        self.password = password
        self.salt = salt
        
    def control_master_password(self):
        kdf = Scrypt(
                    length = 32,  # Желаемая длинна производного ключа 
                    salt = self.salt,
                    n=2**14,      # Стоимость памяти, в большинсттве случаях достаточно 2**14. Для более конфиденциальных данных можно 2**20, но время обработки возрастёт
                    r=8,          # Размер блока (рекомендуется r=8)
                    p=1           # Параллелизм (рекомендуется p=1)
                )
        kdf.verify(self.password.encode(), self.master_hash)
        

        
#   Класс шифрования данных
class Encryption:
    # Инициализируем объект
    def __init__(self, salt: bytes , master_password: str,user_service: str, user_name:str, user_password: str):
        self.salt = salt
        self.master_password = master_password
        self.user_service = user_service
        self.user_name = user_name
        self.user_password = user_password
        
        #   Создаём ключ для шифрования
    def get_encryption_key(self):
        kdf = Scrypt(
            length = 32,  # Желаемая длинна производного ключа 
            salt = self.salt,
            n = 2**14,      # Стоимость памяти, в большинсттве случаях достаточно 2**14. Для более конфиденциальных данных можно 2**20, но время обработки возрастёт
            r = 8,          # Размер блока (рекомендуется r=8)
            p = 1           # Параллелизм (рекомендуется p=1)
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_password.encode("utf-8")))
        return key

    # Шифруем данные
    def encryption(self):
        key = self.get_encryption_key()
        f = Fernet(key)
        enc_user_service = f.encrypt(self.user_service.encode("utf-8"))
        enc_user_name = f.encrypt(self.user_name.encode("utf-8"))
        enc_user_password = f.encrypt(self.user_password.encode("utf-8"))
        return enc_user_service, enc_user_name, enc_user_password
    # Дешифровка данных  
    def decryption(self):
        key = self.get_encryption_key()
        f = Fernet(key)
        
        dec_user_service = f.decrypt(self.user_service.decode("utf-8"))
        dec_user_name = f.decrypt(self.user_name.decode("utf-8"))
        dec_user_password = f.decrypt(self.user_password.decode("utf-8"))
        return dec_user_service, dec_user_name, dec_user_password
