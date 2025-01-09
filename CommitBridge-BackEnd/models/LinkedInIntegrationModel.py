import mysql.connector
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
import os

class LinkedInIntegrationModel:
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
        """Fetch all LinkedIn integration records from the database."""
        cur = self.conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM `LinkedInIntegration`')
        integrations = cur.fetchall()
        cur.close()
        return integrations

    def fetch_integration_by_id(self, integration_id):
        """Fetch a specific LinkedIn integration record by its ID."""
        cur = self.conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM `LinkedInIntegration` WHERE `id` = %s', (integration_id,))
        integration = cur.fetchone()
        cur.close()
        return integration

    def create_integration(self, access_token, linkedin_id_urn):
        """Create a new LinkedIn integration in the database with encrypted credentials."""
        encrypted_access_token = self.encrypt_data(access_token)
        encrypted_linkedin_id_urn = self.encrypt_data(linkedin_id_urn)

        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO `LinkedInIntegration` (`AccessToken`, `LinkedInIDURN`) VALUES (%s, %s)',
            (encrypted_access_token, encrypted_linkedin_id_urn)
        )
        self.conn.commit()
        cur.close()

    def update_integration(self, integration_id, access_token=None, linkedin_id_urn=None):
        """Update an existing LinkedIn integration's credentials with encrypted data."""
        cur = self.conn.cursor()
        updates = []
        params = []
        if access_token:
            updates.append("`AccessToken` = %s")
            params.append(self.encrypt_data(access_token))
        if linkedin_id_urn:
            updates.append("`LinkedInIDURN` = %s")
            params.append(self.encrypt_data(linkedin_id_urn))
        params.append(integration_id)
        query = f'UPDATE `LinkedInIntegration` SET {", ".join(updates)} WHERE `id` = %s'
        cur.execute(query, tuple(params))
        self.conn.commit()
        cur.close()

    def delete_integration(self, integration_id):
        """Delete a LinkedIn integration record by its ID."""
        cur = self.conn.cursor()
        cur.execute('DELETE FROM `LinkedInIntegration` WHERE `id` = %s', (integration_id,))
        self.conn.commit()
        cur.close()

    def get_linkedin_credentials(self):
        """Fetch and decrypt LinkedIn API access token and numeric ID from the database."""
        query = "SELECT access_token, linkedin_id FROM linkedin_credentials LIMIT 1"
        cursor = self.conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            return {
                "access_token": self.decrypt_data(row[0]),
                "linkedin_id": self.decrypt_data(row[1]),
            }
        return None

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
