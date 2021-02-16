#  Copyright (c) 2021 Hombrelab <me@hombrelab.com>

import voluptuous as vol
from dsmr_parser import obis_references as obis_ref
from homeassistant.helpers import config_validation as cv

DOMAIN = "smartmeter"
UUID = "428c5946-7a5a-488b-bda3-9a5cdbcd506b"

SW_MANUFACTURER = "Hombrelab"
SW_NAME = "Smartmeter Reader"
SW_MODEL = "websocket"
SW_VERSION = "2.0.008"

TITLE = "Home"

SERVICE = "consume"

# config keys
DSMRVERSION = 'dsmrversion'
PRECISION = 'precision'
TIMEZONE = 'timezone'

# config values
DSMRVERSION_VALUE = "2.2"
PRECISION_VALUE = 3
TIMEZONE_VALUE = "Europe/Amsterdam"

DSMRVERSIONS = [
    "5B",
    "5",
    "4",
    "2.2"
]

GAS_CONSUMPTION_NAME = 'Smartmeter Gas Consumption'
GAS_HOURLY_CONSUMPTION_NAME = 'Smartmeter Hourly Gas Consumption'
GAS_HOURLY_LAST_UPDATE_NAME = 'Smartmeter Hourly Gas Last Update'

# list of entities
ENTITIES = [
    [
        'Smartmeter Power Consumption',
        'mdi:flash',
        obis_ref.CURRENT_ELECTRICITY_USAGE
    ],
    [
        'Smartmeter Power Production',
        'mdi:flash',
        obis_ref.CURRENT_ELECTRICITY_DELIVERY
    ],
    [
        'Smartmeter Power Tariff',
        'mdi:flash',
        obis_ref.ELECTRICITY_ACTIVE_TARIFF
    ],
    [
        'Smartmeter Power Consumption (low)',
        'mdi:flash',
        obis_ref.ELECTRICITY_USED_TARIFF_1
    ],
    [
        'Smartmeter Power Consumption (normal)',
        'mdi:flash',
        obis_ref.ELECTRICITY_USED_TARIFF_2
    ],
    [
        'Smartmeter Power Production (low)',
        'mdi:flash',
        obis_ref.ELECTRICITY_DELIVERED_TARIFF_1
    ],
    [
        'Smartmeter Power Production (normal)',
        'mdi:flash',
        obis_ref.ELECTRICITY_DELIVERED_TARIFF_2
    ],
    [
        'Smartmeter Power Consumption Phase L1',
        'mdi:flash',
        obis_ref.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE
    ],
    [
        'Smartmeter Power Consumption Phase L2',
        'mdi:flash',
        obis_ref.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE
    ],
    [
        'Smartmeter Power Consumption Phase L3',
        'mdi:flash',
        obis_ref.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE
    ],
    [
        'Smartmeter Power Production Phase L1',
        'mdi:flash',
        obis_ref.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE
    ],
    [
        'Smartmeter Power Production Phase L2',
        'mdi:flash',
        obis_ref.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE
    ],
    [
        'Smartmeter Power Production Phase L3',
        'mdi:flash',
        obis_ref.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE
    ],
    [
        'Smartmeter Long Power Failure Count',
        'mdi:flash-off',
        obis_ref.LONG_POWER_FAILURE_COUNT
    ],
    [
        'Smartmeter Voltage Sags Phase L1',
        'mdi:pulse',
        obis_ref.VOLTAGE_SAG_L1_COUNT
    ],
    [
        'Smartmeter Voltage Sags Phase L2',
        'mdi:pulse',
        obis_ref.VOLTAGE_SAG_L2_COUNT
    ],
    [
        'Smartmeter Voltage Sags Phase L3',
        'mdi:pulse',
        obis_ref.VOLTAGE_SAG_L3_COUNT
    ],
    [
        'Smartmeter Voltage Swells Phase L1',
        'mdi:pulse',
        obis_ref.VOLTAGE_SWELL_L1_COUNT
    ],
    [
        'Smartmeter Voltage Swells Phase L2',
        'mdi:pulse',
        obis_ref.VOLTAGE_SWELL_L2_COUNT
    ],
    [
        'Smartmeter Voltage Swells Phase L3',
        'mdi:pulse',
        obis_ref.VOLTAGE_SWELL_L3_COUNT
    ],
    [
        'Smartmeter Voltage Phase L1',
        'mdi:flash',
        obis_ref.INSTANTANEOUS_VOLTAGE_L1
    ],
    [
        'Smartmeter Voltage Phase L2',
        'mdi:flash',
        obis_ref.INSTANTANEOUS_VOLTAGE_L2
    ],
    [
        'Smartmeter Voltage Phase L3',
        'mdi:flash',
        obis_ref.INSTANTANEOUS_VOLTAGE_L3
    ],
    [
        'Smartmeter Current Phase L1',
        'mdi:flash',
        obis_ref.INSTANTANEOUS_CURRENT_L1
    ],
    [
        'Smartmeter Current Phase L2',
        'mdi:flash',
        obis_ref.INSTANTANEOUS_CURRENT_L2
    ],
    [
        'Smartmeter Current Phase L3',
        'mdi:flash',
        obis_ref.INSTANTANEOUS_CURRENT_L3
    ],
    [
        'Smartmeter Power Consumption (both)',
        'mdi:flash',
        obis_ref.ELECTRICITY_USED_TARIFF_1
    ],
]

ENTITIES_SCHEMA = vol.Schema(
    {
        vol.Required('telegram'): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(DSMRVERSION, default=DSMRVERSION_VALUE): cv.string,
                vol.Required(PRECISION, default=PRECISION_VALUE): int,
                vol.Required(TIMEZONE, default=TIMEZONE_VALUE): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA
)
