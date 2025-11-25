from core.controller import BaseController
from models.goods import Goods, GoodsDAO
from models.basket import BasketDAO
from models.ratings import RatingsDAO
from urllib.parse import unquote

def index(req):
    ctrl = BaseController(req)
    with GoodsDAO() as goods_dao:
        goods = goods_dao.get_all()
        basket_counts = {}
        if ctrl.user and not ctrl.user.is_admin:
            with BasketDAO() as basket_dao:
                items = basket_dao.get_active_by_user(ctrl.user.id)
                for it in items:
                    basket_counts[it.goods_id] = basket_counts.get(it.goods_id, 0) + 1

        # Отримуємо рейтинги для всіх товарів
        with RatingsDAO() as ratings_dao:
            goods_ratings = {}
            for good in goods:
                avg_rating, count = ratings_dao.get_average_rating(good.id)
                user_rating = None
                if ctrl.user and not ctrl.user.is_admin:
                    user_rating = ratings_dao.get_by_user_and_goods(ctrl.user.id, good.id)

                goods_ratings[good.id] = {
                    'average_rating': round(avg_rating, 1) if avg_rating else 0,
                    'rating_count': count,
                    'user_rating': user_rating.stars if user_rating else 0
                }

    ctrl.render('catalog.html', {
        'user': ctrl.user,
        'goods': goods,
        'basket_counts': basket_counts,
        'goods_ratings': goods_ratings
    })

def add_goods(req):
    ctrl = BaseController(req)
    data = ctrl.parse_form()
    name = data.get('name', '')
    url = data.get('url')
    image_url = url.lstrip('/') if url else ''
    price = data.get('price')
    description = data.get('description', '')
    if name and url and price:
        goods = Goods(None, name, image_url, float(price), description, False)
        with GoodsDAO() as dao:
            dao.create(goods)
    ctrl.redirect('/')

def delete_goods(req):
    ctrl = BaseController(req)
    data = ctrl.parse_form()
    id_ = data.get('id')
    if id_:
        with GoodsDAO() as dao:
            dao.delete(int(id_))
    ctrl.redirect('/')

def update_goods(req):
    ctrl = BaseController(req)
    data = ctrl.parse_form()
    id_ = data.get('id')
    name = data.get('name', '')
    url = data.get('url')
    image_url = url.lstrip('/') if url else ''
    price = data.get('price')
    description = data.get('description', '')
    if id_ and name and url and price:
        goods = Goods(int(id_), name, image_url, float(price), description, False)
        with GoodsDAO() as dao:
            dao.update(goods)
    ctrl.redirect('/')
