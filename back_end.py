
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
import msal
import app_config_b2c as app_config
import requests




# session is a variable because of the Session object that receives the app as input
#the session variable is a dictionary stored wherever you define it... on the application server 
# you define where it is stored with the SESSION_TYPE...which is located in our config file "app_config_b2c as app_config"
#this configuration is passed to your application on line 13
app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route("/")
def index():  #this is the landing page of our app
    if not session.get("user"):  #this is going to check the session object and see if there is a value for the key "user" basically check if someone is logged in
        return redirect(url_for("login")) #if no one is logged in takes us to the login route
    token = _get_token_from_cache(app_config.SCOPE)
    return render_template('index.html', user=session["user"], version=msal.__version__, token=token)

@app.route("/login")
def login():
    #print(session["flow"]["auth_uri"])
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE) #going to add a value to the "flow" key using the function _build_auth_code_flow and pass in the values from our app config   SCOPES. go to line 84 for the function
    #print(session)
    print(session["flow"]["auth_uri"])
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD  appends /getatoken to your route
def authorized():
    try:
        cache = _load_cache()  #uses data from your session and creates new object
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(  #this returns your token based on your login info because of this method...go to line 115 for description
            session.get("flow", {}), request.args) #this is where it gets your token. in form of a dictionary
        #result will use buildmsalapp function and take that output and apply the  acquire token by auth code flow method with session.get {flow} and request.args as arguments
        #request.args contains an immutable dictionary with a token and objectid for identification
        if "error" in result:  #if you dont have token and get error. 
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims") #these are the claims you defined in your user flow in AAD B2C
        
        _save_cache(cache)
        
        
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    return redirect(url_for("index"))  #takes us to the home page once logged in. go to line 23

@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

@app.route("/graphcall")
def graphcall():
    #your token is stored in the cache 
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    
    #bear_token = token["id_token"]
   
    return render_template('display.html', result=token)

#TODO review this function and source code
def _load_cache():
    cache = msal.SerializableTokenCache()
    
    if session.get("token_cache"):
        
        cache.deserialize(session["token_cache"])
        
    
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None, authority=None): #welcome back you now have the info for authentication in an object go back to line 84 function
    return msal.ConfidentialClientApplication( #return a MSAL function to get our identity and token info using client ID, Client Secret and authority from our app config which is just the login page for our app. go to that file to line 24
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _build_auth_code_flow(authority=None, scopes=None): #if there is a scope or authority pass in as input to the _build_msal_app function go to line 79
    return _build_msal_app(authority=authority).initiate_auth_code_flow(  #this method is a method of the object that gets passed into the ConfidentialClientApplication object. Basicaically initiates our flow based on our authorized claims
        scopes or [],
        redirect_uri=url_for("authorized", _external=True))  #redirects us to our authorized route go to line 37

def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result

app.jinja_env.globals.update(_build_auth_code_flow=_build_auth_code_flow)  # Used in template











if __name__ == "__main__":
    app.run(host='localhost',port=5006,debug=True)