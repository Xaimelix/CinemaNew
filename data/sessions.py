import sqlalchemy
import sqlalchemy.orm as orm

from .db_session import SqlAlchemyBase


class Session(SqlAlchemyBase):
    __tablename__ = 'sessions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    id_film = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("films.id"), nullable=False, unique=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cost = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    id_room = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("rooms.id"), nullable=True)
    room = orm.relationship('Room')
    film = orm.relationship('Film')
