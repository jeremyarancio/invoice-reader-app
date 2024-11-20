import sqlmodel

from invoice_reader import settings
from invoice_reader import models # noqa: F401


connect_args = {"check_same_thread": False}
engine = sqlmodel.create_engine(settings.DATABASE_URL, echo=True, connect_args=connect_args)


def create_db_and_tables():
	sqlmodel.SQLModel.metadata.create_all(engine)


def get_session():
	with sqlmodel.Session(engine) as session:
		yield session