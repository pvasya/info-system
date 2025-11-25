from core.controller import BaseController
from models.ratings import RatingsDAO
import json

def rate_goods(req):
    ctrl = BaseController(req)
    if not ctrl.user or ctrl.user.is_admin:
        return ctrl.json_response({'error': 'Unauthorized'}, 403)

    if req.command != 'POST':
        return ctrl.json_response({'error': 'Method not allowed'}, 405)

    try:
        length = int(req.headers.get('Content-Length', 0))
        raw = req.rfile.read(length).decode('utf-8') if length > 0 else '{}'
        data = json.loads(raw)
        goods_id = data.get('goods_id')
        stars = data.get('stars')

        if not goods_id or not stars:
            return ctrl.json_response({'error': 'Missing required fields'}, 400)

        try:
            goods_id = int(goods_id)
            stars = int(stars)
            if stars < 1 or stars > 5:
                return ctrl.json_response({'error': 'Stars must be between 1 and 5'}, 400)
        except (ValueError, TypeError):
            return ctrl.json_response({'error': 'Invalid data types'}, 400)

        with RatingsDAO() as dao:
            dao.add_or_update_rating(ctrl.user.id, goods_id, stars)

            avg_rating, count = dao.get_average_rating(goods_id)
            user_rating = dao.get_by_user_and_goods(ctrl.user.id, goods_id)

        avg_num = float(avg_rating) if avg_rating else 0.0

        return ctrl.json_response({
            'success': True,
            'average_rating': round(avg_num, 1),
            'rating_count': count,
            'user_rating': user_rating.stars if user_rating else 0
        })
    except json.JSONDecodeError:
        return ctrl.json_response({'error': 'Invalid JSON'}, 400)
    except Exception as e:
        print(f"Error in rate_goods: {e}")
        return ctrl.json_response({'error': 'Internal server error'}, 500)

def get_goods_rating(req):
    ctrl = BaseController(req)
    goods_id = req.GET.get('goods_id')

    if not goods_id:
        return ctrl.json_response({'error': 'Missing goods_id'}, 400)

    try:
        goods_id = int(goods_id)
    except (ValueError, TypeError):
        return ctrl.json_response({'error': 'Invalid goods_id'}, 400)

    try:
        with RatingsDAO() as dao:
            avg_rating, count = dao.get_average_rating(goods_id)

            user_rating = None
            if ctrl.user and not ctrl.user.is_admin:
                user_rating = dao.get_by_user_and_goods(ctrl.user.id, goods_id)

            return ctrl.json_response({
                'average_rating': round(avg_rating, 1) if avg_rating else 0,
                'rating_count': count,
                'user_rating': user_rating.stars if user_rating else 0
            })
    except Exception as e:
        print(f"Error in get_goods_rating: {e}")
        return ctrl.json_response({'error': 'Internal server error'}, 500)
