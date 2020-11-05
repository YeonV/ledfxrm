import asyncio
from datetime import timedelta
import socket
_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
import logging
import requests
import json

import homeassistant.loader as loader
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from custom_components.ledfxrm.const import (
    CONF_PORT,
    CONF_HOST,
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
)


SCAN_INTERVAL = timedelta(seconds=300)
DOMAIN = 'ledfxrm'
DEPENDENCIES = ['mqtt']


# ================================================================ #
# TODO: IP and Port should come from config
# ================================================================ #
ip = '192.168.1.56:8888'



def json_extract(obj, key):
    arr = []
    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr
    values = extract(obj, arr, key)
    return values

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    thehost = entry.data.get(CONF_HOST)
    theport = entry.data.get(CONF_PORT)

    coordinator = LedfxrmDataUpdateCoordinator(
        hass, thehost=thehost, theport=theport
    )
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            hass.async_add_job(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )

    entry.add_update_listener(async_reload_entry)
    return True


class LedfxrmDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass, thehost, theport):
        """Initialize."""
        self.api = requests.get("http://" + thehost + ":" + theport + "/api/info")
        self.platforms = []
        logging.warning('API: %s', self.api.json())
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            data = await self.api.async_get_data()
            logging.warning('%s', data.json())
            return data.get("data", {})
        except Exception as exception:
            raise UpdateFailed(exception)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)







# def setup(hass, config):
#     hass.states.set('ledfxrm.ledfx_Remote', 'by Blade',{ 'icon': 'mdi:emoticon-devil' })


    
#     # ================================================================ #
#     # TODO: Create a CommandLine Switch for starting/stopping the server. 
#     # Commands should come from config
#     # this is a non working-dummy
#     # ================================================================ #
#     hass.states.set('switch.ledfxrm_start', False,{ 'icon': 'mdi:led-strip', 'platform': 'command_line', 'command_on': 'echo "some bash command"', 'command_off': 'echo "some bash command"' })
    
    

    
#     # ================================================================ #
#     # TODO: Refactor this to be an async setup, not triggered by mqtt
#     # ================================================================ #
#     mqtt = hass.components.mqtt
#     topic_trigger = 'blade/ledfx/info'
#     def message_received_trigger(msg):
#         name = 'test'
#         version = 'test'
#         scenes = 0
#         scenenames = []
#         try:
#             r0 = requests.get("http://" + ip + "/api/info")
#             logging.warning('%s', r0.json())
#             names = json_extract(r0.json(), 'name')
#             versions = json_extract(r0.json(), 'version')
#             name = names[0]
#             version = versions[0]
#         except:
#             pass
#         try:
#             r2 = requests.get("http://" + ip + "/api/scenes")
#             logging.warning('%s', r2.json())
#             for k, v in r2.json().items():
#                 if isinstance(v, (dict, list)):
#                     for ke, va in v.items():
#                         scenenames.append(ke)
#             logging.warning('%s', str(scenenames))
#             scenes = len(scenenames)
#             logging.warning('%i', scenes)
#         except:
#             pass
#         try:
#             r1 = requests.get("http://" + ip + "/api/devices")
#             logging.warning('%s', r1.json())
#             devicenames = json_extract(r1.json(), 'name')
#             pixels = json_extract(r1.json(), 'pixel_count')
#             devices = 0
#             logging.warning('%s', str(pixels))
#             devices = len(devicenames);
#             pixelsum = sum(pixels)

#             # ================================================================ #
#             # Fill Dummy Entity with data from all apis
#             # ================================================================ #
#             hass.states.set('ledfxrm.ledfx_Remote', 'by Blade',{ 'friendly_name': name, 'icon': 'mdi:led-strip-variant', 'Version': version, 'Devices': devices, 'Pixel Count': pixelsum, 'Scenes': scenes })


#             # ================================================================ #
#             # TODO: Remove this if automated works
#             #
#             # Update Manual-added input_select
#             # ================================================================ #
#             service_data = {'entity_id': 'input_select.ledfxscenes' ,'options': scenenames}
#             hass.services.call('input_select', 'set_options', service_data)
            
            
#             # ================================================================ #
#             # TODO: Create input_select Entity:
#             #
#             #    input_select:
#             #      ledfxscenes:
#             #        name: Scenes
#             #        options:
#             #          - 'blade-ish'
#             #          - 'off'
#             #        initial: 'off'
#             #        icon: mdi:led-strip
#             #
#             # this is a WORKING sample
#             # ================================================================ #
#             hass.states.set('input_select.ledfx_scenes', 'off',{ 'friendly_name': 'LedFX Scenes', 'icon': 'mdi:image-multiple-outline', 'initial': 'off', 'options': scenenames })
            
#             # ================================================================ #
#             # TODO: Create Automation Entity
#             #
#             #    - id: '1604492341312'
#             #      alias: Set LedFX Scene
#             #      description: ''
#             #      trigger:
#             #      - entity_id: input_select.ledfxscenes
#             #        platform: state
#             #      condition: []
#             #      action:
#             #      - data_template:
#             #          payload: '{{ states("input_select.ledfxscenes") }}'
#             #        service: rest_command.ledfx_scene
#             #      mode: single
#             #
#             # this is a non working dummy
#             # ================================================================ #
#             hass.states.set('automation.ledfx_set_scene', 'on',{ 'alias': 'LedFX Set Scene','description': 'Set Effect on InputSelect change', 'icon': 'mdi:image-outline', 'trigger': [{'entity_id': 'input_select.ledfx_scenes', 'platform': 'state'}], 'condition': [], 'action': [{'data_template': {'payload': '{{ states("input_select.ledfx_scenes") }}'}, 'service': 'rest_command.ledfx_scene'}],'mode': 'single' })


#             # ================================================================ #
#             # TODO: Create RestCommand entity
#             # IP & Port should come from config
#             #
#             #    rest_command:
#             #      ledfx_scene:
#             #        url: 'http://192.168.1.56:8888/api/scenes'
#             #        method: 'PUT'
#             #        payload: '{"id": "{{ payload }}", "action": "activate"}'
#             #        content_type: application/json
#             #
#             # ================================================================ #
            
            
            
#         except:
#             pass
#     mqtt.subscribe(topic_trigger, message_received_trigger)

#     return True
