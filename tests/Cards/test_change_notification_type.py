from random import choice
import pytest
from config.config_data import CARD_ID, CARD_TOKEN
from config.config_url import CHANGE_NOTIFICATION_TYPE
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from statuses import statusCode, notificationType


class TestChangeNotificationType(BaseCase):
    def test_change_notification_type_with_card_id(self, select_value):
        notification_type_before_req = select_value('notification_types', 'cards', 'id', CARD_ID)
        if notification_type_before_req == notificationType.SMS:
            notification_type = notificationType.PUSH
        else:
            notification_type = notificationType.SMS

        data_for_change_notification_type = self.change_notification_type(cardId=CARD_ID, cardToken='', notificationType=notification_type)
        card_response = MyRequests.post(url=CHANGE_NOTIFICATION_TYPE, data=data_for_change_notification_type)
        Assertions.assert_status_code_and_message(card_response, statusCode.APPROVED, 'Approved')

        notification_type_in_DB = select_value('notification_types', 'cards', 'id', CARD_ID)
        Assertions.check_DB(notification_type_in_DB, notification_type, 'Notification_type is not change!')

    def test_change_notification_type_with_card_token(self, select_value):
        notification_type_before_req = select_value('notification_types', 'cards', 'id', CARD_ID)
        if notification_type_before_req == notificationType.SMS:
            notification_type = notificationType.PUSH
        else:
            notification_type = notificationType.SMS

        data_for_change_notification_type = self.change_notification_type(cardId=0, cardToken=CARD_TOKEN, notificationType=notification_type)
        card_response = MyRequests.post(url=CHANGE_NOTIFICATION_TYPE, data=data_for_change_notification_type)
        Assertions.assert_status_code_and_message(card_response, statusCode.APPROVED, 'Approved')

        notification_type_in_DB = select_value('notification_types', 'cards', 'id', CARD_ID)
        Assertions.check_DB(notification_type_in_DB, notification_type, 'Notification_type is not change!')


    @pytest.mark.parametrize('cardId, cardToken, notificationTypes, expectedStatusCode, expectedMsg',
                             [
                                 (221111, "", notificationType.SMS, statusCode.NOTFOUND, 'Not found : Card not found'),  # invalid_card_id
                                 (CARD_ID, "1234", notificationType.PUSH, statusCode.NOTFOUND, 'Not found : Card not found')  # invalid_card_token
                             ]
                            )
    def test_change_notification_type_negative_cases(self, cardId, cardToken, notificationTypes, expectedStatusCode, expectedMsg, select_value):
        notification_type_before_req = select_value('notification_types', 'cards', 'id', CARD_ID)
        if notification_type_before_req == notificationType.SMS and notificationTypes == notificationType.SMS:
            notificationTypes = notificationType.PUSH
        else:
            notificationTypes = notificationType.SMS

        data_for_change_notification_type = self.change_notification_type(cardId=cardId, cardToken=cardToken, notificationType=notificationTypes)
        card_response = MyRequests.post(url=CHANGE_NOTIFICATION_TYPE, data=data_for_change_notification_type)
        Assertions.assert_status_code_and_message(card_response, expectedStatusCode, expectedMsg)

    def test_change_invalid_notification_type(self, select_value):
        data_for_change_notification_type = self.change_notification_type(cardId=CARD_ID, cardToken='', notificationType=4)
        card_response = MyRequests.post(url=CHANGE_NOTIFICATION_TYPE, data=data_for_change_notification_type)
        Assertions.assert_status_code_and_message(card_response, statusCode.BADREQUEST, 'Invalid Notification Type')

    def test_change_notification_type_with_already_exist(self, select_value):
        notification_type_in_db = select_value('notification_types', 'cards', 'id', CARD_ID)

        data_for_change_notification_type = self.change_notification_type(cardId=CARD_ID, cardToken='', notificationType=notification_type_in_db)
        card_response = MyRequests.post(url=CHANGE_NOTIFICATION_TYPE, data=data_for_change_notification_type)
        Assertions.assert_status_code_and_message(card_response, statusCode.BADREQUEST, 'Card NotificationType is already an Sms notification to phone number!')
