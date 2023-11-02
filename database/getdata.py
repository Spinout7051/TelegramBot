from loguru import logger

from sqlalchemy import desc

from database.model import Hotel, Journal, User, session


@logger.catch
def get_user_data(telegram_user_id):
    telegram_user = session.query(User).filter(User.telegram_id == telegram_user_id).first()
    db_data = session.query(Journal).filter(Journal.user_id == telegram_user.id).order_by(desc(Journal.date)).limit(5)

    return db_data


@logger.catch
def get_journal_data(journal_id):
    db_data = session.query(Journal).filter(Journal.id == journal_id).first()

    return db_data


@logger.catch
def get_hotel_data(journal_id):
    db_data = session.query(Hotel).filter(Hotel.journal_id == journal_id).all()

    return db_data
