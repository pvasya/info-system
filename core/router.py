from controllers import auth_controller, catalog_controller, profile_controller, basket_controller, orders_controller, blacklist_controller, error_controller, ratings_controller

class Router:
    def __init__(self):
        self.routes = {
            'GET': {
                '/': catalog_controller.index,
                '/login': auth_controller.show_login,
                '/register': auth_controller.show_register,
                '/logout': auth_controller.logout,
                '/profile': profile_controller.view_profile,
                '/basket': basket_controller.view_basket,
                '/orders': orders_controller.view_orders,
                '/blacklist': blacklist_controller.view_blacklist,
                '/goods/rating': ratings_controller.get_goods_rating,
            },
            'POST': {
                '/login': auth_controller.login,
                '/register': auth_controller.register,
                '/goods/add': catalog_controller.add_goods,
                '/goods/update': catalog_controller.update_goods,
                '/goods/delete': catalog_controller.delete_goods,
                '/goods/rate': ratings_controller.rate_goods,
                '/profile/update': profile_controller.update_profile,
                '/basket/add': basket_controller.add_to_basket,
                '/basket/remove': basket_controller.remove_from_basket,
                '/orders/create': orders_controller.create_order,
                '/orders/complete': orders_controller.complete_order,
                '/blacklist/toggle': blacklist_controller.toggle_blacklist,
            }
        }

    def handle(self, request_handler):
        method = request_handler.command
        path = request_handler.path.split('?')[0]
        handler = self.routes.get(method, {}).get(path)
        if handler:
            handler(request_handler)
        else:
            error_controller.not_found(request_handler)