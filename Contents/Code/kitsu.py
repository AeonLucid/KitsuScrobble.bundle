import urllib
# Use boolean 'Dict["logged_in"]' to check if the user is currently signed into Kitsu.

class KitsuApi:
    def __init__(self, api_url, api_oauth_url, api_client_id, api_client_secret):
        self.api_url = api_url
        self.api_oauth_url = api_oauth_url
        self.api_client_id = api_client_id
        self.api_client_secret = api_client_secret
        self.access_token = None

    # Sets the access_token used by requests that require authentication.
    def set_token(self, access_token):
        self.access_token = access_token

    # A valid authentication request returns a dictionary with:
    # - access_token
    # - refresh_token
    # - created_at
    # - expires_in
    # - token_type (bearer)
    # - scope (public)
    def authenticate(self, username, password):
        return JSON.ObjectFromURL("%s/token" % self.api_oauth_url, values=dict(
                grant_type="password",
                client_id=self.api_client_id,
                client_secret=self.api_client_secret,
                username=username,
                password=password))

    # A valid refresh request returns a dictionary with:
    # - access_token
    # - refresh_token
    # - created_at
    # - expires_in
    # - token_type (bearer)
    # - scope (public)
    def authenticate_refresh(self, refresh_token):
        return JSON.ObjectFromURL("%s/token" % self.api_oauth_url, values=dict(
                grant_type="refresh_token",
                refresh_token=refresh_token))

    def get_current_user(self):
        return JSON.ObjectFromURL("%s/users?filter[self]" % self.api_url, headers=dict(
            Accept="application/vnd.api+json",
            Authorization="Bearer %s" % self.access_token
        ))

    def lookup_anime(self, tvdb_season, title):
        headers=dict(Accept="application/vnd.api+json")
        matched = None
        # Anime has a tvdb id
        if tvdb_season:
            mapping = JSON.ObjectFromURL("%s/mappings?filter[externalSite]=thetvdb/season&filter[externalId]=%s" % (self.api_url, tvdb_season), headers=headers)["data"][0]
            # Mapping to tvdb exists in Kitsu database
            if mapping:
                matched = JSON.ObjectFromURL(mapping["relationships"]["media"]["links"]["related"], headers=headers)["data"]
                # matched = JSON.ObjectFromURL("%s/anime/%s" % (self.api_url, mapping["id"]), headers=headers)["data"]
        # Search by Anime title
        results = JSON.ObjectFromURL("%s/anime?filter[text]=%s" % (self.api_url, urllib.quote(title)), headers=headers)["data"]
        # Filter matched Anime from search results
        if matched is not None:
            for result in results:
                if result["id"] == matched["id"]:
                    results.remove(result)
                    break
            results = [matched] + results
        return results

class KitsuError(Exception):
    pass
