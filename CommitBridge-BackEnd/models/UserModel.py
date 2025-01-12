import bcrypt
import mysql.connector
import jwt
from datetime import datetime, timedelta
import secrets

class UserModel:
    def __init__(self):
        self.conn = self.get_db_connection()
        self.create_or_update_table()

    def get_db_connection(self):
        return mysql.connector.connect(
            host="localhost",
            database="commitbridge",
            user="root",
            password="root"
        )

    def create_or_update_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS `UserTb` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `Name` VARCHAR(255) NOT NULL,
                `Email` VARCHAR(255) NOT NULL UNIQUE,
                `Password` VARCHAR(255),
                `timeZone` VARCHAR(50) DEFAULT 'UTC',
                `picture` VARCHAR(255) NULL,
                `reset_token` VARCHAR(255),
                `reset_token_expiry` DATETIME
            );
            """)
            self.conn.commit()

    def hash_password(self, password):
        if not password:
            return ''
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, plain_password, hashed_password):
        if not plain_password or not hashed_password:
            return False
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def create_user(self, name, email, password='', timezone="UTC", picture=None, oauth_provider=None):
        hashed_password = self.hash_password(password) if password else ''
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                'INSERT INTO `UserTb` (`Name`, `Email`, `Password`, `timeZone`, `picture`, `oauth_provider`) VALUES (%s, %s, %s, %s, %s, %s)',
                (name, email, hashed_password, timezone, picture, oauth_provider)
            )
            self.conn.commit()
            return self.fetch_user_by_email(email)

    def fetch_user_by_email(self, email):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute('SELECT * FROM `UserTb` WHERE `Email` = %s', (email,))
            return cursor.fetchone()

    def authenticate_user(self, email, password):
        user = self.fetch_user_by_email(email)
        if user and self.verify_password(password, user['Password']):
            return user
        return None

    def update_user(self, user_id, name=None, email=None, password=None, timezone=None, picture=None):
        updates = []
        params = []

        if name:
            updates.append("`Name` = %s")
            params.append(name)
        if email:
            updates.append("`Email` = %s")
            params.append(email)
        if password:
            hashed_password = self.hash_password(password)
            updates.append("`Password` = %s")
            params.append(hashed_password)
        if timezone:
            updates.append("`timeZone` = %s")
            params.append(timezone)
        if picture:
            updates.append("`picture` = %s")
            params.append(picture)

        params.append(user_id)

        query = f'UPDATE `UserTb` SET {", ".join(updates)} WHERE `id` = %s'
        with self.conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            self.conn.commit()

    def generate_token(self, user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, 'your-secret-key', algorithm='HS256')

    def close_connection(self):
        self.conn.close()

    def change_password(self, user_id, old_password, new_password):
        user = self.fetch_user_by_id(user_id)
        if not user:
            return False, "User not found"
        
        if not self.verify_password(old_password, user['Password']):
            return False, "Incorrect old password"
        
        hashed_password = self.hash_password(new_password)
        self.update_user(user_id, password=hashed_password)
        return True, "Password changed successfully"

    def reset_password(self, user_id, new_password):
        hashed_password = self.hash_password(new_password)
        with self.conn.cursor() as cursor:
            cursor.execute('UPDATE `UserTb` SET `Password` = %s WHERE `id` = %s',
                           (hashed_password, user_id))
            self.conn.commit()
        
        return True, "Password reset successfully"

    def fetch_user_by_id(self, user_id):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute('SELECT * FROM `UserTb` WHERE `id` = %s', (user_id,))
            return cursor.fetchone()

    def generate_password_reset_token(self, email):
        user = self.fetch_user_by_email(email)
        if not user:
            return None
        
        token = secrets.token_urlsafe(32)
        expiration = datetime.utcnow() + timedelta(hours=1)
        
        with self.conn.cursor() as cursor:
            cursor.execute(
                'UPDATE `UserTb` SET `reset_token` = %s, `reset_token_expiry` = %s WHERE `id` = %s',
                (token, expiration, user['id'])
            )
            self.conn.commit()
        
        return token

    def verify_reset_token(self, token):
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute('SELECT * FROM `UserTb` WHERE `reset_token` = %s AND `reset_token_expiry` > %s', 
                           (token, datetime.utcnow()))
            user = cursor.fetchone()
        
        if user:
            return user
        return None

    def set_password(self, user_id, new_password):
        hashed_password = self.hash_password(new_password)
        with self.conn.cursor() as cursor:
            cursor.execute('UPDATE `UserTb` SET `Password` = %s WHERE `id` = %s',
                           (hashed_password, user_id))
            self.conn.commit()
        return True, "Password set successfully"

