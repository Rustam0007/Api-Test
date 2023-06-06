import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CREATE_CREDIT_URL
from config.config_data import CARD_ID, FIRST_ACCOUNT_EXT_REF, FIRST_ACCOUNT_ID
from statuses import statusCode, transactionTypes


class TestCreateCredit(BaseCase):

    def test_create_credit(self, select_value, update_value):
        update_value('cards', 'syncStateStatus', 1, 'id', CARD_ID)

        # credit operation
        data = self.create_credit(account=FIRST_ACCOUNT_EXT_REF, deferred=False, transactionType=transactionTypes.QRPAYMENT, amount=7)
        credit_response = MyRequests.post(url=CREATE_CREDIT_URL, data=data)
        Assertions.assert_status_code_and_message(credit_response, statusCode.APPROVED, 'Approved')

        availableBalance = credit_response.json()['availableBalance']
        availableBalanceInDB = select_value('balance', 'accounts', 'id', FIRST_ACCOUNT_ID)
        if type(availableBalance) is int:
            availableBalance = f"{availableBalance}.00"
        Assertions.check_DB(str(availableBalanceInDB), str(availableBalance),
                            f"Unexpected availableBalance\n"
                            f"Expected {availableBalanceInDB}\n "
                            f"Actual {availableBalance}"
                            )

    def test_create_credit_when_status_declared(self, select_value, update_value):
        update_value('cards', 'syncStateStatus', 12, 'id', CARD_ID)

        # credit operation
        data = self.create_credit(account=FIRST_ACCOUNT_EXT_REF, deferred=False, transactionType=transactionTypes.QRPAYMENT, amount=7)
        credit_response = MyRequests.post(url=CREATE_CREDIT_URL, data=data)
        Assertions.assert_status_code_and_message(credit_response, statusCode.APPROVED, 'Approved')

        availableBalance = credit_response.json()['availableBalance']
        availableBalanceInDB = select_value('balance', 'accounts', 'id', FIRST_ACCOUNT_ID)
        if type(availableBalance) is int:
            availableBalance = f"{availableBalance}.00"
        Assertions.check_DB(str(availableBalanceInDB), str(availableBalance),
                            f"Unexpected availableBalance\n"
                            f"Expected {availableBalanceInDB}\n "
                            f"Actual {availableBalance}"
                            )
        update_value('cards', 'syncStateStatus', 1, 'id', CARD_ID)

    def test_create_credit_when_card_is_inActive(self, update_value):
        # Изменяем статус карты на InActive во время этого кейса чтобы проверить валидацию
        update_value('cards', 'syncStateStatus', 0, 'id', CARD_ID)

        data = self.create_credit(account=FIRST_ACCOUNT_EXT_REF, deferred=False, transactionType=transactionTypes.QRPAYMENT, amount=10)
        credit_response = MyRequests.post(url=CREATE_CREDIT_URL, data=data)
        Assertions.assert_status_code_and_message(credit_response, statusCode.NOTFOUND, f"Not found : Account {FIRST_ACCOUNT_EXT_REF} not found")

        # Обратно вернем статус на Open
        update_value('cards', 'syncStateStatus', 1, 'id', CARD_ID)

    @pytest.mark.parametrize('account, deferred, transactionType, amount, externalRef, expectedStatusCode, expectedMsg',
                             [
                                 (FIRST_ACCOUNT_EXT_REF + '9210', False, transactionTypes.QRPAYMENT, 10, None, statusCode.BADREQUEST, "Account must contain 20 number"),
                                 (FIRST_ACCOUNT_EXT_REF, False, transactionTypes.QRPAYMENT, 0, None, statusCode.BADREQUEST, "Amount must be between 0.01 and 10000000"),
                                 (FIRST_ACCOUNT_EXT_REF, False, transactionTypes.QRPAYMENT, 10, "tester", statusCode.DUPLICATETRANSACTION, "Duplicate account credit record ExternalRef: qa")
                             ])
    def test_create_credit_negative_cases(self, account, deferred, transactionType, amount, externalRef, expectedStatusCode, expectedMsg):
        data = self.create_credit(account=account, deferred=deferred, transactionType=transactionType, amount=amount, externalRef=externalRef)
        credit_response = MyRequests.post(url=CREATE_CREDIT_URL, data=data)
        Assertions.assert_status_code_and_message(credit_response, expectedStatusCode, expectedMsg)

    @pytest.mark.parametrize('statusBeforeReq, statusAfterReq, account, deferred, transactionType, expectedStatusCode, expectedMsg',
                             [
                                 (0, 1, FIRST_ACCOUNT_EXT_REF, False, transactionTypes.QRPAYMENT, statusCode.SENDERUNAVAILABLE, "Account is Not Active"),
                                 (9, 1, FIRST_ACCOUNT_EXT_REF, False, transactionTypes.QRPAYMENT, statusCode.SENDERUNAVAILABLE, "Account is Closed Fimi"),
                                 (5, 1, FIRST_ACCOUNT_EXT_REF, False, transactionTypes.QRPAYMENT, statusCode.SENDERUNAVAILABLE, "Account is Information Only"),
                             ])
    def test_create_credit_negative_cases_from_account_status(self, update_value, statusBeforeReq, statusAfterReq, account, deferred, transactionType, expectedStatusCode, expectedMsg):
        # Изменяем статус счёта на InActive во время этого кейса чтобы проверить валидацию
        update_value('accounts', 'syncStateStatus', statusBeforeReq, 'external_ref', FIRST_ACCOUNT_EXT_REF)

        data = self.create_credit(account=account, deferred=deferred, transactionType=transactionType, amount=10)
        credit_response = MyRequests.post(url=CREATE_CREDIT_URL, data=data)
        Assertions.assert_status_code_and_message(credit_response, expectedStatusCode, expectedMsg)

        # Обратно вернем статус на Open
        update_value('accounts', 'syncStateStatus', statusAfterReq, 'external_ref', FIRST_ACCOUNT_EXT_REF)

