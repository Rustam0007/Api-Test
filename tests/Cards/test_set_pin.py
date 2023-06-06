import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import SET_PIN_URL
from config.config_data import CARD_ID, PERSON_EXT_REF, CARD_MASKED_PAN, CARD_TOKEN
from statuses import statusCode


class TestSetPin(BaseCase):
    def test_set_pin(self, update_value, select_value):
        update_value('cards', 'pin', False, 'id', CARD_ID)

        data = self.set_pin(cardToken=CARD_TOKEN, personExternalRef=PERSON_EXT_REF, pin='2211')
        set_pin_response = MyRequests.post(url=SET_PIN_URL, data=data)
        Assertions.assert_status_code_and_message(set_pin_response, statusCode.APPROVED, 'Approved')

        pan = set_pin_response.json()['maskedPan']
        assert pan == CARD_MASKED_PAN, f"Unexpected PAN. " \
                                         f"Expected {CARD_MASKED_PAN}\n" \
                                         f"Actually {pan}\n"

        pinStatusInDB = select_value('pin',
                                     'cards',
                                     'token',
                                     CARD_TOKEN
                                     )

        Assertions.check_DB(pinStatusInDB, True,
                            "Unexpected PIN status. "
                            "Expected True. "
                            f"Actually {pinStatusInDB}")

    @pytest.mark.parametrize('cardToken, personExternalRef, pin, expectedStatusCode, expectedMsg',
                             [
                                 ('1234', PERSON_EXT_REF, '2211', statusCode.NOTFOUND, 'No card found with specified CardToken and PersonExternalRef'), #incorrect_card_token
                                 (CARD_TOKEN, '221119829', '2211', statusCode.NOTFOUND, 'No card found with specified CardToken and PersonExternalRef') #incorrect_person_external_ref

                             ])
    def test_set_pin_negative_cases(self, cardToken, personExternalRef, pin, expectedStatusCode, expectedMsg):
        data = self.set_pin(cardToken=cardToken,
                            personExternalRef=personExternalRef,
                            pin=pin)
        set_pin_response = MyRequests.post(url=SET_PIN_URL, data=data)
        Assertions.assert_status_code_and_message(set_pin_response, expectedStatusCode, expectedMsg)

