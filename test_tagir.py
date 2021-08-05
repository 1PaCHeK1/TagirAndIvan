import unittest
import requests as r
# Create your tests here.


class CreateTask(unittest.TestCase):

    def _testrigth(self, link, mesg):
        response = r.get(link)
        self.assertEqual(response.json().get('msg', None), mesg)

    def _testslezhka(self, mesg):
        response = r.get('http://localhost:8000/charecters/roblox_status/1192394560/')
        self.assertEqual(response.json().get('msg', None), mesg)


    def test_star5(self):
        self._testrigth('http://localhost:8000/charecters/st5/',
                       'https://allstartd.fandom.com/wiki/Character_List#5_Stars')

    def test_star6(self):
        self._testrigth('http://localhost:8000/charecters/st6',
                       'https://allstartd.fandom.com/wiki/Character_List#6_Stars')

    def test_orbs(self):
        self._testrigth('http://localhost:8000/charecters/orbs',
                       'https://allstartd.fandom.com/wiki/Orbs')

    def test_slezhka(self):
        status = 'Offline'
        self._testslezhka(status)



