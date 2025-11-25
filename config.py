import os

# Database configuration
DB = {
    'dbname': os.getenv('DB_NAME', 'online_store'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'kvayb'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
}

# Server configuration
HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 8000))

# Static files directory
STATIC_DIR = '/static/'