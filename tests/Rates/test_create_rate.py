from random import choice
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from config.config_url import CREATE_RATE_URL
from statuses import statusCode, cardCurrency


class TestCreateRate(BaseCase):
    from_currency = choice([cardCurrency.RUB, cardCurrency.USD])
    from_amount, to_amount, rev_from_amount, rev_to_amount = None, None, None, None
    if from_currency == cardCurrency.USD:
        from_amount = 1
        to_amount = 11.11
        rev_from_amount = 11
        rev_to_amount = 1
    if from_currency == cardCurrency.RUB:
        from_amount = 1
        to_amount = 0.14
        rev_from_amount = 0.15
        rev_to_amount = 1

    def test_create_rate(self):
        data = self.create_rate(
            fromCurrency=self.from_currency,
            toCurrency=cardCurrency.TJS,
            fromAmount=self.from_amount,
            toAmmount=self.to_amount,
            revFromAmount=self.rev_from_amount,
            revToAmount=self.rev_to_amount
        )
        rate_response = MyRequests.post(url=CREATE_RATE_URL, data=data)

        Assertions.assert_status_code_and_message(rate_response, statusCode.APPROVED, 'Approved')
        Assertions.json_has_keys_in_payload(rate_response,
                                            keyInPayload='rates',
                                            names=[
                                                'rateGroup',
                                                'fromCurrency',
                                                'toCurrency',
                                                'fromAmount',
                                                'toAmount']
                                            )
