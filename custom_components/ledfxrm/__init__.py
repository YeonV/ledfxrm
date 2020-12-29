import asyncio
import aiohttp
from datetime import timedelta
import logging
import json
import socket
from collections import OrderedDict

_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
from time import sleep

import homeassistant.loader as loader
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady, PlatformNotReady
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.util.color import color_hs_to_RGB
from homeassistant import bootstrap


from custom_components.ledfxrm.const import (
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
    SWITCH,
    LIGHT,
    CONF_HOST,
    CONF_PORT,
    CONF_START,
    CONF_STOP,
    CONF_SCAN_INTERVAL,
    CONF_SHOW_SUBDEVICES,
    CONF_SHOW_BLADELIGHT,
    CONF_START_METHOD,
    CONF_STOP_METHOD,
    CONF_START_BODY,
    CONF_STOP_BODY,
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

    thehost = entry.data.get(CONF_HOST)
    theport = entry.data.get(CONF_PORT)
    theversion = entry.data.get("version")
    thestart = entry.data.get(CONF_START)
    thestop = entry.data.get(CONF_STOP)
    thescan = entry.data.get(CONF_SCAN_INTERVAL)
    thesubdevices = entry.data.get(CONF_SHOW_SUBDEVICES)
    theblade_light = entry.data.get(CONF_SHOW_BLADELIGHT)
    thestart_method = entry.data.get(CONF_START_METHOD)
    thestart_body = entry.data.get(CONF_START_BODY)
    thestop_method = entry.data.get(CONF_STOP_METHOD)
    thestop_body = entry.data.get(CONF_STOP_BODY)
    coordinator = LedfxrmDataUpdateCoordinator(
        hass,
        thehost,
        theport,
        theversion,
        thestart,
        thestop,
        thescan,
        thesubdevices,
        theblade_light,
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
        theblade_light,
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
        self.theblade_light = theblade_light
        self.devicestates = {}
        self.devices = {}
        self.virtuals = {}
        self.thestart_method = thestart_method
        self.thestart_body = thestart_body
        self.thestop_method = thestop_method
        self.thestop_body = thestop_body
        self._transition_time = 0.02

    async def update(self):
        url = "http://" + self.thehost + ":" + str(self.theport) + "/api/info"
        url2 = "http://" + self.thehost + ":" + str(self.theport) + "/api/devices"
        url3 = "http://" + self.thehost + ":" + str(self.theport) + "/api/scenes"
        url4 = "http://" + self.thehost + ":" + str(self.theport) + "/api/virtuals"
        yz = {}
        rest_info = {}
        rest_devices = {}
        rest_scenes = {}
        rest_virtuals = {}
        yz["rest_info"] = {}
        yz["rest_devices"] = {}
        yz["rest_scenes"] = {}
        yz["rest_virtuals"] = {}

        loop = asyncio.get_event_loop()
        async with aiohttp.ClientSession(loop=loop, trust_env=True) as session:
            try:
                async with session.get(url, ssl=False) as response:
                    if response.status == 200:
                        rest_info = await response.json()
                        yz["rest_info"] = rest_info
                    else:
                        logging.warning(
                            "CANT CONNECT TO LEDFX - INFO: %s", response.status
                        )

            except aiohttp.ClientConnectorError as e:
                # logging.warning("CANT CONNECT TO LEDFX - INFO - 2: %s", e)
                # raise PlatformNotReady
                return {}

            try:
                async with session.get(url2, ssl=False) as resp_devices:
                    if resp_devices.status == 200:
                        rest_devices = await resp_devices.json()
                        yz["rest_devices"] = rest_devices
                        self.devices = yz["rest_devices"]
                        if len(self.devicestates) == 0:
                            for k in rest_devices["devices"]:
                                if (
                                    len(rest_devices["devices"][k].get("effect", {}))
                                    > 0
                                ):
                                    effect = rest_devices["devices"][k].get("effect")
                                    power = True
                                else:

                                    effect = {}
                                    power = False
                                self.devicestates[k] = {
                                    "power": power,
                                    "effect": effect,
                                }
                    else:
                        logging.warning(
                            "CANT CONNECT TO LEDFX - DEVICES: %s", resp_devices.status
                        )

            except aiohttp.ClientConnectorError as e:
                logging.warning("CANT CONNECT TO LEDFX - DEVICES - 2: %s", e)

            try:
                async with session.get(url3, ssl=False) as resp_scenes:
                    if resp_scenes.status == 200:
                        rest_scenes = await resp_scenes.json()
                        yz["rest_scenes"] = rest_scenes
                    else:
                        logging.warning(
                            "CANT CONNECT TO LEDFX - SCENES: %s", resp_scenes.status
                        )

            except aiohttp.ClientConnectorError as e:
                logging.warning("CANT CONNECT TO LEDFX - SCENES - 2: %s", e)

            try:
                async with session.get(url4, ssl=False) as resp_virtuals:
                    if resp_virtuals.status == 200:
                        rest_virtuals = await resp_virtuals.json()
                        yz["rest_virtuals"] = rest_virtuals
                        self.virtuals = yz["rest_virtuals"]
                        # logging.warning("VIRTUALS: %s", rest_virtuals)
                    else:
                        logging.warning(
                            "CANT CONNECT TO LEDFX - VIRTUALS: %s", resp_virtuals.status
                        )

            except aiohttp.ClientConnectorError as e:
                logging.warning("CANT CONNECT TO LEDFX - VIRTUALS - 2: %s", e)
            # async with session.get(url, ssl=False) as resp:
            #     rest_info = await resp.json()
            #     yz["rest_info"] = rest_info

            # async with session.get(url2, ssl=False) as resp_devices:
            #     rest_devices = await resp_devices.json()
            #     yz["rest_devices"] = rest_devices
            #     self.devices = yz["rest_devices"]
            #     # logging.warning("INTERNAL STATES b4: %s", self.devicestates)
            #     if len(self.devicestates) == 0:
            #         for k in rest_devices["devices"]:
            #             # logging.warning("NOWWW: %s", k)
            #             # logging.warning("THENN: %s", rest_devices['devices'][k])
            #             if len(rest_devices["devices"][k].get("effect", {})) > 0:
            #                 # logging.warning("GOT EFFECT FROM LEDFX: %s", rest_devices['devices'][k].get('effect'))
            #                 effect = rest_devices["devices"][k].get("effect")
            #                 power = True
            #             else:

            #                 effect = {}
            #                 power = False
            #             self.devicestates[k] = {
            #                 "power": power,
            #                 "effect": effect,  # self.devicestates[k].get('effect', {})
            #             }
            #     # logging.warning("INTERNAL STATES after: %s", self.devicestates)

            # async with session.get(url3, ssl=False) as resp_scenes:
            #     rest_scenes = await resp_scenes.json()
            #     yz["rest_scenes"] = rest_scenes

        if rest_info is not None:
            self.connected = True

        return {
            "info": rest_info,
            "devices": rest_devices,
            "virtuals": rest_virtuals,
            "scenes": rest_scenes,
            "show_subdevices": self.thesubdevices,
        }

    async def async_set_transition_time(self, time):
        self._transition_time = time

    async def async_change_something(self, state):
        loop = asyncio.get_event_loop()
        async with aiohttp.ClientSession(loop=loop, trust_env=True) as session:
            # logging.warning(
            #     "SERVER COMMAND --- %s ------ %s ------ %s ------ %s --- ",
            #     self.thestart_method,
            #     self.thestop_method,
            #     self.thestart_body,
            #     self.thestop_body,
            # )
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
                    ) as resp_stop:
                        logging.debug("start: %s", resp_stop)
                if self.thestop_method == "DELETE":
                    async with session.delete(
                        "http://" + self.thestop, ssl=False
                    ) as resp_stop:
                        logging.debug("start: %s", resp_stop)
                if self.thestop_method == "PUT":
                    async with session.put(
                        "http://" + self.thestop, json=self.thestop_body, ssl=False
                    ) as resp_stop:
                        logging.debug("start: %s", resp_stop)
                if self.thestop_method == "POST":
                    async with session.post(
                        "http://" + self.thestop, json=self.thestop_body, ssl=False
                    ) as resp_stop:
                        logging.debug("start: %s", resp_stop)

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

    async def async_blade_off(self):
        b = OrderedDict(self.devices.get("devices"))
        for key in sorted(b):
            # logging.warning(
            #     "BLADE OFF internal --- %s --- %s --- %s",
            #     self.devices.get("devices").get(key).get("config").get("name"),
            #     self.devices.get("devices").get(key).get("config").get("ip_address"),
            #     self.devices.get("devices").get(key).get("config").get("pixel_count"),
            # )
            for i in range(
                self.devices.get("devices").get(key).get("config").get("pixel_count")
            ):

                m = []
                m.append(1)
                m.append(255)
                m.append(i)
                m.extend([0, 0, 0])
                m = bytes(m)
                _sock.sendto(
                    m,
                    (
                        self.devices.get("devices")
                        .get(key)
                        .get("config")
                        .get("ip_address"),
                        21324,
                    ),
                )
                sleep(0.02)

        return None

    async def async_blade_on(self, state):
        # logging.warning(
        #     "CHECK THIS: %s ------------- %s",
        #     self.virtuals,
        #     state,
        # )

        testcolor = color_hs_to_RGB(state.get("hs_color")[0], state.get("hs_color")[1])
        b = OrderedDict(self.devices.get("devices"))
        for key in sorted(b):
            # logging.warning(
            #     "BLADE ON internal --- %s --- %s --- %s",
            #     self.devices.get("devices").get(key).get("config").get("name"),
            #     self.devices.get("devices").get(key).get("config").get("ip_address"),
            #     self.devices.get("devices").get(key).get("config").get("pixel_count"),
            # )
            for i in range(
                self.devices.get("devices").get(key).get("config").get("pixel_count")
            ):

                m = []
                m.append(1)
                m.append(255)
                m.append(i)
                m.extend(testcolor)
                m = bytes(m)
                _sock.sendto(
                    m,
                    (
                        self.devices.get("devices")
                        .get(key)
                        .get("config")
                        .get("ip_address"),
                        21324,
                    ),
                )
                sleep(self._transition_time)
        self._hs = state.get("hs_color")
        return None

    async def async_virtual_on(self, state):
        # logging.warning("CHECK THIS: %s", state)

        testcolor = color_hs_to_RGB(state.get("hs_color")[0], state.get("hs_color")[1])
        b = self.virtuals.get("virtuals").get("list")[0].get("items")
        c = sorted(b, key=lambda x: x.get("order_number"))
        # logging.warning("B: %s \n C: %s \n\n", b, c)
        for key in c:
            # logging.warning(
            #     "VIRTUAL ON internal --- %s: %s",
            #     key.get("name"),
            #     key.get("pixel_density"),
            # )
            for i in range(key.get("used_pixel")):

                m = []
                m.append(1)
                m.append(255)
                if key.get("invert") == True:
                    m.append(key.get("led_end") - i - 1)
                else:
                    m.append(key.get("led_start") + i - 1)
                m.extend(testcolor)
                m = bytes(m)
                _sock.sendto(
                    m,
                    (
                        key.get("config").get("ip_address"),
                        21324,
                    ),
                )
                if key.get("pixel_density") is not None:
                    sleep((60 / key.get("pixel_density")) * self._transition_time)
                else:
                    sleep(self._transition_time)
        self._hs = state.get("hs_color")
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
        theblade_light,
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
        self.theblade_light = theblade_light
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
            theblade_light,
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
            scenes = {}
            devices = {}
            virtuals = {}
            # logging.warning("UPDATING %s", data)
            if data != {}:

                scenes = data.get("scenes").get("scenes")
                devices = data.get("devices").get("devices")
                if scenes != {}:
                    logging.warning("UPDATING WTF %s", data)
                    self.scenes = scenes
                    self.devices = devices
                    self.number_scenes = len(scenes)
                    self.lost = False
                    self.connected = True
                    self.available = True

                virtuals = data.get("virtuals").get("virtuals")
                if virtuals != {}:
                    # logging.warning("YYYEEEEESSSS %s", virtuals)
                    self.virtuals = virtuals
                return data

            if self.lost is not True:
                logging.warning("UPDATE FAILED %s", data)
                self.connected = False
                self.available = False
                self.lost = True
                raise PlatformNotReady
        except Exception as exception:
            # raise PlatformNotReady
            # raise UpdateFailed(exception)
            # logging.warning("UPDATE FAILED 2 %s", exception)
            if hasattr(self, "lost"):
                if self.lost is not True:
                    self.connected = False
                    self.available = False
                    self.lost = True
                    raise UpdateFailed(exception)
            return {
                "info": {"name": "Not Ready", "version": "1.0"},
                "scenes": {"scenes": {}},
                "devices": {"devices": {}},
                "virtuals": {"virtuals": {}},
            }


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