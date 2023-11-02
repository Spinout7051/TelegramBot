from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from settings import DATABASE_NAME


engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Journal(Base):
    __tablename__ = 'journal'
    id = Column(Integer, primary_key=True)
    command_name = Column(String(16), nullable=False)
    search_city = Column(String(16), nullable=False)
    hotels_count = Column(String(16), nullable=False)
    need_photos = Column(Boolean, nullable=False)
    photos_count = Column(String(16), nullable=False)
    price_range = Column(String(16))
    town_distance = Column(String(16))
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    hotel = relationship('Hotel', backref='journal')


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(16), nullable=False, unique=True)
    journal = relationship('Journal', backref='user')


class Hotel(Base):
    __tablename__ = 'hotel'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    address = Column(String(16), nullable=False)
    price = Column(String(16))
    overall_score = Column(String(16))
    distance = Column(String(16))
    journal_id = Column(Integer, ForeignKey('journal.id'))


Base.metadata.create_all(engine)
