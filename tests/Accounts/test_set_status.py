from random import choice
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import SET_STATUS_URL
from config.config_data import FIRST_ACCOUNT_ID
from statuses import statusCode, accountStatus


class TestSetSatus(BaseCase):
    statuses = [accountStatus.OPEN, accountStatus.OPENPRIMARYACCOUNT]
    status = choice(statuses)

    def test_set_status(self, select_value):
        # set status to account
        data = self.set_status(accountId=FIRST_ACCOUNT_ID, status=self.status)
        set_status_response = MyRequests.post(url=SET_STATUS_URL, data=data)
        Assertions.assert_status_code_and_message(set_status_response, statusCode.APPROVED, 'Approved')

        statusInDB = select_value('syncStateStatus', 'accounts', 'id', FIRST_ACCOUNT_ID)

        Assertions.check_DB(statusInDB, self.status,
                            f"Unexpected status. "
                            f"Expected {self.status}. "
                            f"Actually {statusInDB}")

    def test_set_status_with_invalid_account_id(self):
        data = self.set_status(accountId=22117744, status=self.status)
        set_status_response = MyRequests.post(url=SET_STATUS_URL, data=data)
        Assertions.assert_status_code_and_message(set_status_response, statusCode.NOTFOUND, "Not found : Account not found.")