import logging
import asyncio
import datetime
from .const import (
    DOMAIN
)

from homeassistant.core import HomeAssistant
from datetime import datetime, timedelta

_LOGGER = logging.getLogger(__name__)

class Status_Cache():
    def __init__(self,homeassistant:HomeAssistant, myTCSSession):
        
        self._homeassistant = homeassistant
        self._myTCSSession = myTCSSession
        
        self._sensor_states_cache = {}
        self._program_states_cache = {}
        self._last_update = datetime.now() - timedelta(days=1)

        homeassistant.loop.create_task(self.update_cache_periodically())

    @property
    def last_cache_update(self):
        return  self._last_update

    async def fetch_and_cache_states(self):
        #_LOGGER.info("Refresh")
        try:
            #zones = await self._homeassistant.async_add_executor_job(self._myTCSSession.get_zones)
            #self._sensor_states_cache = {zone.idx: zone for zone in zones.root}

            #programs = await self._homeassistant.async_add_executor_job(self._myTCSSession.get_programs)
            #self._program_states_cache = {i: valore for i, valore in enumerate(programs.root)}

            self._last_update = datetime.now()
        except:
            _LOGGER.warning(f"Error on periodic status request from TCS")

    def get_sensor_state(self,sensor_id,propertyName):
        return getattr(self._sensor_states_cache.get(sensor_id, "Stato sconosciuto"), propertyName, None)
        #return sensor_states_cache.get(sensor_id, "Stato sconosciuto").status

    def get_program_state(self,program_id,propertyName):
        return getattr(self._program_states_cache.get(program_id, "Stato sconosciuto"), propertyName, None)
        #return sensor_states_cache.get(sensor_id, "Stato sconosciuto").status

    async def update_cache_periodically(self,interval_seconds=5):
        while True:
            #_LOGGER.info("Refresh")
            await self.fetch_and_cache_states()
            await asyncio.sleep(interval_seconds)