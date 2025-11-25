from core.controller import BaseController
from models.user import UserDAO
from core.logger import logger
import bcrypt
from urllib.parse import unquote_plus

def view_profile(req):
    ctrl = BaseController(req)
    if not ctrl.require_login(): return
    ctrl.render('profile.html', {'user': ctrl.user})


def update_profile(req):
    ctrl = BaseController(req)
    if not ctrl.require_login(): return
    data = ctrl.parse_form()
    user = ctrl.user

    user.username = unquote_plus(data.get('username', user.username).strip())
    user.real_name = unquote_plus(data.get('name', user.real_name).strip())
    user.email = unquote_plus(data.get('email', user.email).strip())
    user.address = unquote_plus(data.get('address', user.address).strip())

    new_pw = unquote_plus(data.get('password', '').strip())
    if new_pw:
        pw_bytes = new_pw.encode('utf-8')
        hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt()).decode('utf-8')
        user.password_hash = hashed

    UserDAO().update(user)
    logger.info(f"User {user.username} updated profile successfully.")

    ctrl.redirect('/profile')
