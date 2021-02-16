# Smartmeter Reader
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs) ![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/hombrelab/home-assistant-smartmeter-reader) ![GitHub commit activity](https://img.shields.io/github/last-commit/hombrelab/home-assistant-smartmeter-reader)  

This [Smartmeter Reader]((https://github.com/hombrelab/home-assistant-smartmeter-reader)) custom component for [home-assistant](https://www.home-assistant.io) is an alternative to 2 existing integrations:  
- [DSMR](https://www.home-assistant.io/integrations/dsmr)
- [DSMR Reader](https://www.home-assistant.io/integrations/dsmr_reader)  

REMARK: the smartmeter-reader component is based on the above mentioned integrations.  
I wanted the extended functionality of the DSMR integration that the DSMR-reader integration does not offer.  

The sensor does not (yet) have support for the Belgian market.

The Hombre Smartmeter application publishes a JSON object including the telegram to homeassistant the smartmeter service.
The Hombre Smartmeter application als sends the raw telegram to the DSMR-Reader by [dsmr-reader](https://github.com/dennissiemensma/dsmr-reader).  

```json
{
    "telegram": "/ISk5\\2MT382-1000\r\n\r\n0-0:96.1.1(4B384547303034303436333935353037)\r\n1-0:1.8.1(12345.678*kWh)\r\n1-0:1.8.2(12345.678*kWh)\r\n1-0:2.8.1(12345.678*kWh)\r\n1-0:2.8.2(12345.678*kWh)\r\n0-0:96.14.0(0002)\r\n1-0:1.7.0(001.19*kW)\r\n1-0:2.7.0(000.00*kW)\r\n0-0:17.0.0(016*A)\r\n0-0:96.3.10(1)\r\n0-0:96.13.1(303132333435363738)\r\n0-0:96.13.0(303132333435363738393A3B3C3D3E3F303132333435363738393A3B3C3D3E3F303132333435363738393A3B3C3D3E3F303132333435363738393A3B3C3D3E3F303132333435363738393A3B3C3D3E3F)\r\n0-1:96.1.0(3232323241424344313233343536373839)\r\n0-1:24.1.0(03)\r\n0-1:24.3.0(090212160000)(00)(60)(1)(0-1:24.2.1)(m3)\r\n(00006.001)\r\n0-1:24.4.0(1)\r\n!\r\n"
}
```

### Installation
Copy this folder to `<config_dir>/custom_components/dsmr_reader/` or use [hacs](https://github.com/custom-components/hacs) and point it to this [GitHub repository](https://github.com/hombrelab/home-assistant-smartmeter-reader).  

Setup is done through the integration page:
- **dsmr_version**: _required_  the version of the telegram default=2.2
- **precision**: _required_ the precision to show the readings with default=3
- **timezone**: _required_  the timezon you are in default=Europe/Amsterdam
