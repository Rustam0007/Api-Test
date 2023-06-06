import uuid
from random import randint, choice
from time import strftime


class BaseCase:
    @staticmethod
    def create_person(fullname=None, sex=None, externalRef=None):
        if externalRef is None:
            externalRef = f"{uuid.uuid4()}"
        return {
            "externalRef": externalRef,
            "fullName": fullname,
            "sex": sex,
            "vip": 0
        }

    @staticmethod
    def create_company(externalRef=None, name=None):
        if externalRef is None:
            externalRef = uuid.uuid4()

        return {
            "externalRef": f"{externalRef}",
            "name": name
        }

    @staticmethod
    def change_company(externalRef=None, name=None):
        if externalRef is None:
            externalRef = f"{uuid.uuid4()}"
        if name is None:
            name = f"Autotest_company_None_Name-{randint(1, 100)}"

        return {
            "externalRef": externalRef,
            "name": name
        }

    @staticmethod
    def change_limit_card(id, newValue):
        return {
            "id": id,
            "newValue": newValue
        }

    @staticmethod
    def change_limit_account(id, newValue):
        return {
            "id": id,
            "newValue": newValue
        }

    @staticmethod
    def create_named_card(personId=None, companyExternalRef=None, typeOfCard=None, phone=None):
        arr = '1234567890'
        cms = ''
        for i in range(9):
            cms = cms + choice(arr)
        if phone is None:
            phone = int('992'+cms)
        return {
            "personId": personId,
            "companyExternalRef": companyExternalRef,
            "panId": 0,
            "type": typeOfCard,
            "phone": phone
        }

    @staticmethod
    def create_instant_bulk(cardType=None, size=None):
        return {
            "cardType": cardType,
            "size": size
        }

    @staticmethod
    def create_instant_card(cardId=None, personId=None, phone=None):
        return {
          "cardId": cardId,
          "personId": personId,
          "phone": phone
        }

    @staticmethod
    def set_pin(cardToken=None, personExternalRef=None, pin=None):
        return {
            "cardToken": cardToken,
            "personExternalRef": personExternalRef,
            "pin": pin
        }

    @staticmethod
    def pan_reserve(pan=None, cardType=None, personExternalRef=None):
        return {
          "pan": pan,
          "cardType": cardType,
          "personExternalRef": personExternalRef
        }

    @staticmethod
    def change_default_account(cardToken=None, accountId=None):
        return {
            "cardToken": cardToken,
            "accountId": accountId
        }

    @staticmethod
    def create_rate(fromCurrency, toCurrency, fromAmount, toAmmount, revFromAmount, revToAmount):
        return {
            "rateGroup": 7,
            "fromCurrency": fromCurrency,
            "toCurrency": toCurrency,
            "fromAmount": fromAmount,
            "toAmount": toAmmount,
            "revFromAmount": revFromAmount,
            "revToAmount": revToAmount,
            "settingDate": f"{strftime('%Y-%m-%d')}",
            "exchangeDate": f"{strftime('%Y-%m-%d')}"
        }

    @staticmethod
    def create_template_message(templateMessage=None, tranCodeId=None, responseCodeId=None):
        return {
            "templateMessage": templateMessage,
            "templateMessageFimiType": [
                {
                    "tranCodeId": tranCodeId,
                    "responseCodeId": responseCodeId
                }
            ]
        }

    @staticmethod
    def edit_template_message(templateMessageId=None, templateMessage=None):
        return {
            "templateMessageId": templateMessageId,
            "templateMessage": templateMessage,
            "templateMessageFimiType": [
                {
                    "tranCodeId": 16,
                    "responseCodeId": 1
                }
            ]
        }

    @staticmethod
    def create_account(cardId=None, personId=None, externalRef=None, currency=None):
        num = '123456789009876545675431919236278264903287264911920321'
        add = ''
        for i in range(18):
            add = add + choice(num)
        if externalRef is not None:
            return {
                "cardId": cardId,
                "personId": personId,
                "defaultCardAccount": {
                    "externalRef": externalRef,
                    "currency": 972
                },
                "additionalAccounts": []
            }
        if currency is not None:
            return {
                "cardId": cardId,
                "personId": personId,
                "defaultCardAccount": {
                    "externalRef": f"{choice(num)}{add}{choice(num)}",
                    "currency": currency
                },
                "additionalAccounts": []
            }

        return {
            "cardId": cardId,
            "personId": personId,
            "defaultCardAccount": {
                "externalRef": f"{choice(num)}{add}{choice(num)}",
                "currency": 972
            },
            "additionalAccounts": [
                {
                    "externalRef": f"{choice(num)}{add}{choice(num)}",
                    "currency": 643
                }
            ]
        }
    @staticmethod
    def create_only_one_account(cardId=None, personId=None):
        num = '12345678900987654321'
        add = ''
        for i in range(18):
            add = add + choice(num)
        currency = choice([972, 643, 840])
        return {
            "cardId": cardId,
            "personId": personId,
            "defaultCardAccount": {
                "externalRef": f"{choice(num)}{add}{choice(num)}",
                "currency": currency
            },
            "additionalAccounts": []
        }

    @staticmethod
    def create_credit(account=None, deferred=None, transactionType=None, amount=None, externalRef=None):
        if externalRef is not None:
            externalRef = externalRef
            return {
                "account": account,
                "amount": amount,
                "externalRef": f"{externalRef}",
                "transactionType": transactionType,
                "deferred": deferred,
                "description": "AUTOTEST BY CREDIT",
                "orderId": 0
            }

        return {
            "account": account,
            "amount": amount,
            "externalRef": f"{uuid.uuid4()}",
            "transactionType": transactionType,
            "deferred": deferred,
            "description": "AUTOTEST BY CREDIT",
            "orderId": 0
        }

    @staticmethod
    def create_debit(account=None, deferred=None, transactionType=None, amount=None, externalRef=None):
        if externalRef is not None:
            externalRef = externalRef
            return {
                "account": account,
                "amount": amount,
                "externalRef": f"{externalRef}",
                "transactionType": transactionType,
                "deferred": deferred,
                "description": "AUTOTEST BY CREDIT",
                "orderId": 0
            }
        return {
            "account": account,
            "amount": amount,
            "externalRef": f"{uuid.uuid4()}",
            "transactionType": transactionType,
            "deferred": deferred,
            "description": "AUTOTEST DEBIT",
            "orderId": 0
        }

    @staticmethod
    def create_credit_by_pan(pan=None, deferred=None, transactionType=None, amount=None, currency=None):
        if amount is None:
            amount = 7
        if currency is None:
            currency = 972

        return {
          "pan": pan,
          "amount": amount,
          "currency": currency,
          "externalRef": f"{uuid.uuid4()}",
          "transactionType": transactionType,
          "deferred": deferred,
          "description": "AUTOTEST CREDIT - BY PAN ",
          "orderId": 0
        }

    @staticmethod
    def create_credit_bulk(firstAccount=None, secondAccount=None):
        return {
            "bulkRqInfo": [
                {
                  "account": firstAccount,
                  "amount": 10,
                  "externalRef": f"{uuid.uuid4()}",
                  "description": "AUTOTEST",
                  "orderId": 0
                },
                {
                  "account": secondAccount,
                  "amount": 10,
                  "externalRef": f"{uuid.uuid4()}",
                  "description": "AUTOTEST",
                  "orderId": 0
                }
            ]
        }

    @staticmethod
    def create_debit_bulk(firstAccount=None, secondAccount=None, firstAmount=None, secondAmount=None):
        return {
            "bulkRqInfo": [
                {
                  "account": firstAccount,
                  "amount": firstAmount,
                  "externalRef": f"{uuid.uuid4()}",
                  "description": "AUTOTEST",
                  "orderId": 0
                },
                {
                  "account": secondAccount,
                  "amount": secondAmount,
                  "externalRef": f"{uuid.uuid4()}",
                  "description": "AUTOTEST",
                  "orderId": 0
                }
            ]
        }

    @staticmethod
    def set_status(accountId=None, status=None):
        return {
          "accountId": accountId,
          "status": status
        }
    @staticmethod
    def change_card_status(cardId=None, status=None, cardToken=None):
        return {
          "cardId": cardId,
          "cardToken": cardToken,
          "status": status,
          "reason": "AUTOTEST",
          "deferred": False
        }

    @staticmethod
    def change_card_fees_status(feeId=None, fromStatus=None, toStatus=None, feeType=None):
        if feeId is None:
            return {
                "fromStatus": fromStatus,
                "toStatus": toStatus,
                "feeType": feeType
            }
        if feeType is None:
            return {
                "id": feeId,
                "fromStatus": fromStatus,
                "toStatus": toStatus
            }

        return {
          "id": feeId,
          "fromStatus": fromStatus,
          "toStatus": toStatus,
          "feeType": feeType
        }

    @staticmethod
    def change_ecom_status(cardToken=None, cardEComStatus=None):
        return {
          "cardToken": cardToken,
          "cardEComStatus": cardEComStatus
        }

    @staticmethod
    def change_cms(cardId=None, cardToken=None, newPhone=None):
        return {
            "cardId": cardId,
            "cardToken": cardToken,
            "newPhone": newPhone,
            "deferred": False
        }
    @staticmethod
    def change_notification_type(cardId=None, cardToken=None, notificationType=None):
        return {
          "cardId": cardId,
          "cardToken": cardToken,
          "notificationType": notificationType
        }

    @staticmethod
    def change_risk_country(cardToken=None, status=None):
        return {
          "cardToken": cardToken,
          "status": status
        }
