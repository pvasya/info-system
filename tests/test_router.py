# python -m pytest
import pytest
from core.router import Router

def test_get_routes_present():
    router = Router()
    assert '/' in router.routes['GET']
    assert '/login' in router.routes['GET']
    assert '/logout' in router.routes['GET']

def test_post_routes_present():
    router = Router()
    assert '/login' in router.routes['POST']
    assert '/goods/add' in router.routes['POST']
    assert '/orders/create' in router.routes['POST']
