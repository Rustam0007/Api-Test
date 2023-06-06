import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CREATE_COMPANY_URL
from statuses import statusCode


class TestCreateCompany(BaseCase):
    def test_create_company(self, remove_value):
        data = self.create_company(name="Autotest_Company")
        response = MyRequests.post(url=CREATE_COMPANY_URL, data=data)
        company_id = response.json()['id']

        Assertions.assert_status_code_and_message(response, statusCode.APPROVED, 'Approved')

        remove_value('limit_account', 'id', company_id)
        remove_value('limit_card', 'id', company_id)
        remove_value('client_company', 'id', company_id)

    @pytest.mark.parametrize('externalRef, name, expectedStatusCode, expectedMsg',
                             [
                                 ('', 'Autotest_Company', statusCode.BADREQUEST, 'The ExternalRef field is required.'), # empty_external_ref
                                 (None, '', statusCode.BADREQUEST, 'The Name field is required.'), # empty_name
                                 (700, 'Autotest_Company', 926, 'Already registered company with 700 ExternalRef') # already_existing

                             ])
    def test_create_company_negative_cases(self, externalRef, name, expectedStatusCode, expectedMsg):
        data = self.create_company(externalRef=externalRef, name=name)
        response = MyRequests.post(url=CREATE_COMPANY_URL, data=data)

        Assertions.assert_status_code_and_message(response, expectedStatusCode, expectedMsg)


