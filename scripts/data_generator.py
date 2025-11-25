import os
import random
import time
from contextlib import closing

import psycopg2

optionAddSomething = False
optionAddgood = True

DB_CONFIG = {
    "dbname": os.environ.get("DB_NAME", "online_store"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", "kvayb"),
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 5432)),
}

SLEEP_SECONDS = int(os.environ.get("GENERATOR_INTERVAL", 15))


def ensure_seed_data(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM goods")
        goods_count = cur.fetchone()[0]
        if goods_count == 0:
            sample_goods = [
                ("Laptop", 25000.0, "Productivity laptop","https://scriveiner.com/cdn/shop/files/1M_3.jpg"),
                ("Headphones", 3500.0, "Noise cancelling","https://scriveiner.com/cdn/shop/files/1M_3.jpg"),
                ("Smartphone", 18000.0, "Latest model","https://scriveiner.com/cdn/shop/files/1M_3.jpg"),
            ]
            cur.executemany(
                "INSERT INTO goods (name, price, description,url) VALUES (%s, %s, %s, %s)",
                sample_goods,
            )

        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            cur.execute(
                """
                INSERT INTO users (username, name, password, email, address, is_admin)
                VALUES ('demo', 'Demo User', '$2b$12$NbpxNTC/IInArxqCo1m0I.DRY2ORUEoxpO7xzIRpQcC4Q8p9m4G2y',
                        'demo@example.com', 'Kyiv', FALSE)
                """
            )


def add_new_goods(conn):
    """Додає 1 новий товар щохвилини"""
    with conn.cursor() as cur:
        product_names = ["Laptop", "Phone", "Tablet", "Headphones", "Mouse", "Keyboard", "Monitor", "Speaker", "Camera", "Watch"]
        name = f"{random.choice(product_names)} {random.randint(100, 999)}"
        price = round(random.uniform(1000, 40000), 2)
        description = f"Auto-generated {random.randint(1, 1000)}"
        image_urls = [
            "https://scriveiner.com/cdn/shop/files/1M_3.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/IBM_PC_5150.jpg/640px-IBM_PC_5150.jpg",
            "https://www.edmunds.com/assets/m/cs/cms/030987c2-78ad-446c-920d-0235a13d2977/2026-tesla-model-y-performance_600.jpg",
        ]
        url = random.choice(image_urls)
        
        cur.execute(
            "INSERT INTO goods (name, price, description, url) VALUES (%s, %s, %s, %s)",
            (name, price, description, url),
        )
        print(f"[data-generator] Added new product: {name} - {price} UAH, URL: {url}")


def apply_random_updates(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM goods")
        goods_ids = [row[0] for row in cur.fetchall()]

        if goods_ids:
            chosen_id = random.choice(goods_ids)
            new_price = round(random.uniform(1000, 40000), 2)
            cur.execute(
                "UPDATE goods SET price = %s WHERE id = %s",
                (new_price, chosen_id),
            )

        cur.execute("SELECT id FROM users LIMIT 1")
        user_row = cur.fetchone()
        if not user_row:
            return

        user_id = user_row[0]
        if goods_ids:
            order_items = random.sample(goods_ids, k=min(len(goods_ids), random.randint(1, 3)))
        else:
            order_items = []

        if order_items:
            cur.execute(
                "INSERT INTO orders (user_id, is_active) VALUES (%s, TRUE) RETURNING id",
                (user_id,),
            )
            order_id = cur.fetchone()[0]
            for good_id in order_items:
                cur.execute(
                    "INSERT INTO order_items (order_id, good_id, quantity) VALUES (%s, %s, %s)",
                    (order_id, good_id, random.randint(1, 4)),
                )


def main():
    if not optionAddSomething:
        print("[data-generator] Script disabled by option2.")
        return

    while True:
        try:
            with closing(psycopg2.connect(**DB_CONFIG)) as conn:
                conn.autocommit = False
                ensure_seed_data(conn)
                
                
                if optionAddgood:
                    add_new_goods(conn)
                
                apply_random_updates(conn)
                conn.commit()
        except Exception as exc:
            print(f"[data-generator] error: {exc}")
        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    main()
