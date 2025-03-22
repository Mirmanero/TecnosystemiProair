import base64
import json
import aiohttp
import asyncio
import logging
from .string_helpers import StringHelpers  # Assumendo che la classe sia in un file separato

_LOGGER = logging.getLogger(__name__)

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

    async def login_to_tecnosistemi(self):
        _LOGGER.info("login to Tecnosystemi")

        headers = {
            "token": self.login_token,
            "Authorization": "Basic " + base64.b64encode(f"{self.login_user}:{self.login_password}".encode()).decode(),
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.login_url, headers=headers, json=self.login_req) as response:
                    if response.status == 200:
                        self.login_resp = await response.json()
                        _LOGGER.info("response 200")
                        _LOGGER.info(self.login_resp)
                        self.token = self.login_resp.get("Token")
                        return True
                    else:
                        _LOGGER.error(f"response error {response.status}")
                        return False

        except Exception as e:
            _LOGGER.error(f"Errore durante il login: {e}")
            return False