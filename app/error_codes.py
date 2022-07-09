from enum import Enum

class PaymentErrorCode(Enum):
    INVALID = "invalid_phone"
    PAYMENT_ERROR = "payment_error"
class ValidationError(Enum):
    INVALID = "invalid_phone"
    PaymentErrorCode = "payment Error"
