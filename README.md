# Smartmeter Reader
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs) ![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/hombrelab/home-assistant-smartmeter-reader) ![GitHub commit activity](https://img.shields.io/github/last-commit/hombrelab/home-assistant-smartmeter-reader)  

This [Smartmeter Reader]((https://github.com/hombrelab/home-assistant-smartmeter-reader)) custom component for [home-assistant](https://www.home-assistant.io) is an alternative to 2 existing integrations:  
- [DSMR](https://www.home-assistant.io/integrations/dsmr)
- [DSMR Reader](https://www.home-assistant.io/integrations/dsmr_reader)  

The smartmeter-reader sensor subscribes to **RAW Telegram MQTT data** sent by [dsmr-reader](https://github.com/dennissiemensma/dsmr-reader).  

REMARK: the smartmeter-reader component is based on the above mentioned integrations.  
I wanted the extended functionality of the DSMR integration that the DSMR-reader integration does not offer.  
At the same time I wanted to make use of MQTT.

The sensor does not (yet) have support for the Belgian market.

### Installation
Copy this folder to `<config_dir>/custom_components/dsmr_reader/` or use [hacs](https://github.com/custom-components/hacs) and point it to this [GitHub repository](https://github.com/hombrelab/home-assistant-smartmeter-reader).  

Setup is done through the integration page:
- **topic**: _required_ MQTT topic the component has to subscribe to
- **precision**: _required_ the precision to show the readings with 
- **dsmr_version**: _required_  the version of the telegram
