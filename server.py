import datetime
import locale
import os

import flask
from flask import render_template, redirect, request
from flask_login import login_required, logout_user
from sqlalchemy import update

import cool_func
from api.API_REQ import get_trailer
from cool_func import to_date_datetime_format
from data.films import Film
from data.genres import Genre
from data.sessions import Session
from data.tickets import Ticket
from data.rooms import Room
from forms.login import *

from data import db_session
from data.users import User
from forms.register import RegisterForm

from db_main import get_tickets, add_ticket, avatar

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/cinema.db")


@app.route('/')
@app.route('/index')
def index():
    """Основная старница"""
    locale.setlocale(
        category=locale.LC_ALL,
        locale="Russian"
    )
    now_date = f"{datetime.datetime.today().strftime('%d-%m').split('-')[0]} {datetime.datetime.today().strftime('%B')}"
    db_sess = db_session.create_session()
    # datetime.datetime.today().strftime('%Y-%m-%d'))
    # '2023-04-28'
    count_sessions = len(
        db_sess.query(Session).filter(Session.date == datetime.datetime.today().strftime('%Y-%m-%d')).all())
    sessions = db_sess.query(Session).filter(Session.date == datetime.datetime.today().strftime('%Y-%m-%d')).all()
    films = db_sess.query(Film).all()
    return render_template('base.html', current_user=current_user, title='Кинотеатр',
                           today=now_date, count_sessions=count_sessions, sessions=sessions, films=films)


@app.route('/create_sessions', methods=['POST', 'GET'])
def create_sessions():
    """Создание сессии в кинотеатре. Форма."""
    if request.method == 'GET':
        return render_template('create_sessions.html')
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        """проверка на дату, если не введена, то в БД сеанс не добавляем"""
        if request.form['date'] and request.form['time'] and not db_sess.query(Session).filter(
                Session.date == request.form['date'], Session.time == request.form['time']).all():
            session = Session(
                id_film=request.form['id_film'],
                date=request.form['date'],
                time=request.form['time'],
                cost=request.form['cost'],
                amount=request.form['amount'],
                id_room=request.form['id_room']
            )
            db_sess.add(session)
            db_sess.commit()
        return redirect('/')


@app.route('/schedule')
def schedule():
    """Расписание. Возвращает html с постерами"""
    db_sess = db_session.create_session()
    sessions = db_sess.query(Session).filter(Session.date == datetime.datetime.today().strftime('%Y-%m-%d')).all()
    films = db_sess.query(Film).all()
    week = []
    today_human = datetime.datetime.today().strftime('%Y-%m-%d')
    locale.setlocale(
        category=locale.LC_ALL,
        locale="Russian"
    )
    today = datetime.datetime.today()
    start = today - datetime.timedelta(days=today.weekday())
    make_week = [start + datetime.timedelta(days=i) for i in range(7)]
    for i in make_week:
        if i == today:
            week.append((i.strftime('%d'), i.strftime('%m'), i.strftime('%B'),
                         '(Сегодня)'))
        else:
            week.append((i.strftime('%d'), i.strftime('%m'), i.strftime('%B')))
    return render_template('schedule.html', sessions=sessions, films=films, today_human=today_human, week=week)


@app.route('/schedule/<date>')
def schedule_date(date):
    db_sess = db_session.create_session()
    date = f'{datetime.datetime.today().year}-' + date
    date_datetime_format = to_date_datetime_format(date)
    date_for_session_db = date_datetime_format.strftime('%Y-%m-%d')
    sessions = db_sess.query(Session).filter(Session.date == date_for_session_db).all()
    films = db_sess.query(Film).all()
    week = []
    today_human = datetime.datetime.today().strftime('%Y-%m-%d')
    locale.setlocale(
        category=locale.LC_ALL,
        locale="Russian"
    )
    today = datetime.datetime.today()
    start = today - datetime.timedelta(days=today.weekday())
    make_week = [start + datetime.timedelta(days=i) for i in range(7)]
    for i in make_week:
        if i == today:
            week.append((i.strftime('%d'), i.strftime('%m'), i.strftime('%B'),
                         '(Сегодня)'))
        else:
            week.append((i.strftime('%d'), i.strftime('%m'), i.strftime('%B')))
    light_the_button_with_date = date.split('-')[-1]
    return render_template('schedule.html', sessions=sessions, films=films, today_human=today_human,
                           week=week, light_the_button_with_date=light_the_button_with_date)


@app.route('/session/<sess_id>/<id_film>')
def session(sess_id, id_film):
    """Страница только с одним фильмом"""
    db_sess = db_session.create_session()
    id_film = int(id_film)
    '''получение информации из таблицы Film'''
    film = db_sess.query(Film).filter(Film.id == id_film).first()
    kinop_id = film.kinopoisk_id
    poster = film.url_poster
    name = film.name
    desc = film.description
    country = film.country
    year = film.year
    genre = db_sess.query(Genre).filter(Genre.id == film.id_genre).first()
    genre = genre.name
    amount_tickets = db_sess.query(Session.amount).filter(Session.id == sess_id).first()[0]

    '''получение из формации из таблицы Session'''
    session = db_sess.query(Session).filter(Session.id == sess_id).first()
    id_room = session.id_room
    amount_room = db_sess.query(Room.amount).filter(Room.id == id_room).first()[0]
    amount = amount_room - amount_tickets



    '''загрузка трейлера'''
    resp = get_trailer(kinop_id)
    error = 0
    if int(resp['total']) > 0 and 'watch' not in \
            str([i['url'] for i in resp['items'] if i['site'] == 'YOUTUBE'][0]).split('/')[-1]:
        trailer_url_y = str([i['url'] for i in resp['items'] if i['site'] == 'YOUTUBE'][0]).split('/')[-1]
    else:
        trailer_url_y = 'ScMzIvxBSi4'  # placeholder video
        error = 1
    return render_template('session.html', id_film=id_film, poster=poster, name=name, desc=desc, country=country,
                           year=year, genre=genre, amount=amount,
                           trailer_url_y=trailer_url_y, error=error, sess_id=sess_id)


@app.route('/purchase-page/<sess_id>')
def purchase_page(sess_id):
    """Покупка билета"""
    db_sess = db_session.create_session()
    session = db_sess.query(Session).filter(Session.id == sess_id).first()
    amount_tickets = session.amount
    id_room = session.id_room
    amount_room = db_sess.query(Room.amount).filter(Room.id == id_room).first()[0]
    amount = amount_room - amount_tickets
    sess_id = int(sess_id)
    if amount - 1 > 0:
        date = db_sess.query(Session.date).filter((Session.id == sess_id)).first()[0]
        time = db_sess.query(Session.time).filter((Session.id == sess_id)).first()[0]
        cost = db_sess.query(Session.cost).filter((Session.id == sess_id)).first()[0]
        id_room = db_sess.query(Session.id_room).filter((Session.id == sess_id)).first()[0]
        no_places = False
    else:
        date = 0
        time = 0
        cost = 0
        id_room = 0
        no_places = True
    return render_template('purchase_page.html', date=date, time=time, cost=cost, id_room=id_room, sess_id=sess_id,
                           no_places=no_places)


@app.route('/bought/<sess_id>')
@login_required
def ticket_bought(sess_id):
    """Покупка билета. Заглушка, но работает корректно. Сделать дизайн!!!"""
    db_sess = db_session.create_session()
    sess_id = int(sess_id)
    print(sess_id, current_user.id)
    add_ticket(sess_id, current_user.id)

    # get_tickets(current_user.login)
    return redirect("/profile")


@app.errorhandler(401)
def unauthorized(error):
    return render_template('Error 401.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    dir = 'static/img/tickets'
    if len(os.listdir(dir)) > 0:
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
    logout_user()
    return redirect("/")


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    if request.method == 'POST':
        f = request.files['file']
        f.save('static/img/avatar.png')
        print(f.read())
    tickets_count = len(os.listdir(path="static/img/tickets"))
    return render_template('profile.html', tickets=tickets_count)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            avatar()
            get_tickets(user.login)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(login=form.login.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/video-load-error')
def video_load_error():
    return render_template('video_load_error.html')

def delete_past_sessions():
    """Удаляет прошедшие сессии фильмов автоматически. Желательно включать каждый день"""
    db_sess = db_session.create_session()
    sessions = db_sess.query(Session).all()
    for i in sessions:
        res = cool_func.is_date1_lower_date2(cool_func.to_date_datetime_format(i.date),
                                             to_date_datetime_format(datetime.datetime.now().strftime('%Y-%m-%d')))
        if res:
            db_sess.query(Session).filter(Session.id == i.id).delete()
            db_sess.commit()


if __name__ == '__main__':
    delete_past_sessions()
    app.run(port=8080, host='127.0.0.1')
