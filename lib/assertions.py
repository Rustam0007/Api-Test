from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_code_status(response: Response, expected_code):
        assert response.status_code == expected_code, \
            f"Error! Expected: {expected_code}. Actual: {response.status_code}"

    @staticmethod
    def assert_status_code_and_message(response: Response, expected_code, expected_message):

        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert response_as_dict['code'] == expected_code, f"Unexpected code. " \
                                                        f"Expected {expected_code}. " \
                                                        f"Actually {response_as_dict['code']}"
        assert response_as_dict['message'] == expected_message, f"Unexpected message. " \
                                                        f"Expected {expected_message}. " \
                                                        f"Actually {response_as_dict['message']}"

    @staticmethod
    def json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON not have key '{name}'"

    @staticmethod
    def json_has_keys_in_payload(response: Response, keyInPayload=None, arrIndex=None, names=None):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        if keyInPayload is not None and arrIndex is not None:
            for name in names:
                assert name in response_as_dict[keyInPayload][arrIndex], f"Response JSON not have key '{name}'"
        elif keyInPayload is not None:
            for name in names:
                assert name in response_as_dict[keyInPayload], f"Response JSON not have key '{name}'"
        else:
            for name in names:
                assert name in response_as_dict, f"Response JSON not have key '{name}'"

    @staticmethod
    def check_DB(select, expectedselectValue, error_message):

        assert select == expectedselectValue, error_message
