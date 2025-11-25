from core.dao_base import DAOBase
from datetime import datetime

class Order:
    def __init__(self, id, user_id, is_active, created_at, changed_status_by_admin_id=None):
        self.id = id
        self.user_id = user_id
        self.is_active = is_active
        self.created_at = created_at
        self.changed_status_by_admin_id = changed_status_by_admin_id

class OrderDAO(DAOBase):
    def get_all(self):
        query = """
            SELECT id, user_id, is_active, created_at, changed_status_by_admin_id
            FROM orders
            ORDER BY id DESC
        """
        self.cur.execute(query)
        return [Order(*row) for row in self.cur.fetchall()]

    def get_by_user(self, user_id):
        query = """
            SELECT id, user_id, is_active, created_at, changed_status_by_admin_id
            FROM orders
            WHERE user_id = %s
            ORDER BY id DESC
        """
        self.cur.execute(query, (user_id,))
        return [Order(*row) for row in self.cur.fetchall()]

    def create(self, order):
        query = """
            INSERT INTO orders (user_id, is_active)
            VALUES (%s, TRUE)
            RETURNING id
        """
        self.cur.execute(query, (order.user_id,))
        new_id = self.cur.fetchone()[0]
        self.commit()
        return new_id

    def complete(self, order_id):
        query = "UPDATE orders SET is_active = FALSE WHERE id = %s"
        self.cur.execute(query, (order_id,))
        self.commit()

    def get_by_id(self, order_id):
        query = """
            SELECT id, user_id, is_active, created_at, changed_status_by_admin_id
            FROM orders
            WHERE id = %s
        """
        self.cur.execute(query, (order_id,))
        row = self.cur.fetchone()
        return Order(*row) if row else None
