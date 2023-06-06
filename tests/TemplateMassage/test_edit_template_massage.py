import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_data import TEMPLATE_ID
from config.config_url import EDIT_TEMPLATE_MESSAGE_URL
from statuses import statusCode


class TestEditTemplateMessage(BaseCase):
    template = 'EDIT Пополнение карты {Card}; Сумма {Amount}, ' \
               '{Purchase}; Терминал {Terminal}. ' \
               'Текущий баланс {Balance}. ' \
               'Дата {Date}. '

    def test_edit_template_message(self, update_value, select_value):
        # На всякий случай проверяем статус шаблона чтобы он не был удален. Если он удален запрос даст ошибку
        update_value('template_msg', 'is_removed', False, 'id', TEMPLATE_ID)

        data = self.edit_template_message(templateMessageId=TEMPLATE_ID, templateMessage=self.template)
        edit_template_response = MyRequests.post(url=EDIT_TEMPLATE_MESSAGE_URL, data=data)

        template_in_db = select_value('template', 'template_msg', 'id', TEMPLATE_ID)

        Assertions.assert_status_code_and_message(edit_template_response, statusCode.APPROVED, 'Approved')
        assert template_in_db == self.template, "Template do not edit!"

    @pytest.mark.parametrize('template_id, expectedStatusCode, expectedMsg',
                             [
                                 (1223221, statusCode.NOTFOUND, "Template message not found or was deleted!") # invalid template_id
                             ])
    def test_edit_template_message_negative_cases(self, template_id, expectedStatusCode, expectedMsg):
        data = self.edit_template_message(templateMessageId=template_id, templateMessage=self.template)
        edit_template_response = MyRequests.post(url=EDIT_TEMPLATE_MESSAGE_URL, data=data)

        Assertions.assert_status_code_and_message(edit_template_response, expectedStatusCode, expectedMsg)