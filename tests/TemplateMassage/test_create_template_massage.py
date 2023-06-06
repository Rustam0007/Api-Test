from random import randint
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CREATE_TEMPLATE_MESSAGE_URL
from statuses import statusCode


class TestCreateTemplateMessage(BaseCase):
    randomNumber = randint(1, 9999)
    template = 'Пополнение карты {Card}; Сумма {Amount}, ' \
               '{Purchase}; Терминал {Terminal}. ' \
               'Текущий баланс {Balance}. ' \
               'Дата {Date}. ' \
               f'AUTOTEST-{randomNumber}'

    def test_create_template_message(self, select_value, existing_in_db, remove_value):
        data = self.create_template_message(templateMessage=self.template, tranCodeId=16, responseCodeId=1)
        template_message_response = MyRequests.post(url=CREATE_TEMPLATE_MESSAGE_URL, data=data)

        Assertions.assert_status_code_and_message(template_message_response, statusCode.APPROVED, 'Approved')
        assert existing_in_db('template_msg', 'template', self.template) == True, \
            f"Template do not create."

        # Находим id созданного нам шаблона и удаляем его чтобы не мусорить БД
        template_id = select_value('id', 'template_msg', 'template', self.template)
        remove_value('fimi_tran_response_template_message', 'template_message_id', template_id)
        remove_value('template_msg', 'template', self.template)

    @pytest.mark.parametrize('template, expectedStatusCode, expectedMsg',
                             [
                                 ('', statusCode.BADREQUEST, 'The TemplateMessage field is required.'), # empty template
                             ])
    def test_edit_template_message_negative_cases(self, template, expectedStatusCode, expectedMsg):
        data = self.create_template_message(templateMessage=template, tranCodeId=16, responseCodeId=1)
        edit_template_response = MyRequests.post(url=CREATE_TEMPLATE_MESSAGE_URL, data=data)

        Assertions.assert_status_code_and_message(edit_template_response, expectedStatusCode, expectedMsg)