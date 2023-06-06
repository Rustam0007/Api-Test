import pytest
from config.config_data import CARD_TOKEN
from config.config_url import CHANGE_RISK_COUNTRY_USAGE
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from statuses import statusCode


class TestChangeRiskCountry(BaseCase):
    def test_change_risk_country(self, select_value):
        risk_country_value = select_value('risk_country', 'cards', 'token', CARD_TOKEN)
        if risk_country_value == 1:
            risk_country_value = 0
        else:
            risk_country_value = 1

        data_for_change_risk_country = self.change_risk_country(cardToken=CARD_TOKEN, status=risk_country_value)
        risk_country_response = MyRequests.post(url=CHANGE_RISK_COUNTRY_USAGE, data=data_for_change_risk_country)
        Assertions.assert_status_code_and_message(risk_country_response, statusCode.APPROVED, 'Approved')

        risk_country_value_in_DB = select_value('risk_country', 'cards', 'token', CARD_TOKEN)
        Assertions.check_DB(risk_country_value_in_DB, risk_country_value, "Risk country value in column do not change!")


    @pytest.mark.parametrize('cardToken, status, expectedStatusCode, expectedMsg',
                             [
                                 ('1', 1, statusCode.NOTFOUND, 'CardToken: 1 not found'),  # invalid_card_token
                                 (CARD_TOKEN, 3, statusCode.BADREQUEST, 'Invalid Status')  # invalid_status_type
                             ])
    def test_change_risk_country_negative_cases(self, cardToken, status, expectedStatusCode, expectedMsg):
        data_for_change_risk_country = self.change_risk_country(cardToken=cardToken, status=status)
        risk_country_response = MyRequests.post(url=CHANGE_RISK_COUNTRY_USAGE, data=data_for_change_risk_country)
        Assertions.assert_status_code_and_message(risk_country_response, expectedStatusCode, expectedMsg)

    def test_change_risk_country_already_exist_status(self, select_value):
        risk_country_value = select_value('risk_country', 'cards', 'token', CARD_TOKEN)
        response_message = ''
        if risk_country_value == 1:
            response_message = 'Card RiskCountryUsage status is already an Active!'
        else:
            response_message = 'Actually Card RiskCountryUsage status is already an InActive!'

        data_for_change_risk_country = self.change_risk_country(cardToken=CARD_TOKEN, status=risk_country_value)
        risk_country_response = MyRequests.post(url=CHANGE_RISK_COUNTRY_USAGE, data=data_for_change_risk_country)
        Assertions.assert_status_code_and_message(risk_country_response, statusCode.BADREQUEST, response_message)
