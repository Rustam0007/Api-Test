import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CREATE_CREDIT_BY_PAN_URL
from config.config_data import CARD_PAN, FIRST_ACCOUNT_ID, CARD_ID, FIRST_ACCOUNT_EXT_REF
from statuses import statusCode, cardCurrency, transactionTypes


class TestCreateCreditByPan(BaseCase):
    def test_create_credit_by_pan(self, select_value):
        # credit_by_pan operation
        data = self.create_credit_by_pan(pan=CARD_PAN, deferred=False, transactionType=transactionTypes.QRPAYMENT, amount=10, currency=cardCurrency.TJS)
        credit_response = MyRequests.post(url=CREATE_CREDIT_BY_PAN_URL, data=data)
        Assertions.assert_status_code_and_message(credit_response, statusCode.APPROVED, 'Approved')

        availableBalance = credit_response.json()['availableBalance']
        availableBalanceInDB = select_value('balance', 'accounts', 'id', FIRST_ACCOUNT_ID)
        if type(availableBalance) is int:
            availableBalance = f"{availableBalance}.00"

        Assertions.check_DB(str(availableBalanceInDB), str(availableBalance),
                            f"Unexpected availableBalance.\n"
                            f"Expected {availableBalanceInDB}\n"
                            f"Actual {availableBalance}"
                            )

    def test_create_credit_byPan_when_status_declared(self, select_value, update_value):
        update_value('cards', 'syncStateStatus', 12, 'id', CARD_ID)

        # credit operation
        data = self.create_credit_by_pan(pan=CARD_PAN, deferred=False, transactionType=transactionTypes.QRPAYMENT, amount=10, currency=cardCurrency.TJS)
        credit_response = MyRequests.post(url=CREATE_CREDIT_BY_PAN_URL, data=data)
        Assertions.assert_status_code_and_message(credit_response, statusCode.APPROVED, 'Approved')

        availableBalance = credit_response.json()['availableBalance']
        availableBalanceInDB = select_value('balance', 'accounts', 'id', FIRST_ACCOUNT_ID)
        if type(availableBalance) is int:
            availableBalance = f"{availableBalance}.00"

        Assertions.check_DB(str(availableBalanceInDB), str(availableBalance),
                            f"Unexpected availableBalance.\n"
                            f"Expected {availableBalanceInDB}\n"
                            f"Actual {availableBalance}"
                            )

        update_value('cards', 'syncStateStatus', 1, 'id', CARD_ID)

    def test_create_credit_byPan_when_card_is_inActive(self, update_value):
        # Изменяем статус карты на InActive во время этого кейса чтобы проверить валидацию
        update_value('cards', 'syncStateStatus', 0, 'id', CARD_ID)

        data = self.create_credit_by_pan(pan=CARD_PAN, deferred=False, transactionType=transactionTypes.QRPAYMENT, amount=10, currency=cardCurrency.TJS)
        credit_response = MyRequests.post(url=CREATE_CREDIT_BY_PAN_URL, data=data)
        Assertions.assert_status_code_and_message(credit_response, statusCode.INVALIDCARD, f"Card is not active/open or not exist!")

        # Обратно вернем статус на Open
        update_value('cards', 'syncStateStatus', 1, 'id', CARD_ID)

    @pytest.mark.parametrize('pan, deferred, transactionType, currency, amount, expectedStatusCode, expectedMsg',
                             [
                                 (CARD_PAN+'123', False, transactionTypes.QRPAYMENT, cardCurrency.TJS, 100, statusCode.BADREQUEST, "Pan must contain 16 number"), #invalid_pan
                                 (CARD_PAN, False, transactionTypes.QRPAYMENT, cardCurrency.TJS, 0, statusCode.BADREQUEST, "Amount must be between 0.01 and 10000000"), #invalid_amount
                                 (CARD_PAN, False, transactionTypes.QRPAYMENT, 2211, 100, statusCode.BADREQUEST, "Invalid currency") #invalid_currency
                             ])
    def test_create_credit_with_invalid_pan(self, pan, deferred, transactionType, currency, amount, expectedStatusCode, expectedMsg):
        data = self.create_credit_by_pan(pan=pan, deferred=deferred, transactionType=transactionType, currency=currency, amount=amount)
        credit_response = MyRequests.post(url=CREATE_CREDIT_BY_PAN_URL, data=data)
        Assertions.assert_status_code_and_message(credit_response, expectedStatusCode, expectedMsg)

    @pytest.mark.parametrize('statusBeforeReq, statusAfterReq, pan, expectedStatusCode, expectedMsg',
        [
            (0, 1, CARD_PAN, statusCode.NOTFOUND, "Not found : Card does not have account with specified currency"),
            (9, 1, CARD_PAN, statusCode.NOTFOUND, "Not found : Card does not have account with specified currency"),
            (5, 1, CARD_PAN, statusCode.NOTFOUND, "Not found : Card does not have account with specified currency"),
        ])
    def test_create_credit_negative_cases_from_account_status(self, update_value, statusBeforeReq, statusAfterReq, pan, expectedStatusCode, expectedMsg):
        # Изменяем статус счёта на InActive во время этого кейса чтобы проверить валидацию
        update_value('accounts', 'syncStateStatus', statusBeforeReq, 'external_ref', FIRST_ACCOUNT_EXT_REF)

        data = self.create_credit_by_pan(pan=pan, deferred=False, transactionType=transactionTypes.QRPAYMENT, currency=cardCurrency.TJS, amount=10)
        credit_response = MyRequests.post(url=CREATE_CREDIT_BY_PAN_URL, data=data)
        Assertions.assert_status_code_and_message(credit_response, expectedStatusCode, expectedMsg)

        # Обратно вернем статус на Open
        update_value('accounts', 'syncStateStatus', statusAfterReq, 'external_ref', FIRST_ACCOUNT_EXT_REF)
