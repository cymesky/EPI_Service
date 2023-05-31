from sqlalchemy import Column, Integer, DECIMAL, inspect
from sqlalchemy.ext.declarative import declarative_base
from typing import Type
from sqlalchemy.engine import Engine

Base = declarative_base()


class EexGermany(Base):
    __tablename__ = 'eex_germany'

    id = Column(Integer, primary_key=True)
    quarter = Column(Integer)
    year = Column(Integer)
    price = Column(DECIMAL(precision=10, scale=2))

    @classmethod
    def table_exists(cls: Type['EexGermany'], engine: Engine) -> bool:
        inspector = inspect(engine)
        return inspector.has_table(cls.__tablename__)

    @classmethod
    def create_table(cls: Type['EexGermany'], engine: Engine):
        Base.metadata.create_all(engine)

    def __repr__(self) -> str:
        return f"Q{self.quarter} {self.year} - {self.price}/MWh"
