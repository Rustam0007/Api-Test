import random
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CHANGE_COMPANY_URL
from config.config_data import COMPANY_EXT_REF
from statuses import statusCode


class TestChangeCompanyName(BaseCase):
    nameForCompany = f'Autotest_Change_Company_Name-{random.randint(1, 1000)}'

    def test_change_company_name(self, select_value, update_value):
        data = self.change_company(f"{COMPANY_EXT_REF}", self.nameForCompany)
        response = MyRequests.post(url=CHANGE_COMPANY_URL, data=data)
        Assertions.assert_status_code_and_message(response, statusCode.APPROVED, 'Approved')

        Assertions.check_DB(select_value('name', 'client_company', 'id', response.json()['id']),
                            self.nameForCompany,
                            f"Unexpected company name"
                            f"Expected {self.nameForCompany}"
                            f"Actual {select_value('name', 'client_company', 'id', response.json()['id'])}"
                            )

        # Вернем название компании в начальное значение
        update_value('client_company', 'name', 'OOO-Faha-company', 'external_ref', f"{COMPANY_EXT_REF}")
    @pytest.mark.parametrize('externalRef, name, expectedStatusCode, expectedMsg',
                             [
                                 ('', nameForCompany, statusCode.NOTFOUND, 'Not found'), # empty_external_ref
                                 (f"{COMPANY_EXT_REF}", '', statusCode.BADREQUEST, 'The Name field is required.')  # empty_name

                             ])
    def test_change_company_name_invalid_cases(self, externalRef, name, expectedStatusCode, expectedMsg):
        data = self.change_company(externalRef=externalRef, name=name)
        response = MyRequests.post(url=CHANGE_COMPANY_URL, data=data)
        Assertions.assert_status_code_and_message(response, expectedStatusCode, expectedMsg)