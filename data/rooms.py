import sqlalchemy

from .db_session import SqlAlchemyBase


class Room(SqlAlchemyBase):
    __tablename__ = 'rooms'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
