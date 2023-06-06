from time import sleep, time

import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CREATE_INSTANT_BULK_URL, CREATE_INSTANT_CARD_URL, CREATE_ACCOUNT_URL
from config.config_data import PERSON_ID
from statuses import statusCode, syncStateStatus, cardType


class TestCreateInstantBulk(BaseCase):
    def test_create_instant_bulk(self, select_value, remove_value):
        #Create instant bulk
        data_for_create_bulk = self.create_instant_bulk(cardType=cardType.VISAGOLD, size=1)
        instant_bulk_response = MyRequests.post(url=CREATE_INSTANT_BULK_URL, data=data_for_create_bulk)
        cardId = instant_bulk_response.json()['cardInfoList'][0]['cardId']
        Assertions.assert_status_code_and_message(instant_bulk_response, statusCode.APPROVED, "Approved")
        Assertions.json_has_keys_in_payload(instant_bulk_response,
                                            keyInPayload='cardInfoList',
                                            arrIndex=0,
                                            names=['pan', 'cardType', 'expiration'])

        sleep(5)
        #Create Instant Card
        data_for_create_instant_card = self.create_instant_card(cardId=cardId,
                                                                personId=PERSON_ID,
                                                                phone=992001020308)
        create_instant_response = MyRequests.post(url=CREATE_INSTANT_CARD_URL, data=data_for_create_instant_card)
        Assertions.assert_status_code_and_message(create_instant_response, statusCode.APPROVED, 'Approved')


        #Create Account
        data_for_account = self.create_only_one_account(personId=PERSON_ID, cardId=cardId)
        create_account_response = MyRequests.post(url=CREATE_ACCOUNT_URL, data=data_for_account)
        Assertions.assert_status_code_and_message(create_account_response, statusCode.APPROVED, 'Approved')


        start_time = time()  # запоминаем текущее время
        timeout = 120  # задаем таймаут в секундах

        while (time() - start_time) < timeout:
            if select_value('syncStateStatus', 'cards', 'id', cardId) == syncStateStatus.SYNCED:
                break
            sleep(1)

        if select_value('syncStateStatus', 'cards', 'id', cardId) != syncStateStatus.SYNCED:
            raise Exception(f"ОШИБКА: syncStateStatus карты не равен 10")

        # очищяем БД после создание карты и счёта
        remove_value('accounts', 'cards_id', cardId)
        remove_value('cards', 'id', cardId)

    @pytest.mark.parametrize('cardType, size, expectedStatusCode, expectedMsg',
                             [
                                 (2211, 1, statusCode.BADREQUEST, 'CardType Invalid Card Type'), # invalid_card_type
                                 (cardType.VISAGOLD, 0, statusCode.BADREQUEST, 'Size must be between 1 and 100') #zero_size
                             ])
    def test_create_instant_bulk_with_invalid_card_type(self, cardType, size, expectedStatusCode, expectedMsg):
        data_for_create_bulk = self.create_instant_bulk(cardType=cardType, size=size)
        instant_bulk_response = MyRequests.post(url=CREATE_INSTANT_BULK_URL, data=data_for_create_bulk)
        Assertions.assert_status_code_and_message(instant_bulk_response, expectedStatusCode, expectedMsg)