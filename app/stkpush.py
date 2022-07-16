import logging
import time
import math
import base64
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
from rest_framework.response import Response
from phonenumber_field.phonenumber import PhoneNumber
from decouple import config
# from piczangu.settings import env
from .models import *
from .serializer import *

logging = logging.getLogger("default")


class MpesaGateWay:
    shortcode = None
    consumer_key = None
    consumer_secret = None
    access_token_url = None
    access_token = None
    access_token_expiration = None
    checkout_url = None
    timestamp = None

    def __init__(self):
        now = datetime.now()
        self.shortcode = config("shortcode")
        self.consumer_key = config("consumer_key")
        self.consumer_secret = config("consumer_secret")
        self.access_token_url = config("access_token_url")
        self.password = self.generate_password()
        self.c2b_callback = config("c2b_callback")
        self.b2c_queuetimeouturl = config("b2c_queuetimeouturl")
        self.b2c_result = config("b2c_result")
        self.checkout_url = config("checkout_url")
        self.b2c_checkout_url = config("b2c_checkout_url")
        self.security_credential = config("security_credential")

        try:
            self.access_token = self.getAccessToken()
            if self.access_token is None:
                raise Exception("Request for access token failed.")
        except Exception as e:
            logging.error("Error {}".format(e))
        else:
            self.access_token_expiration = time.time() + 3400

    def getAccessToken(self):
        try:
            res = requests.get(
                self.access_token_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
            )
        except Exception as err:
            logging.error("Error {}".format(err))
            raise err
        else:
            token = res.json()["access_token"]
            self.headers = {"Authorization": "Bearer %s" % token}
            return token

    class Decorators:
        @staticmethod
        def refreshToken(decorated):
            def wrapper(gateway, *args, **kwargs):
                if (
                    gateway.access_token_expiration
                    and time.time() > gateway.access_token_expiration
                ):
                    token = gateway.getAccessToken()
                    gateway.access_token = token
                return decorated(gateway, *args, **kwargs)

            return wrapper

    def generate_password(self):
        """Generates mpesa api password using the provided shortcode and passkey"""
        now = datetime.now()
        self.timestamp = now.strftime("%Y%m%d%H%M%S")
        password_str = config("shortcode") + \
            config("pass_key") + self.timestamp
        password_bytes = password_str.encode("ascii")
        return base64.b64encode(password_bytes).decode("utf-8")

    @Decorators.refreshToken
    def stk_push_request(self, payload):
        serializer_class = TransactionSerializer
        request = payload["request"]
        data = payload["data"]
        amount = data["amount"]
        phone_number = data["phone_number"]
        req_data = {
            "BusinessShortCode": self.shortcode,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": math.ceil(float(amount)),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.c2b_callback,
            "AccountReference": "Test",
            "TransactionDesc": "Test",
        }

        res = Transaction.objects.create(requests.post(
            self.checkout_url, json=req_data, headers=self.headers, timeout=30
        ))
        res_data = res.json()
        logging.info("Mpesa request data {}".format(req_data))
        logging.info("Mpesa response info {}".format(res_data))

        if res.ok:
            data["ip"] = request.META.get("REMOTE_ADDR")
            data["checkout_request_id"] = res_data["CheckoutRequestID"]
            res_data.save()
            Transaction.objects.create(**data)
            print(res_data)
        return res_data

    def check_status(self, data):
        try:
            status = data["Body"]["stkCallback"]["ResultCode"]
        except Exception as e:
            logging.error(f"Error: {e}")
            status = 1
        return status

    def get_transaction_object(data):
        checkout_request_id = data
        transaction, _ = Transaction.objects.get_or_create(
            checkout_request_id=checkout_request_id
        )

        return transaction

    def handle_successful_pay(self, data, transaction):
        items = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
        for item in items:
            if item["Name"] == "Amount":
                amount = item["Value"]
            elif item["Name"] == "MpesaReceiptNumber":
                receipt_no = item["Value"]
            elif item["Name"] == "PhoneNumber":
                phone_number = item["Value"]

        transaction.amount = amount
        transaction.phone_number = PhoneNumber(raw_input=phone_number)
        transaction.receipt_no = receipt_no
        transaction.confirmed = True

        return transaction

    def callback_handler(self, data):
        status = self.check_status(data)
        transaction = self.get_transaction_object()
        if status == 0:
            self.handle_successful_pay(data, transaction)
        else:
            transaction.status = 1

        transaction.status = status
        print(transaction)
        transaction.save()

        transaction_data = TransactionSerializer(transaction).data
        print(transaction_data)

        logging.info("Transaction completed info {}".format(transaction_data))

        return Response({"status": "ok", "code": 0}, status=200)

    #! b2c


class MpesaB2CPayment:
    shortcode = None
    consumer_key = None
    consumer_secret = None
    access_token_url = None
    access_token = None
    access_token_expiration = None
    checkout_url = None
    timestamp = None

    def __init__(self):
        now = datetime.now()
        self.shortcode = config("shortcode")
        self.consumer_key = config("consumer_key")
        self.consumer_secret = config("consumer_secret")
        self.access_token_url = config("access_token_url")
        self.password = self.generate_password()
        self.c2b_callback = config("c2b_callback")
        self.b2c_queuetimeouturl = config("b2c_queuetimeouturl")
        self.b2c_result = config("b2c_result")
        self.checkout_url = config("checkout_url")
        self.b2c_checkout_url = config("b2c_checkout_url")
        self.security_credential = config("security_credential")

        try:
            self.access_token = self.getAccessToken()
            if self.access_token is None:
                raise Exception("Request for access token failed.")
        except Exception as e:
            logging.error("Error {}".format(e))
        else:
            self.access_token_expiration = time.time() + 3400

    def getAccessToken(self):
        try:
            res = requests.get(
                self.access_token_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
            )
        except Exception as err:
            logging.error("Error {}".format(err))
            raise err
        else:
            token = res.json()["access_token"]
            self.headers = {"Authorization": "Bearer %s" % token}
            return token

    class Decorators:
        @staticmethod
        def refreshToken(decorated):
            def wrapper(gatewayb, *args, **kwargs):
                if (
                    gatewayb.access_token_expiration
                    and time.time() > gatewayb.access_token_expiration
                ):
                    token = gatewayb.getAccessToken()
                    gatewayb.access_token = token
                return decorated(gatewayb, *args, **kwargs)

            return wrapper

    def generate_password(self):
        """Generates mpesa api password using the provided shortcode and passkey"""
        now = datetime.now()
        self.timestamp = now.strftime("%Y%m%d%H%M%S")
        password_str = config("shortcode") + \
            config("pass_key") + self.timestamp
        password_bytes = password_str.encode("ascii")
        return base64.b64encode(password_bytes).decode("utf-8")

    @Decorators.refreshToken
    def b2c_request(self, payload):
        serializer_class = B2CTransactionSerializer
        request = payload["request"]
        data = payload["data"]
        req_data = {
            "InitiatorNametestapi": "testapi",    
            "SecurityCredential": self.security_credential,
            "CommandID": "BusinessPayment",
            "Amount": 1,
            "PartyA": 600988,
            "PartyB": 254798670839,
            "Remarks": "Test remarks",
            "QueueTimeOutURL": self.b2c_queuetimeouturl,
            "ResultURL": self.b2c_result,
            "Occassion": "null"
        }

        res = B2CTransaction.objects.create(requests.post(
            self.b2c_checkout_url, json=req_data, headers=self.headers, timeout=30
        ))
        res_data = res.json()
        logging.info("Mpesa request data {}".format(req_data))
        logging.info("Mpesa response info {}".format(res_data))

        if res.ok:
            data["ip"] = request.META.get("REMOTE_ADDR")
            data["OriginatorConversationId"] = res_data["OriginatorConversationId"]
            res_data.save()
            B2CTransaction.objects.create(**data)
            print('£******')
            print(res_data)
        return res_data

    def check_status(self, data):
        try:
            status = data["Result"]["ResultParameters"]["ResultCode"]["ResultParameter"]["ReferenceData"]["ReferenceItem"]
        except Exception as e:
            logging.error(f"Error: {e}")
            status = 1
        return status

    def get_b2c_transaction_object(data):
        OriginatorConversationId = data
        transaction, _ = B2CTransaction.objects.get_or_create(
            OriginatorConversationId=OriginatorConversationId
        )

        return transaction

    def handle_successful_b2c_pay(self, data, transaction):
        ResultParameters = data["Result"]["ResultParameters"]["ResultParameter"]["ReferenceData"]["ReferenceItem"]
        for ResultParameter in  ResultParameters:
            if  ResultParameter["Name"] == "TransactionAmount":
                amount =  ResultParameter["Value"]
            elif  ResultParameter["Name"] == "TransactionReceipt":
                receipt_no =  ResultParameter["Value"]
            elif  ResultParameter["Name"] == "ReceiverPartyPublicName":
                ReceiverPartyPublicName =  ResultParameter["Value"]
            elif  ResultParameter["Name"] == "B2CRecipientIsRegisteredCustomer":
                B2CRecipientIsRegisteredCustomer =  ResultParameter["Value"]
            elif  ResultParameter["Name"] == "B2CChargesPaidAccountAvailableFunds":
                B2CChargesPaidAccountAvailableFunds =  ResultParameter["Value"]
            elif  ResultParameter["Name"] == "B2CUtilityAccountAvailableFunds":
                B2CUtilityAccountAvailableFunds =  ResultParameter["Value"]
            elif  ResultParameter["Name"] == "B2CWorkingAccountAvailableFunds":
                B2CWorkingAccountAvailableFunds =  ResultParameter["Value"]
           

        transaction.amount = amount
        transaction.ReceiverPartyPublicName = ReceiverPartyPublicName
        transaction.receipt_no = receipt_no
        transaction.B2CRecipientIsRegisteredCustomer =  B2CRecipientIsRegisteredCustomer   
        transaction.B2CChargesPaidAccountAvailableFunds = B2CChargesPaidAccountAvailableFunds
        transaction.B2CUtilityAccountAvailableFunds  = B2CUtilityAccountAvailableFunds 
        transaction.B2CWorkingAccountAvailableFunds = B2CWorkingAccountAvailableFunds
        transaction.confirmed = True

        return transaction

    def b2c_callback_handler(self, data):
        status = self.check_status(data)
        transaction = self.get_b2c_transaction_object()
        if status == 0:
            self.handle_successful_b2c_pay(data, transaction)
        else:
            transaction.status = 1

        transaction.status = status
        print('***£***')
        print(transaction)
        transaction.save()

        transaction_data = B2CTransactionSerializer(transaction).data
        print('**$****')
        print(transaction_data)

        logging.info("Transaction completed info {}".format(transaction_data))

        return Response({"status": "ok", "code": 0}, status=200)
    