import sqlalchemy

from .db_session import SqlAlchemyBase


class Genre(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)