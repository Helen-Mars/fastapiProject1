from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator
from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel



sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    print("Startup: Create DB and tables")
    create_db_and_tables()
    yield
    print("Shutting down: Close DB and tables")
    cleanup_resources()


def cleanup_resources():
    # Your logic to clean up resources, such as closing DB connections
    pass


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
