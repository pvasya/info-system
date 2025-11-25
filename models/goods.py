from core.dao_base import DAOBase

class Goods:
    def __init__(self, id, name, image_url, price, description, is_deleted):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.price = price
        self.description = description
        self.is_deleted = is_deleted

class GoodsDAO(DAOBase):
    def get_all(self):
        query = """
            SELECT id, name, url, price, description, is_deleted
            FROM goods
            WHERE NOT is_deleted
            ORDER BY id
        """
        self.cur.execute(query)
        return [Goods(*row) for row in self.cur.fetchall()]

    def find_by_id(self, id_):
        query = """
            SELECT id, name, url, price, description, is_deleted
            FROM goods
            WHERE id = %s AND NOT is_deleted
        """
        self.cur.execute(query, (id_,))
        row = self.cur.fetchone()
        return Goods(*row) if row else None

    def create(self, goods):
        query = """
            INSERT INTO goods (name, url, price, description, is_deleted)
            VALUES (%s, %s, %s, %s, FALSE)
            RETURNING id
        """
        self.cur.execute(query, (goods.name, goods.image_url, goods.price, goods.description))
        new_id = self.cur.fetchone()[0]
        self.commit()
        return new_id

    def delete(self, goods_id):
        query = "UPDATE goods SET is_deleted = TRUE WHERE id = %s"
        self.cur.execute(query, (goods_id,))
        self.commit()

    def update(self, goods):
        query = """
            UPDATE goods
            SET name = %s, url = %s, price = %s, description = %s
            WHERE id = %s
        """
        self.cur.execute(query, (goods.name, goods.image_url, goods.price, goods.description, goods.id))
        self.commit()
