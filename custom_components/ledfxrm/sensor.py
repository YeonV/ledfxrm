"""Sensor platform for ledfxrm."""
from custom_components.ledfxrm.const import DEFAULT_NAME, DOMAIN, ICON_SCENE, ICON_STRIP, NUMBER_SCENES, NUMBER_DEVICES
from custom_components.ledfxrm.entity import LedfxrmEntity
from typing import Any, Callable, Dict, List, Optional

async def async_setup_entry( hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([LedfxrmSensor(coordinator, entry),LedfxrmDeviceSensor(coordinator, entry)])

class LedfxrmDeviceSensor(LedfxrmEntity):
    """ledfxrm Sensor class."""
    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + '_devices'
        
    @property
    def name(self):
        """Return the name of the sensor."""
        return NUMBER_DEVICES

    @property
    def state(self):
        """Return the state of the sensor."""
        devicenames = self.coordinator.data.get('devices').get('devices')
        return len(devicenames)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON_STRIP

class LedfxrmSensor(LedfxrmEntity):
    """ledfxrm Sensor class."""
    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + '_scenes'
    @property
    def name(self):
        """Return the name of the sensor."""
        return NUMBER_SCENES

    @property
    def state(self):
        """Return the state of the sensor."""
        scenenames = self.coordinator.data.get('scenes').get('scenes')
        return len(scenenames)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON_SCENE