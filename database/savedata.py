import datetime

from loguru import logger

from commands import userdata
from database.model import Hotel, Journal, User, session


@logger.catch
def add_user(telegram_id):
    entry = session.query(User).filter_by(telegram_id=telegram_id).first()
    if entry:
        return entry.id

    entry = User(telegram_id=telegram_id)
    session.add(entry)
    session.flush()
    return entry.id


@logger.catch
def add_search_result_data(search_result_data, journal_id):
    for data in search_result_data:
        entry = Hotel(
            name=data.get('hotel_name'),
            address=data.get('hotel_address'),
            price=data.get('price'),
            overall_score=data.get('overallScore'),
            distance=data.get('distance'),
            journal_id=journal_id,
        )
        session.add(entry)
        session.flush()


@logger.catch
def add_journal_data(search_result_data):
    user_id = add_user(telegram_id=userdata.input_user_data.id_telegram_user)
    date = datetime.datetime.now()

    town_distance = ''.join(str(userdata.input_user_data.town_distance))
    price_range = ''.join(str(userdata.input_user_data.price_range))

    new_data = Journal(command_name=userdata.input_user_data.command_name,
                       search_city=userdata.input_user_data.search_city,
                       hotels_count=userdata.input_user_data.hotels_count,
                       need_photos=userdata.input_user_data.need_photos,
                       photos_count=userdata.input_user_data.photos_count,
                       price_range=price_range,
                       town_distance=town_distance,
                       date=date,
                       user_id=user_id)

    session.add(new_data)
    session.flush()

    add_search_result_data(search_result_data=search_result_data, journal_id=new_data.id)

    session.commit()
