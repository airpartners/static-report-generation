import json
import requests

def refreshToken():
    with open('token.json', 'r') as f:
        creds = json.load(f)
    
    params = {
            "grant_type": "refresh_token",
            "client_id": creds["client_id"],
            "client_secret": creds["client_secret"],
            "refresh_token": creds["refresh_token"]
    }

    authorization_url = "https://oauth2.googleapis.com/token"

    r = requests.post(authorization_url, data=params)

    if r.ok:
        print(r.json())

        creds['token'] = r.json()['access_token']

        with open('token.json', 'w') as f:
            json.dump(creds, f)
        
        return 1
    else:
        return 0

if __name__=="__main__":
    refreshToken()