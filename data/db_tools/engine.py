import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def create_database_engine() -> Engine:
    db_username = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_name = os.getenv("POSTGRES_DB")

    if not all([db_username, db_password, db_host, db_name]):
        raise ValueError("Missing PostgreSQL environment variables")

    return create_engine(("postgresql://"
                          f"{db_username}:{db_password}@"
                          f"{db_host}/{db_name}"))
