import pytest
from config.config_data import CARD_ID, CARD_TOKEN
from config.config_url import CHANGE_CARD_STATUS_URL
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from statuses import statusCode, cardStatus


class TestChangeCardStatus(BaseCase):

    def test_change_card_status_with_card_id(self):
        data_for_change_status = self.change_card_status(cardId=CARD_ID, cardToken="", status=cardStatus.INACTIVE)
        card_response = MyRequests.post(url=CHANGE_CARD_STATUS_URL, data=data_for_change_status)
        Assertions.assert_status_code_and_message(card_response, statusCode.APPROVED, 'Approved')

    def test_change_card_status_with_card_token(self):
        data_for_change_status = self.change_card_status(cardId=0, status=cardStatus.OPEN, cardToken=CARD_TOKEN)
        card_response = MyRequests.post(url=CHANGE_CARD_STATUS_URL, data=data_for_change_status)
        Assertions.assert_status_code_and_message(card_response, statusCode.APPROVED, 'Approved')


    @pytest.mark.parametrize('cardId, cardStatus, cardToken, expectedStatusCode, expectedMsg',
                             [
                                 (22117744, cardStatus.OPEN, "", statusCode.NOTFOUND, 'Not found : Card not found'),  # invalid_card_id
                                 (CARD_ID, 2211, "", statusCode.BADREQUEST, 'Invalid card status')  # invalid_status
                             ]
                            )
    def test_change_card_status_with_invalid_card_id(self, cardId, cardStatus, cardToken, expectedStatusCode, expectedMsg):
        data_for_change_status = self.change_card_status(cardId=cardId, status=cardStatus, cardToken=cardToken)
        card_response = MyRequests.post(url=CHANGE_CARD_STATUS_URL, data=data_for_change_status)
        Assertions.assert_status_code_and_message(card_response, expectedStatusCode, expectedMsg)
