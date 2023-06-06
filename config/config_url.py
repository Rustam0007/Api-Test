from config.DB_config import URL

# Person
CREATE_PERSON_URL = f"{URL}/api/Person"

# Card
CREATE_NAMED_CARD_URL = f"{URL}/api/Card/Named"
CHANGE_CARD_STATUS_URL = f"{URL}/api/Card/ChangeStatus"
CHANGE_ECOM_STATUS_URL = f"{URL}/api/Card/ChangeEComStatus"
CHANGE_CARD_CMS_URL = f"{URL}/api/Card/ChangeCmsAbonent"
SET_PIN_URL = f"{URL}/api/Card/SetPin"
CHANGE_DEFAULT_ACCOUNT_URL = f"{URL}/api/Card/Account/ChangeDefault"
CREATE_INSTANT_BULK_URL = f"{URL}/api/Card/Instant/Bulk"
CREATE_INSTANT_CARD_URL = f"{URL}/api/Card/Instant"
PAN_RESERVE_URL = f"{URL}/api/Card/Pan/Reserve"
CHANGE_NOTIFICATION_TYPE = f"{URL}/api/Card/ChangeNotificationType"
CHANGE_RISK_COUNTRY_USAGE = f"{URL}/api/Card/ChangeRiskCountryUsage"

# Account
CREATE_ACCOUNT_URL = f"{URL}/api/Account"
CREATE_DEBIT_URL = f"{URL}/api/Account/Debit"
CREATE_CREDIT_URL = f"{URL}/api/Account/Credit"
CREATE_CREDIT_BY_PAN_URL = f"{URL}/api/Account/CreditByPan"
CREATE_CREDIT_BULK_URL = f"{URL}/api/Account/Credit/Bulk"
CREATE_DEBIT_BULK_URL = f"{URL}/api/Account/Debit/Bulk"
SET_STATUS_URL = f"{URL}/api/Account/SetStatus"

# Company
CREATE_COMPANY_URL = f"{URL}/api/Company"
CHANGE_COMPANY_URL = f"{URL}/api/Company/Change"
CHANGE_LIMIT_CARD_URL = f"{URL}/api/Company/LimitCard/Change"
CHANGE_LIMIT_ACCOUNT_URL = f"{URL}/api/Company/LimitAccount/Change"

# Card fees
CHANGE_CARD_FEES_STATUS = f"{URL}/api/CardFees/ChangeStatus"
CALCULATE_CARD_FEES = f"{URL}/api/CardFees/Calculate"


# Rate
CREATE_RATE_URL = f"{URL}/api/Rates/Add"

# Template Message
CREATE_TEMPLATE_MESSAGE_URL = f"{URL}/api/TemplateMessage/Create"
EDIT_TEMPLATE_MESSAGE_URL = f"{URL}/api/TemplateMessage/Edit"
DELETE_TEMPLATE_MESSAGE_URL = f"{URL}/api/TemplateMessage/Delete"
