# """Switch platform for ledfxrm."""
# from homeassistant.components.switch import SwitchDevice

# from custom_components.ledfxrm.const import DEFAULT_NAME, DOMAIN, ICON_POWER, SWITCH
# from custom_components.ledfxrm.entity import LedfxrmEntity


# async def async_setup_entry(hass, entry, async_add_devices):
#     """Setup sensor platform."""
#     coordinator = hass.data[DOMAIN][entry.entry_id]
#     async_add_devices([LedfxrmBinarySwitch(coordinator, entry)])


# class LedfxrmBinarySwitch(LedfxrmEntity, SwitchDevice):
#     """ledfxrm switch class."""

#     async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
#         """Turn on the switch."""
#         await self.coordinator.api.async_change_something(True)
#         await self.coordinator.async_request_refresh()

#     async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
#         """Turn off the switch."""
#         await self.coordinator.api.async_change_something(False)
#         await self.coordinator.async_request_refresh()

#     @property
#     def name(self):
#         """Return the name of the switch."""
#         return f"{DEFAULT_NAME}_{SWITCH}"

#     @property
#     def icon(self):
#         """Return the icon of this switch."""
#         return ICON_POWER

#     @property
#     def is_on(self):
#         """Return true if the switch is on."""
#         return self.coordinator.api.something