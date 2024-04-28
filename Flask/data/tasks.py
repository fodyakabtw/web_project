import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Tasks(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    task = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    answ = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    n_t = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
