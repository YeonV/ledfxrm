import asyncio
import aiohttp
from datetime import timedelta
import logging
import json

import homeassistant.loader as loader
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant import bootstrap


from custom_components.ledfxrm.const import (
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
    SWITCH,
    CONF_SCAN_INTERVAL
)

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    
    #str_mydict = ''.join('{}{}'.format(key, val) for key, val in entry.data.items())
    #logging.warning('ENTRY: %s', str_mydict)
    
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)
        
    thehost = entry.data.get('host')
    theport = entry.data.get('port')
    theversion = entry.data.get('version')
    thestart = entry.data.get('start')
    thestop = entry.data.get('stop')
    thescan = entry.data.get('scan_interval')
    
    coordinator = LedfxrmDataUpdateCoordinator(
        hass, thehost, theport, theversion, thestart, thestop, thescan
    )
    
    await coordinator.async_refresh()
    
    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            if platform is SWITCH:
                if thestart is None:
                    continue
                if thestart == '192.168.1.56:1337/?ledfxstart':
                    continue
            coordinator.platforms.append(platform)
            hass.async_add_job(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )
    entry.add_update_listener(async_reload_entry)
    return True



class myClient():
    def __init__(self, thehost, theport, thestart, thestop):
        self.thehost = thehost
        self.theport = theport
        self.thestart = thestart
        self.thestop = thestop
        self.connected = False
        self.effect = 'off'
        
    async def update(self):
        url = "http://" + self.thehost + ":" + str(self.theport) + "/api/info"
        url2 = "http://" + self.thehost + ":" + str(self.theport) + "/api/devices"
        url3 = "http://" + self.thehost + ":" + str(self.theport) + "/api/scenes"
        yz = {}
        yz['rest_info'] = {}
        yz['rest_devices'] = {}
        yz['rest_scenes'] = {}
        loop = asyncio.get_event_loop()
        async with aiohttp.ClientSession(loop=loop, trust_env = True) as session:
            async with session.get(url, ssl=False) as resp:                
                rest_info = await resp.json()
                yz['rest_info'] = rest_info
        
            async with session.get(url2, ssl=False) as resp_devices:                
                rest_devices = await resp_devices.json()                
                yz['rest_devices'] = rest_devices
        
            async with session.get(url3, ssl=False) as resp_scenes:                
                rest_scenes = await resp_scenes.json()                
                yz['rest_scenes'] = rest_scenes                
    
        if len(rest_info) > 0:
            self.connected = True
        return {'info':rest_info, 'devices': rest_devices, 'scenes': rest_scenes}
        
    async def async_change_something(self, state):
        loop = asyncio.get_event_loop()
        async with aiohttp.ClientSession(loop=loop, trust_env = True) as session:
            if state is True:
                async with session.get("http://" + self.thestart, ssl=False) as resp_start:
                    logging.debug('start: %s', resp_start)
                return True
            if state is False:
                async with session.get("http://" + self.thestop, ssl=False) as resp_stop:
                    logging.debug('stop: %s', resp_stop)
        return None
            
            
    async def async_set_scene(self, effect):
        if effect is None:
            return
        url3 = "http://" + self.thehost + ":" + str(self.theport) + "/api/scenes"
        loop = asyncio.get_event_loop()
        async with aiohttp.ClientSession(loop=loop, trust_env = True) as session:
            async with session.put(url3, json={"id": effect, "action": "activate"}, ssl=False) as resp_scenes:                
                res_set_scene = await resp_scenes.json()     
                self.effect = effect
        return None
        
class LedfxrmDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""
    def __init__(self, hass: HomeAssistant, thehost, theport, theversion, thestart, thestop, thescan):
    #def __init__(self, hass: HomeAssistant, thehost, theport, theversion, thestart, thestop):
        """Initialize."""
        self.theversion = theversion
        self.thehost = thehost
        self.theport = theport
        self.thestop = thestop
        self.thestart = thestart
        self.thescan = thescan
        scan_interval = timedelta(seconds=self.thescan)
        self.api = myClient(thehost, theport, thestart, thestop)
        self.platforms = []
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=scan_interval)

    async def _async_update_data(self):
        """Update data via library."""
        
        try:
            #logging.warning('SCAN_INTERVAL_CHECK %s', self.thescan)
            data = await self.api.update()
            scenes = data.get('scenes').get('scenes')
            self.scenes = scenes
            
            self.number_scenes = len(scenes)
            
            return data
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