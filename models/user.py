from core.dao_base import DAOBase

class User:
    def __init__(self, id, username, password_hash, real_name, address, email, is_admin, is_blocked, cookie):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.real_name = real_name
        self.address = address
        self.email = email
        self.is_admin = is_admin
        self.is_blocked = is_blocked
        self.cookie = cookie

class UserDAO(DAOBase):
    def find_by_cookie(self, cookie):
        query = '''
            SELECT id, username, name, password, email, address, is_blocked, is_admin, cookie
            FROM users
            WHERE cookie = %s
        '''
        self.cur.execute(query, (cookie,))
        row = self.cur.fetchone()
        if not row:
            return None
        return User(
            id=row[0],
            username=row[1],
            password_hash=row[3],
            real_name=row[2],
            address=row[5],
            email=row[4],
            is_admin=row[7],
            is_blocked=row[6],
            cookie=row[8]
        )

    def get_by_id(self, user_id):
        query = '''
            SELECT id, username, name, password, email, address, is_blocked, is_admin, cookie
            FROM users
            WHERE id = %s
        '''
        self.cur.execute(query, (user_id,))
        row = self.cur.fetchone()
        if not row:
            return None
        return User(
            id=row[0],
            username=row[1],
            password_hash=row[3],
            real_name=row[2],
            address=row[5],
            email=row[4],
            is_admin=row[7],
            is_blocked=row[6],
            cookie=row[8]
        )


    def find_by_username(self, username):
        query = '''
            SELECT id, username, name, password, email, address, is_blocked, is_admin, cookie
            FROM users
            WHERE username = %s
        '''
        self.cur.execute(query, (username,))
        row = self.cur.fetchone()
        if not row:
            return None
        return User(
            id=row[0],
            username=row[1],
            password_hash=row[3],
            real_name=row[2],
            address=row[5],
            email=row[4],
            is_admin=row[7],
            is_blocked=row[6],
            cookie=row[8]
        )

    def blacklist(self, user_id, block=True):
        query = 'UPDATE users SET is_blocked = %s WHERE id = %s'
        self.cur.execute(query, (block, user_id))
        self.commit()

    def update(self, user):
        query = '''
            UPDATE users
            SET username = %s,
                name = %s,
                password = %s,
                email = %s,
                address = %s,
                is_blocked = %s,
                is_admin = %s
            WHERE id = %s
        '''
        self.cur.execute(query, (
            user.username,
            user.real_name,
            user.password_hash,
            user.email,
            user.address,
            user.is_blocked,
            user.is_admin,
            user.id
        ))
        self.commit()

    def get_all(self):
        query = '''
            SELECT id, username, name, password, email, address, is_blocked, is_admin, cookie
            FROM users
            ORDER BY id
        '''
        self.cur.execute(query)
        rows = self.cur.fetchall()
        users = []
        for row in rows:
            users.append(User(
                id=row[0],
                username=row[1],
                password_hash=row[3],
                real_name=row[2],
                address=row[5],
                email=row[4],
                is_admin=row[7],
                is_blocked=row[6],
                cookie=row[8]
            ))
        return users

    def find_by_email(self, email):
        query = '''
            SELECT id, username, name, password, email, address, is_blocked, is_admin, cookie
            FROM users
            WHERE email = %s
        '''
        self.cur.execute(query, (email,))
        row = self.cur.fetchone()
        if not row:
            return None
        return User(
            id=row[0],
            username=row[1],
            password_hash=row[3],
            real_name=row[2],
            address=row[5],
            email=row[4],
            is_admin=row[7],
            is_blocked=row[6],
            cookie=row[8]
        )

    def create(self, user):
        query = '''
            INSERT INTO users (username, name, password, email, address, is_blocked, is_admin, cookie)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        '''
        self.cur.execute(query, (
            user.username,
            user.real_name,
            user.password_hash,
            user.email,
            user.address,
            user.is_blocked,
            user.is_admin,
            user.cookie
        ))
        new_id = self.cur.fetchone()[0]
        self.commit()
        return new_id