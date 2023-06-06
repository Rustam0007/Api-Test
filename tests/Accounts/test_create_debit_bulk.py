from time import sleep, time
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CREATE_DEBIT_BULK_URL
from config.config_data import FIRST_ACCOUNT_EXT_REF, SECOND_ACCOUNT_EXT_REF
from statuses import statusCode, transactionStatus


class TestCreateDebitBulk(BaseCase):
    def test_create_debit_bulk(self, select_value):
        # Debit operation
        data = self.create_debit_bulk(firstAccount=FIRST_ACCOUNT_EXT_REF, secondAccount=SECOND_ACCOUNT_EXT_REF, firstAmount=10, secondAmount=10)
        debit_response = MyRequests.post(url=CREATE_DEBIT_BULK_URL, data=data)
        Assertions.assert_status_code_and_message(debit_response, statusCode.ACCEPTED, "Accepted for further process")

        getFirstExternalRef = data['bulkInfo'][0]['externalRef']
        getSecondExternalRef = data['bulkInfo'][1]['externalRef']

        start_time = time()  # запоминаем текущее время
        timeout = 80  # задаем таймаут в секундах

        while (time() - start_time) < timeout:
            if select_value('syncStateStatus', 'account_debit', 'external_ref', f'{getFirstExternalRef}') == transactionStatus.APPROVED and \
                    select_value('syncStateStatus', 'account_debit', 'external_ref', f'{getSecondExternalRef}') == transactionStatus.APPROVED:
                break
            sleep(1)

        if select_value('syncStateStatus', 'account_debit', 'external_ref', f'{getFirstExternalRef}') != transactionStatus.APPROVED \
                or select_value('syncStateStatus', 'account_debit', 'external_ref', f'{getSecondExternalRef}') != transactionStatus.APPROVED:
            raise Exception(f"ОШИБКА: Статусы не стали равны 1")

    @pytest.mark.parametrize('firstAccount, secondAccount, firstAmount, secondAmount, expectedStatusCode, expectedMsg',
                             [
                                 (FIRST_ACCOUNT_EXT_REF + '9210', SECOND_ACCOUNT_EXT_REF, 10, 20, statusCode.BADREQUEST, "Account must contain 20 number"),
                                 (FIRST_ACCOUNT_EXT_REF, SECOND_ACCOUNT_EXT_REF + '9210', 10, 20, statusCode.BADREQUEST, "Account must contain 20 number")
                             ])
    def test_create_debit_negative_cases(self, firstAccount, secondAccount, firstAmount, secondAmount, expectedStatusCode, expectedMsg):
        data = self.create_debit_bulk(firstAccount=firstAccount, secondAccount=secondAccount, firstAmount=firstAmount, secondAmount=secondAmount)
        debit_response = MyRequests.post(url=CREATE_DEBIT_BULK_URL, data=data)
        Assertions.assert_status_code_and_message(debit_response, expectedStatusCode, expectedMsg)
