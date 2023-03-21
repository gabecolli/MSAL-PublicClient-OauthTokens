import msal
import requests
import test_app_config as app_config
# Set up authentication parameters
tenantID = 'ef690698-ed24-452d-9b9a-32f84e98b437'
authority = 'https://login.microsoftonline.com/' + tenantID
client_id = "f4e9f9d4-3959-4e2f-a198-e3f952124faa"
scope = ['https://kvmma.onmicrosoft.com/api-app-id/test.scope']

# Initialize MSAL public client application
app = msal.PublicClientApplication(client_id=client_id, authority=authority)

# Use interactive authentication flow to get user access token
result = app.acquire_token_interactive(scopes=scope)
print(result)