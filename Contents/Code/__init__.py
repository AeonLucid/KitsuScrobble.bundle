PLUGIN_NAME = "HBScrobbler"
ROUTE_BASE = PLUGIN_NAME.lower()

API_AUTHENTICATE_URL = "http://hummingbird.me/api/v1/users/authenticate"

####################################################################################################
def Start():
    Log.Info("[%s] Starting up." % PLUGIN_NAME)

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
    Log.Debug("Attempting HummingBird authentication.")

    if Prefs["username"] and Prefs["password"]:
        try:
            authToken = JSON.ObjectFromURL(API_AUTHENTICATE_URL, values=dict(
                username=Prefs["username"],
                password=Prefs["password"]))

            Dict["logged_in"] = True
            Dict["auth_token"] = authToken
            Log.Info("[%s] Authentication was successful." % PLUGIN_NAME)
            return True
        except Ex.HTTPError, e:
            Dict["logged_in"] = False
            Log.Error("[%s] %s" % (PLUGIN_NAME, e.content))
            Log.Error("[%s] Authentication failed." % PLUGIN_NAME)
        except:
            Dict["logged_in"] = False
            Log.Error("[%s] Authentication failed." % PLUGIN_NAME)
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


@route("/video/%s/lookup-unmatched-anime" % ROUTE_BASE)
def LookupUnmatchedAnime():
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
