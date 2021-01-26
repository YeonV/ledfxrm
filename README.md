# LedFx ReMote for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-blue.svg?logo=home-assistant&logoColor=white)](https://github.com/custom-components/hacs) [![hass_badge](https://img.shields.io/badge/HASS-Integration-blue.svg?logo=home-assistant&logoColor=white)](https://github.com/custom-components/hacs) ![state](https://img.shields.io/badge/STATE-beta-blue.svg?logo=github&logoColor=white) ![version](https://img.shields.io/github/v/release/YeonV/ledfxrm?label=VERSION&logo=git&logoColor=white) [![license](https://img.shields.io/badge/LICENSE-MIT-blue.svg?logo=github&logoColor=white)](https://github.com/YeonV/ledfxrm/blob/main/LICENSE) [![creator](https://img.shields.io/badge/CREATOR-Yeon-blue.svg?logo=github&logoColor=white)](https://github.com/YeonV) [![creator](https://img.shields.io/badge/A.K.A-Blade-darkred.svg?logo=github&logoColor=white)](https://github.com/YeonV)
![version](https://img.shields.io/github/workflow/status/YeonV/ledfxrm/Cron%20actions?label=HACS%20Cron&logo=github-actions&logoColor=white)

---

![logo](https://user-images.githubusercontent.com/28861537/99007089-cac6e100-2543-11eb-99d3-01bf0b487d29.png)

[Custom Integration](https://github.com/hacs/integration) for [Home Assistant](https://github.com/home-assistant) to control any (local/remote) [LedFx-server](https://github.com/LedFx/LedFx)

---

## Main Features

### LedFx Remote

- Select your LedFx scene from inside Home Assistant!
- Display the number of scenes/devices/pixels connected to LedFx
- Start and stop the LedFx server (custom Endpoint required!)

### LedFx Device Remote

- Toggle the power for devices configured in LedFx
- Display number of pixels per device
- Display IP per device
- Display current running effect-name

| Default | With Devices |
|:-------:|:------------:|
| ![tile](https://github.com/YeonV/ledfxrm/raw/main/docs/tile.png) | ![tile_adv](https://github.com/YeonV/ledfxrm/raw/main/docs/tile_adv.png) |

## Requirements:

- [LedFx](https://github.com/LedFx/LedFx/tree/dev)
  - minimum version: v0.9.0 (so atm you need the dev-branch)
  - with at least one scene setup
  - the ledfx config.yaml file defines your host as 127.0.0.1 by default. The host needs to be changed to  0.0.0.0 in order for this integration to function properly.
  - [LedFx Docs](https://ledfx.readthedocs.io/en/latest/)
- [hass](https://github.com/home-assistant) - (HomeAssistant)
- [HACS](https://hacs.xyz/) - (HomeAssistantCommunityStore)

## QuickStart

- Add Repo to HACS:

  - Navigate to HACS in Home Assistant
  - Select "Integrations"
  - Select the menu hamburger in the upper right of the screen
  - Select "Custsom repositories"
  - Add the url for this repository and select integration as the cattegory

- Install integration via HACS:

  - The integration should now be visible, select "Install"
  - Restart Home Assistant for the changes to take effect

- Add integration to Home Assistant:

  - In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "LedFx Remote"

- Configuration is done in the UI
  - Add the IP of the machine running LedFx to the "Host" field
  - Leave the default port of 8888 or change it to match your configuration
    - (LedFx Server needs to be online and running)
    - no changes are needed in configuration.yaml
    - all Settings are handled via UI
  - Open the light entity and change your scenes :)

**[Step by Step Installation - Images-Guide](https://github.com/YeonV/ledfxrm/wiki/Step-by-Step-Images)**

## Detailed Features

- Everything configurable via UI :)
- AutoCreate Entities with `GET` Informations from all LedFx-API-Endpoints:
  - Binary Sensor (Is LedFx online?)
  - Devices Sensor (Number of Devices inside LedFx)
  - Scenes Sensor (Number of Scenes inside LedFx)
  - Pixels Sensor (Number of Pixels inside LedFx)
  - Switch (if start/stop is set in config - custom `GET`-call)
  - Light
    - EffectList (Filled with scenes from LedFx)
    - Off->On - just toggles a manual sync (double click the switch)
- EffectList-Change will fire LedFx via `PUT`
- Scan_intervall in seconds via UI:
  - Note: This also defines how long you can interact with it (start server), after a disconnect (kill server)
  - Recommendation: set to a high number. Polling is only to get changes made inside LedFx.
- SubDevices: (config via UI)
  - Get the Devices running inside LedFx including their states
  - ON / OFF Button
    - OFF Button saves the current effect running on the current device
    - ON Button will use that state if available otherwise sends "Gradient"
- Start/Stop Server:
  - Set custom Endpoints for Start and Stop
  - Configurable methods: `GET`, `DELETE`, `PUT`, `POST`
  - Configurable body: json (untested)
- NEW: Add Blade-Light: 1 effect throught multiple devices

## Upcoming Features


- Make also use of the after setup config flow (options)
  - Allow editing of setup-settings
  - Allow disable poll (If you have everything setup in ledfx, there is no need to poll for new infos all the time)
  - Make fallback "gradient" somehow editable for the user

## Screens

<details>
<summary>show</summary>
<p>
Default:

![ledfx-remote](https://user-images.githubusercontent.com/28861537/100016798-46dde600-2dda-11eb-90c5-8229024a2e39.png)

![setup](https://github.com/YeonV/ledfxrm/raw/main/docs/setup.png)

![main](https://github.com/YeonV/ledfxrm/raw/main/docs/main.png)

![scene_selector_1](https://github.com/YeonV/ledfxrm/raw/main/docs/scene_selector_1.png)

![scene_selector_2](https://github.com/YeonV/ledfxrm/raw/main/docs/scene_selector_2.png)

With Subdevices:

![setup_adv](https://github.com/YeonV/ledfxrm/raw/main/docs/setup_adv.png)

![main_adv](https://github.com/YeonV/ledfxrm/raw/main/docs/main_adv.png)

![subdevices](https://github.com/YeonV/ledfxrm/raw/main/docs/subdevice.png)

</p>
</details>

## Credits

[![ledfx-github](https://img.shields.io/badge/Github-LedFx-blue.svg?logo=github&logoColor=white)](https://github.com/LedFx/LedFx/tree/dev/ledfx) [![ledfx-discord](https://img.shields.io/badge/Discord-LedFx-blue.svg?logo=discord&logoColor=white)](https://discord.gg/wJ755dY) [![wled-github](https://img.shields.io/badge/Github-WLED-blue.svg?logo=github&logoColor=white)](https://github.com/Aircoookie/WLED) [![wled-discord](https://img.shields.io/badge/Discord-WLED-blue.svg?logo=discord&logoColor=white)](https://discord.gg/KuqP7NE)

[![homeassistant-github](https://img.shields.io/badge/Github-HomeAssistant-blue.svg?logo=github&logoColor=white)](https://github.com/home-assistant) [![hacs-github](https://img.shields.io/badge/Github-HACS-blue.svg?logo=github&logoColor=white)](https://github.com/hacs/) [![blueprint-github](https://img.shields.io/badge/Github-blueprint-blue.svg?logo=github&logoColor=white)](https://github.com/custom-components/blueprint)

## Special Thanks

[![frenck](https://img.shields.io/badge/Github-Frenck-blue.svg?logo=github&logoColor=white)](https://github.com/frenck) [![THATDONFC](https://img.shields.io/badge/Github-THATDONFC-blue.svg?logo=github&logoColor=white)](https://github.com/THATDONFC) [![on](https://img.shields.io/badge/Github-On-blue.svg?logo=github&logoColor=white)](https://github.com/OnFreund) [![Tinkerer](https://img.shields.io/badge/Github-Tinkerer-blue.svg?logo=github&logoColor=white)](https://github.com/DubhAd)
