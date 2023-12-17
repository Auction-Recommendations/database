from sqlalchemy import Column, Integer, String, DateTime, UUID, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)


class Lot(Base):
    __tablename__ = 'lots'

    id = Column(String, primary_key=True)
    name = Column(String)
    city = Column(String)
    priceStart = Column(Integer)
    sellerId = Column(String)


class View(Base):
    __tablename__ = 'views'

    id = Column(UUID(as_uuid=True), primary_key=True)
    viewedAt = Column(DateTime(timezone=False))
    lotId = Column(String)
    userId = Column(String)


