from random import choice
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CHANGE_DEFAULT_ACCOUNT_URL
from config.config_data import FIRST_ACCOUNT_ID, SECOND_ACCOUNT_ID, CARD_ID, CARD_TOKEN
from statuses import statusCode


class TestChangeDefaultAccount(BaseCase):
    def test_change_default_account(self, select_value):
        default_account_before_req = select_value('id', 'accounts', 'cards_id', f'{CARD_ID}', 'cards_default', True)

        account_id = choice([FIRST_ACCOUNT_ID, SECOND_ACCOUNT_ID])
        while account_id == default_account_before_req:
            account_id = choice([FIRST_ACCOUNT_ID, SECOND_ACCOUNT_ID])

        data = self.change_default_account(cardToken=CARD_TOKEN, accountId=account_id)
        change_default_account_response = MyRequests.post(url=CHANGE_DEFAULT_ACCOUNT_URL, data=data)
        Assertions.assert_status_code_and_message(change_default_account_response, statusCode.APPROVED, 'Approved')

        default_account_after_req = select_value('id', 'accounts', 'cards_id', f'{CARD_ID}', 'cards_default', True)

        assert default_account_before_req != default_account_after_req, 'Default account do not change!'

    def test_change_default_account_with_invalid_card_token(self):
        account_id = choice([FIRST_ACCOUNT_ID, SECOND_ACCOUNT_ID])

        data = self.change_default_account(cardToken='1234', accountId=account_id)

        change_default_account_response = MyRequests.post(url=CHANGE_DEFAULT_ACCOUNT_URL, data=data)
        Assertions.assert_status_code_and_message(change_default_account_response, statusCode.NOTFOUND, "CardToken 1234 not found or doesn't belong to user")