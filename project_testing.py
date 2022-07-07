import bson
import requests.models

from starwars_mongodb_task import *


def test_get_api_status_code():
    assert type(get_api_status_code("https://swapi.dev/api/starships/?page=3")) \
           == requests.models.Response


def test_forming_url():
    assert type(get_api_status_code(forming_url(2))) == requests.models.Response


def test_add_data_to_list():
    assert len(add_data_to_list(starship_list)) == 36
    assert add_data_to_list(starship_list)[4]['pilots'][0][:5] == 'https'


def test_api_name_to_object_id():
    pilot_details = api_name_to_object_id(add_data_to_list(starship_list))[4]['pilots']
    assert type(pilot_details[0]) == bson.objectid.ObjectId
