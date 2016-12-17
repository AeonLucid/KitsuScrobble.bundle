import sys
import time
from kitsu import KitsuApi

PLUGIN_NAME = "KitsuScrobble"
ROUTE_BASE = PLUGIN_NAME.lower()

REFRESH_TOKEN_OFFSET_SECONDS = 3600

# Temporarily until Kitsu allows proper client registration
Kitsu = KitsuApi("https://kitsu.io/api/edge",
                 "https://kitsu.io/api/oauth",
                 "dd031b32d2f56c990b1425efe6c42ad847e7fe3ab46bf1299f05ecd856bdb7dd",
                 "54d7307928f63414defd96399fc31ba847961ceaecef3a5fd93144e960c0e151")

####################################################################################################
def Start():
    Log.Info("[%s] Starting up." % PLUGIN_NAME)
    Log.Info("[%s] Running on python '%s'." % (PLUGIN_NAME, sys.version))

    # Make sure that the user is authenticated if previ
    # ous credentials were known.
    # If this is true, start the background process
    Authenticate()


####################################################################################################
def ValidatePrefs():
    Log.Info("[%s] Validating preferences." % PLUGIN_NAME)

    # If this is true, start the background process if not yet started
    # If this is false, stop the background process if it was started
    return Authenticate(force_reauth=True)


####################################################################################################
def Authenticate(force_reauth=False):
    Log.Debug("[%s] Attempting Kitsu authentication." % PLUGIN_NAME)

    if Prefs["username"] and Prefs["password"]:
        try:
            # Was never logged in.
            if force_reauth or "logged_in" in Dict and not Dict["logged_in"]:
                Log.Debug("[%s] Attempting Kitsu authentication by using the username and password." % PLUGIN_NAME)
                authData = Kitsu.authenticate(Prefs["username"], Prefs["password"])
            # Access token expired.
            elif "logged_in" in Dict and "auth_data" in Dict and Dict["logged_in"] \
                    and Dict["auth_data"]["created_at"] + Dict["auth_data"]["expires_in"] - REFRESH_TOKEN_OFFSET_SECONDS <= time.time():
                Log.Debug("[%s] Attempting Kitsu reauthentication by using the refresh token." % PLUGIN_NAME)
                authData = Kitsu.authenticate_refresh(Dict["auth_data"]["refresh_token"])
            # Already authenticated.
            else:
                Kitsu.set_token(Dict["auth_data"]["access_token"])
                Log.Debug("[%s] User is already authenticated." % PLUGIN_NAME)
                return True

            Kitsu.set_token(authData["access_token"])

            userData = Kitsu.get_current_user()

            Dict["logged_in"] = True
            Dict["auth_data"] = authData
            Dict["user_data"] = dict(
                id=userData["data"][0]["id"],
                name=userData["data"][0]["attributes"]["name"],
            )

            Log.Info("[%s] Authentication was successful." % PLUGIN_NAME)
            return True
        except Ex.HTTPError, e:
            Log.Error("[%s] Authentication failed." % PLUGIN_NAME)
            Log.Error("[%s] %s" % (PLUGIN_NAME, e.content))
        except Exception, e:
            Log.Error("[%s] Authentication failed even more." % PLUGIN_NAME)
            Log.Error("[%s] %s" % (PLUGIN_NAME, e))

        Dict["logged_in"] = False
        Dict["auth_data"] = None
        Dict["user_data"] = None
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
    # r = requests.get(API_AUTHENTICATE_URL)
    # Log.Debug(r.status_code)

    if not Dict["logged_in"]:
        return ObjectContainer(header="Login", message="Enter your username and password in the %s preferences" % PLUGIN_NAME)

    # results = Kitsu.lookup_anime(None, 'Cowboy Bebop')
    # for result in results:
    #     Log.Info(result["attributes"]["canonicalTitle"])
    # results = Kitsu.lookup_anime(31628, 'Code Geass: Lelouch of the Rebellion Season 2')
    # for result in results:
    #     Log.Info(result["attributes"]["canonicalTitle"])
    # results = Kitsu.lookup_anime(17760, 'Code Geass: Lelouch of the Rebellion')
    # for result in results:
    #     Log.Info(result["attributes"]["canonicalTitle"])

    return ObjectContainer(header="Login Failed", message="Hello")
