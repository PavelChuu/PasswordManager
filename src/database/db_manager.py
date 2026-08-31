import os
import sqlite3 as sl
from ..crypto.encryptor import generate_master_hash, Encryption

#   Класс для сощдания БД и заполнения Config
class Init:
    def __init__(self, date: tuple):
        self.date = date
    # Созадём баззы данных, если они не созданы
        cursor.execute('''
                    CREATE TABLE iF NOT EXISTS Config(
                        master_hash BLOB,
                        salt BLOB
                    )
                    ''')
        cursor.execute('''
                    CREATE TABLE iF NOT EXISTS Password(
                        id INTEGER PRIMARY KEY,
                        user_service BLOB,
                        user_name BLOB,
                        user_password BLOB
                    )
                    ''')
    # Записываем master_hash и salt в базу данных, если их там нет
    def create_hash(self):
        date = self.date
        cursor.execute('''
                        SELECT master_hash FROM Config
                        LIMIT 1
                    ''')
        # Проверка, есть ли в таблице записи, если нет - записывает в неё master_hash и salt. Если да - останавливает функцию
        if cursor.fetchone() == None:
            cursor.execute('INSERT INTO Config (master_hash, salt) VALUES (?, ?)',
                        (date)
                        )
        else: return

class CRUD:
    def __init__(self, master_password: str, user_service: str, user_name:str, user_password: str):
        self.master_password = master_password
        self.user_service = user_service
        self.user_name = user_name
        self.user_password = user_password
        cursor.execute('''
                                SELECT salt FROM Config
                                LIMIT 1
                                ''')
        self.salt = cursor.fetchone()[0]
        
    def create_date(self):
        date = Encryption(salt=self.salt, master_password=self.master_password, user_service=self.user_service, user_name=self.user_name, user_password=self.user_password)
        date.get_encryption_key()
        
        user_service, user_name, user_password = date.encryption()
        cursor.execute('INSERT INTO Password (user_service, user_name, user_password) VALUES (?, ?, ?)',
                            (user_service, user_name, user_password)
                            )
        conection.commit()
        
    def read_date(self):
        cursor.execute('''
                       SELECT user_service, user_name, user_password FROM Password
                       ''')
        results = cursor.fetchall()
        for result in results:
            user_service, user_name, user_password = result
            date = Encryption(salt=self.salt, master_password=self.master_password, user_service = user_service, user_name = user_name, user_password = user_password)
            date.get_encryption_key()
            user_service, user_name, user_password = date.decryption()
            print(user_service, user_name, user_password)
            
    def update_date():
        return
    
    def delete_date():
        return
        
        
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "database.db")
conection = sl.connect(db_path)
cursor = conection.cursor()

date = generate_master_hash(master_password="123jhj")
init = Init(date)
init.create_hash()
conection.commit()

obj = CRUD(master_password="123456asd", user_service="Youtube", user_name="123admin", user_password="fdyrtfzdcgycgjr756")
#obj.create_date()
obj.read_date()


conection.commit()
conection.close()