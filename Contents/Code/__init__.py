import sys

PLUGIN_NAME = "KitsuScrobble"
ROUTE_BASE = PLUGIN_NAME.lower()

API_CLIENT_ID = "dd031b32d2f56c990b1425efe6c42ad847e7fe3ab46bf1299f05ecd856bdb7dd"  # Temporarily until Kitsu allows proper client registration
API_CLIENT_SECRET = "54d7307928f63414defd96399fc31ba847961ceaecef3a5fd93144e960c0e151"  # Temporarily until Kitsu allows proper client registration
API_AUTHENTICATE_URL = "https://staging.kitsu.io/api/oauth/token"

####################################################################################################
def Start():
    Log.Info("[%s] Starting up." % PLUGIN_NAME)
    Log.Info("[%s] Running on python '%s'." % (PLUGIN_NAME, sys.version))
    
    # Clear user data
    Dict.Reset()
    # Authenticate user
    Authenticate()


####################################################################################################
def ValidatePrefs():
    Log.Info("[%s] Validating preferences." % PLUGIN_NAME)

    return Authenticate()


####################################################################################################
def Authenticate():
    Log.Debug("Attempting Kitsu authentication.")

    if Prefs["username"] and Prefs["password"]:
        try:
            authToken = JSON.ObjectFromURL(API_AUTHENTICATE_URL, values=dict(
                grant_type="password",
                client_id=API_CLIENT_ID,
                client_secret=API_CLIENT_SECRET,
                username=Prefs["username"],
                password=Prefs["password"]))

            Log.Info("[%s] %s" % (PLUGIN_NAME, authToken))

            Dict["logged_in"] = True
            Dict["auth_token"] = authToken
            Log.Info("[%s] Authentication was successful." % PLUGIN_NAME)
            return True
        except Ex.HTTPError, e:
            Dict["logged_in"] = False
            Log.Error("[%s] Authentication failed." % PLUGIN_NAME)
            Log.Error("[%s] %s" % (PLUGIN_NAME, e.content))
        except Exception, e:
            Dict["logged_in"] = False
            Log.Error("[%s] Authentication failed even more." % PLUGIN_NAME)
            Log.Error("[%s] %s" % (PLUGIN_NAME, e))
    return False


####################################################################################################
@handler("/video/%s" % ROUTE_BASE, PLUGIN_NAME)
def MainMenu():
    return ObjectContainer(
        no_cache=True,
        no_history=True,
        objects=[
            DirectoryObject(
                key=Callback(LookupUnmatchedAnime),
                title="Lookup unmatched anime"
            ),
            PrefsObject(title="Preferences")
        ]
    )


####################################################################################################
@route("/video/%s/lookup-unmatched-anime" % ROUTE_BASE)
def LookupUnmatchedAnime():
    r = requests.get(API_AUTHENTICATE_URL)
    Log.Debug(r.status_code)

    if not Dict["logged_in"]:
        return ObjectContainer(header="Login", message="Enter your username and password in the %s preferences" % PLUGIN_NAME)

    # response = JSON.ObjectFromURL(request_url)
    # collection = response["collection"]
    
    # oc = ObjectContainer(title2 = "My Stream")
    # for activity in collection:
    #     origin = activity["origin"]
    #     if not origin["streamable"] or "stream_url" not in origin:
    #         continue
    #     AddTrack(oc, origin)
    
    # if "next_href" in response:
    #     next_href = response["next_href"]

    return ObjectContainer(header="Login Failed", message="Hello")
