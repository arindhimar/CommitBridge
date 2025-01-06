import mysql.connector


class LinkedInIntegrationModel:
    def __init__(self):
        self.conn = self.get_db_connection()

    def get_db_connection(self):
        return mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def fetch_all_integrations(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM `LinkedInIntegration`')
        integrations = cur.fetchall()
        cur.close()
        return integrations

    def fetch_integration_by_id(self, integration_id):
        cur = self.conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM `LinkedInIntegration` WHERE `id` = %s', (integration_id,))
        integration = cur.fetchone()
        cur.close()
        return integration

    def create_integration(self, access_token, linkedin_id_urn):
        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO `LinkedInIntegration` (`AccessToken`, `LinkedInIDURN`) VALUES (%s, %s)',
            (access_token, linkedin_id_urn)
        )
        self.conn.commit()
        cur.close()

    def update_integration(self, integration_id, access_token=None, linkedin_id_urn=None):
        cur = self.conn.cursor()
        updates = []
        params = []
        if access_token:
            updates.append("`AccessToken` = %s")
            params.append(access_token)
        if linkedin_id_urn:
            updates.append("`LinkedInIDURN` = %s")
            params.append(linkedin_id_urn)
        params.append(integration_id)
        query = f'UPDATE `LinkedInIntegration` SET {", ".join(updates)} WHERE `id` = %s'
        cur.execute(query, tuple(params))
        self.conn.commit()
        cur.close()

    def delete_integration(self, integration_id):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM `LinkedInIntegration` WHERE `id` = %s', (integration_id,))
        self.conn.commit()
        cur.close()

    def close_connection(self):
        self.conn.close()
