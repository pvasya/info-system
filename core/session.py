from http import cookies
from models.user import UserDAO

SESSION_COOKIE = 'session_id'

def load_session(request_handler):
    cookie_header = request_handler.headers.get('Cookie')
    if not cookie_header:
        return None
    cookie = cookies.SimpleCookie(cookie_header)
    morsel = cookie.get(SESSION_COOKIE)
    if not morsel:
        return None
    session_id = morsel.value
    user = UserDAO().find_by_cookie(session_id)
    return user

def set_session(request_handler, user):
    request_handler.send_header(
        'Set-Cookie',
        f"{SESSION_COOKIE}={user.cookie}; Path=/; HttpOnly"
    )

def clear_session(request_handler):
    request_handler.send_header(
        'Set-Cookie',
        f"{SESSION_COOKIE}=; Path=/; Max-Age=0; HttpOnly"
    )