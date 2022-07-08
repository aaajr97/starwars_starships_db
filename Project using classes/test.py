import unittest

import bson

from starwars_mongodb_classes import *


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.starship = Starship()

    def test_forming_url(self):
        actual = self.starship.forming_url()
        expected = "https://swapi.dev/api/starships/?page=1"
        self.assertEqual(actual, expected)

    def test_get_api_status_code(self):
        actual = type(self.starship.get_api_status_code())
        expected = requests.models.Response
        self.assertEqual(actual, expected)

    def test_add_data_to_list(self):
        self.starship.add_data_to_list()
        self.assertEqual(len(self.starship.starship_list), 36)
        self.assertEqual(self.starship.starship_list[4]['pilots'][0][:5], 'https')

    def test_api_name_to_object_id(self):
        self.starship.add_data_to_list()
        self.starship.api_name_to_object_id()
        pilot_details = self.starship.starship_list[4]['pilots']
        actual = type(pilot_details[0])
        expected = bson.objectid.ObjectId
        self.assertEqual(actual, expected)

    def test_create_starwars_mongodb_collection(self):
        self.starship.add_data_to_list()
        self.starship.api_name_to_object_id()
        actual = self.starship.create_starwars_mongodb_collection('starships')
        mongodb_starships = []
        for document in self.starship.db.starships.find({}):
            mongodb_starships.append(document)
        expected = mongodb_starships
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
