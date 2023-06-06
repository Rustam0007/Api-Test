from time import sleep

import pytest
from config.config_url import CHANGE_CARD_FEES_STATUS
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from statuses import statusCode, transactionStatus, feeType


class TestChangeCardFeesStatus(BaseCase):
    def test_change_all_card_fees_status(self, update_value):
        card_response = MyRequests.post(url=CHANGE_CARD_FEES_STATUS, data={})
        Assertions.assert_status_code_and_message(card_response, statusCode.APPROVED, 'Approved')

        # обратно вернем статус с 3 на 12
        update_value('fees', 'syncStateStatus', transactionStatus.NEEDCONFIRMATION, 'syncStateStatus', 3)

    def test_change_card_fees_status_with_fee_id(self, select_value, update_value):
        fee_id = select_value('id', 'fees', 'fee_type', feeType.SMS_FEE, 'syncStateStatus', transactionStatus.NEEDCONFIRMATION)
        status_before_req = select_value('syncStateStatus', 'fees', 'id', fee_id)

        data_for_change_status = self.change_card_fees_status(feeId=fee_id,
                                                              fromStatus=transactionStatus.NEEDCONFIRMATION,
                                                              toStatus=transactionStatus.ACCEPTED, feeType=None)
        card_response = MyRequests.post(url=CHANGE_CARD_FEES_STATUS, data=data_for_change_status)
        Assertions.assert_status_code_and_message(card_response, statusCode.APPROVED, 'Approved')

        status_after_req = select_value('syncStateStatus', 'fees', 'id', fee_id)
        assert status_before_req != status_after_req, 'Card fees status do not change!'

        # обратно вернем статус с 3 на 12
        update_value('fees', 'syncStateStatus', transactionStatus.NEEDCONFIRMATION, 'id', fee_id)

    def test_change_card_fees_status_with_fee_type(self, select_value, update_value):
        fee_id = select_value('id', 'fees', 'fee_type', feeType.SMS_FEE, 'syncStateStatus', transactionStatus.NEEDCONFIRMATION)
        status_before_req = select_value('syncStateStatus', 'fees', 'id', fee_id)

        data_for_change_status = self.change_card_fees_status(feeId=None,
                                                              fromStatus=transactionStatus.NEEDCONFIRMATION,
                                                              toStatus=transactionStatus.ACCEPTED, feeType=feeType.SMS_FEE)
        card_response = MyRequests.post(url=CHANGE_CARD_FEES_STATUS, data=data_for_change_status)
        Assertions.assert_status_code_and_message(card_response, statusCode.APPROVED, 'Approved')

        status_after_req = select_value('syncStateStatus', 'fees', 'id', fee_id)
        assert status_before_req != status_after_req, 'Card fees status do not change!'

        # обратно вернем статус с 3 на 12
        update_value('fees', 'syncStateStatus', transactionStatus.NEEDCONFIRMATION, 'syncStateStatus', transactionStatus.ACCEPTED)

    @pytest.mark.parametrize('fee_id, from_status, to_status, fee_type, expectedStatusCode, expectedMsg',
                             [
                                 (2211, transactionStatus.NEEDCONFIRMATION, transactionStatus.ACCEPTED, 2211, 910, 'FeeType: Invalid Card Fee Type')  # invalid_fee_type
                             ]
                            )
    def test_change_card_fees_status_invalid_cases(self, fee_id, from_status, to_status, fee_type, expectedStatusCode, expectedMsg):
        data_for_change_status = self.change_card_fees_status(feeId=fee_id, fromStatus=from_status, toStatus=to_status, feeType=fee_type)
        card_response = MyRequests.post(url=CHANGE_CARD_FEES_STATUS, data=data_for_change_status)
        Assertions.assert_status_code_and_message(card_response, expectedStatusCode, expectedMsg)
