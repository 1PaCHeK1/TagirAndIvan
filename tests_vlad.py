import unittest
import requests as r
import json
# Create your tests here.

class CreateTask(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_crashtitle(self):
        # response = r.post("http://localhost:8000/todo/create/", json={'tg_id' : 1, 'title' : ''})
        # self.assertEqual(response.status_code, 400)
        self._test("http://localhost:8000/todo/create/", {'tg_id' : 1, 'title' : ''}, 400)
    
    def test_createtask(self):
        # response = r.post("http://localhost:8000/todo/create/", json={'tg_id' : 1, 'title' : 'test'})
        # self.assertEqual(response.status_code, 200)
        self._test("http://localhost:8000/todo/create/", {'tg_id' : 1, 'title' : 'test'}, 200)
    
    def _test(self, link, json, status_code):
        response = r.post(link, json=json)
        self.assertEqual(response.status_code, status_code)
        self.assertEquals()