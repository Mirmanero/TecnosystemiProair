import base64
import requests
import json
from datetime import datetime
from .login import Login  
import aiohttp
import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

class Status:
    STATUS_URL = "https://proair.azurewebsites.net/api/v1/GetCUState?cuSerial=414309111391&PIN=2909"
    
    def __init__(self, login:Login):
        self.login_user = "mirmanero@gmail.com"
        self.login_password = "PwdProAir"
        self.status_resp = None
        self._login = login
    
    class StatusResp:
        def __init__(self, data):
            self.zones = [Status.StatusZone(zone) for zone in data.get("Zones", [])]
            self.errors = data.get("Errors", 0)
            self.serial = data.get("Serial", "")
            self.name = data.get("Name", "")
            self.fw_ver = data.get("FWVer", "")
            self.is_off = data.get("IsOFF", False)
            self.is_cooling = data.get("IsCooling", False)
            self.operating_mode_cooling = data.get("OperatingModeCooling", 0)
            self.last_config_update = datetime.fromisoformat(data.get("LastConfigUpdate", "1970-01-01T00:00:00"))
            self.last_sync_update = datetime.fromisoformat(data.get("LastSyncUpdate", "1970-01-01T00:00:00"))
            self.num_errors = data.get("NumErrors", 0)
            self.icon = data.get("Icon", 0)
            self.ir_present = data.get("IrPresent", 0)
            self.temp_can = data.get("TempCan", 0)
            self.ip = data.get("IP", "")
            self.f_inv = data.get("FInv", 0)
            self.f_est = data.get("FEst", 0)
    
    class StatusZone:
        def __init__(self, data):
            self.zone_id = data.get("ZoneId", 0)
            self.name = data.get("Name", "")
            self.is_master = data.get("IsMaster", False)
            self.is_off = data.get("IsOFF", False)
            self.temp = data.get("Temp", "")
            self.set_temp = data.get("SetTemp", "")
            self.serranda = data.get("Serranda", 0)
            self.serranda_set = data.get("SerrandaSet", 0)
            self.fancoil = data.get("Fancoil", 0)
            self.fancoil_set = data.get("FancoilSet", 0)
            self.ev = data.get("EV", 0)
            self.is_crono_mode = data.get("IsCronoMode", False)
            self.is_crono_active = data.get("IsCronoActive", False)
            self.errors = data.get("Errors", 0)
            self.umd = data.get("Umd", "")
            self.set_umd = data.get("SetUmd", "")
            self.c_win = data.get("CWin", 0)
            self.c_badge = data.get("CBadge", 0)
            self.c_off = data.get("COff", False)
    
    async def request_status(self):
        try:
            headers = {
                "token": self._login.next_token(),
                "Accept": "*/*",
                "Host": "proair.azurewebsites.net",
                "Authorization": "Basic " + base64.b64encode(f"{self.login_user}:{self.login_password}".encode()).decode()
            }
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.STATUS_URL, headers=headers) as response:
                        if response.status == 200:
                            _LOGGER.debug("risposta 200!!")
                            self.status_resp = self.StatusResp(await response.json())
                            return True
                        else:
                            _LOGGER.error(f"Errore recupero degli stati: {response.status}")
                            return False
            except Exception as e:
                _LOGGER.error(f"Errore recupero degli stati: {e}")
                return False


            
        except Exception:
            pass
        return False

