from homeassistant.components.binary_sensor import SensorEntity

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .status_cache import Status_Cache
from datetime import datetime

import logging

_LOGGER = logging.getLogger(__name__)


#li sto trattando tutti come porte ma non è vero!
class DoorSensor(SensorEntity):
    def __init__(self, obj:TcsZoneObj, entry):
        self._name =obj.description
        #self._area_id = area_id
        self._sensor_id = obj.idx
        self._status_cache = entry.runtime_data["cache"]
        
        self._entry = entry
        self.obj = obj
        

    @property
    def name(self):
        return f"zone_{self._entry.title}_{self._sensor_id}_{self._name}"

    @property
    def unique_id(self):
        return f"zone_{self._entry.title}_{self._sensor_id}_{self._name}"

    @property
    def is_on(self):
        # Usa get_sensor_state per ottenere lo stato dal cache
        try:

            cacheState = self._status_cache.get_sensor_state(self._sensor_id,"status").value
            self._attr_available = True

            if cacheState == 'OPEN':
                return True
            elif cacheState == 'CLOSED':
                return False       
            else:
                self._attr_available = False
        except:
            self._attr_available = False
            return False


        
    @property
    def extra_state_attributes(self):
        """Attributi extra come memoria allarme e dettagli."""
        return {
            "inLowBattery": self.inLowBattery,
            "last cache update": self._status_cache.last_cache_update.isoformat()
        }
    @property
    def inLowBattery(self):
        return  self._status_cache.get_sensor_state(self._sensor_id,"inLowBattery")

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    _LOGGER.debug("async_setup_entry Sensor")
    #entities = [TecnoalarmAreaControlPanel(hass, entry.data)]
    zones = entry.runtime_data["zones"]

    for zone in zones.root:
        # Accedere al campo 'description' per ogni elemento

        if zone.allocated:
            _LOGGER.debug(f"adding #{zone.idx} {zone.description}")
            async_add_entities([DoorSensor(zone,entry)])



    #retzones = await zoneConRiattivazione(settings)

    #allocatedZones = [item for item in retzones if item.get("allocated") == True]

    #for item in allocatedZones:
        # Accedere al campo 'description' per ogni elemento
    #    description = item.get("description", "Descrizione non trovata")
    #    idx = item.get("idx", "idx non trovato")
    #    status = item.get("status", "status non trovato")
    #    _LOGGER.debug("adding " + description)
    #    async_add_entities([DoorSensor(name=str(idx).zfill(2) + "_" + description, area_id=1,sensor_id= idx)])

    return
    