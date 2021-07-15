from django.test import TestCase

import unittest
import requests as r
import json
# Create your tests here.

class CreateTask(unittest.TestCase):

    def test_crashtitle(self):
        response = r.post("http://localhost:8000/todo/create/", json={'tg_id' : 1, 'title' : ''})
        self.assertEqual(response.status_code, 400)

    def test_createtask(self):
        response = r.post("http://localhost:8000/todo/create/", json={'tg_id' : 1, 'title' : 'test'})
        self.assertEqual(response.status_code, 200)
