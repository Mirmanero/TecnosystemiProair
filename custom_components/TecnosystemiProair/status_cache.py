import logging
import asyncio
import datetime
from .const import (
    DOMAIN
)

from homeassistant.core import HomeAssistant
from datetime import datetime, timedelta
from .status import Status

_LOGGER = logging.getLogger(__name__)

class Status_Cache():
    def __init__(self,homeassistant:HomeAssistant, status:Status):
        
        self._homeassistant = homeassistant
        self.status = status
        
        self._sensor_states_cache = {}
        self._last_update = datetime.now()
        self._last_login = datetime.now()
        self._sensor_states_cache = {zone.zone_id: zone for zone in status.status_resp.zones}

        homeassistant.loop.create_task(self.update_cache_periodically())

    @property
    def last_cache_update(self):
        return  self._last_update

    async def fetch_and_cache_states(self):
        _LOGGER.debug("Refresh Tecnosystemi")

        try:
            if datetime.now() - self._last_login > timedelta(hours=1):
                _LOGGER.info("new login to tecnosystemi")

                reconnected = await self.status._login.login_to_tecnosistemi()

                if reconnected:
                    self._last_login = datetime.now()
                else:
                    _LOGGER.warning("error re-login to tecnosystemi")

            if await self.status.request_status():
                zones = self.status.status_resp.zones
                #zones = await self._homeassistant.async_add_executor_job(self._myTCSSession.get_zones)
                self._sensor_states_cache = {zone.zone_id: zone for zone in zones}
                _LOGGER.debug(zones[0].temp)

                self._last_update = datetime.now()
            else:
                _LOGGER.debug("Error request Status")
        except:
            _LOGGER.warning(f"Error on periodic status request from Tecnosystemi")

    def get_sensor_state(self,sensor_id,propertyName):
        return getattr(self._sensor_states_cache.get(sensor_id, "Stato sconosciuto"), propertyName, None)
        #return sensor_states_cache.get(sensor_id, "Stato sconosciuto").status

    

    async def update_cache_periodically(self,interval_seconds=120):
        while True:
            #_LOGGER.info("Refresh")
            await self.fetch_and_cache_states()
            await asyncio.sleep(interval_seconds)