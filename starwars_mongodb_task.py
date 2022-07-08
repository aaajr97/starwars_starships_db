# TASK INSTRUCTIONS
# Data was pulled from https://swapi.dev/.
# 1) Compile lists that contain starwars starship data
# 2) Replace the pilot URL with corresponding objectID from starwars characters mongodb collection
# 3) Load the new list as a new collection into mongodb, containing the new Objectids
import requests
import pymongo
from pprint import pprint

client = pymongo.MongoClient()
db = client['starwars']

starship_list = []  # list that starship data will be appended to


# Function that obtains status code of an api
def get_api_status_code(url: str):
    api_response = requests.get(url)
    return api_response


# Function that concatenates the different parts of a API url
def forming_url(i: int):
    base_url = "https://swapi.dev/api"
    endpoint = "/starships/?page="
    page_number = i
    api_url = f"{base_url}{endpoint}{page_number}"
    return api_url


# function that appends api data to list given that the response sends a 200 code
# code iterates through different urls as the urls differ in page number
def add_data_to_list(empty_list: list, i=1):
    url = forming_url(i)
    while get_api_status_code(url).status_code == 200:
        for ship_details in requests.get(url).json()["results"]:
            empty_list.append(ship_details)
        i += 1
        url = forming_url(i)
    return empty_list


add_data_to_list(starship_list)


# function that converts pilot details to a reference objectID obtained from a mongodb characters collection
def api_name_to_object_id(api_list: list):
    for starship_details in api_list:
        for index in range(len(starship_details['pilots'])):
            result = requests.get(starship_details['pilots'][index]).json()
            identification = db.characters.find_one({"name": result["name"]}, {'_id': 1})
            starship_details['pilots'][index] = identification['_id']

    return api_list


# function that returns a list of mongodb collections
def collection_name_list():
    return db.list_collection_names()


# # function that appends each item(mongodb document) from a list into a new collection
# # function uses "collection_name_list" function to check if there is already a collection with the same name,
# # if so, the function deletes the documents within said collection, and append new documents
def create_starwars_mongodb_collection(object_id_list: list, collection_name: str):
    if collection_name in collection_name_list():
        db[collection_name].delete_many({})
    for details in object_id_list:
        db[collection_name].insert_one(details)
    return object_id_list


#pprint(create_starwars_mongodb_collection(api_name_to_object_id(starship_list), 'starships'))
