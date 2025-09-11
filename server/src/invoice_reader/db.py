import sqlmodel

from invoice_reader import (
    models,  # noqa: F401
    settings,
)

engine = sqlmodel.create_engine(settings.DATABASE_URL, echo=False)


def create_db_and_tables():
    sqlmodel.SQLModel.metadata.create_all(engine)


def get_session():
    with sqlmodel.Session(engine) as session:
        yield session
