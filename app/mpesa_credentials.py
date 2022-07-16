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
    SecurityCredential="c0YghxRzS5emWWrU51pLL4qmeJCU5kbPzpn91NDnUO2gIp04ARiKBoLf9kSdZsodhs3fXJqDkl4VzHwkVhGAXplAWe76TlQvjRtXRDd0kxx65oEB54ZJc0jJ/JV5Vc46s6LRY/eKcGCMqc7UO05bW7bApQTbbJIPLNpk8w6gSIIgJMCv2m4TYFmYZ1d0Qrcf20nw/GY/x+QLGLlX7/br8SvzaLFKamZ2SfYI5/F4sMkiSi/TgFnSbRsFU3nSbBjA6dCcevAa8yFZb++YsnSJgHx3NvmQnFXrFIjheqaZDsHOyZR+35u7A8ODkhfuluH+qcY5xuDvacuXQZMxkMGAgA=="
    callback_url ='https://a3c7-41-90-185-245.in.ngrok.io/callback'
    access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'