import requests
import webbrowser

# Replace your_client_id with your registered application ID.
client_id = "65707857-1b72-4a83-8600-a3c21f96c578"
client_secret =".Pm8Q~ZyPAoEMj2oQdhZtz6EUEEOz_GMrOeD6aUk"
# The authorization URL.
authorization_url = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={client_id}&scope=openid%20profile%20https://ads.microsoft.com/msads.manage%20offline_access&response_type=code&redirect_uri=http://localhost:5000&state=ClientStateGoesHere&prompt=login"

# Open the authorization URL in the default web browser.
webbrowser.open(authorization_url)

# Wait for the user to grant permission and enter the response URI.
code = input("Grant consent in the browser, and then enter the response URI here: ")
code = code.split("=")[-1]

# Get the initial access and refresh tokens.
response = requests.post(
    "https://login.microsoftonline.com/common/oauth2/v2.0/token",
    data={
        "client_id": client_id,
        "client_secret":client_secret,
        "scope": "https://ads.microsoft.com/msads.manage offline_access",
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:5000",
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)

# Check if token retrieval was successful
if response.status_code != 200:
    print("Failed to get tokens. Response status code: ", response.status_code)
    print("Response content: ", response.content)
    exit()

oauth_tokens = response.json()
print("Access token: ", oauth_tokens.get("access_token"))
print("Access token expires in: ", oauth_tokens.get("expires_in"))
print("Refresh token: ", oauth_tokens.get("refresh_token"))

# Use the refresh token to get new access and refresh tokens.
response = requests.post(
    "https://login.microsoftonline.com/common/oauth2/v2.0/token",
    data={
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://ads.microsoft.com/msads.manage offline_access",
        "grant_type": "refresh_token",
        "refresh_token": oauth_tokens["refresh_token"],
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)

# Check if token refresh was successful
if response.status_code != 200:
    print("Failed to refresh tokens. Response status code: ", response.status_code)
    print("Response content: ", response.content)
    exit()

oauth_tokens = response.json()
print("New Access token: ", oauth_tokens["access_token"])
print("New Access token expires in: ", oauth_tokens["expires_in"])
