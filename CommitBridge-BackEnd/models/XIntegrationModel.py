import mysql.connector
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
import os

class XIntegrationModel:
    def __init__(self):
        """Initialize the database connection."""
        self.conn = self.get_db_connection()

    def get_db_connection(self):
        """Establish a connection to the MySQL database."""
        return mysql.connector.connect(
            host="localhost",
            database="commitbridge",
            user="root",
            password="root"
        )

    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data using AES encryption."""
        iv = os.urandom(16)  # AES block size is 16 bytes
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
        return b64encode(iv + encrypted_data).decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt encrypted data using AES decryption."""
        encrypted_data = b64decode(encrypted_data.encode())
        iv, encrypted_data = encrypted_data[:16], encrypted_data[16:]
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        return decrypted_data.decode()

    def fetch_all_integrations(self):
        """Fetch all X integration records from the database."""
        cur = self.conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM `XIntegration`')
        integrations = cur.fetchall()
        cur.close()
        return integrations

    def fetch_integration_by_id(self, integration_id):
        """Fetch a specific X integration record by its ID."""
        cur = self.conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM `XIntegration` WHERE `id` = %s', (integration_id,))
        integration = cur.fetchone()
        cur.close()
        return integration

    def create_integration(self, bearer_token, api_key, api_secret, access_token, access_token_secret):
        """Create a new X integration in the database with encrypted credentials."""
        encrypted_bearer_token = self.encrypt_data(bearer_token)
        encrypted_api_key = self.encrypt_data(api_key)
        encrypted_api_secret = self.encrypt_data(api_secret)
        encrypted_access_token = self.encrypt_data(access_token)
        encrypted_access_token_secret = self.encrypt_data(access_token_secret)

        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO `XIntegration` (`BearerToken`, `APIKey`, `APISecret`, `AccessToken`, `AccessTokenSecret`) VALUES (%s, %s, %s, %s, %s)',
            (encrypted_bearer_token, encrypted_api_key, encrypted_api_secret, encrypted_access_token, encrypted_access_token_secret)
        )
        self.conn.commit()
        cur.close()

    def update_integration(self, integration_id, bearer_token=None, api_key=None, api_secret=None, access_token=None, access_token_secret=None):
        """Update an existing X integration's credentials with encrypted data."""
        cur = self.conn.cursor()
        updates = []
        params = []
        if bearer_token:
            updates.append("`BearerToken` = %s")
            params.append(self.encrypt_data(bearer_token))
        if api_key:
            updates.append("`APIKey` = %s")
            params.append(self.encrypt_data(api_key))
        if api_secret:
            updates.append("`APISecret` = %s")
            params.append(self.encrypt_data(api_secret))
        if access_token:
            updates.append("`AccessToken` = %s")
            params.append(self.encrypt_data(access_token))
        if access_token_secret:
            updates.append("`AccessTokenSecret` = %s")
            params.append(self.encrypt_data(access_token_secret))
        params.append(integration_id)
        query = f'UPDATE `XIntegration` SET {", ".join(updates)} WHERE `id` = %s'
        cur.execute(query, tuple(params))
        self.conn.commit()
        cur.close()

    def delete_integration(self, integration_id):
        """Delete an X integration record by its ID."""
        cur = self.conn.cursor()
        cur.execute('DELETE FROM `XIntegration` WHERE `id` = %s', (integration_id,))
        self.conn.commit()
        cur.close()

    def get_x_credentials(self):
        """Fetch and decrypt X API credentials from the database."""
        query = """
        SELECT bearer_token, api_key, api_secret, access_token, access_token_secret
        FROM x_credentials
        LIMIT 1
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            return {
                "bearer_token": self.decrypt_data(row[0]),
                "api_key": self.decrypt_data(row[1]),
                "api_secret": self.decrypt_data(row[2]),
                "access_token": self.decrypt_data(row[3]),
                "access_token_secret": self.decrypt_data(row[4]),
            }
        return None

    def get_latest_post_content(self):
        """Fetch the latest post content from the database."""
        query = "SELECT content FROM x_posts ORDER BY created_at DESC LIMIT 1"
        cursor = self.conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        return row[0] if row else None

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
