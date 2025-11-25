from core.dao_base import DAOBase

class BasketItem:
    def __init__(self, id, user_id, goods_id, is_active):
        self.id = id
        self.user_id = user_id
        self.goods_id = goods_id
        self.is_active = is_active

class BasketDAO(DAOBase):
    def get_active_by_user(self, user_id):
        query = """
            SELECT id, user_id, good_id, is_active
            FROM basket
            WHERE user_id = %s AND is_active = TRUE
        """
        self.cur.execute(query, (user_id,))
        return [BasketItem(*row) for row in self.cur.fetchall()]

    def add(self, user_id, goods_id):
        query = """
            INSERT INTO basket (user_id, good_id, is_active)
            VALUES (%s, %s, TRUE)
        """
        self.cur.execute(query, (user_id, goods_id))
        self.commit()

    def clear(self, user_id):
        query = """
            UPDATE basket
            SET is_active = FALSE
            WHERE user_id = %s AND is_active = TRUE
        """
        self.cur.execute(query, (user_id,))
        self.commit()

    def remove(self, user_id, goods_id):
        query = """
            UPDATE basket
            SET is_active=FALSE
            WHERE id IN (
              SELECT id FROM basket
              WHERE user_id=%s AND good_id=%s AND is_active=TRUE
              ORDER BY id DESC
              LIMIT 1
            )
        """
        self.cur.execute(query, (user_id, goods_id))
        self.commit()
