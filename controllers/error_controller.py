from core.controller import BaseController


def not_found(req):
    ctrl = BaseController(req)
    ctrl.render('404.html', {'user': ctrl.user, 'is_404': True}, status=404)