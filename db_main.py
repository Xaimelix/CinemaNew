import PIL
import os

from data import db_session
from flask import Flask

from PIL import ImageFont, ImageDraw, Image

from data.films import Film
from data.genres import Genre
from data.rooms import Room
from data.sessions import Session
from data.tickets import Ticket
from data.users import User

from api.api_code import get_genres, get_films

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init("db/cinema.db")
db_sess = db_session.create_session()


def main():
    film = Film()
    room = Room()
    session = Session()
    ticket = Ticket()
    user = User()

    # Добавление жанров
    # for i in get_genres():
    #     genre = Genre()
    #     genre.name = i
    #     db_sess.add(genre)

    # Добавление фиьмов
    for i in get_films():
        film = Film()
        film.name = i['nameRu']
        film.duration = i['filmLength']
        film.year = i['year']
        film.country = i['countries'][0]['country']
        film.url_poster = i['posterUrl']
        film.rating = i['ratingKinopoisk']
        film.description = i['description']
        film.short_description = i['shortDescription']
        film.url_kinopoisk = i['webUrl']
        film.kinopoisk_id = i['kinopoiskId']
        name_genre = i['genres'][0]['genre']
        for genre in db_sess.query(Genre).all():
            if genre.name == name_genre:
                film.id_genre = genre.id

        db_sess.add(film)
    db_sess.commit()

    # app.run()


def draw_ticket(session_id, number):
    id_session = session_id
    session = db_sess.query(Session).filter(Session.id == id_session).first()
    date = f'{session.date[8:]}.{session.date[5:7]}.{session.date[2:4]}'
    time = session.time
    cost = session.cost

    id_room = session.id_room
    room = db_sess.query(Room).filter(Room.id == id_room).first()
    room_name = room.name

    id_film = session.id_film
    film = db_sess.query(Film).filter(Film.id == id_film).first()
    film_name = film.name
    # db_sess.commit()

    img = Image.open("static/img/ticket.png")
    draw = ImageDraw.Draw(img)
    try:
        font_very_big = ImageFont.truetype("static/fonts/Disket-Mono-Bold.ttf", 600)
        font_very_big_two = ImageFont.truetype("static/fonts/Disket-Mono-Bold.ttf", 350)
        font_big = ImageFont.truetype("static/fonts/Disket-Mono-Bold.ttf", 58)
        font_small = ImageFont.truetype("static/fonts/Disket-Mono-Bold.ttf", 45)
    except Exception as e:
        print(e)
    draw.text((980, 495), date, (174, 0, 38), font=font_big)
    draw.text((1400, 495), time, (174, 0, 38), font=font_big)
    print(film_name)
    draw.text((500, 665), film_name, (174, 0, 38), font=font_small)
    draw.text((150, 740), f'{cost} р.', (174, 0, 38), font=font_big)
    if number < 10:
        draw.text((1960, 100), str(number), (174, 0, 38), font=font_very_big)
    else:
        draw.text((1910, 220), str(number), (174, 0, 38), font=font_very_big_two)

    line_height_big = sum(font_big.getmetrics())
    fontimage = Image.new('L', (font_big.getsize(room_name)[0], line_height_big))
    ImageDraw.Draw(fontimage).text((0, 0), room_name, fill=255, font=font_big)
    fontimage = fontimage.rotate(90, resample=Image.BICUBIC, expand=True)
    img.paste((174, 0, 38), box=(15, 250), mask=fontimage)
    img = img.resize((850, 280), PIL.Image.LANCZOS)
    img.save(f'static/img/tickets/ticket_{number}.png')
        # return f'{id_session}, {film_name}, {date}, {time}, {room_name}'
def get_tickets(user_name):
    user = db_sess.query(User).filter(User.login == user_name).first()
    user_id = user.id
    c = 0
    tickets = db_sess.query(Ticket).filter(Ticket.id_user == user_id)
    for ticket in tickets:
        c += 1
        draw_ticket(ticket.id_session, c)

def add_ticket(session_id, user_id):
    db_session.global_init("db/cinema.db")
    db_sess = db_session.create_session()
    ticket = Ticket()
    session = db_sess.query(Session).filter(Session.id == session_id).first()
    # print(session)
    ticket.id_session = session_id
    ticket.id_user = user_id
    # print(session.amount)
    session.amount += 1
    db_sess.add(ticket)
    db_sess.merge(session)
    db_sess.commit()
    print(len(os.listdir('static/img/tickets')))
    draw_ticket(ticket.id_session, len(os.listdir('static/img/tickets')) + 1)

def avatar():
    img = Image.open("static/img/d_avatar.png")
    img.save('static/img/avatar.png')




if __name__ == '__main__':
    # main()
    get_tickets('igor565')
