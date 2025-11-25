from core.controller import BaseController
from core.session import set_session, clear_session
from models.user import UserDAO, User
from core.logger import logger
import bcrypt
import uuid

def show_login(req):
    ctrl = BaseController(req)
    if ctrl.user:
        ctrl.redirect('/')
        return
    ctrl.render('login.html')

def login(req):
    ctrl = BaseController(req)
    data = ctrl.parse_form()
    username = data.get('username', '')
    password = data.get('password', '')

    user = UserDAO().find_by_username(username)
    if user and not user.is_blocked:
        pw_bytes = password.encode('utf-8')
        stored_hash = user.password_hash.encode('utf-8')
        if bcrypt.checkpw(pw_bytes, stored_hash):
            handler = ctrl.req
            handler.send_response(302)
            set_session(handler, user)
            handler.send_header('Location', '/')
            handler.end_headers()
            logger.info(f"User {user.username} login successfully.")
            return

    logger.warning(f"Anonymous login attempt with username: {username}")
    ctrl.render('login.html', {'error': 'Wrong username or password'}, 401)
    
def logout(req):
    ctrl = BaseController(req)
    handler = ctrl.req
    handler.send_response(302)
    clear_session(handler)
    handler.send_header('Location', '/')
    handler.end_headers()
    logger.info(f"User {ctrl.user.username} logout successfully.")

def show_register(req):
    ctrl = BaseController(req)
    if ctrl.user:
        ctrl.redirect('/')
        return
    ctrl.render('register.html')

def register(req):
    ctrl = BaseController(req)
    if ctrl.user:
        ctrl.redirect('/')
        return

    data = ctrl.parse_form()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    email = data.get('email', '').strip()
    name = data.get('name', '').strip()
    address = data.get('address', '').strip()

   
    errors = []

    if not username or len(username) < 3:
        errors.append('Username must be at least 3 characters long')

    if not password or len(password) < 6:
        errors.append('Password must be at least 6 characters long')

    if not email or '@' not in email:
        errors.append('Please enter a valid email address')

    if not name:
        errors.append('Name is required')

  
    if UserDAO().find_by_username(username):
        errors.append('Username already exists')

    if UserDAO().find_by_email(email):
        errors.append('Email already exists')

    if errors:
        ctrl.render('register.html', {'errors': errors, 'form_data': data})
        return

  
    cookie = str(uuid.uuid4())

   
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

  
    new_user = User(
        id=None,
        username=username,
        password_hash=password_hash,
        real_name=name,
        address=address,
        email=email,
        is_admin=False,  
        is_blocked=False,
        cookie=cookie
    )

    try:
        UserDAO().create(new_user)
        logger.info(f"New user registered: {username}")

    
        handler = ctrl.req
        handler.send_response(302)
      
        user = UserDAO().find_by_username(username)
        set_session(handler, user)
        handler.send_header('Location', '/')
        handler.end_headers()

    except Exception as e:
        logger.error(f"Error registering user {username}: {str(e)}")
        ctrl.render('register.html', {'errors': ['Registration failed. Please try again.'], 'form_data': data})
