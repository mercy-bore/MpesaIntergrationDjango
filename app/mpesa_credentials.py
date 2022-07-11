import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
class MpesaC2bCredential:
    consumer_key = 'JnHLddwQJBWIJ83GHePJ5irqNNqJ6Rjt'
    consumer_secret = 'cBc2TJOtQLD0zH3F'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL,
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
class LipanaMpesaPpassword:
    now = datetime.now()
    lipa_time = now.strftime('%Y%m%d%H%M%S')
    Business_short_code = "174379"
    Test_c2b_shortcode = "600344"
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')
    SecurityCredential= "l0SibbbSZXfy7/E3tdd5yq3V9ac8y1je+eHubrz5uPZL56CjE96Hg4thHhjs9DUd1K10bbeM222RPYx4fGCDyKDa5sAuo1EA7dHD7vy8NkVnZv4aJ7OL5HKRNUQpAP50fuI9I7sVs9wwbammjYzw0UvHHFrxfa7fjBDpAQ6Sa43bqmwsWgRquWyqDiCcgtkjg3HIIwJXcMZgGo1Je6HdUI1xw4bgu62dg+Zlvudft7pEcdJrCYPqzT3Z+IkbFZV0kkCthdVulCvkvyIc1mHsZqLOaNz+wRW2EhPCh9lXxOrJKgg5qoNut87VIdOpvAnZ3+Aju6ulumFZwZnBJpj8NQ==ss"
    callback_url ='https://4b6d-41-90-187-177.in.ngrok.io/callback'
    access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'