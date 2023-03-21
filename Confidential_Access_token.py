import msal
import jwt
import json 
import requests 
import pandas as pd 
from datetime import datetime
import test_app_config as app_config

accessToken = None 
requestHeaders = None 
tokenExpiry = None 
queryResults = None 
graphURI = 'https://graph.microsoft.com'
#latestreg
def msgraph_auth():
    global accessToken
    global requestHeaders
    global tokenExpiry
    tenantID = 'ef690698-ed24-452d-9b9a-32f84e98b437'
    authority = 'https://login.microsoftonline.com/' + tenantID
    clientID = app_config.CLIENT_ID
    clientSecret = app_config.CLIENT_SECRET
    scope = ['https://graph.microsoft.com/.default']

    app = msal.ConfidentialClientApplication(clientID, authority=authority, client_credential = clientSecret)

    try:
        accessToken = app.acquire_token_silent(scope, account=None)
        if not accessToken:
            try:
                accessToken = app.acquire_token_for_client(scopes=scope)
                if accessToken['access_token']:
                    print('New access token retreived....')
                    print(accessToken['access_token'])
                else:
                    print('Error aquiring authorization token. Check your tenantID, clientID and clientSecret.')
            except:
                pass 
        else:
            print('Token retreived from MSAL Cache....')

        decodedAccessToken = jwt.decode(accessToken['access_token'], verify=False)
        accessTokenFormatted = json.dumps(decodedAccessToken, indent=2)
        print('Decoded Access Token')
        print(accessTokenFormatted)

        # Token Expiry
        tokenExpiry = datetime.fromtimestamp(int(decodedAccessToken['exp']))
        print('Token Expires at: ' + str(tokenExpiry))
        return
    except Exception as err:
        print(err)

def msgraph_request(resource,requestHeaders):
    # Request
    results = requests.get(resource, headers=requestHeaders).json()
    return results


# Auth
msgraph_auth()

# Query
queryResults = msgraph_request(graphURI +'/v1.0/users',requestHeaders)

# Results to Dataframe
try:
    df = pd.read_json(json.dumps(queryResults['value']))
    # set ID column as index
    df = df.set_index('id')
    print(str(df['displayName'] + " " + df['mail']))

except:
    print(json.dumps(queryResults, indent=2))