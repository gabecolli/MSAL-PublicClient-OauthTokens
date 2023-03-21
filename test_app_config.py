import os


#this  is current in your AADB2C tenant
CLIENT_ID = "fae0de65-3848-4d36-9f93-c6738ac133e7" # Application (client) ID of app registration

CLIENT_SECRET = "dH.8Q~IrNdReGL-axgt9ddmgkvDAtT4fUL5.McWh" # Placeholder - for use ONLY during testing.
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")
#https://kvmma.b2clogin.com/kvmma.onmicrosoft.com/oauth2/v2.0/authorize?p=B2C_1_susi&client_id=7a7c85a1-e1f0-4ffd-86eb-f7125cf9c016&nonce=defaultNonce&redirect_uri=https%3A%2F%2Flocalhost&scope=openid&response_type=code&prompt=login
AUTHORITY = "https://kvmma.b2clogin.com/kvmma.onmicrosoft.com/B2C_1_susi"  # For multi-tenant app

B2C_RESET_PASSWORD_AUTHORITY = "https://kvmma.b2clogin.com/kvmma.onmicrosoft.com/B2C_1_reset"
# AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"

REDIRECT_PATH = "/getAToken"  
SCOPE = []

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session




