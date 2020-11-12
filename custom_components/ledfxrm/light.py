"""Light platform for ledfxrm."""
from homeassistant.components.light import LightEntity, ATTR_EFFECT, SUPPORT_EFFECT, ATTR_EFFECT_LIST 

from custom_components.ledfxrm.const import DEFAULT_NAME, DOMAIN, ICON_ASCENE, LIGHT, START_KILL_SERVER, NUMBER_SCENES, NUMBER_DEVICES
from custom_components.ledfxrm.entity import LedfxrmEntity
import logging
from typing import Any, Dict, Optional

async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([LedfxrmBinaryLight(coordinator, entry)])


class LedfxrmBinaryLight(LedfxrmEntity, LightEntity):
    """ledfxrm light class."""
    
    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self.coordinator.api.async_change_something(True)
        await self.coordinator.async_request_refresh()
        

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.coordinator.api.async_change_something(False)
        await self.coordinator.async_request_refresh()
    
    async def async_set_effect(self, effect):
        """Activate effect."""
        logging.warning('EFFECT SELECTED: %s', effect)
        if not effect:
            return
        
        await self.coordinator.api.async_set_scene(effect)
        
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
        return "LedFX"

    @property
    def icon(self):
        """Return the icon of this light."""
        return ICON_ASCENE

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
        return {
            NUMBER_SCENES: len(scenenames),
            NUMBER_DEVICES: len(devicenames),
        }
    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.coordinator.api.connected
        
        
   
