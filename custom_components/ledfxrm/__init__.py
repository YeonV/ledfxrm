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
    CONF_SCAN_INTERVAL,
    CONF_SHOW_SUBDEVICES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""

    # str_mydict = ''.join('{}{}'.format(key, val) for key, val in entry.data.items())
    # logging.warning('ENTRY: %s', str_mydict)

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    thehost = entry.data.get("host")
    theport = entry.data.get("port")
    theversion = entry.data.get("version")
    thestart = entry.data.get("start")
    thestop = entry.data.get("stop")
    thescan = entry.data.get("scan_interval")
    thesubdevices = entry.data.get("show_subdevices")
    thestart_method = entry.data.get("start_method")
    thestart_body = entry.data.get("start_body")
    thestop_method = entry.data.get("stop_method")
    thestop_body = entry.data.get("stop_body")
    coordinator = LedfxrmDataUpdateCoordinator(
        hass,
        thehost,
        theport,
        theversion,
        thestart,
        thestop,
        thescan,
        thesubdevices,
        thestart_method,
        thestart_body,
        thestop_method,
        thestop_body,
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
                if thestart == "192.168.1.56:1337/?ledfxstart":
                    continue
            coordinator.platforms.append(platform)
            hass.async_add_job(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )
    entry.add_update_listener(async_reload_entry)
    return True


class myClient:
    def __init__(
        self,
        thehost,
        theport,
        thestart,
        thestop,
        thesubdevices,
        thestart_method,
        thestart_body,
        thestop_method,
        thestop_body,
    ):
        self.thehost = thehost
        self.theport = theport
        self.thestart = thestart
        self.thestop = thestop
        self.connected = False
        self.effect = "off"
        self.thesubdevices = thesubdevices
        self.devicestates = {}
        self.thestart_method = thestart_method
        self.thestart_body = thestart_body
        self.thestop_method = thestop_method
        self.thestop_body = thestop_body

    async def update(self):
        url = "http://" + self.thehost + ":" + str(self.theport) + "/api/info"
        url2 = "http://" + self.thehost + ":" + str(self.theport) + "/api/devices"
        url3 = "http://" + self.thehost + ":" + str(self.theport) + "/api/scenes"
        yz = {}
        yz["rest_info"] = {}
        yz["rest_devices"] = {}
        yz["rest_scenes"] = {}

        loop = asyncio.get_event_loop()
        async with aiohttp.ClientSession(loop=loop, trust_env=True) as session:
            async with session.get(url, ssl=False) as resp:
                rest_info = await resp.json()
                yz["rest_info"] = rest_info

            async with session.get(url2, ssl=False) as resp_devices:
                rest_devices = await resp_devices.json()
                yz["rest_devices"] = rest_devices
                # logging.warning("INTERNAL STATES b4: %s", self.devicestates)
                if len(self.devicestates) == 0:
                    for k in rest_devices["devices"]:
                        # logging.warning("NOWWW: %s", k)
                        # logging.warning("THENN: %s", rest_devices['devices'][k])
                        if len(rest_devices["devices"][k].get("effect", {})) > 0:
                            # logging.warning("GOT EFFECT FROM LEDFX: %s", rest_devices['devices'][k].get('effect'))
                            effect = rest_devices["devices"][k].get("effect")
                            power = True
                        else:

                            effect = {}
                            power = False
                        self.devicestates[k] = {
                            "power": power,
                            "effect": effect,  # self.devicestates[k].get('effect', {})
                        }
                # logging.warning("INTERNAL STATES after: %s", self.devicestates)

            async with session.get(url3, ssl=False) as resp_scenes:
                rest_scenes = await resp_scenes.json()
                yz["rest_scenes"] = rest_scenes

        if len(rest_info) > 0:
            self.connected = True

        return {
            "info": rest_info,
            "devices": rest_devices,
            "scenes": rest_scenes,
            "show_subdevices": self.thesubdevices,
        }

    async def async_change_something(self, state):
        loop = asyncio.get_event_loop()
        async with aiohttp.ClientSession(loop=loop, trust_env=True) as session:
            logging.warning(
                "SERVER COMMAND --- %s ------ %s ------ %s ------ %s --- ",
                self.thestart_method,
                self.thestop_method,
                self.thestart_body,
                self.thestop_body,
            )
            if state is True:
                if self.thestart_method == "GET":
                    async with session.get(
                        "http://" + self.thestart, ssl=False
                    ) as resp_start:
                        logging.debug("start: %s", resp_start)
                if self.thestart_method == "DELETE":
                    async with session.delete(
                        "http://" + self.thestart, ssl=False
                    ) as resp_start:
                        logging.debug("start: %s", resp_start)
                if self.thestart_method == "PUT":
                    async with session.put(
                        "http://" + self.thestart, json=self.thestart_body, ssl=False
                    ) as resp_start:
                        logging.debug("start: %s", resp_start)
                if self.thestart_method == "POST":
                    async with session.post(
                        "http://" + self.thestart, json=self.thestart_body, ssl=False
                    ) as resp_start:
                        logging.debug("start: %s", resp_start)
                return True
            if state is False:
                if self.thestop_method == "GET":
                    async with session.get(
                        "http://" + self.thestop, ssl=False
                    ) as resp_start:
                        logging.debug("start: %s", resp_start)
                if self.thestop_method == "DELETE":
                    async with session.delete(
                        "http://" + self.thestop, ssl=False
                    ) as resp_start:
                        logging.debug("start: %s", resp_start)
                if self.thestop_method == "PUT":
                    async with session.put(
                        "http://" + self.thestop, json=self.thestop_body, ssl=False
                    ) as resp_start:
                        logging.debug("start: %s", resp_start)
                if self.thestop_method == "POST":
                    async with session.post(
                        "http://" + self.thestop, json=self.thestop_body, ssl=False
                    ) as resp_start:
                        logging.debug("start: %s", resp_start)

                async with session.get(
                    "http://" + self.thestop, ssl=False
                ) as resp_stop:
                    logging.debug("stop: %s", resp_stop)
        return None

    async def async_set_scene(self, effect):
        if effect is None:
            return
        url3 = "http://" + self.thehost + ":" + str(self.theport) + "/api/scenes"
        loop = asyncio.get_event_loop()
        async with aiohttp.ClientSession(loop=loop, trust_env=True) as session:
            async with session.put(
                url3, json={"id": effect, "action": "activate"}, ssl=False
            ) as resp_scenes:
                res_set_scene = await resp_scenes.json()
                self.effect = effect
        return None

    async def async_device_off(self, state):
        # logging.warning('DEVICE OFF internal --- %s --- %s', state, self.devicestates[state].get('effect'))
        url4 = (
            "http://"
            + self.thehost
            + ":"
            + str(self.theport)
            + "/api/devices/"
            + state
            + "/effects"
        )
        loop = asyncio.get_event_loop()

        async with aiohttp.ClientSession(loop=loop, trust_env=True) as session:
            async with session.get(url4, ssl=False) as get_effect:
                testing = await get_effect.json()
                if testing["effect"] != {}:
                    self.devicestates[state]["effect"] = testing["effect"]
                    # logging.warning("Turning Off, found effect: %s", self.devicestates[state].get('effect'))
                    async with session.delete(url4, ssl=False) as del_effect:
                        await del_effect.json()
                # else:
                # logging.warning("Turning Off, No effect:")

        self.devicestates[state]["power"] = False
        return None

    async def async_device_on(self, state):
        # logging.warning('DEVICE ON internal --- %s --- %s', state, self.devicestates[state].get('effect'))
        url4 = (
            "http://"
            + self.thehost
            + ":"
            + str(self.theport)
            + "/api/devices/"
            + state
            + "/effects"
        )
        loop = asyncio.get_event_loop()
        payload = {}
        async with aiohttp.ClientSession(loop=loop, trust_env=True) as session:
            async with session.get(url4, ssl=False) as get_effect:
                testing = await get_effect.json()
                if testing["effect"] != {}:
                    # logging.warning("Turning on, found effect: %s", testing['effect'])
                    self.devicestates[state]["effect"] = testing["effect"]

                # payload = {'config': self.devicestates[state].get('effect').get('config')}
                payload = self.devicestates[state].get("effect")

                if payload is None or payload == {}:
                    payload = {
                        "config": {
                            "modulation_effect": "sine",
                            "modulation_speed": 0.5,
                            "gradient_name": "Spectral",
                            "gradient_repeat": 1,
                            "speed": 1.0,
                            "flip": False,
                            "brightness": 1.0,
                            "mirror": False,
                            "blur": 0.0,
                            "modulate": False,
                            "gradient_roll": 0,
                        },
                        "name": "Gradient",
                        "type": "gradient",
                    }

                # logging.warning("Setting Effect, %s", payload)
                async with session.post(url4, json=payload, ssl=False) as set_effect:
                    await set_effect.json()
        self.devicestates[state]["power"] = True
        return None


class LedfxrmDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        thehost,
        theport,
        theversion,
        thestart,
        thestop,
        thescan,
        thesubdevices,
        thestart_method,
        thestart_body,
        thestop_method,
        thestop_body,
    ):
        # def __init__(self, hass: HomeAssistant, thehost, theport, theversion, thestart, thestop):
        """Initialize."""
        self.theversion = theversion
        self.thehost = thehost
        self.theport = theport
        self.thestop = thestop
        self.thestart = thestart
        self.thescan = thescan
        self.thesubdevices = thesubdevices
        self.thestart_method = thestart_method
        self.thestart_body = thestart_body
        self.thestop_method = thestop_method
        self.thestop_body = thestop_body
        scan_interval = timedelta(seconds=self.thescan)
        self.api = myClient(
            thehost,
            theport,
            thestart,
            thestop,
            thesubdevices,
            thestart_method,
            thestart_body,
            thestop_method,
            thestop_body,
        )
        self.platforms = []
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=scan_interval)

    async def _async_update_data(self):
        """Update data via library."""

        try:
            # logging.warning('SCAN_INTERVAL_CHECK %s', self.thescan)
            data = await self.api.update()
            scenes = data.get("scenes").get("scenes")
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