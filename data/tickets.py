import sqlalchemy
import sqlalchemy.orm as orm

from .db_session import SqlAlchemyBase


class Ticket(SqlAlchemyBase):
    __tablename__ = 'tickets'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    id_session = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("sessions.id"), nullable=False)
    user = orm.relationship('User')
    session = orm.relationship('Session')