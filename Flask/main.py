from flask import Flask, render_template, redirect, request, make_response, session, abort
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
import datetime as dt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=1)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title="Регистрация", form=form, message='Пароли разные!')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form, message="Пользователь уже существует")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login1.html', message='Неверный логин или пароль',
                               form=form, title='Авторизация')
    return render_template('login1.html', titlle='Авторизация', form=form)


@app.route('/')
def index():
    return render_template('index.html', title='-')


def main():
    db_session.global_init('db/info.db')
    app.run()


if __name__ == '__main__':
    main()
