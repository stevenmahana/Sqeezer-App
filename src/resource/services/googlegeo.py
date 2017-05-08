import time
import datetime

import memcache
import requests

#from src.lib import Pw


cache = memcache.Client(['127.0.0.1:11211'], debug=0)
_cache = 60
#_access_key = Pw.p('GOOGLEAPI')

class GoogleGeo(object):
    '''
    https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA
    https://maps.googleapis.com/maps/api/geocode/json?address=Mountain+View,+CA
    https://maps.googleapis.com/maps/api/geocode/json?address=san+francisco,+CA
    '''

    BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'
    QRY_URL = False
    GET_URL = False
    HTTP = False
    POST = False
    AUTH = False
    nowDate = datetime.datetime.now()
    timestamp = time.mktime(nowDate.timetuple())


    def __init__(self, auth = None):
        print('>> googleapis')
        self.QRY_URL = self.BASE_URL # MOVE TO _QRY IF YOU NEED TO APPEND URL


    def _QRY(self,data):
        '''
            https://rekognition.com/developer/face
        '''
        self.PAYLOAD = data
        p = self.buildParams(data)

        call = self._CALL(p)
        response = self.filter(call)

        return response


    def filter(self, data):
        '''

        :param data:
        :return:
        '''
        result = []

        if not data:
            return result

        if data['status'] == 'OK':
            for v in data['results']:
                result.append(self.processResults(v))

        return result


    def processResults(self, data):

        if not data:
            return data

        geo = {
            'personCity': '',
            'personStreetAddress': '',
            'personDisplayAddress': '',
            'personIpAddress': '',
            'personCountry': '',
            'personStateProvince': '',
            'personPostalCode': '',
            'personTimeZone': '',
            'personLon': '',
            'personLat': ''
        }

        for key, value in data.iteritems():

            if key == 'address_components':
                for v in value:
                    if v['types'] == [ "street_number" ]:
                        geo['personStreetAddress'] = str(v['long_name']+' ')

                    if v['types'] == [ "route" ]:
                        geo['personStreetAddress'] += str(v['long_name'])

                    if v['types'] == [ "postal_code" ]:
                        geo['personPostalCode'] = str(v['long_name'])

                    if v['types'] == [ "locality", "political" ]:
                        geo['personCity'] = str(v['long_name'])

                    if v['types'] == [ "administrative_area_level_1", "political" ]:
                        geo['personStateProvince'] = str(v['short_name'])

                    if v['types'] == [ "country", "political" ]:
                        geo['personCountry'] = str(v['short_name'])

            if key == 'formatted_address':
                geo['personDisplayAddress'] = str(value)

            if key == 'geometry':
                geo['personLon'] = str(value['location']['lng'])
                geo['personLat'] = str(value['location']['lat'])



        return geo


    def buildParams(self, data):
        '''
            https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA
            https://maps.googleapis.com/maps/api/geocode/json?address=Mountain+View,+CA
            https://maps.googleapis.com/maps/api/geocode/json?address=san+francisco,+CA
        :param data:
            'image_link'
        :return:
            param dict
        '''

        # default params
        address = '';

        if data['address']:
            streetaddress = data['address'].replace(" ", "+")
            if data['city']:
                address += streetaddress+',+'
            else:
                address += streetaddress

        if data['city']:
            city = data['city'].replace(" ", "+")
            if data['region']:
                address += city+',+'
            else:
                address += city

        if data['region']:
            region = data['region'].replace(" ", "+").upper()
            address += region

        p = {
            'address' : address
        }

        if data['postalCode']:
            p['components'] = 'country:US|postal_code:' + str(data['postalCode'])

        return p


    def _CALL(self, p = None):# _cache == cache time

        if p['address']:
            k = str(p['address']) #use address as key
        else:
            k = str(p['components']) #use postal code as key

        #cache.delete(k)
        ch = cache.get(k)

        if ch is None:
            r = requests.get(self.QRY_URL, params=p)
            print('>> googleapis not cached')

            if r.status_code != 200:
                return {}
            else:
                cache.set(k, r.json(), _cache)
                return r.json()
        else:
            print('>> googleapis cached')
            return ch
