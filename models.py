import os
import atexit

from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped, relationship

from typing import List


POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRS_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRS_PORT}/{POSTGRES_DB}"


engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    advertisements: Mapped[List['Advertisement']] = relationship('Advertisement', back_populates="owner", cascade="all, delete-orphan")

    @property
    def json(self):
        return {
            "user_id": self.id,
            "name": self.name,
            "advertisements": [{'advertisemrnt_id': adv.id, 'title': adv.title, 'description': adv.description} for adv in self.advertisements]
            }
    
class Advertisement(Base):

    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    owner: Mapped['User'] = relationship('User', back_populates="advertisements")

    @property
    def json(self):
        return {
            "advertisement_id": self.id,
            "title": self.title,
            "description": self.description,
            "owner": self.owner.name
            }

Base.metadata.create_all(bind=engine)

atexit.register(engine.dispose)