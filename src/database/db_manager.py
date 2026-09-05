import os
import sqlite3 as sl
from ..crypto.encryptor import generate_master_hash, Encryption

#   Класс для сощдания БД и заполнения Config
class Init:
    def __init__(self, date: tuple):
        self.date = date
    # Созадём базы данных, если они не созданы
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
                        user_password BLOB,
                        password_salt BLOB
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
    def __init__(self, master_password: str = None, user_service: str = None, user_name: str = None, user_password: str = None):
        self.master_password = master_password
        self.user_service = user_service
        self.user_name = user_name
        self.user_password = user_password
        
        # Добавление записи в БД
    def create_date(self):
        password_salt = os.urandom(16) # Для каждой записи создаётся своя соль
        date = Encryption(salt=password_salt, master_password=self.master_password, user_service=self.user_service, user_name=self.user_name, user_password=self.user_password)
        date.get_encryption_key() # Получаем ключ шифрования
        user_service, user_name, user_password = date.encryption() 
        
        cursor.execute('INSERT INTO Password (user_service, user_name, user_password, password_salt) VALUES (?, ?, ?, ?)',
                            (user_service, user_name, user_password, password_salt))
        conection.commit()
        
        # Чтение всех записей в БД
    def read_date(self):
        cursor.execute('''
                      SELECT user_service, user_name, user_password, password_salt FROM Password
                      ''')
        results = cursor.fetchall()
        
        # Прогоняем полученный кортеж через decryption (Скорее всего передалаю, выглядит плохо)
        for result in results:
            user_service, user_name, user_password, password_salt = result
            date = Encryption(user_service = user_service, user_name = user_name, user_password = user_password, salt = password_salt, master_password = self.master_password)
            date.get_encryption_key()
            user_service, user_name, user_password = date.decryption()
            print(user_service, user_name, user_password)
        conection.commit()
        
        # Обновление записи в БД по её ID    
    def update_date(self, select_id = None):
        password_salt = os.urandom(16) # При каждом изминение данных в БД, запись получат новую соль
        date = Encryption(salt=password_salt, master_password=self.master_password, user_service=self.user_service, user_name=self.user_name, user_password=self.user_password)
        date.get_encryption_key() # Получаем ключ шифрования
        user_service, user_name, user_password = date.encryption()
                
        cursor.execute('''
                       UPDATE Password
                       SET user_service = ?, user_name = ?, user_password = ?, password_salt = ?
                       WHERE id = ?
                       ''', (user_service, user_name, user_password, password_salt, select_id))
        conection.commit()

        # Удаление записи из ДБ по её ID 
    def delete_date(self, select_id = None):
        cursor.execute('''
                       DELETE FROM Password
                       WHERE id = ?
                       ''',  (select_id,))
        conection.commit()
        
        
# Объявляем БД и указываем пути        
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "database.db")
conection = sl.connect(db_path)
cursor = conection.cursor()

date = generate_master_hash(master_password="123jhj")
init = Init(date)
init.create_hash()
conection.commit()

obj = CRUD(master_password="123456asd", user_service="YouTube", user_name="tsjfgbxcgdzs", user_password="5475436gjnvchf")
#obj.create_date()
#obj.update_date(select_id= 2)
obj.delete_date(select_id= 2)
obj.read_date()


conection.commit()
conection.close()