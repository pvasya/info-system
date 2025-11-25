from core.controller import BaseController
from models.basket import BasketDAO
from models.goods import GoodsDAO

def add_to_basket(req):
    ctrl = BaseController(req)
    if not ctrl.require_login() or ctrl.user.is_admin:
        ctrl.redirect('/')
        return
    data = ctrl.parse_form()
    gid = data.get('id')
    if gid:
        BasketDAO().add(ctrl.user.id, int(gid))
    ctrl.redirect('/')

def remove_from_basket(req):
    ctrl = BaseController(req)
    if not ctrl.require_login() or ctrl.user.is_admin:
        ctrl.redirect('/')
        return
    data = ctrl.parse_form()
    gid = data.get('id')
    if gid:
        BasketDAO().remove(ctrl.user.id, int(gid))
    ctrl.redirect('/')

def view_basket(req):
    ctrl = BaseController(req)
    if not ctrl.require_login():
        return
    if ctrl.user.is_admin:
        ctrl.redirect('/')
        return

    items = BasketDAO().get_active_by_user(ctrl.user.id)

    counts = {}
    for it in items:
        counts[it.goods_id] = counts.get(it.goods_id, 0) + 1

    goods_list = []
    total = 0
    for gid, qty in counts.items():
        goods = GoodsDAO().find_by_id(gid)
        if goods:
            goods_list.append({'goods': goods, 'quantity': qty})
            total += goods.price * qty

    ctrl.render('basket.html', {
        'user': ctrl.user,
        'items': goods_list,
        'total': total
    })
