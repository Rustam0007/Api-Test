from random import choice

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CHANGE_ECOM_STATUS_URL
from config.config_data import CARD_TOKEN
from statuses import statusCode, eComStatus


class TestChangeEcomStatus(BaseCase):
    ecom_status = [eComStatus.INACTIVE, eComStatus.ACTIVE]

    def test_change_ecom_status(self):
        data_for_change_ecom_status = self.change_ecom_status(
            cardToken=CARD_TOKEN,
            cardEComStatus=choice(self.ecom_status))
        ecom_response = MyRequests.post(url=CHANGE_ECOM_STATUS_URL, data=data_for_change_ecom_status)
        Assertions.assert_status_code_and_message(ecom_response, statusCode.APPROVED, 'Approved')

    def test_change_ecom_status_with_invalid_card_token(self):
        data_for_change_ecom_status = self.change_ecom_status(
            cardToken='1234',
            cardEComStatus=choice(self.ecom_status))
        ecom_response = MyRequests.post(url=CHANGE_ECOM_STATUS_URL, data=data_for_change_ecom_status)
        Assertions.assert_status_code_and_message(ecom_response, statusCode.NOTFOUND,
                                                  "CardToken 1234 not found or doesn't belong to user")
