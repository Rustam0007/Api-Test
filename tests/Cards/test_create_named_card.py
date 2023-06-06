from time import sleep, time
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CREATE_NAMED_CARD_URL, CREATE_ACCOUNT_URL
from config.config_data import PERSON_ID
from statuses import statusCode, syncStateStatus


class TestCreateNamedCard(BaseCase):
    def test_create_named_card(self, select_value, remove_value):
        data_for_card = self.create_named_card(personId=PERSON_ID, companyExternalRef="",
                                               phone=992001020304, typeOfCard=1)
        card_response = MyRequests.post(url=CREATE_NAMED_CARD_URL, data=data_for_card)
        Assertions.assert_status_code_and_message(card_response, statusCode.APPROVED, 'Approved')
        Assertions.json_has_keys_in_payload(card_response, names=['cardId', 'panId', 'pan', 'expiration'])

        cardId = card_response.json()['cardId']

        data_for_account = self.create_only_one_account(personId=PERSON_ID, cardId=cardId)
        MyRequests.post(url=CREATE_ACCOUNT_URL, data=data_for_account)

        start_time = time()
        timeout = 120

        while (time() - start_time) < timeout:
            if select_value('syncStateStatus', 'cards', 'id', cardId) == syncStateStatus.SYNCED:
                break
            sleep(1)

        if select_value('syncStateStatus', 'cards', 'id', cardId) != syncStateStatus.SYNCED:
            raise Exception(f"ОШИБКА: syncStateStatus карты не равен 10")

        # очищяем БД после создание карты и счёта
        remove_value('accounts', 'cards_id', cardId)
        remove_value('cards', 'id', cardId)


    @pytest.mark.parametrize(
        'personId, companyExternalRef, phone, typeOfCard, expectedStatusCode, expectedMsg',
         [
             (1234567890, "", 992001020304, 1, statusCode.INTERNALERROR, 'Internal server error'), #incorrect_person_id
             (PERSON_ID, "0987654321", 992001020304, 1, statusCode.NOTFOUND, 'No company found with externalId 0987654321'), #incorrect_company
             (PERSON_ID, "", 992001020304, 2211, statusCode.BADREQUEST, 'Invalid Card Type') #incorrect_card_type
         ])
    def test_create_named_card_negative_cases(self,
                                              personId,
                                              companyExternalRef,
                                              phone,
                                              typeOfCard,
                                              expectedStatusCode,
                                              expectedMsg):
        data_for_card = self.create_named_card(personId=personId, companyExternalRef=companyExternalRef,
                                               phone=phone, typeOfCard=typeOfCard)
        card_response = MyRequests.post(url=CREATE_NAMED_CARD_URL, data=data_for_card)
        Assertions.assert_status_code_and_message(card_response, expectedStatusCode, expectedMsg)
