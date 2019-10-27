import unittest
import json
import requests


class TestPOSTMethod(unittest.TestCase):

    def test_POST_200(self):
        url = 'http://localhost:8000/kv/'
        request = {"key": "president", "value": {"name": "vladimir", "surname": "putin"}}
        jsn = json.dumps(request)
        response = requests.post(url, data=jsn)
        self.assertEqual(str(response), '<Response [200]>')

        url = 'http://localhost:8000/kv/president/'
        requests.delete(url)

    def test_POST_400(self):
        url = 'http://localhost:8000/kv/'
        request = {"key": "president", "not_value": {"name": "vladimir", "surname": "putin"}}
        jsn = json.dumps(request)
        response = requests.post(url, data=jsn)
        self.assertEqual(str(response), '<Response [400]>')

    def test_POST_409(self):
        url = 'http://localhost:8000/kv/'
        request = {"key": "president", "value": {"name": "vladimir", "surname": "putin"}}
        jsn = json.dumps(request)
        requests.post(url, data=jsn)
        response = requests.post(url, data=jsn)
        self.assertEqual(str(response), '<Response [409]>')

        url = 'http://localhost:8000/kv/president/'
        requests.delete(url)


class TestPUTMethod(unittest.TestCase):

    def test_PUT_200(self):
        url = 'http://localhost:8000/kv/'
        request = {"key": "president", "value": {"name": "dmitry", "surname": "medvedev"}}
        jsn = json.dumps(request)
        response = requests.post(url, data=jsn)

        url = 'http://localhost:8000/kv/president/'
        request = {"value": {"name": "vladimir", "surname": "putin"}}
        jsn = json.dumps(request)
        response = requests.put(url, data=jsn)
        self.assertEqual(str(response), '<Response [200]>')

        url = 'http://localhost:8000/kv/president/'
        requests.delete(url)

    def test_PUT_400(self):
        url = 'http://localhost:8000/kv/president/'
        request = {"the_best_president": {"name": "vladimir", "surname": "putin"}}
        jsn = json.dumps(request)
        response = requests.put(url, data=jsn)
        self.assertEqual(str(response), '<Response [400]>')

    def test_PUT_404(self):
        url = 'http://localhost:8000/kv/president/'
        request = {"value": {"name": "alexey", "surname": "navalny"}}
        jsn = json.dumps(request)
        response = requests.put(url, data=jsn)
        self.assertEqual(str(response), '<Response [404]>')


class TestGETMethod(unittest.TestCase):

    def test_GET_200(self):
        url = 'http://localhost:8000/kv/'
        request = {"key": "money", "value": {"amount": "1.000.000$", "for": "duck_house"}}
        jsn = json.dumps(request)
        requests.post(url, data=jsn)

        url = 'http://localhost:8000/kv/money/'
        response = requests.get(url)
        self.assertEqual(str(response), '<Response [200]>')

        url = 'http://localhost:8000/kv/money/'
        requests.delete(url)

    def test_GET_404(self):
        url = 'http://localhost:8000/kv/ukrainian_crimea/'
        response = requests.get(url)
        self.assertEqual(str(response), '<Response [404]>')


class TestDELETEMethod(unittest.TestCase):

    def test_DELETE_200(self):
        url = 'http://localhost:8000/kv/'
        request = {"key": "opposite", "value": {"name": "navalny"}}
        jsn = json.dumps(request)
        response = requests.post(url, data=jsn)

        url = 'http://localhost:8000/kv/opposite/'
        response = requests.delete(url)
        self.assertEqual(str(response), '<Response [200]>')

    def test_GET_NOT_FOUND(self):
        url = 'http://localhost:8000/kv/putin/'
        response = requests.delete(url)
        self.assertEqual(str(response), '<Response [404]>')


if __name__ == '__main__':
    unittest.main()
