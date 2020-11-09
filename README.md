# Removed ALL functionality!!
# Refactoring to be a real HomAssistant Integration installable via HACS

---

last working state: https://github.com/YeonV/ledfxrm/commit/43a0c9dd9746070e5744d202ebd4aead4bbfa05e

---

# LedFX Remote for HomeAssistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)


A proof of concept, for controlling a remote [ledfx-server](https://github.com/ahodges9/LedFx) via [Home Assistant](https://github.com/home-assistant)

### How to

- copy this folder inside custom_compontents
- at the moment a lot of manual work is needed:
  - add `ledfxrm:` to your configuration.yml
  - edit this __init__.py and change your IP
  - inside this file there are comment-snippets
  - create the rest_command, input_select and automation as showed in those snippets
  - sent a MQTT message to `blade/ledfx/info` to trigger the sync  
  
Refactoring this sh.t asap

### What does it do?

When the sync runs, 3 API-endpoints of ledfx are fetched: info, devices, scenes
A Summary-Entity is created with those infos:

![summary](https://user-images.githubusercontent.com/28861537/98367840-9c726e80-2036-11eb-9121-6b8aaddbbdfd.png)

A picklist is created/upadted and filled with the scenes

![dropdown](https://user-images.githubusercontent.com/28861537/98367833-98465100-2036-11eb-8a6b-ad538dd31960.png)

=> changing the dropdown will activate the selected scene.

### Credits

[Tinkerer](https://github.com/DubhAd/)

https://github.com/ahodges9/LedFx/tree/dev/ledfx

https://github.com/Aircoookie/WLED

https://github.com/custom-components/blueprint

https://github.com/hacs/

https://github.com/home-assistant
