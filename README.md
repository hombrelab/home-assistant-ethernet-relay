# Ethernet Relay Switch
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs) ![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/hombrelab/home-assistant-ethernet-relay) ![GitHub commit activity](https://img.shields.io/github/last-commit/hombrelab/home-assistant-ethernet-relay)  

The [ethernet-relay](https://github.com/hombrelab/home-assistant-ethernet-relay) custom component for [home-assistant](https://www.home-assistant.io) is created to switch the [ds378 Devantech Programmable Ethernet Module](https://www.robot-electronics.co.uk/ds378.html) with 8 relays.

I needed a way to switch my [Occhio luminaires](https://www.occhio.de), controlled using bluetooth technology from [Casambi](https://www.casambi.com).  
I could not find an integration or 'out of the box' technology for that so I combined the ds378 with the [SC-TI-CAS](https://www.casambi.nl/a-52395018/schakelaars/sc-ti-cas/#description)

I am pretty sure it will work with the smaller and larger ones as well but I am not sure about the other ethernet modules.

### Preparations
You have to use TCP/IP in Binary mode on the ds378.

### Installation
Copy this folder to `<config_dir>/custom_components/ethernet_relay/` or use [hacs](https://github.com/custom-components/hacs) and point it to this [GitHub repository](https://github.com/hombrelab/home-assistant-ethernet-relay).  

Setup is done through the integration page:  
- **name**: _required_ (you can have more than one setup so choose a unique name)  
- icon: _optional_  
- host: _required_ host ipaddress or hostname of the module  
- port: _required_ port of the module  
- model: _optional_ module model 
- relays: _required_ number of relays the module has  

This is how I created a light template:

```yaml
---
- platform: template
  lights:
    occhio_living:
      friendly_name: Occhio living
      turn_on:
        - service: ethernet_relay.set_pulse
          entity_id: switch.occhio_switch_1
          data:
            pulse: 500
        - service: switch.turn_on
          entity_id: switch.occhio_switch_1
      turn_off:
        - service: ethernet_relay.set_pulse
          entity_id: switch.occhio_switch_1
          data:
            pulse: 500
        - service: switch.turn_off
          entity_id: switch.occhio_switch_1
```