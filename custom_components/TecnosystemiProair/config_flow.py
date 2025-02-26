from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import callback

from typing import Any
from .const import (
    DOMAIN
)

import voluptuous as vol
import logging


#class OTPException(ValueError): ...

_LOGGER = logging.getLogger(__name__)

VOL_SCHEMA_HOMECONFIG = vol.Schema(
    {
        vol.Required("homeName", description={"suggested_value": "My Home"}): str,
        vol.Required("email", description={"suggested_value": "my-email@domain.com"}): str,
        vol.Required("password"): str,
        vol.Required("serial", description={"suggested_value": "0123456789"}): str,
        vol.Required("PIN"): str,

    }
)




@callback
def configured_instances(hass):
    return [
        entry.entry_id for entry in hass.config_entries.async_entries(DOMAIN)
    ]

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None)-> ConfigFlowResult:
        _LOGGER.info("Start Config Flow")
        errors = {}

        if user_input is not None:
            _LOGGER.debug(user_input)
            try:
                #self.user_data = user_input
                
                return self.async_create_entry(title=user_input["homeName"],
                                               data=user_input)
            except Exception as e:
                _LOGGER.debug(f"General Error: {e}")
                errors["base"] = "general_error"

        return self.async_show_form(step_id="user", 
                                    data_schema=VOL_SCHEMA_HOMECONFIG,
                                    errors=errors)
    
    
