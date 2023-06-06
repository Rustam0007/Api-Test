from time import sleep, time
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CREATE_NAMED_CARD_URL, CREATE_ACCOUNT_URL
from config.config_data import PERSON_ID, CARD_ID
from statuses import statusCode, cardCurrency
from statuses import syncStateStatus


class TestCreateAccount(BaseCase):
    def test_create_account(self, select_value, remove_value):
        data_for_card = self.create_named_card(personId=PERSON_ID, phone=992001020305,
                                               typeOfCard=2, companyExternalRef="")
        card_response = MyRequests.post(url=CREATE_NAMED_CARD_URL, data=data_for_card)
        cardId = card_response.json()['cardId']

        data_for_account = self.create_account(personId=PERSON_ID, cardId=cardId)
        account_response = MyRequests.post(url=CREATE_ACCOUNT_URL, data=data_for_account)
        Assertions.assert_status_code_and_message(account_response, statusCode.APPROVED, 'Approved')

        firstAccountId = account_response.json()['accounts'][0]['id']
        secondAccountId = account_response.json()['accounts'][1]['id']

        start_time = time()  # запоминаем текущее время
        timeout = 80  # задаем таймаут в секундах

        while (time() - start_time) < timeout:
            if \
                    select_value('syncStateStatus', 'accounts', 'id', firstAccountId) == syncStateStatus.SYNCED and \
                    select_value('syncStateStatus', 'accounts', 'id', secondAccountId) == syncStateStatus.SYNCED:
                break
            sleep(1)

        if \
                select_value('syncStateStatus', 'accounts', 'id', firstAccountId) != syncStateStatus.SYNCED and \
                select_value('syncStateStatus', 'accounts', 'id', secondAccountId) != syncStateStatus.SYNCED:
            raise Exception(f"ОШИБКА: syncStateStatus счетов не равны 10")

        # очищяем БД после создание карты и счёта
        remove_value('accounts', 'cards_id', cardId)
        remove_value('cards', 'id', cardId)

    # Negative cases
    @pytest.mark.parametrize('personId, cardId, externalRef, currency, expectedStatusCode, expectedMsg',
                             [
                                 (123456789, CARD_ID, None, cardCurrency.TJS, statusCode.INTERNALERROR, 'Internal server error'), # with_incorrect_person_id
                                 (PERSON_ID, 1234567890, None, cardCurrency.RUB, statusCode.INTERNALERROR, 'Internal server error'),  # with_incorrect_card_id
                                 (PERSON_ID, CARD_ID, '1234567253645238291', cardCurrency.USD, statusCode.BADREQUEST, "ExternalRef must contain 20 number"),  # with_19_number_in_account
                                 (PERSON_ID, CARD_ID, '123456725364125238291', cardCurrency.RUB, statusCode.BADREQUEST, "ExternalRef must contain 20 number"),  # with_21_number_in_account
                                 (123456789, CARD_ID, None, 2211, statusCode.BADREQUEST, "Invalid currency"),  # with_invalid_currency

                             ])
    def test_create_account_negative_cases(self, personId, cardId, externalRef, currency, expectedStatusCode, expectedMsg):
        data_for_account = self.create_account(personId=personId, cardId=cardId, externalRef=externalRef, currency=currency)
        account_response = MyRequests.post(url=CREATE_ACCOUNT_URL, data=data_for_account)
        Assertions.assert_status_code_and_message(account_response, expectedStatusCode, expectedMsg)

