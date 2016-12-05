PLUGIN_NAME = "HummingBirdScrobbler"


def Start():
    Log.Info("[%s] Starting HummingBirdScrobbler." % PLUGIN_NAME)


def ValidatePrefs():
    Log.Info("[%s] Nothing to validate for HummingBirdScrobbler" % PLUGIN_NAME)


####################################################################################################
@handler('/video/hummingbirdscrobbler', PLUGIN_NAME)
def MainMenu():
    oc = ObjectContainer(no_cache=True)
    oc.add(PrefsObject(title="Preferences"))
    return oc
