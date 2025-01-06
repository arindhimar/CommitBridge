import mysql.connector


class UserModel:
    def __init__(self):
        self.conn = self.get_db_connection()

    def get_db_connection(self):
        return mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def fetch_all_users(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM `UserTb`')
        users = cur.fetchall()
        cur.close()
        return users

    def fetch_user_by_id(self, user_id):
        cur = self.conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM `UserTb` WHERE `id` = %s', (user_id,))
        user = cur.fetchone()
        cur.close()
        return user

    def create_user(self, name, email, password, timezone="UTC"):
        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO `UserTb` (`Name`, `Email`, `Password`, `timeZone`) VALUES (%s, %s, %s, %s)',
            (name, email, password, timezone)
        )
        self.conn.commit()
        cur.close()

    def update_user(self, user_id, name=None, email=None, password=None, timezone=None):
        cur = self.conn.cursor()
        updates = []
        params = []
        if name:
            updates.append("`Name` = %s")
            params.append(name)
        if email:
            updates.append("`Email` = %s")
            params.append(email)
        if password:
            updates.append("`Password` = %s")
            params.append(password)
        if timezone:
            updates.append("`timeZone` = %s")
            params.append(timezone)
        params.append(user_id)
        query = f'UPDATE `UserTb` SET {", ".join(updates)} WHERE `id` = %s'
        cur.execute(query, tuple(params))
        self.conn.commit()
        cur.close()

    def delete_user(self, user_id):
        cur = self.conn.cursor()
        cur.execute('DELETE FROM `UserTb` WHERE `id` = %s', (user_id,))
        self.conn.commit()
        cur.close()

    def close_connection(self):
        self.conn.close()
