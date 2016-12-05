PLUGIN_NAME = "HummingBirdScrobbler"

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
    Log.Debug("Attempting HummingBird authentication")

    if Prefs['username'] and Prefs['password']:
        try:
            authToken = JSON.ObjectFromURL(API_AUTHENTICATE_URL, values=dict(
                username=Prefs['username'],
                password=Prefs['password']))

            Dict['logged_in'] = True
            Dict['auth_token'] = authToken
            Log.Info("[%s] Authentication was successful." % PLUGIN_NAME)
            return True
        except Ex.HTTPError, e:
            Dict['logged_in'] = False
            Log.Error("[%s] %s" % (PLUGIN_NAME, e.content))
            Log.Error("[%s] Authentication failed." % PLUGIN_NAME)
        except:
            Dict['logged_in'] = False
            Log.Error("[%s] Authentication failed." % PLUGIN_NAME)
    return False


####################################################################################################
@handler('/video/hummingbirdscrobbler', PLUGIN_NAME)
def MainMenu():
    oc = ObjectContainer(no_cache=True)
    oc.add(PrefsObject(title="Preferences"))
    return oc
