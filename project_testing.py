import bson
import requests.models

from starwars_mongodb_task import *


def test_get_api_status_code():
    assert type(get_api_status_code("https://swapi.dev/api/starships/?page=3")) \
           == requests.models.Response


def test_forming_url():
    assert type(get_api_status_code(forming_url(2))) == requests.models.Response


def test_add_data_to_list():
    empty_list = []
    assert len(add_data_to_list(empty_list)) == 36
    assert add_data_to_list(empty_list)[4]['pilots'][0][:5] == 'https'


def test_api_name_to_object_id():
    test_list = add_data_to_list(starship_list)
    pilot_details = api_name_to_object_id(test_list)[4]['pilots']
    assert type(pilot_details[0]) == bson.objectid.ObjectId


def test_create_starwars_mongodb_collection():
    test_list = []
    appended_documents = \
        create_starwars_mongodb_collection(api_name_to_object_id(add_data_to_list(test_list)), 'starships')
    mongodb_starships = []
    for document in db.starships.find({}):
        mongodb_starships.append(document)

    assert appended_documents == mongodb_starships
