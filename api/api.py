from datetime import datetime
import requests

from loguru import logger

from settings import (
    CURRENCY,
    LOCALE,
    RAPIDAPI_KEY,
    RAPIDAPI_HOST
)


HEADERS = {
    'X-RapidAPI-Key': RAPIDAPI_KEY,
    'X-RapidAPI-Host': RAPIDAPI_HOST
}


@logger.catch
def locations_search(city):
    url = 'https://hotels4.p.rapidapi.com/locations/v3/search'

    querystring = {'q': city, 'locale': LOCALE}
    response = requests.request('GET', url, headers=HEADERS, params=querystring).json()

    return response


@logger.catch
def properties_list(regionId, resultsSize, price, sort):

    """
    Sort, One of the following:
    PRICE_RELEVANT (Price + our picks)
    REVIEW (Guest rating)
    DISTANCE (Distance from downtown)
    PRICE_LOW_TO_HIGH (Price)
    PROPERTY_CLASS (Star rating)
    RECOMMENDED (Recommended)
    """

    url = 'https://hotels4.p.rapidapi.com/properties/v2/list'

    # Получаем дни check_in и check_out для получения актуальных цен
    now_day = datetime.now()

    check_in = {
            'day': now_day.day + 1,
            'month': now_day.month,
            'year': now_day.year
        }

    check_out = {
            'day': now_day.day + 2,
            'month': now_day.month,
            'year': now_day.year
        }

    payload = {
        'currency': CURRENCY,
        'eapid': 1,
        'locale': LOCALE,
        'siteId': 300000001,
        'destination': {'regionId': regionId},
        'checkInDate': check_in,
        'checkOutDate': check_out,
        'rooms': [
            {
                'adults': 1,
            }
        ],
        'resultsStartingIndex': 0,
        'resultsSize': resultsSize,
        'sort': sort,
        'filters': {'price': price}
    }

    response = requests.request('POST', url, json=payload, headers=HEADERS).json()

    return response


@logger.catch
def get_details(propertyId):
    url = 'https://hotels4.p.rapidapi.com/properties/v2/detail'

    payload = {
        'currency': CURRENCY,
        'eapid': 1,
        'locale': LOCALE,
        'siteId': 300000001,
        'propertyId': propertyId
    }

    response = requests.request('POST', url, json=payload, headers=HEADERS).json()

    return response


@logger.catch
def get_hotel_photos(id_hotel):
    url = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'
    querystring = {'id': id_hotel}

    response = requests.request('GET', url, headers=HEADERS, params=querystring).json()
    return response
