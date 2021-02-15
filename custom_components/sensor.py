#  Copyright (c) 2021 Hombrelab <me@hombrelab.com>

import asyncio
import logging

import pytz
from dsmr_parser import obis_references as obis_ref
from dsmr_parser import telegram_specifications
from dsmr_parser.parsers import TelegramParser
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import HomeAssistantType

from . import SmartmeterDevice
from .const import (
    DOMAIN,
    UUID,

    SERVICE,

    DSMRVERSION,
    PRECISION,
    TIMEZONE,

    ENTITIES,
    ENTITIES_SCHEMA,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry, async_add_entities):
    """set up entities based on a config entry"""

    _version = entry.data[DSMRVERSION]
    _precision = entry.data[PRECISION]
    _timezone = pytz.timezone(entry.data[TIMEZONE])

    # Protocol version specific obis
    if _version in "4":
        _gas_obis = obis_ref.HOURLY_GAS_METER_READING
        _parser = TelegramParser(telegram_specifications.V4)
    elif _version in "5":
        _gas_obis = obis_ref.HOURLY_GAS_METER_READING
        _parser = TelegramParser(telegram_specifications.V5)
    elif _version in ("5B",):
        _gas_obis = obis_ref.BELGIUM_HOURLY_GAS_METER_READING
        _parser = TelegramParser(telegram_specifications.BELGIUM_FLUVIUS)
    else:
        _gas_obis = obis_ref.GAS_METER_READING
        _parser = TelegramParser(telegram_specifications.V2_2)

    # Define mapping for electricity mappings
    elements = ENTITIES
    elements += [
        [
            'Smartmeter Gas Consumption',
            'mdi:fire',
            _gas_obis
        ],
    ]

    # generate smart entities
    entities = [
        ElecticityEntity(name, icon, obis, _precision, _timezone, _parser)
            for name, icon, obis in elements
    ]

    elements = [
        [
            'Smartmeter Hourly Gas Consumption',
            'mdi:fire',
            _gas_obis
        ],
        [
            'Smartmeter Hourly Gas Last Update',
            'mdi:update',
            _gas_obis
        ],
    ]

    # generate gas entities
    entities += [
        GasEntity(name, icon, obis, _precision, _timezone, _parser)
            for name, icon, obis in elements
    ]

    # Set up the sensor platform
    async_add_entities(entities)

    async def async_consume_service(call):
        """handle calls to the service."""
        telegram = call.data.get('telegram')
        telegram = telegram.replace(" ", "")
        telegram = telegram.replace("\\r\\n", "\r\n")

        for entity in entities:
            entity.set_consumed(telegram)

    hass.services.async_register(
        DOMAIN,
        SERVICE,
        async_consume_service,
        schema=ENTITIES_SCHEMA,
    )


class ElecticityEntity(SmartmeterDevice, RestoreEntity):
    """representation of a electricity entity"""

    def __init__(self, name, icon, obis, precision, timezone, parser):
        """initialize the electricity entity"""
        self._name = name
        self._icon = icon
        self._obis = obis
        self._element = self._name.lower().replace(" ", "_")

        self._unit = ''

        self._obis = obis
        self._precision = precision
        self._timezone = timezone
        self._parser = parser

        self._data = ''
        self._telegram = ''

        self._state = '-'
        self._attributes = {}

    async def async_added_to_hass(self):
        """run when entity is about to be added"""
        await super().async_added_to_hass()

        state = await self.async_get_last_state()

        if state:
            try:
                self._state = state.state
                self._attributes = state.attributes
            except ValueError as err:
                _LOGGER.warning(f"could not restore {self.name}: {err}")

    def get_attribute(self, name):
        """get the attribute value if the object has it"""
        attribute = self._telegram[self._obis]

        return getattr(attribute, name, None)

    @staticmethod
    def translate_tariff(value):
        # Convert 2/1 to normal/low
        # DSMR V2.2: Note: Rate code 1 is used for low rate and rate code 2 is
        # used for normal rate.
        if value == '0002':
            return 'normal'
        if value == '0001':
            return 'low'

        return None

    def set_consumed(self, data):
        """set the telegram for the electricity reading"""
        if data is not None:
            self._data = data
            self._telegram = self._parser.parse(data)

    def update(self):
        try:
            self._unit = self.get_attribute('unit')

            if self.name == 'Smartmeter Hourly Gas Consumption' and self._unit:
                self._unit = f"{self._unit}/h"
        except Exception:
            self._unit = ''

        try:
            value = self.get_attribute('value')
        except:
            self._state = '-'

            return

        if self.name == 'Smartmeter Power Consumption (both)':
            value = value + self._telegram[obis_ref.ELECTRICITY_USED_TARIFF_2].value
        elif self._obis == obis_ref.ELECTRICITY_ACTIVE_TARIFF:
            self._state = self.translate_tariff(value)

            return

        try:
            value = round(float(value), self._precision)
        except TypeError:
            pass

        if value is not None:
            self._state = value
        else:
            self._state = '-'

    @property
    def unique_id(self) -> str:
        """return the unique id"""
        return f"{UUID}.{self._element}"

    @property
    def name(self) -> str:
        """return the name of the entity"""
        return self._name

    @property
    def icon(self) -> str:
        """return the icon to be used for this entity"""
        return self._icon

    @property
    def unit_of_measurement(self):
        """return the unit of measurement"""
        return self._unit

    @property
    def state(self):
        """return the state of the entity"""
        return self._state

    @property
    def state_attributes(self):
        """return the state attributes"""
        return {'data': self._data}


class GasEntity(ElecticityEntity):
    """representation of a gas entity"""

    def __init__(self, name, icon, obis, precision, timezone, parser):
        """initialize the gas entity"""
        super().__init__(name, icon, obis, precision, timezone, parser)

        self._previous_state = None
        self._previous_timestamp = None

    def update(self):
        if 'previous_state' in self._attributes:
            self._previous_state = self._attributes['previous_state']
            self._previous_timestamp = self._attributes['previous_timestamp']

        # check if the timestamp for the object differs from the previous one
        if self._telegram != '':
            timestamp = self.get_attribute('datetime')
            timestamp = timestamp.astimezone(self._timezone)

            state = self.get_attribute('value')

            if timestamp is not None and timestamp != self._previous_timestamp:
                _LOGGER.error(f"{self._name} {self._previous_state}")
                if self._previous_state is None:
                    self._previous_state = state
                    self._previous_timestamp = timestamp

                diff = state - self._previous_state
                timediff = timestamp - self._previous_timestamp
                total_seconds = timediff.total_seconds()

                if self.name == 'Smartmeter Hourly Gas Consumption':
                    self._state = round(float(diff) / total_seconds * 3600, self._precision)
                else:
                    self._state = timestamp.strftime('%X')

                self._previous_state = self._state
                self._previous_timestamp = timestamp
        else:
            self._state = '-'

    @property
    def device_state_attributes(self):
        """return the state attributes"""
        return {'data': self._data, 'previous_state': self._previous_state, 'previous_timestamp': self._previous_timestamp}
