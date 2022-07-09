import logging
import time
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
from piczangu.settings import env
import environ
from decouple import config
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword

env = environ.Env()
logging = logging.getLogger("default")

class MpesaGateWay:
    shortcode = 174379
    consumer_key = None
    consumer_secret = None
    access_token_url = None
    access_token = None
    access_token_expiration = None

    def __init__(self):
        now = datetime.now()
        self.shortcode = LipanaMpesaPpassword.Business_short_code
        self.consumer_key = config("consumer_key")
        self.consumer_secret = config("consumer_secret")
        self.access_token_url = config("access_token_url")

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