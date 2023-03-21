import msal
import requests
import test_app_config as app_config
# Set up authentication parameters


tenantID = 'TENANTID'
#TODO authority = 'https://login.microsoftonline.com/' + tenantID
authority = 'https://{b2chostname}a.b2clogin.com/{B2CHOSTNAME}.onmicrosoft.com/{B2c policy name}'



client_id = "Client ID"
scope = ['https://{B2Chostname}.onmicrosoft.com/api-app-id/test.scope']  #this scope was defined in the app registration. Under expose an API
#the scope is arbitrary and can be anything. It is used to define the permissions of the app registration.
#if it was a pre built API like graph the scope cannot be arbitrary and must be one of the scopes defined in the API

# Initialize MSAL public client application
app = msal.PublicClientApplication(client_id=client_id, authority=authority,validate_authority=False)

# Use interactive authentication flow to get user access token
result = app.acquire_token_interactive(scopes=scope,port=5006)
#print(msal.oauth2cli.oidc.Client.obtain_token_by_browser())
print(result)

