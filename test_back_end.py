import requests 
import test_app_config as app_config
url = "https://kvmma.b2clogin.com/kvmma.onmicrosoft.com/oauth2/v2.0/authorize?p=b2c_1_susi"

body = {
    "grant_type": "implicit",
    "client_id" : app_config.CLIENT_ID
}

response = requests.get(url=url, data=body)
