# python -m pytest
import pytest
import config

def test_default_db_config():
    assert config.DB['dbname'] == 'online_store'
    assert config.DB['user'] == 'postgres'
    assert config.DB['password'] == 'kvayb'
    assert config.DB['host'] == 'localhost'
    assert config.DB['port'] == '5432'

def test_default_server_config():
    assert config.HOST == '127.0.0.1'
    assert config.PORT == 8000
    assert config.STATIC_DIR == '/static/'
