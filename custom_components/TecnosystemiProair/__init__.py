"""The TecnosystemiProair integration."""
import logging
import asyncio
from .const import (
    DOMAIN
)
from .string_helpers import StringHelpers 
from .login import Login  
from .status import Status

from homeassistant.core import HomeAssistant
from .status_cache import Status_Cache

_LOGGER = logging.getLogger(__name__)



async def async_setup_entry(hass: HomeAssistant, config: dict):
    """Set up TecnosystemiProair component."""
    _LOGGER.info("Setting up TecnosystemiProair integration")
    _LOGGER.info(config)
    
    global homeassistant
    global status_cache
    homeassistant = hass

    global login, crypt

    crypt = StringHelpers("1a1636b1ns91wr48")
    login = Login("1a1636b1ns91wr48")
    status = Status(login)

    if await hass.async_add_executor_job(login.login_to_tecnosistemi):
        if await hass.async_add_executor_job(status.request_status):
            _LOGGER.info("logged!!")
            _LOGGER.info(status)
            _LOGGER.info(status.status_resp)

            _LOGGER.info(status.status_resp.zones)
            _LOGGER.info(status.status_resp.zones[0])

    #posso creare la cache e aggiornarla
    status_cache = Status_Cache(hass,status)
#    await status_cache.fetch_and_cache_states()

#    _LOGGER.info("prendo le zone")
#    zones = await hass.async_add_executor_job(myTCSSession.get_zones) #NON uso .tp.status.zones perchè allocated non è popolato correttamente...
#    _LOGGER.info("ho zone")

    config.runtime_data = {"status": status, 
                           "cache": status_cache
                           }
    await hass.config_entries.async_forward_entry_setups(config, ["climate"])
    #await hass.config_entries.async_forward_entry_setups(config, ["switch"])
    #await hass.config_entries.async_forward_entry_setups(config, ["alarm_control_panel"])
    
    return True