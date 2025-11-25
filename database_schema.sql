DROP TABLE IF EXISTS ratings, order_items, basket, orders, goods, users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(150),
    password VARCHAR(255) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    address TEXT,
    is_blocked BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    cookie VARCHAR(255)
);

CREATE TABLE goods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    url TEXT,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    description TEXT DEFAULT '',
    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE basket (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    good_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (good_id) REFERENCES goods(id) ON DELETE CASCADE
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_status_by_admin_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_status_by_admin_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    good_id INT NOT NULL,
    quantity INT DEFAULT 1 CHECK (quantity > 0),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (good_id) REFERENCES goods(id) ON DELETE CASCADE
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    good_id INT NOT NULL,
    stars INT NOT NULL CHECK (stars BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, good_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (good_id) REFERENCES goods(id) ON DELETE CASCADE
);

CREATE INDEX idx_basket_user_id ON basket(user_id);
CREATE INDEX idx_basket_good_id ON basket(good_id);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_is_active ON orders(is_active);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_good_id ON order_items(good_id);
CREATE INDEX idx_ratings_user_id ON ratings(user_id);
CREATE INDEX idx_ratings_good_id ON ratings(good_id);
CREATE INDEX idx_goods_is_deleted ON goods(is_deleted);


INSERT INTO users (id, username, name, password, email, address, is_blocked, is_admin, cookie)
VALUES (1, 'kvayb', 'Vasyl Popovych', '$2b$12$NbpxNTC/IInArxqCo1m0I.DRY2ORUEoxpO7xzIRpQcC4Q8p9m4G2y', 'hraq300011@gmail.com', 'Ukraine', FALSE, TRUE, '112734a8-22af-4581-a0b1-4e406e54e1a1');