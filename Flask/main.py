from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.tasks import Tasks
from forms.user import RegisterForm, LoginForm
import datetime as dt
from flask_login import LoginManager, login_user

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
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пользователь уже существует")
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
        return render_template('login_new.html', message='Неверный логин или пароль',
                               form=form, title='Авторизация')
    return render_template('login_new.html', title='Авторизация', form=form)


@app.route('/')
def index():
    return render_template('index.html', title='-')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/task1')
def task1():
    db_sess = db_session.create_session()
    tasks = db_sess.query(Tasks).filter(Tasks.n_t == 1)
    return render_template('task1.html', title='Геометрия на плоскости', tasks=tasks)


@app.route('/task2')
def task2():
    pass


@app.route('/task3')
def task3():
    pass


@app.route('/task4')
def task4():
    db_sess = db_session.create_session()
    tasks = db_sess.query(Tasks).filter(Tasks.n_t == 4)
    return render_template('task1.html', title='Введение в теорию вероятностей', tasks=tasks)


@app.route('/task5')
def task5():
    db_sess = db_session.create_session()
    tasks = db_sess.query(Tasks).filter(Tasks.n_t == 5)
    return render_template('task1.html', title='Задачи на теорию вероятностей', tasks=tasks)


@app.route('/task6')
def task6():
    pass


@app.route('/task7')
def task7():
    pass


@app.route('/task8')
def task8():
    pass


@app.route('/task9')
def task9():
    pass


@app.route('/task10')
def task10():
    db_sess = db_session.create_session()
    tasks = db_sess.query(Tasks).filter(Tasks.n_t == 10)
    return render_template('task1.html', title='Задачи на теорию вероятностей', tasks=tasks)


@app.route('/task11')
def task11():
    pass


@app.route('/task12')
def task12():
    pass


def main():
    db_session.global_init('db/info.db')
    app.run()


if __name__ == '__main__':
    main()
