import api.api as api
from loguru import logger


@logger.catch
def get_hotels(city, hotels_count, need_photos=False, photos_count=0,
               command_name=None, price_range=None, town_distance=None):
    try:
        locations_search_data = api.locations_search(city=city)
        sr = locations_search_data.get('sr')
    except AttributeError as exp:
        print(locations_search_data, exp)
        raise Exception(exp)

    gaiaId_list = []
    hotels_data_list = []

    for item in sr:
        if item.get('type') == 'CITY':
            gaiaId_list.append(item.get('gaiaId'))
            break

    for des_id in gaiaId_list:
        sort = 'PRICE_LOW_TO_HIGH'
        if command_name == 'highprice':
            price = {
                'max': 5000,
                'min': 500,
            }
            properties_json = api.properties_list(regionId=des_id, resultsSize=100, price=price, sort=sort)
        elif command_name == 'lowprice':
            price = {
                'max': 1500,
                'min': 1,
            }
            properties_json = api.properties_list(regionId=des_id, resultsSize=hotels_count, price=price, sort=sort)
        elif command_name == 'bestdeal':
            sort = 'DISTANCE'
            price = {
                'max': int(price_range[1]),
                'min': int(price_range[0]),
            }
            print(f'PRICE ======= {price}')
            properties_json = api.properties_list(regionId=des_id, resultsSize=200, price=price, sort=sort)
            print(properties_json)

        prop_properties_json = properties_json.get('data').get('propertySearch').get('properties')

        if command_name == 'highprice':
            prop_properties_json.reverse()
        elif command_name == 'bestdeal':
            bad_prop = []

            for prop in prop_properties_json:
                hotels_distance = prop.get('destinationInfo').get('distanceFromDestination').get('value')
                if not float(town_distance[0]) <= hotels_distance <= float(town_distance[1]):
                    bad_prop.append(prop)

            for prop in bad_prop:
                prop_properties_json.remove(prop)

        for prop in prop_properties_json[:hotels_count]:
            details_json = api.get_details(prop.get('id'))
            if need_photos:
                hotel_photos_urls_list = []
                images_details_json = details_json.get('data').get('propertyInfo').get('propertyGallery').get('images')

                for image in images_details_json[:photos_count]:
                    hotel_photos_urls_list.append(image.get('image').get('url'))
            else:
                hotel_photos_urls_list = None

            propertyInfo_json = details_json.get('data').get('propertyInfo')
            hotels_data_list.append(
                {
                    'hotel_id': propertyInfo_json.get('summary').get('id'),
                    'hotel_name': propertyInfo_json.get('summary').get('name'),
                    'hotel_address': propertyInfo_json.get('summary').get('location').get(
                        'address').get('addressLine'),
                    'overallScore': propertyInfo_json.get('reviewInfo').get('summary').get(
                        'overallScoreWithDescriptionA11y').get('value'),
                    'price': prop.get('price').get('lead').get('formatted'),
                    'photos': hotel_photos_urls_list,
                    'distance': prop.get('destinationInfo').get('distanceFromDestination').get('value'),
                }
            )

    if len(hotels_data_list) > 0:
        return hotels_data_list

    return None
