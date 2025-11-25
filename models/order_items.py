from core.dao_base import DAOBase

class OrderItem:
    def __init__(self, id, order_id, good_id, quantity):
        self.id = id
        self.order_id = order_id
        self.good_id = good_id
        self.quantity = quantity

class OrderItemsDAO(DAOBase):
    def get_by_order(self, order_id):
        query = """
            SELECT id, order_id, good_id, quantity
            FROM order_items
            WHERE order_id = %s
            ORDER BY id
        """
        self.cur.execute(query, (order_id,))
        return [OrderItem(*row) for row in self.cur.fetchall()]

    def add_item(self, order_id, good_id, quantity=1):
        query = """
            INSERT INTO order_items (order_id, good_id, quantity)
            VALUES (%s, %s, %s)
        """
        self.cur.execute(query, (order_id, good_id, quantity))
        self.commit()

    def update_quantity(self, item_id, quantity):
        query = """
            UPDATE order_items
            SET quantity = %s
            WHERE id = %s
        """
        self.cur.execute(query, (quantity, item_id))
        self.commit()

    def remove_item(self, item_id):
        query = "DELETE FROM order_items WHERE id = %s"
        self.cur.execute(query, (item_id,))
        self.commit()

    def clear_order(self, order_id):
        query = "DELETE FROM order_items WHERE order_id = %s"
        self.cur.execute(query, (order_id,))
        self.commit()
