from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .. import db
from .forms import LoginForm 

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está registrado.')
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.')
            return redirect(url_for('auth.login'))
    return render_template('register.html')