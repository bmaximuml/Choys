from datetime import datetime, timedelta
from logging import getLogger
from os import environ
from requests import get

from ..exceptions import InvalidModeError, RequestError


def get_duration(start, dest, mode='transit', language='en-GB', region='uk', units='metric'):
    return get_distance_matrix(start, dest, mode, language, region, units)[0]


def get_distance(start, dest, mode='transit', language='en-GB', region='uk', units='metric'):
    return get_distance_matrix(start, dest, mode, language, region, units)[1]


def get_distance_matrix(start, dest, mode='transit', language='en-GB', region='uk', units='metric'):
    logger = getLogger()
    if mode not in ['driving', 'walking', 'bicycling', 'transit']:
        raise InvalidModeError(f'Invalid mode: {str(mode)}')

    weekday = datetime.weekday(datetime.now())
    days_until_saturday = 6 if weekday == 6 else 5 - weekday

    midday_today = datetime.today().replace(hour=12, minute=0, second=0, microsecond=0)
    midday_sat = int(datetime.timestamp(midday_today + timedelta(days=days_until_saturday)))
    params = {
        'origins': f'{start}, UK',
        'destinations': dest,
        'key': environ['GMAPI'],
        'mode': mode,
        'language': language,
        'region': region,
        'departure_time': midday_sat,
        'units': units,
    }

    r = get("https://maps.googleapis.com/maps/api/distancematrix/json", params=params)
    # r_json = loads(r.json())
    r_json = r.json()
    if r_json['status']:
        # duration = r_json['rows'][0]['elements'][0]['duration']['value']
        # distance = r_json['rows'][0]['elements'][0]['distance']['value']
        element_status = r_json['rows'][0]['elements'][0]['status']
        if element_status == 'OK':
            duration = r_json['rows'][0]['elements'][0]['duration']
            distance = r_json['rows'][0]['elements'][0]['distance']
            return duration, distance
        else:
            logger.warning(f'Could not find distance for {start}. Status: {element_status}')
            return None, None
    else:
        raise RequestError('Google Maps Distance Matrix request returned an error.', r_json['status'])
