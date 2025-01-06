import mysql.connector



class XIntegrationModel:
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
        cur.execute('SELECT * FROM `XIntegration`')
        integrations = cur.fetchall()
        cur.close()
        return integrations

    def fetch_integration_by_id(self, integration_id):
        cur = self.conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM `XIntegration` WHERE `id` = %s', (integration_id,))
        integration = cur.fetchone()
        cur.close()
        return integration

    def create_integration(self, bearer_token, api_key, api_secret, access_token, access_token_secret):
        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO `XIntegration` (`BearerToken`, `APIKey`, `APISecret`, `AccessToken`, `AccessTokenSecret`) VALUES (%s, %s, %s, %s, %s)',
            (bearer_token, api_key, api_secret, access_token, access_token_secret)
        )
        self.conn.commit()
        cur.close()

    def update_integration(self, integration_id, bearer_token=None, api_key=None, api_secret=None, access_token=None, access_token_secret=None):
        cur = self.conn.cursor()
        updates = []
        params = []
        if bearer_token:
            updates.append("`BearerToken` = %s")
            params.append(bearer_token)
        if api_key:
            updates.append("`APIKey` = %s")
            params.append(api_key)
        if api_secret:
            updates.append("`APISecret` = %s")
            params.append(api_secret)
        if access_token:
            updates.append("`AccessToken` = %s")
            params.append(access_token)
        if access_token_secret:
            updates.append("`AccessTokenSecret` = %s")
            params.append(access_token_secret)
        params.append(integration_id)
        query = f'UPDATE `XIntegration` SET {", ".join(updates)} WHERE `id` = %s'
        cur.execute(query, tuple(params))
        self.conn.commit()
        cur.close()

    def delete_integration(self, integration_id):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM `XIntegration` WHERE `id` = %s', (integration_id,))
        self.conn.commit()
        cur.close()

    def close_connection(self):
        self.conn.close()
