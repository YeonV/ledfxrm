# LedFX ReMote for HomeAssistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-blue.svg)](https://github.com/custom-components/hacs) 
![state](https://img.shields.io/badge/STATE-alpha-blue.svg) 
![version](https://img.shields.io/badge/VERSION-0.1.0-blue.svg) 
[![license](https://img.shields.io/badge/LICENSE-MIT-blue.svg)](https://github.com/YeonV/ledfxrm/blob/main/LICENSE) 
[![creator](https://img.shields.io/badge/CREATOR-Yeon-blue.svg)](https://github.com/YeonV) 
[![creator](https://img.shields.io/badge/a.k.a-Blade-blue.svg)](https://github.com/YeonV) 

---

![logo](https://user-images.githubusercontent.com/28861537/99007089-cac6e100-2543-11eb-99d3-01bf0b487d29.png)


### [Custom Integration](https://github.com/hacs/integration) for [Home Assistant](https://github.com/home-assistant) to control a any (local/remote) [LedFX-server](https://github.com/ahodges9/LedFx)
---

# Features

- Everything configurable via UI
- AutoConnect to 3 LedFX-Rest-API-Endpoints
- Automatically `GET` Informations from all Endpoints
- AutoCreate Entities:
  - Binary Sensor (Is LedFX online?)
  - Devices Sensor (Number of Devices inside LedFX)
  - Scenes Sensor (Number of Scenes inside LedFX)
  - Switch (Upcoming feature! only logging functionality atm)
  - Light 
    - EffectList (Filled with scenes from LedFX)
    - On/Off mirrors Switch - upcoming feature
- EffectList-Change will fire LedFX via `PUT`

# Upcoming Features

- Implement Server Start/Stop Commands
- Make also use of the after setup config flow (options)
  - Allow editing of setup-settings
  - Make SCAN_INTERVAL editable via UI
  - Allow disable poll (If you have everything setup in ledfx, there is no need to poll for new infos all the time)
  - Create a Sync-Button to manually trigger a request
  - Add more `POST` and `PUT` calls

# Requirements:

- [LedFX](https://github.com/ahodges9/LedFx) with at least one scene setup
- [hass](https://github.com/home-assistant) - (HomeAssistant)
- [HACS](https://hacs.xyz/) - (HomeAssistantCommunityStore)

# QuickStart

- Install via Hacs
- Goto Hass-Config-Integration -> Add -> Ledfx Remote
- Fill Ip & port (LedFX Server needs to online)
  - no changes in configuration.yaml needed 
  - all Settings are handled via UI
- Open the light entity and change your scenes :)

# [Step by Step - Images-Guide](https://github.com/YeonV/ledfxrm/wiki/Step-by-Step-Images)

# Screens

![integration](docs/integration.png)

![main](docs/main.png)

![scenes](docs/scenes.png)

# Credits

[![ledfx-github](https://img.shields.io/badge/Github-LedFX-blue.svg)](https://github.com/ahodges9/LedFx/tree/dev/ledfx)
[![ledfx-discord](https://img.shields.io/badge/Discord-LedFX-blue.svg)](https://discord.gg/wJ755dY)

[![wled-github](https://img.shields.io/badge/Github-WLED-blue.svg)](https://github.com/Aircoookie/WLED)
[![wled-discord](https://img.shields.io/badge/Discord-WLED-blue.svg)](https://discord.gg/KuqP7NE)

[![blueprint-github](https://img.shields.io/badge/Github-HomeAssistant-blue.svg)](https://github.com/home-assistant)

[![blueprint-github](https://img.shields.io/badge/Github-HACS-blue.svg)](https://github.com/hacs/)

[![blueprint-github](https://img.shields.io/badge/Github-blueprint-blue.svg)](https://github.com/custom-components/blueprint)


# Special Thanks

[![frenck](https://img.shields.io/badge/Github-Frenck-blue.svg)](https://github.com/frenck)

[![on](https://img.shields.io/badge/Github-On-blue.svg)](https://github.com/OnFreund)

[![Tinkerer](https://img.shields.io/badge/Github-Tinkerer-blue.svg)](https://github.com/DubhAd)
