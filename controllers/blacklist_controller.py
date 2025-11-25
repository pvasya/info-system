from urllib.parse import parse_qs
from core.controller import BaseController
from models.user import UserDAO


def view_blacklist(req):
    ctrl = BaseController(req)
    
    if not ctrl.require_login():
        ctrl.redirect('/login')
        return

    if not ctrl.user.is_admin:
        ctrl.redirect('/')
        return


    users = UserDAO().get_all()
    ctrl.render('blacklist.html', {'user': ctrl.user, 'users': users})


def toggle_blacklist(req):
    ctrl = BaseController(req)
    if not ctrl.require_login() or not ctrl.user.is_admin:
        ctrl.redirect('/')
        return

    content_length = int(req.headers.get('Content-Length', 0))
    post_data = req.rfile.read(content_length).decode()
    form = parse_qs(post_data)
    
    user_id = form.get('user_id', [None])[0]

    if user_id:
        dao = UserDAO()
        user = dao.get_by_id(int(user_id))
        if user and not user.is_admin:
            user.is_blocked = not user.is_blocked
            dao.update(user)

    ctrl.redirect('/blacklist')