from core.controller import BaseController
from models.order import Order, OrderDAO
from models.order_items import OrderItemsDAO
from models.basket import BasketDAO
from models.goods import GoodsDAO
from models.user import UserDAO
from core.logger import logger

def view_orders(req):
    ctrl = BaseController(req)
    if not ctrl.require_login():
        return

    display = []
    if ctrl.user.is_admin:
        raw = OrderDAO().get_all()
        for o in raw:
            u = UserDAO().get_by_id(o.user_id)
            order_items = OrderItemsDAO().get_by_order(o.id)
            goods_list = []
            goods_text_parts = []
            total = 0
            for item in order_items:
                goods = GoodsDAO().find_by_id(item.good_id)
                goods_list.append({
                    'goods': goods,
                    'good_id': item.good_id,
                    'quantity': item.quantity,
                    'subtotal': (goods.price * item.quantity) if goods else 0
                })
                if goods:
                    goods_text_parts.append(f"{goods.name} {float(goods.price):.2f} x {item.quantity}")
                    total += goods.price * item.quantity
                else:
                    goods_text_parts.append(f"[id {item.good_id}] x {item.quantity}")

            display.append({
                'order': o,
                'username': u.username,
                'order_items': goods_list,
                'goods_text': ', '.join(goods_text_parts),
                'total': total
            })
    else:
        raw = OrderDAO().get_by_user(ctrl.user.id)
        for o in raw:
            order_items = OrderItemsDAO().get_by_order(o.id)
            goods_list = []
            goods_text_parts = []
            total = 0
            for item in order_items:
                goods = GoodsDAO().find_by_id(item.good_id)
                goods_list.append({
                    'goods': goods,
                    'good_id': item.good_id,
                    'quantity': item.quantity,
                    'subtotal': (goods.price * item.quantity) if goods else 0
                })
                if goods:
                    goods_text_parts.append(f"{goods.name} {float(goods.price):.2f} x {item.quantity}")
                    total += goods.price * item.quantity
                else:
                    goods_text_parts.append(f"[id {item.good_id}] x {item.quantity}")

            display.append({
                'order': o,
                'order_items': goods_list,
                'goods_text': ', '.join(goods_text_parts),
                'total': total
            })

    ctrl.render('orders.html', {'user': ctrl.user, 'orders': display})

def create_order(req):
    ctrl = BaseController(req)
    if not ctrl.require_login() or ctrl.user.is_admin:
        ctrl.redirect('/')
        return

    items = BasketDAO().get_active_by_user(ctrl.user.id)
    counts = {}
    for it in items:
        counts[it.goods_id] = counts.get(it.goods_id, 0) + 1

    if not counts:
        ctrl.redirect('/')
        return

    new_order = Order(None, ctrl.user.id, True, None)
    order_id = OrderDAO().create(new_order)

    order_items_dao = OrderItemsDAO()
    for gid, qty in counts.items():
        order_items_dao.add_item(order_id, gid, qty)

    BasketDAO().clear(ctrl.user.id)

    goods_names = []
    for gid, qty in counts.items():
        goods = GoodsDAO().find_by_id(gid)
        if goods:
            goods_names.append(f"{qty} - {goods.name}")

    goods_str = ', '.join(goods_names)
    logger.info(f"User {ctrl.user.username} created an order: {goods_str}")
    ctrl.redirect('/orders')

def complete_order(req):
    ctrl = BaseController(req)
    if not ctrl.require_login() or not ctrl.user.is_admin:
        ctrl.redirect('/')
        return
    data = ctrl.parse_form()
    oid = data.get('id')
    if oid:
        OrderDAO().complete(int(oid))
    ctrl.redirect('/orders')