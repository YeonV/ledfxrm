"""Sensor platform for ledfxrm."""
from custom_components.ledfxrm.const import DEFAULT_NAME, DOMAIN, ICON_SCENE, ICON_STRIP, NUMBER_SCENES, NUMBER_DEVICES, NUMBER_PIXELS, ICON_LED
from custom_components.ledfxrm.entity import LedfxrmEntity
from typing import Any, Callable, Dict, List, Optional
import logging

async def async_setup_entry( hass, entry, async_add_displays):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_displays([
        LedfxrmSensor(coordinator, entry),
        LedfxrmDeviceSensor(coordinator, entry),
        LedfxrmPixelSensor(coordinator, entry),
        ])

class LedfxrmPixelSensor(LedfxrmEntity):
    """ledfxrm Sensor class."""
    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + '_pixels'
        
    @property
    def name(self):
        """Return the name of the sensor."""
        return NUMBER_PIXELS

    @property
    def state(self):
        """Return the state of the sensor."""
        devicenames = self.coordinator.data.get('displays').get('displays')
        pixels = 0
        for k in devicenames:
            pixels = pixels + devicenames[k]['config'].get('pixel_count')
        return pixels

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON_LED

class LedfxrmDeviceSensor(LedfxrmEntity):
    """ledfxrm Sensor class."""
    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + '_displays'
        
    @property
    def name(self):
        """Return the name of the sensor."""
        return NUMBER_DEVICES

    @property
    def state(self):
        """Return the state of the sensor."""
        devicenames = self.coordinator.data.get('displays').get('displays')
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