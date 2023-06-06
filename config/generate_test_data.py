from random import randint
from time import time, sleep
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_data import *
from config.config_url import *
from statuses import statusCode, syncStateStatus


def test_generate_test_data(select_value, existing_in_db):
    # Создаем пользователя здесь, например, используя библиотеку requests
    person_data = BaseCase.create_person(fullname="Person(generate_test_data)", sex="M")
    person_response = MyRequests.post(url=CREATE_PERSON_URL, data=person_data)
    Assertions.assert_status_code_and_message(person_response, statusCode.APPROVED, 'Approved')
    person_id = person_response.json()['personId']
    person_ext_ref = select_value('external_ref', 'person', 'id', person_id)

    # Создаем карту
    card_data = BaseCase.create_named_card(personId=person_id, companyExternalRef="", typeOfCard=1)
    card_response = MyRequests.post(url=CREATE_NAMED_CARD_URL, data=card_data)
    Assertions.assert_status_code_and_message(card_response, statusCode.APPROVED, 'Approved')
    card_id = card_response.json()['cardId']
    pan_id = card_response.json()['panId']
    card_pan = card_response.json()['pan']
    card_token = select_value('token', 'cards', 'id', card_id)
    masked_pan = select_value('masked_pan', 'cards', 'id', card_id)

    # Создаем счёт для карты
    account_data = BaseCase.create_account(cardId=card_id, personId=person_id, )
    account_response = MyRequests.post(url=CREATE_ACCOUNT_URL, data=account_data)
    Assertions.assert_status_code_and_message(account_response, statusCode.APPROVED, 'Approved')
    first_account_id = account_response.json()['accounts'][0]['id']
    second_account_id = account_response.json()['accounts'][1]['id']
    first_account_ext_ref = account_response.json()['accounts'][0]['externalRef']
    second_account_ext_ref = account_response.json()['accounts'][1]['externalRef']

    # ID компании для тестов файла Company
    company_id = 88
    company_ext_ref = '777'

    # Создаём Template message для тестов раздела TemplateMessage
    randomNumber = randint(1, 9999)
    template = 'Пополнение карты {Card}; Сумма {Amount}, ' \
               '{Purchase}. ' \
               'Дата {Date}. ' \
               f'AUTOTEST-{randomNumber}'

    data = BaseCase.create_template_message(templateMessage=template, tranCodeId=16, responseCodeId=1)
    template_message_response = MyRequests.post(url=CREATE_TEMPLATE_MESSAGE_URL, data=data)
    Assertions.assert_status_code_and_message(template_message_response, statusCode.APPROVED, 'Approved')
    assert existing_in_db('template_msg', 'template', template) == True, \
        f"Template do not create"
    template_id = select_value('id', 'template_msg', 'template', template)

    # Создаем файл config_data и записываем тестовые данные в него
    with open('config_data.py', 'w') as f:
        f.write(
            f'PERSON_ID = {person_id}\n'
            f'PERSON_EXT_REF = "{person_ext_ref}"\n'
            f'CARD_ID = {card_id}\n'
            f'CARD_TOKEN = "{card_token}"\n'
            f'CARD_PAN_ID = {pan_id}\n'
            f'CARD_PAN = "{card_pan}"\n'
            f'CARD_MASKED_PAN = "{masked_pan}"\n'
            f'FIRST_ACCOUNT_ID = {first_account_id}\n'
            f'SECOND_ACCOUNT_ID = {second_account_id}\n'
            f'FIRST_ACCOUNT_EXT_REF = "{first_account_ext_ref}"\n'
            f'SECOND_ACCOUNT_EXT_REF = "{second_account_ext_ref}"\n'
            f'COMPANY_ID = {company_id}\n'
            f'COMPANY_EXT_REF = {company_ext_ref}\n'
            f'TEMPLATE_ID = {template_id}'

        )
    start_time = time()
    timeout = 120

    while (time() - start_time) < timeout:
        if \
                select_value('syncStateStatus', 'person', 'id', person_id) == syncStateStatus.SYNCED and \
                        select_value('syncStateStatus', 'cards', 'id', card_id) == syncStateStatus.SYNCED and \
                        select_value('syncStateStatus', 'accounts', 'id', first_account_id) == syncStateStatus.SYNCED and \
                        select_value('syncStateStatus', 'accounts', 'id', second_account_id) == syncStateStatus.SYNCED:
            break
        sleep(1)

    if \
            select_value('syncStateStatus', 'person', 'id', person_id) != syncStateStatus.SYNCED and \
                    select_value('syncStateStatus', 'cards', 'id', card_id) != syncStateStatus.SYNCED and \
                    select_value('syncStateStatus', 'accounts', 'id', first_account_id) != syncStateStatus.SYNCED and \
                    select_value('syncStateStatus', 'accounts', 'id', second_account_id) != syncStateStatus.SYNCED:
        raise Exception(f"ОШИБКА: status карты не равен 10")


def test_active_card(select_value):
    status = 1
    data_for_change_status = BaseCase.change_card_status(cardId=CARD_ID, cardToken="", status=status)
    card_response = MyRequests.post(url=CHANGE_CARD_STATUS_URL, data=data_for_change_status)
    Assertions.assert_status_code_and_message(card_response, statusCode.APPROVED, 'Approved')
    if select_value('syncStateStatus', 'cards', 'id', CARD_ID) != status:
        raise Exception(f"ОШИБКА: Статус карты не равен 1")


def test_credit_account(select_value):
    # Пополняем первый счёт чтобы при тесте create_debit у нас не упали тесты
    firstBalanceBeforeCredit = select_value('balance', 'accounts', 'id', FIRST_ACCOUNT_ID)
    data = BaseCase.create_credit(account=FIRST_ACCOUNT_EXT_REF, deferred=False, transactionType=10, amount=1000)
    credit_response = MyRequests.post(url=CREATE_CREDIT_URL, data=data)
    Assertions.assert_status_code_and_message(credit_response, statusCode.APPROVED, 'Approved')
    if select_value('balance', 'accounts', 'id', FIRST_ACCOUNT_ID) < firstBalanceBeforeCredit:
        raise Exception(f"ОШИБКА: Balance первого счёта не изменился")

    # Пополняем второй счёт чтобы при тесте create_debit у нас не упали тесты
    secondBalanceBeforeCredit = select_value('balance', 'accounts', 'id', SECOND_ACCOUNT_ID)
    data = BaseCase.create_credit(account=SECOND_ACCOUNT_EXT_REF, deferred=False, transactionType=10, amount=1000)
    second_credit_response = MyRequests.post(url=CREATE_CREDIT_URL, data=data)
    Assertions.assert_status_code_and_message(second_credit_response, statusCode.APPROVED, 'Approved')
    if select_value('balance', 'accounts', 'id', SECOND_ACCOUNT_ID) < secondBalanceBeforeCredit:
        raise Exception(f"ОШИБКА: Balance второго счёта не изменился")


def test_remove_test_data(remove_value):
    remove_value('accounts', 'id', FIRST_ACCOUNT_ID)
    remove_value('accounts', 'id', SECOND_ACCOUNT_ID)
    remove_value('card_activity_history', 'cards_id', CARD_ID)
    remove_value('cards', 'id', CARD_ID)
    remove_value('person', 'id', PERSON_ID)
    remove_value('fimi_tran_response_template_message', 'template_message_id', TEMPLATE_ID)
    remove_value('template_msg', 'id', TEMPLATE_ID)

    with open('config_data.py', 'w') as file:
        file.write(
            f'PERSON_ID: int\n'
            f'PERSON_EXT_REF: str\n'
            f'CARD_ID: int\n'
            f'CARD_TOKEN: str\n'
            f'CARD_PAN_ID: int\n'
            f'CARD_PAN: str\n'
            f'CARD_MASKED_PAN: str\n'
            f'FIRST_ACCOUNT_ID: int\n'
            f'SECOND_ACCOUNT_ID: int\n'
            f'FIRST_ACCOUNT_EXT_REF: str\n'
            f'SECOND_ACCOUNT_EXT_REF: str\n'
            f'COMPANY_ID: int\n'
            f'COMPANY_EXT_REF: str\n'
            f'TEMPLATE_ID: int\n'
        )
