import base64
import json
import requests
from string_helpers import StringHelpers  # Assumendo che la classe sia in un file separato

class Login:
    def __init__(self, key):
        self.login_token = "Ga5mM61KCm5Bk18lhD5J999jC2Mu0Vaf"
        self.login_user = "UsrProAir"
        self.login_password = "PwdProAir"
        self.login_url = "https://proair.azurewebsites.net/api/v1/Login"

        self.crypt = StringHelpers(key)
        self.token = None

        self.login_req = {
            "DeviceId": "1a1636b1dca6c12b",
            "Platform": "gcm",
            "Password": "GwpjZAa0M3BoLDWuNHXh8A==", #è la password cryptata con string helper
            "TokenPush": "dbveVlO_xJE:APA91bG9-fvgrUjdQL4aTbN4-BLXANsVQ3KK6Bn81ZU53EJF2VsbEzDL8lpBb9BBo2hkWjMFECmNPFa9zWtzO0opLQ9aEVldIoZrVNi0T35P4A8nM0f53nhB83GbwoM4J-NLAciGjDp-",
            "Username": "mirmanero@gmail.com"
        }

        self.login_resp = None

    def next_token(self):
        decoded_token = self.crypt.decrypt(self.token)
        last_num = int(decoded_token[-4:])
        new_decoded_token = decoded_token[:-4] + str(last_num + 1)
        new_encoded_token = self.crypt.encrypt(new_decoded_token)
        self.token = new_encoded_token
        return new_encoded_token

    def login_to_tecnosistemi(self):
        try:
            headers = {
                "token": self.login_token,
                "Authorization": "Basic " + base64.b64encode(f"{self.login_user}:{self.login_password}".encode()).decode(),
                "Content-Type": "application/json",
                "Accept": "*/*"
            }

            response = requests.post(self.login_url, headers=headers, json=self.login_req)

            if response.status_code == 200:
                self.login_resp = response.json()
                self.token = self.login_resp.get("Token")
                return True

            return False
        except Exception as e:
            print(f"Errore durante il login: {e}")
            return False
