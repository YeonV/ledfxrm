"""Switch platform for ledfxrm."""
from homeassistant.components.switch import SwitchEntity

from custom_components.ledfxrm.const import DEFAULT_NAME, DOMAIN, ICON_POWER, SWITCH, START_KILL_SERVER
from custom_components.ledfxrm.entity import LedfxrmEntity
import logging

async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([LedfxrmBinarySwitch(coordinator, entry)])


class LedfxrmBinarySwitch(LedfxrmEntity, SwitchEntity):
    """ledfxrm switch class."""
    
    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self.coordinator.api.async_change_something(True)
        await self.coordinator.async_request_refresh()
        

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.coordinator.api.async_change_something(False)
        await self.coordinator.async_request_refresh()
        
    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + '_switch'
    
    # Wait until one can change the Icon of the On/Off buttons
    #@property
    #def assumed_state(self):
    #    """Return the name of the switch."""
    #    return True
    
    @property
    def name(self):
        """Return the name of the switch."""
        return START_KILL_SERVER

    @property
    def icon(self):
        """Return the icon of this switch."""
        return ICON_POWER

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.coordinator.api.connected