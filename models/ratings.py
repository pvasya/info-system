from core.dao_base import DAOBase

class Rating:
    def __init__(self, id, user_id, good_id, stars):
        self.id = id
        self.user_id = user_id
        self.good_id = good_id
        self.stars = stars

class RatingsDAO(DAOBase):
    def get_by_user_and_goods(self, user_id, good_id):
        try:
            query = """
                SELECT id, user_id, good_id, stars
                FROM ratings
                WHERE user_id = %s AND good_id = %s
            """
            self.cur.execute(query, (user_id, good_id))
            row = self.cur.fetchone()
            return Rating(*row) if row else None
        except Exception as e:
            print(f"Error getting rating: {e}")
            return None

    def get_by_goods(self, good_id):
        try:
            query = """
                SELECT id, user_id, good_id, stars
                FROM ratings
                WHERE good_id = %s
                ORDER BY id DESC
            """
            self.cur.execute(query, (good_id,))
            return [Rating(*row) for row in self.cur.fetchall()]
        except Exception as e:
            print(f"Error getting ratings by goods: {e}")
            self.conn.rollback()
            return []

    def get_average_rating(self, good_id):
        try:
            query = """
                SELECT AVG(stars) as avg_rating, COUNT(*) as count
                FROM ratings
                WHERE good_id = %s
            """
            self.cur.execute(query, (good_id,))
            row = self.cur.fetchone()
            avg = float(row[0]) if row and row[0] is not None else 0.0
            cnt = int(row[1]) if row and row[1] is not None else 0
            return (avg, cnt)
        except Exception as e:
            print(f"Error getting average rating: {e}")
            self.conn.rollback()
            return (0.0, 0)

    def add_or_update_rating(self, user_id, good_id, stars):
        try:
            existing = self.get_by_user_and_goods(user_id, good_id)

            if existing:
            
                query = """
                    UPDATE ratings
                    SET stars = %s
                    WHERE id = %s
                """
                self.cur.execute(query, (stars, existing.id))
            else:
                query = """
                    INSERT INTO ratings (user_id, good_id, stars)
                    VALUES (%s, %s, %s)
                """
                self.cur.execute(query, (user_id, good_id, stars))

            self.commit()
        except Exception as e:
            print(f"Error updating rating: {e}")
            self.conn.rollback()

    def delete_rating(self, user_id, good_id):
        try:
            query = """
                DELETE FROM ratings
                WHERE user_id = %s AND good_id = %s
            """
            self.cur.execute(query, (user_id, good_id))
            self.commit()
        except Exception as e:
            print(f"Error deleting rating: {e}")
            self.conn.rollback()
