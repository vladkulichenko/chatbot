import unittest
import requests
import os

HOST = os.getenv("HOST", "http://127.0.0.1").rstrip("/")
TEST_PORT = os.getenv("TEST_PORT", "8000")
URL = f"{HOST}:{TEST_PORT}"

TIMEOUT = 15


class TestPackageDeliveryChatbot(unittest.TestCase):

    def setUp(self):
        self.url = f"{URL}/testing/"

    def test_response_generation(self):
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": "Hi, whats your name?"
                }
            ]
        }
        response = requests.post(self.url, json=data, timeout=TIMEOUT)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["answer"].startswith("My name is Vio"), True)

    def test_with_estate_data(self):
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": "I need a help with evaluating the estate by adress 4211 Elevator Dr, Austin, "
                               "TX 78731, with total area with 800, which have 2 bedrooms and 1 bathroom. And please "
                               "let me know the average, minimal and the highest prices per square foot"
                }
            ]
        }
        response = requests.post(self.url, json=data, timeout=TIMEOUT)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["answer"].startswith("I've found some listings that match your criteria"), True)

    def test_invalid_data(self):
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": "I need a help with evaluating the estate by adress 4211 Elevator Dr, Austin, "
                               "TX 78731, with total area with 800. And please let me know the average, minimal and "
                               "the highest prices per square foot"
                }
            ]
        }
        response = requests.post(self.url, json=data, timeout=TIMEOUT)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("I'll need to know the number of bedrooms and bathrooms" in response.json()["answer"].lower())

    def test_empty_string_input(self):
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": ""
                }
            ]
        }
        response = requests.post(self.url, json=data, timeout=TIMEOUT)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("How can I assist you today?" in response.json()["answer"])

    def test_whitespace_input(self):
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": "   "
                }
            ]
        }
        response = requests.post(self.url, json=data, timeout=TIMEOUT)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("How can I assist you today?" in response.json()["answer"])


if __name__ == "__main__":
    unittest.main()
