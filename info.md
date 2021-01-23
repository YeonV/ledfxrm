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

- [LedFx](https://github.com/LedFx/LedFx/tree/dev) > v0.9.0
  - with at least one scene setup
  - the ledfx config.yaml file defines your host as 127.0.0.1 by default. The host needs to be changed to  0.0.0.0 in order for this integration to function properly
  - [LedFx Docs](https://ledfx.readthedocs.io/en/latest/)
- [hass](https://github.com/home-assistant) - (HomeAssistant)
- [HACS](https://hacs.xyz/) - (HomeAssistantCommunityStore)

{% if not installed %}

## Installation

- Click "Install"
- Restart Home Assistant for the changes to take effect
- In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "LedFx Remote"
- Configuration is done in the UI

{% endif %}

**[Step by Step Installation - Images-Guide](https://github.com/YeonV/ledfxrm/wiki/Step-by-Step-Images)**

## Credits

[![ledfx-github](https://img.shields.io/badge/Github-LedFx-blue.svg?logo=github&logoColor=white)](https://github.com/LedFx/LedFx/tree/dev) [![ledfx-discord](https://img.shields.io/badge/Discord-LedFx-blue.svg?logo=discord&logoColor=white)](https://discord.gg/xyyHEquZKQ) [![wled-github](https://img.shields.io/badge/Github-WLED-blue.svg?logo=github&logoColor=white)](https://github.com/Aircoookie/WLED) [![wled-discord](https://img.shields.io/badge/Discord-WLED-blue.svg?logo=discord&logoColor=white)](https://discord.gg/KuqP7NE)

[![homeassistant-github](https://img.shields.io/badge/Github-HomeAssistant-blue.svg?logo=github&logoColor=white)](https://github.com/home-assistant) [![hacs-github](https://img.shields.io/badge/Github-HACS-blue.svg?logo=github&logoColor=white)](https://github.com/hacs/) [![blueprint-github](https://img.shields.io/badge/Github-blueprint-blue.svg?logo=github&logoColor=white)](https://github.com/custom-components/blueprint)

## Special Thanks

[![frenck](https://img.shields.io/badge/Github-Frenck-blue.svg?logo=github&logoColor=white)](https://github.com/frenck) [![THATDONFC](https://img.shields.io/badge/Github-THATDONFC-blue.svg?logo=github&logoColor=white)](https://github.com/THATDONFC) [![on](https://img.shields.io/badge/Github-On-blue.svg?logo=github&logoColor=white)](https://github.com/OnFreund) [![Tinkerer](https://img.shields.io/badge/Github-Tinkerer-blue.svg?logo=github&logoColor=white)](https://github.com/DubhAd)
