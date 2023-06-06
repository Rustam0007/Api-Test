from time import sleep, time
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CREATE_CREDIT_BULK_URL
from config.config_data import FIRST_ACCOUNT_EXT_REF, SECOND_ACCOUNT_EXT_REF
from statuses import statusCode, transactionStatus



class TestCreateCreditBulk(BaseCase):
    def test_create_credit_bulk(self, select_value):
        # credit operation
        data = self.create_credit_bulk(firstAccount=FIRST_ACCOUNT_EXT_REF,
                                       secondAccount=SECOND_ACCOUNT_EXT_REF)
        credit_response = MyRequests.post(url=CREATE_CREDIT_BULK_URL, data=data)
        Assertions.assert_status_code_and_message(credit_response, statusCode.ACCEPTED, "Accepted for further process")

        getFirstExternalRef = data['bulkInfo'][0]['externalRef']
        getSecondExternalRef = data['bulkInfo'][1]['externalRef']

        start_time = time()  # запоминаем текущее время
        timeout = 80  # задаем таймаут в секундах

        while (time() - start_time) < timeout:
            if select_value('syncStateStatus', 'credit', 'external_ref', f'{getFirstExternalRef}') == transactionStatus.APPROVED and \
                    select_value('syncStateStatus', 'credit', 'external_ref', f'{getSecondExternalRef}') == transactionStatus.APPROVED:
                break
            sleep(1)

        if select_value('syncStateStatus', 'credit', 'external_ref', f'{getFirstExternalRef}') != transactionStatus.APPROVED \
                or select_value('syncStateStatus', 'credit', 'external_ref', f'{getSecondExternalRef}') != transactionStatus.APPROVED:
            raise Exception(f"ОШИБКА: Статусы не стали равны 1")

    @pytest.mark.parametrize('firstAccount, secondAccount, expectedStatusCode, expectedMsg',
                             [
                                 (FIRST_ACCOUNT_EXT_REF + '9210', SECOND_ACCOUNT_EXT_REF, statusCode.BADREQUEST, "Account must contain 20 number"),
                                 (FIRST_ACCOUNT_EXT_REF, SECOND_ACCOUNT_EXT_REF + '9210', statusCode.BADREQUEST, "Account must contain 20 number"),

                             ])
    def test_create_credit_negative_cases(self, firstAccount, secondAccount, expectedStatusCode, expectedMsg):
        data = self.create_credit_bulk(firstAccount=firstAccount, secondAccount=secondAccount)
        credit_response = MyRequests.post(url=CREATE_CREDIT_BULK_URL, data=data)
        Assertions.assert_status_code_and_message(credit_response, expectedStatusCode, expectedMsg)