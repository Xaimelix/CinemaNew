import sqlalchemy
import sqlalchemy.orm as orm

from .db_session import SqlAlchemyBase


class Film(SqlAlchemyBase):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    id_genre = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("genres.id"), nullable=True)
    genre = orm.relationship('Genre')
    country = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    url_poster = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rating = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    short_description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    url_kinopoisk = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    kinopoisk_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
