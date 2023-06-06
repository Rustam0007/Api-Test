import pytest
from time import sleep, time
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CREATE_PERSON_URL
from statuses import statusCode, syncStateStatus


class TestCreatePerson(BaseCase):
    def test_create_person(self, select_value, remove_value):
        data = self.create_person(fullname="Autotest-Person", sex="M")
        response = MyRequests.post(url=CREATE_PERSON_URL, data=data)
        personId = response.json()['personId']
        Assertions.assert_status_code_and_message(response, statusCode.APPROVED, 'Approved')

        start_time = time()
        timeout = 80

        while (time() - start_time) < timeout:
            if select_value('syncStateStatus', 'person', 'id', personId) == syncStateStatus.SYNCED:
                break
            sleep(1)

        if select_value('syncStateStatus', 'person', 'id', personId) != syncStateStatus.SYNCED:
            raise Exception(f"ОШИБКА: syncStateStatus Клиента не равен 10")

        remove_value('person', 'id', personId)

    @pytest.mark.parametrize('fullname, sex, externalRef, expectedStatusCode, expectedMsg',
        [
            ('Autotest-Person', 'M', '', statusCode.BADREQUEST, 'The ExternalRef field is required.'), #empty external_ref
            ('Autotest-Person'*20, 'M', None, statusCode.INTERNALERROR, 'Internal server error'), #invalid fullname
            ('Autotest-Person', 'B', None, statusCode.BADREQUEST, "Sex: Either 'M' (male) or 'F' (female) accepted") #invalid sex
        ]
    )
    def test_create_person_negative_cases(self,
                                          fullname,
                                          sex,
                                          externalRef,
                                          expectedStatusCode,
                                          expectedMsg):
        data = self.create_person(fullname=fullname, sex=sex, externalRef=externalRef)
        response = MyRequests.post(url=CREATE_PERSON_URL, data=data)
        Assertions.assert_status_code_and_message(response, expectedStatusCode, expectedMsg)

