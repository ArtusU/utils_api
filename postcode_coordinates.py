import requests
import json

BASE_URL = "http://api.postcodes.io/postcodes/"


class PostCodeClient(object):
    def get_data_postcode(self, postcode):
        self.postcode = postcode
        data = requests.get(BASE_URL + postcode).text
        return data
    
    def get_latlng(self, postcode):
        result_str = self.get_data_postcode(postcode)
        resuslt_dict = json.loads(result_str)
        result = resuslt_dict["result"]
        lat = result["latitude"]
        lng = result["longitude"]
        return(lat, lng)