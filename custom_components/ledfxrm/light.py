"""Light platform for ledfxrm."""
from homeassistant.components.light import (
    LightEntity,
    ATTR_EFFECT,
    ATTR_HS_COLOR,
    SUPPORT_EFFECT,
    SUPPORT_TRANSITION,
    SUPPORT_BRIGHTNESS,
    ATTR_EFFECT_LIST,
    SUPPORT_COLOR,
)

from custom_components.ledfxrm.const import (
    DEFAULT_NAME,
    DOMAIN,
    ICON_ASCENE,
    LIGHT,
    START_KILL_SERVER,
    NUMBER_SCENES,
    NUMBER_DEVICES,
    NUMBER_PIXELS,
    ICON_STRIP_DEVICE,
    CONF_SHOW_SUBDEVICES,
    CONF_SHOW_BLADELIGHT,
    CONF_HOST,
    MANUFACTURER,
    VERSION,
)
from custom_components.ledfxrm.entity import LedfxrmEntity  # , LedfxrmEntityDyn
import logging
from typing import Any, Dict, Optional


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    devicenames = coordinator.data.get("devices").get("devices")
    test = entry.data.get(CONF_SHOW_SUBDEVICES)
    test2 = entry.data.get(CONF_SHOW_BLADELIGHT)
    if test is True:
        for k in devicenames:
            async_add_devices(
                [LedfxrmChildLight(coordinator, entry, k, devicenames[k]["config"])]
            )

    if test2 is True:
        async_add_devices(
            [
                LedfxrmLight(coordinator, entry),
                LedfxrmBladeLight(coordinator, entry),
            ]
        )
    else:
        async_add_devices([LedfxrmLight(coordinator, entry)])


class LedfxrmLight(LedfxrmEntity, LightEntity):
    """ledfxrm light class."""

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the light."""
        if ATTR_EFFECT in kwargs:
            await self.coordinator.api.async_set_scene(kwargs["effect"])
            await self.coordinator.async_request_refresh()
            return True

        # await self.coordinator.api.async_change_something(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the light."""
        # await self.coordinator.api.async_change_something(False)
        await self.coordinator.async_request_refresh()

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return SUPPORT_EFFECT

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + "_light"

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
        scenes = self.coordinator.data.get("scenes").get("scenes")
        scenenames = []
        for v in scenes.items():
            for va in v:
                if isinstance(va, str):
                    scenenames.append(va)
        return scenenames

    @property
    def device_state_attributes(self) -> Optional[Dict[str, Any]]:
        """Return the state attributes of the entity."""
        scenenames = self.coordinator.data.get("scenes").get("scenes")
        devicenames = self.coordinator.data.get("devices").get("devices")
        pixels = 0
        for k in devicenames:
            pixels = pixels + devicenames[k]["config"].get("pixel_count")
        return {
            NUMBER_SCENES: len(scenenames),
            NUMBER_DEVICES: len(devicenames),
            NUMBER_PIXELS: pixels,
        }

    @property
    def is_on(self):
        """Return true if the light is on."""
        return self.coordinator.api.connected


class LedfxrmChildLight(LedfxrmLight):
    """ledfxrm light class."""

    def __init__(
        self,
        coordinator,
        config_entry,
        devicename="NoName",
        deviceconfig={"NoConfig": "NoConfig"},
    ):
        super().__init__(coordinator, config_entry)
        self.config_entry = config_entry
        self.entity_id = "ledfxrm.ledfxrm"
        self.devicename = devicename
        # self.coordinator = coordinator
        # self.config_entry = LightEntity
        self.deviceconfig = deviceconfig
        # logging.warning("WTTTTFFFFFFF \nCOOOOO: %s", coordinator)
        # logging.warning("WTTTTFFFFFFF \nName: %s\nConfig: %s", devicename, deviceconfig)

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the light."""
        # if ATTR_EFFECT in kwargs:
        # await self.coordinator.api.async_set_scene(kwargs['effect'])
        # await self.coordinator.async_request_refresh()
        #    return True

        await self.coordinator.api.async_device_on(self.devicename)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the light."""
        # await self.coordinator.api.async_change_something(False)
        await self.coordinator.api.async_device_off(self.devicename)
        await self.coordinator.async_request_refresh()

    # @property
    # def supported_features(self) -> int:
    #    """Flag supported features."""
    #    return SUPPORT_EFFECT

    @property
    def assumed_state(self):
        """Return the name of the switch."""
        return True

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + "." + self.devicename

    @property
    def name(self):
        """Return the name of the light."""
        return "⮑ " + self.devicename

    @property
    def friendly_name(self):
        """Return the name of the light."""
        return self.deviceconfig["name"]

    @property
    def icon(self):
        """Return the icon of this light."""
        return ICON_STRIP_DEVICE

    @property
    def effect(self):
        """Return the current effect."""
        return None

    @property
    def effect_list(self):
        """Return the icon of this light."""
        return None

    @property
    def device_state_attributes(self) -> Optional[Dict[str, Any]]:
        """Return the state attributes of the entity."""
        # logging.warning("OMMMMG: %s ", self.coordinator.api.devicestates)
        if self.deviceconfig == {}:
            return {"status": "error"}
        return {
            "IP": self.deviceconfig["ip_address"],
            "Pixels": self.deviceconfig["pixel_count"],
            "Refresh Rate": self.deviceconfig["refresh_rate"],
            "Mode": self.coordinator.api.devicestates[self.devicename]["effect"].get(
                "name", "OFF"
            ),
        }

    @property
    def is_on(self):
        """Return true if the light is on."""
        return self.coordinator.api.devicestates[self.devicename]["power"]


class LedfxrmBladeLight(LedfxrmLight):
    """ledfxrm light class."""

    def __init__(self, coordinator, config_entry={}):
        super().__init__(coordinator, config_entry)
        self.config_entry = config_entry
        self.entity_id = "ledfxrm.ledfxrm"
        self._hs = None
        self._transition_time = 0.00
        self._effectlist = [
            "wipe 0.01",
            "wipe 0.02",
            "wipe 0.03",
            "wipe 0.04",
            "wipe 0.05",
        ]
        # self.devicename = devicename
        self.coordinator = coordinator
        # self.config_entry = LightEntity
        # self.deviceconfig = deviceconfig

        # logging.warning(
        #     "YZ01 \n %s \n ----- \n %s",
        #     self.coordinator.api.devicestates,
        #     dir(self.coordinator.api),
        # )
        # logging.warning("WTTTTFFFFFFF \nName: %s\nConfig: %s", devicename, deviceconfig)

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the light."""

        # logging.warning(
        #     "YZ02 \n %s \n",
        #     kwargs,
        # )
        if "hs_color" in kwargs:
            await self.coordinator.api.async_blade_on(kwargs)
            self._hs = kwargs["hs_color"]
        if "effect" in kwargs:
            # logging.warning(
            #     "YZ03 \n %s \n",
            #     float(kwargs["effect"].split()[1]),
            # )
            await self.coordinator.api.async_set_transition_time(
                float(kwargs["effect"].split()[1])
            )
            # await self.coordinator.api.async_blade_on(kwargs)
            # self._hs = kwargs["hs_color"]
        # await self.coordinator.api.async_set_scene(kwargs["effect"])
        # await self.coordinator.async_request_refresh()
        # return True
        # if ATTR_EFFECT in kwargs:
        # await self.coordinator.api.async_set_scene(kwargs['effect'])
        # await self.coordinator.async_request_refresh()
        #    return True

        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the light."""

        logging.warning(
            "YZ02 \n %s \n",
            kwargs,
        )
        # await self.coordinator.api.async_change_something(False)
        await self.coordinator.api.async_blade_off()
        await self.coordinator.async_request_refresh()

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        # flags = SUPPORT_BRIGHTNESS | SUPPORT_COLOR
        flags = SUPPORT_EFFECT | SUPPORT_COLOR
        return flags

    @property
    def hs_color(self) -> tuple:
        """Return the color property."""
        return self._hs

    # @property
    # def effect(self):
    #     """Return the current effect."""
    #     return self._effect

    @property
    def effect_list(self):
        return self._effectlist

    @property
    def assumed_state(self):
        """Return the name of the switch."""
        return True

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + ".blade-light"

    @property
    def name(self):
        """Return the name of the light."""
        return "Blade Light"

    @property
    def icon(self):
        """Return the icon of this light."""
        return ICON_STRIP_DEVICE

    @property
    def device_state_attributes(self) -> Optional[Dict[str, Any]]:
        """Return the state attributes of the entity."""
        devicenames = self.coordinator.data.get("devices").get("devices")
        pixels = 0
        for k in devicenames:
            pixels = pixels + devicenames[k]["config"].get("pixel_count")

        # logging.warning("OMMMMG: %s ", devicenames)

        # return {"Pixels": pixels, "Devices": list(devicenames.keys())}
        return {
            "Pixels": pixels,
            "Devices": len(list(devicenames.keys())),
            "Description": "One to rule them all",
        }

    @property
    def is_on(self):
        """Return true if the light is on."""
        # return self.coordinator.api.devicestates[self.devicename]["power"]
        return True
