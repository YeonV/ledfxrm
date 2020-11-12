"""Adds config flow for Ledfxrm."""
from homeassistant import config_entries
from homeassistant.core import callback
import asyncio
import aiohttp
import async_timeout
import voluptuous as vol
import logging
import requests
from custom_components.ledfxrm.const import (  # pylint: disable=unused-import
    CONF_HOST,
    CONF_PORT,
    DOMAIN,
    PLATFORMS,
)

YZSTART = "start"
YZSTOP = "stop"
YZHOST = "host"
YZPORT = "port"


class LedfxrmFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Ledfxrm."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        #logging.warning('Config FLOW!!!')
        self._errors = {}
        
    async def async_step_user( self, user_input=None ):
        """Handle a flow initialized by the user."""
        self._errors = {}
    
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            #logging.warning('UserInput: %s', user_input[YZHOST)
            #logging.warning('UserInput: %s', user_input[YZPORT])
            name, version = await self.get_rest_status(
                user_input[YZHOST], user_input[YZPORT]
            )
            if name:
                #service_data = {'entity_id': 'input_select.ledfx_seceneselector' ,'options': api['rest_scenes']}
                #hass.services.call('input_select', 'set_options', service_data)
                data_attr = {YZHOST: user_input[YZHOST], YZPORT: user_input[YZPORT], 'version': version, 'name': name, 'start': user_input[YZSTART], 'stop': user_input[YZSTOP]}
                return self.async_create_entry(
                    title=name, data= data_attr
                )
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return LedfxrmOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(YZHOST, default="192.168.1.56"): str,
                    vol.Required(YZPORT, default=8888): int,
                    vol.Required(YZSTART, default="command to start server"): str,
                    vol.Required(YZSTOP, default="command to kill server"): str
                }
            ),
            errors=self._errors,
        )
        
    
            
    async def get_rest_status(self, thehost, theport):
        """Return true if credentials is valid."""
        # logging.warning('Host: %s', thehost)
        # logging.warning('Port: %s', str(theport))
        loop = asyncio.get_event_loop()
        url = "http://" + thehost + ":" + str(theport) + "/api/info"
        async with aiohttp.ClientSession(loop=loop, trust_env = True) as session:
            async with session.get(url, ssl=False) as resp:                
                rest_info = await resp.json()
                name = rest_info['name']
                version = rest_info['version']
                logging.warning('Config for %s | Version: %s', name, version)
        #return yz
        return name, version
        


class LedfxrmOptionsFlowHandler(config_entries.OptionsFlow):
    """Ledfxrm config flow options handler."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_HOST), data=self.options
        )
