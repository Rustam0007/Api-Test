import random
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_data import COMPANY_ID
from config.config_url import CHANGE_LIMIT_ACCOUNT_URL
from statuses import statusCode


class TestChangeLimitAccount(BaseCase):
    def test_change_limit_account(self, select_value):
        limit_id_before_request = select_value(
            column='id', table='limit_account', critery='id', criteryValue=COMPANY_ID,
            secondCritery='card_type', secondCriteryValue=1,
            thirdCritery='currency', thirdCriteryValue=643,
            fourthCritery='limit_type_id', fourthCriteryValue=9
        )
        value_before_request = select_value(column='value', table='limit_account', critery='id', criteryValue=limit_id_before_request)
        data = self.change_limit_account(id=limit_id_before_request, newValue=f"{random.randint(1, 10000)}")
        response = MyRequests.post(url=CHANGE_LIMIT_ACCOUNT_URL, data=data)
        limit_id_after_request = response.json()['id']
        value_after_request = select_value(column='value', table='limit_account', critery='id', criteryValue=limit_id_after_request)

        Assertions.assert_status_code_and_message(response, statusCode.APPROVED, 'Approved')

        assert value_before_request != value_after_request, f'Unexpected result.\n Expected {value_after_request}.\n Actually {value_before_request}'

    @pytest.mark.parametrize('limitId, newValue, expectedStatusCode, expectedMsg',
                             [
                                 (22117744, random.randint(1, 10000), statusCode.NOTFOUND, 'limit account with id:22117744 not found') # incorrect id
                             ])
    def test_change_limit_account_negative_cases(self, limitId, newValue, expectedStatusCode, expectedMsg):
        data = self.change_limit_account(id=limitId, newValue=newValue)
        response = MyRequests.post(url=CHANGE_LIMIT_ACCOUNT_URL, data=data)
        Assertions.assert_status_code_and_message(response, expectedStatusCode, expectedMsg)

