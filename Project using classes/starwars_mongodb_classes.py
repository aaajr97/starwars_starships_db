import requests
import pymongo
from pprint import pprint

client = pymongo.MongoClient()


class Starship:
    def __init__(self, base_url="https://swapi.dev/api", endpoint="/starships/?page="):
        self.base_url = base_url
        self.endpoint = endpoint
        self.starship_list = []
        self.db = client['starwars']
        self.page_number = 1

    def forming_url(self):
        return f"{self.base_url}{self.endpoint}{self.page_number}"

    def get_api_status_code(self):
        return requests.get(self.forming_url())

    def add_data_to_list(self):
        url = self.forming_url()
        while self.get_api_status_code().status_code == 200:
            for details in requests.get(url).json()["results"]:
                self.starship_list.append(details)
            self.page_number += 1
            url = self.forming_url()

    def api_name_to_object_id(self):
        for details in self.starship_list:
            for index in range(len(details['pilots'])):
                pilot_details = requests.get(details['pilots'][index]).json()
                identification = self.db.characters.find_one({"name": pilot_details["name"]}, {'_id': 1})
                details['pilots'][index] = identification['_id']

    def create_starwars_mongodb_collection(self, collection_name: str):
        if collection_name in self.db.list_collection_names():
            self.db[collection_name].delete_many({})
        for details in self.starship_list:
            self.db[collection_name].insert_one(details)
        return self.starship_list


