"""LedfxrmEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import logging

from custom_components.ledfxrm.const import DOMAIN, NAME, VERSION, MANUFACTURER


class LedfxrmEntity(CoordinatorEntity):
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @property
    def device_info(self):
        logging.warning('YZ: %s', self.coordinator.data)
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME,
            "model": self.coordinator.data.get("info").get("name"),
            "manufacturer": MANUFACTURER,
            "sw_version": self.coordinator.data.get("info").get("version"),
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "time": str(self.coordinator.data.get("time")),
            "static": self.coordinator.data.get("version"),
        }