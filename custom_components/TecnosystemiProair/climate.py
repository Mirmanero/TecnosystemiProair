from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .status_cache import Status_Cache
from datetime import datetime
from .status import Status

import logging

_LOGGER = logging.getLogger(__name__)


#li sto trattando tutti come porte ma non è vero!
class TecnosystemiSensor(ClimateEntity):
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_hvac_mode = HVACMode.AUTO

    def __init__(self, obj:Status.StatusZone, entry):
        self._name =obj.name
        #self._area_id = area_id
        self._sensor_id = obj.zone_id
        self._status_cache = entry.runtime_data["cache"]
        
        self._entry = entry
        self.obj = obj
        
        self._temperature: float | None = None
        self._humidity: float | None = None

        self._temperature = obj.temp
        self._humidity = obj.umd
        self._attr_hvac_modes = [
            HVACMode.AUTO,
            HVACMode.HEAT,
            HVACMode.COOL,
            HVACMode.OFF,
        ]


    @property
    def name(self):
        return f"zone_{self._entry.title}_{self._sensor_id}_{self._name}"

    @property
    def unique_id(self):
        return f"zone_{self._entry.title}_{self._sensor_id}_{self._name}"

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        #_LOGGER.debug("current_temperature")
        try:
            
            self._temperature = int(self._status_cache.get_sensor_state(self._sensor_id,"temp"))/10
            _LOGGER.debug(f"current_temperature: {self._temperature}")

            self._attr_available = True
        except:
            _LOGGER.debug(f"errror current_temperature")
            #self._attr_available = False
        return self._temperature
    
    @property
    def current_humidity(self) -> float | None:
        """Return the current humidity."""
        #_LOGGER.debug("current_humidity")
        try:
            
            self._humidity = int(self._status_cache.get_sensor_state(self._sensor_id,"umd"))/10
            #_LOGGER.debug(f"current_humidity: {self._humidity}")
            self._attr_available = True
        except:
            _LOGGER.debug(f"errror current_humidity")
            #self._attr_available = False

        return self._humidity
    

    

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    _LOGGER.debug("async_setup_entry Sensor")
    #entities = [TecnoalarmAreaControlPanel(hass, entry.data)]
    status = entry.runtime_data["status"]
    zones = status.status_resp.zones

    for zone in zones:
        # Accedere al campo 'description' per ogni elemento

        
        _LOGGER.debug(f"adding #{zone.zone_id} {zone.name}")
        async_add_entities([TecnosystemiSensor(zone,entry)])



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
    