##Public_Access_Token.py

intended for mobile app development where you cannot 
store an application secret. This will acquire a token interactively by opening a browser
and prompting the user to login. 
Be sure to use the B2C authority endpoint if you are getting tokens for B2C USER access. if using the 
`https://login.microsoftonline.com/{tenantID}` this is going to acquire tokens from an administrative context.
For example if you sign up a user into B2C using the SUSI userflow with an *@gmail* or other email provider 
and attempt to acquire a token for that user using this endpoint it will fail. 

###In reference to scopes
be sure to add the required scopes you want the token to be able to access to your app registration
if you are wanting to access your APIs that are not protected by AAD B2C by default you will need to 
1. create an app registration for your API
2. expose the API under App registration and create an APP-ID URI for your API
3. add the desired scopes for your API. these are defined by you. If for example your using a graph API you need to follow that scheme. 
4. when requesting a token for the desired scopes to your API you will need to inlcude that in your request in the format of ['https://{B2Chostname}.onmicrosoft.com/{api-app-id}/your.scope']. be sure this is a DataType List even if its only a single value. 

Lastly be sure to specify a port in your acquire_token_interactively method. `http://localhost` is hard coded into the MSAL library but a port is not specified. meaning it will simply choose a system available port. This port that you define needs to be specified as your redirect URI in your app registration as `http://localhost:{port_num}`

##ConfidentialClientApplication Class 
this is similiar, however there are some differences. The main being the use of the Client Secret to authenticate your app to AAD and using different flows. 
This use case works well for Web Application where you can securely store the Client Secret. **DO NOT HARD CODE THE SECRET.** Store it as an ENV variable at a minimum but the use of managed identities and Azure Key Vault is recommended. 