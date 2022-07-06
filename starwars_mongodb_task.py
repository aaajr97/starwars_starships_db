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
# Function takes url link in string form as input
def get_api_status_code(url: str):
    api_status_code = requests.get(url).status_code
    return api_status_code


# function that appends api data to list given that the response sends a 200 code
# code iterates through different urls as the urls differ in page number
def add_data_to_list():
    url = "https://swapi.dev/api/starships/?page=1"
    i = 1
    while get_api_status_code(url) == 200:
        for ship_details in requests.get(url).json()["results"]:
            starship_list.append(ship_details)
        i += 1
        url = f'https://swapi.dev/api/starships/?page={i}'
    return starship_list


pprint(add_data_to_list())