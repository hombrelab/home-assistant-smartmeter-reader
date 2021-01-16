#  Copyright (c) 2021 Hombrelab <me@hombrelab.com>

# Constants for the Smartmeter Reader component

import pytz

from dsmr_parser import obis_references as obis_ref
from datetime import timedelta

DOMAIN = "smartmeter_reader"
UUID = "1531923f-ed21-4e72-8def-a7e900c71c8e"

SW_MANUFACTURER = "Hombrelab"
SW_NAME = "Smartmeter Reader"
SW_VERSION = "2.0.000"

TITLE = "Home"

# labels
DSMRVERSION = 'dsmrversion'
PRECISION = 'precision'
TOPIC = "topic"

# default values
DEFAULT_DSMRVERSION = "2.2"
DEFAULT_PRECISION = 3
DEFAULT_TOPIC = "home-assistant/smartmeter/telegram"

AMS_TIMEZONE = pytz.timezone("Europe/Amsterdam")

DSMRVERSIONS = [
    "5B",
    "5",
    "4",
    "2.2"
]

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
