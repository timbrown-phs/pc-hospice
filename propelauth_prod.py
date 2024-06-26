from propelauth_py import init_base_auth, UnauthorizedException
from streamlit.web.server.websocket_headers import _get_websocket_headers

class Auth:
    def __init__(self, auth_url, integration_api_key):
        self.auth = init_base_auth(auth_url, integration_api_key)
        self.auth_url = auth_url

    def get_user(self):
        access_token = get_access_token()

        if not access_token:
            return None

        try:
            # print("Got Token")
            return self.auth.validate_access_token_and_get_user("Bearer " + access_token)
        except UnauthorizedException as err:
            print("Error validating access token", err)
            return None

    def get_account_url(self):
        return self.auth_url + "/account"

    def get_logout_url(self):
        return self.auth_url + "/auth/logout"

def get_access_token():
    headers = _get_websocket_headers()

    if headers is None:
        return None

    cookies = headers.get("Cookie") or headers.get("cookie") or ""
    # print(cookies)
    for cookie in cookies.split(";"):
        split_cookie = cookie.split("=")
        # print(split_cookie)
        if len(split_cookie) == 2 and split_cookie[0].strip() == "__pa_at":
            return split_cookie[1].strip()

    return None

# Configuration, please edit
auth = Auth(
    "https://auth.predictivehealthsolutions.co",
    "b62cc0767b4c82a66ed82ad941b14f19499b84384d14d16952420c70f35ea597b0eef010882f4a657a73090b563a4bcd"
)
