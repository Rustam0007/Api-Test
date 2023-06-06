import requests
from lib.logger import Logger
from config.DB_config import HEADER_KEY, HEADER_VALUE


class MyRequests:
    @staticmethod
    def post(url: str, data: dict = None, files: dict = None):
        return MyRequests._send(url, data, 'POST', files)

    @staticmethod
    def get(url: str, data: dict = None):
        return MyRequests._send(url, data, 'GET')

    @staticmethod
    def put(url: str, data: dict = None):
        return MyRequests._send(url, data, 'PUT')

    @staticmethod
    def delete(url: str, data: dict = None):
        return MyRequests._send(url, data, 'DELETE')

    @staticmethod
    def _send(url: str, data: dict, method: str, files: dict = None):

        Logger.add_request(url, data, method)

        if method == 'GET':
            response = requests.get(url, params=data, headers={HEADER_KEY: HEADER_VALUE, "Content-Type": "application/json"})
        elif method == 'POST' and files is None:
            response = requests.post(url, json=data, headers={HEADER_KEY: HEADER_VALUE, "Content-Type": "application/json"})
        elif files is not None and method == 'POST':
            response = requests.post(url, data=data, headers={HEADER_KEY: HEADER_VALUE, "Content-Type": None}, files=files)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers={HEADER_KEY: HEADER_VALUE, "Content-Type": "application/json"})
        elif method == 'DELETE':
            response = requests.delete(url, json=data, headers={HEADER_KEY: HEADER_VALUE, "Content-Type": "application/json"})
        else:
            raise Exception(f"BAD HTTP METHOD '{method}'")

        Logger.add_response(response)

        return response
