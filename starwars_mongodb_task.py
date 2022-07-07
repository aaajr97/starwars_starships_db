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
def add_data_to_list(i=1):
    url = forming_url(i)
    while get_api_status_code(url).status_code == 200:
        for ship_details in requests.get(url).json()["results"]:
            starship_list.append(ship_details)
        i += 1
        url = forming_url(i)
    return starship_list

#pprint(add_data_to_list())
