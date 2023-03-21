import msal
import requests
import test_app_config as app_config
# Set up authentication parameters


tenantID = 'ef690698-ed24-452d-9b9a-32f84e98b437'
#TODO authority = 'https://login.microsoftonline.com/' + tenantID
authority = 'https://kvmma.b2clogin.com/kvmma.onmicrosoft.com/B2C_1_susi'

client_id = "f4e9f9d4-3959-4e2f-a198-e3f952124faa"
scope = ['https://kvmma.onmicrosoft.com/api-app-id/test.scope']  #this scope was defined in the app registration. Under expose an API
#the scope is arbitrary and can be anything. It is used to define the permissions of the app registration.
#if it was a pre built API like graph the scope cannot be arbitrary and must be one of the scopes defined in the API

# Initialize MSAL public client application
app = msal.PublicClientApplication(client_id=client_id, authority=authority,validate_authority=False)

# Use interactive authentication flow to get user access token
result = app.acquire_token_interactive(scopes=scope,port=5006)
#print(msal.oauth2cli.oidc.Client.obtain_token_by_browser())
print(result)

