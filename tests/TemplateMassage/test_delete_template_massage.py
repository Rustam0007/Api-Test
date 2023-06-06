import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import DELETE_TEMPLATE_MESSAGE_URL
from config.config_data import TEMPLATE_ID
from statuses import statusCode


class TestDeleteTemplateMessage(BaseCase):
    def test_delete_template_message(self, select_value):
        delete_template_response = MyRequests.post(url=f"{DELETE_TEMPLATE_MESSAGE_URL}/{TEMPLATE_ID}")

        deleteStatus = select_value('is_removed', 'template_msg', 'id', TEMPLATE_ID)
        Assertions.assert_status_code_and_message(delete_template_response, statusCode.APPROVED, 'Approved')
        assert deleteStatus == True, 'Template is not Deleted'

    @pytest.mark.parametrize('template_id, expectedStatusCode, expectedMsg',
                             [
                                 (12345678, statusCode.NOTFOUND, "Template message not found or was deleted!") # invalid template_id
                             ])
    def test_delete_template_message_negative_cases(self, template_id, expectedStatusCode, expectedMsg):
        delete_template_response = MyRequests.post(url=f"{DELETE_TEMPLATE_MESSAGE_URL}/{template_id}")

        Assertions.assert_status_code_and_message(delete_template_response, expectedStatusCode, expectedMsg)
