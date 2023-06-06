from random import choice
import pytest
from config.config_data import CARD_ID, CARD_TOKEN
from config.config_url import CHANGE_CARD_CMS_URL
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from statuses import statusCode


class TestChangeCMS(BaseCase):
    arr = '1234567890'
    newPhone = ''
    for i in range(9):
        newPhone = newPhone + choice(arr)

    def test_change_cms_with_card_id(self, select_value):
        phone_before_req = select_value('phoneNumber', 'cards', 'id', CARD_ID)

        cmsData = self.change_cms(cardId=CARD_ID, cardToken="", newPhone=self.newPhone)
        changeCms = MyRequests.post(url=CHANGE_CARD_CMS_URL, data=cmsData)
        phone_after_req = select_value('phoneNumber', 'cards', 'id', CARD_ID)

        Assertions.assert_status_code_and_message(changeCms, statusCode.APPROVED, 'Approved')
        assert phone_before_req != phone_after_req, 'CMSAbonent do not change'

    def test_change_cms_with_card_token(self, select_value):
        phone_before_req = select_value('phoneNumber', 'cards', 'id', CARD_ID)
        cmsData = self.change_cms(cardId=0, cardToken=CARD_TOKEN, newPhone=992000010101)
        changeCms = MyRequests.post(url=CHANGE_CARD_CMS_URL, data=cmsData)
        phone_after_req = select_value('phoneNumber', 'cards', 'id', CARD_ID)

        Assertions.assert_status_code_and_message(changeCms, statusCode.APPROVED, 'Approved')
        assert phone_before_req != phone_after_req, 'CMSAbonent do not change'

    @pytest.mark.parametrize('cardId, cardToken, newPhone, expectedStatusCode, expectedMsg',
                             [
                                 (22117744, "", 992001020307, statusCode.NOTFOUND, 'Not found : Card not found'),  # invalid_card_id
                                 (0, "123", 992001020307, statusCode.NOTFOUND, 'Not found : Card not found')  # invalid_card_token
                             ])
    def test_change_cms_negative_cases(self, cardId, cardToken, newPhone, expectedStatusCode, expectedMsg):
        cmsData = self.change_cms(cardId=cardId, newPhone=newPhone, cardToken=cardToken)
        changeCms = MyRequests.post(url=CHANGE_CARD_CMS_URL, data=cmsData)
        Assertions.assert_status_code_and_message(changeCms, expectedStatusCode, expectedMsg)
