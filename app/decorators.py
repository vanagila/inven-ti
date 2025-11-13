from functools import wraps
from flask import session, redirect, url_for, flash, request

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        is_admin = session.get('is_admin', False)

        if not user_id:
            flash('Você precisa estar logado.', 'danger')
            return redirect(url_for('auth.login', next=request.url))
        
        if not is_admin:
            flash('Acesso restrito a administradores.', 'warning')
            return redirect(url_for('auth.painel'))
        
        return view_func(*args, **kwargs)
    return wrapper

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')

        if not user_id:
            flash('Você precisa estar logado.', 'danger')
            return redirect(url_for('auth.login', next=request.url))
        
        return view_func(*args, **kwargs)
    return wrapper