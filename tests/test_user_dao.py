# python -m pytest
import pytest
from models.user import UserDAO, User
from unittest.mock import MagicMock

@pytest.fixture
def dao():
    dao = UserDAO()
    dao.cur = MagicMock()
    return dao

def test_find_by_username_returns_user(dao):
    dao.cur.fetchone.return_value = (1, 'emily', 'Emily Swift', 'hash', 'mail', 'addr', False, False, 'cookie')
    user = dao.find_by_username('emily')
    assert user.username == 'emily'
    assert user.real_name == 'Emily Swift'
    assert user.email == 'mail'

def test_find_by_username_none(dao):
    dao.cur.fetchone.return_value = None
    user = dao.find_by_username('missing')
    assert user is None
