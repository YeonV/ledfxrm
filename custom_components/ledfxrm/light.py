"""Light platform for ledfxrm."""
from homeassistant.components.light import LightEntity, ATTR_EFFECT, SUPPORT_EFFECT, ATTR_EFFECT_LIST 

from custom_components.ledfxrm.const import DEFAULT_NAME, DOMAIN, ICON_ASCENE, LIGHT, START_KILL_SERVER, NUMBER_SCENES, NUMBER_DEVICES, NUMBER_PIXELS, ICON_STRIP_DEVICE
from custom_components.ledfxrm.entity import LedfxrmEntity #, LedfxrmEntityDyn
import logging
from typing import Any, Dict, Optional

async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    devicenames = coordinator.data.get('devices').get('devices')
    logging.warning("AND HERE WE GO: %s", coordinator.thesubdevices)
    for k in devicenames:
        async_add_devices([LedfxrmChildLight(coordinator, entry, k, devicenames[k]['config'])])
        
    async_add_devices([
        LedfxrmBinaryLight(coordinator, entry)
        ])


class LedfxrmBinaryLight(LedfxrmEntity, LightEntity):
    """ledfxrm light class."""
    
    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the light."""
        if ATTR_EFFECT in kwargs:
            await self.coordinator.api.async_set_scene(kwargs['effect'])
            await self.coordinator.async_request_refresh()
            return True
            
        #await self.coordinator.api.async_change_something(True)
        await self.coordinator.async_request_refresh()
        

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the light."""
        #await self.coordinator.api.async_change_something(False)
        await self.coordinator.async_request_refresh()
    

        
    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return SUPPORT_EFFECT
        
    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + '_light'
    
    @property
    def name(self):
        """Return the name of the light."""
        return "LedFX Scene-Selector"

    @property
    def icon(self):
        """Return the icon of this light."""
        return ICON_ASCENE
        
    @property
    def effect(self):
        """Return the current effect."""
        return self.coordinator.api.effect

    @property
    def effect_list(self):
        """Return the icon of this light."""
        scenes = self.coordinator.data.get('scenes').get('scenes')
        scenenames = []
        for v in scenes.items():
            for va in v:
                if isinstance(va, str):
                    scenenames.append(va)
        return scenenames
        
    @property
    def device_state_attributes(self) -> Optional[Dict[str, Any]]:
        """Return the state attributes of the entity."""
        scenenames = self.coordinator.data.get('scenes').get('scenes')
        devicenames = self.coordinator.data.get('devices').get('devices')
        pixels = 0
        for k in devicenames:
            pixels = pixels + devicenames[k]['config'].get('pixel_count')
        return {
            NUMBER_SCENES: len(scenenames),
            NUMBER_DEVICES: len(devicenames),
            NUMBER_PIXELS: pixels
        }
    @property
    def is_on(self):
        """Return true if the light is on."""
        return self.coordinator.api.connected
        




class LedfxrmChildLight(LedfxrmEntity, LightEntity):
    """ledfxrm light class."""
    def __init__(self,LedfxrmEntity, LightEntity, devicename='NoName', deviceconfig={'NoConfig': 'NoConfig'}):
        self.devicename = devicename
        self.coordinator = LedfxrmEntity
        self.config_entry = LightEntity
        self.deviceconfig = deviceconfig
        #logging.warning("WTTTTFFFFFFF \nCOOOOO: %s", coordinator)
        #logging.warning("WTTTTFFFFFFF \nName: %s\nConfig: %s", devicename, deviceconfig)
    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the light."""
        #if ATTR_EFFECT in kwargs:
            #await self.coordinator.api.async_set_scene(kwargs['effect'])
            #await self.coordinator.async_request_refresh()
        #    return True
            
        await self.coordinator.api.async_device_on(self.devicename)
        await self.coordinator.async_request_refresh()
        

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the light."""
        #await self.coordinator.api.async_change_something(False)
        await self.coordinator.api.async_device_off(self.devicename)
        await self.coordinator.async_request_refresh()
    

        
    #@property
    #def supported_features(self) -> int:
    #    """Flag supported features."""
    #    return SUPPORT_EFFECT
        
    @property
    def assumed_state(self):
        """Return the name of the switch."""
        return True
        
    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        
        #return self.config_entry.entry_id + '_light'
        
        #return DOMAIN + '_light_' + self.name
        #return 'ledfxrm.ledfxrm.' + self.devicename
        return self.config_entry.entry_id + '.' + self.devicename 
    @property
    def name(self):
        """Return the name of the light."""
        #logging.warning('33333 \n\n %s \n\n', self)
        return self.devicename
    @property
    def friendly_name(self):
        """Return the name of the light."""
        #logging.warning('33333 \n\n %s \n\n', self)
        return self.deviceconfig['name']
        
    @property
    def icon(self):
        """Return the icon of this light."""
        return ICON_STRIP_DEVICE
        
    #@property
    #def effect(self):
    #    """Return the current effect."""
    #    return self.coordinator.api.effect

    #@property
    #def effect_list(self):
    #    """Return the icon of this light."""
    #    scenes = self.coordinator.data.get('scenes').get('scenes')
    #    scenenames = []
    #    for v in scenes.items():
    #        for va in v:
    #            if isinstance(va, str):
    #                scenenames.append(va)
    #    return scenenames
        
    @property
    def device_state_attributes(self) -> Optional[Dict[str, Any]]:
        """Return the state attributes of the entity."""
        if self.deviceconfig == {}:
            return {'status': 'error'}
        return {
            'IP': self.deviceconfig['ip_address'],
            'Pixels': self.deviceconfig['pixel_count'],
            'Refresh Rate': self.deviceconfig['refresh_rate']
        }
        
    @property
    def is_on(self):
        """Return true if the light is on."""
        return self.coordinator.api.devicestates[self.devicename]