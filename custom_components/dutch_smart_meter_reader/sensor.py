"""
Sensor for the Dutch Smart Meter Reader component.
"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.restore_state import RestoreEntity

import logging

from dsmr_parser import telegram_specifications
from dsmr_parser.parsers import TelegramParser
from dsmr_parser import obis_references as obis_ref

_LOGGER = logging.getLogger(__name__)

from . import DSMRDevice

from .const import (
    UUID,
    DSMRVERSION,
    PRECISION,
    TOPIC,
    AMS_TIMEZONE,
    ENTITIES
)


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry, async_add_entities):
    """Set up entities based on a config entry."""

    # Connect to MQTT Topic
    mqtt = hass.components.mqtt

    dsmr_version = entry.data[DSMRVERSION]

    # Protocol version specific obis
    if dsmr_version in "4":
        gas_obis = obis_ref.HOURLY_GAS_METER_READING
        telegram_specs = telegram_specifications.V4
    elif dsmr_version in "5":
        gas_obis = obis_ref.HOURLY_GAS_METER_READING
        telegram_specs = telegram_specifications.V5
    elif dsmr_version in ("5B",):
        gas_obis = obis_ref.BELGIUM_HOURLY_GAS_METER_READING
        telegram_specs = telegram_specifications.BELGIUM_FLUVIUS
    else:
        gas_obis = obis_ref.GAS_METER_READING
        telegram_specs = telegram_specifications.V2_2

    # Define list of name,obis mappings to generate entities
    elements = ENTITIES
    elements += [
        [
            'Dutch Smart Meter Reader Gas Consumption',
            'mdi:fire',
            gas_obis
        ],
    ]

    derivative_elements = [
        [
            'Dutch Smart Meter Reader Hourly Gas Consumption',
            'mdi:fire',
            gas_obis
        ],
        [
            'Dutch Smart Meter Reader Hourly Gas Last Update',
            'mdi:update',
            gas_obis
        ],
    ]

    # Generate device entities
    entities = [
        DSMREntity(name, icon, obis, entry.data[PRECISION], telegram_specs) for name, icon, obis in elements
    ]

    # Add derivative entities
    entities += [
        DerivativeDSMREntity(name, icon, obis, entry.data[PRECISION], telegram_specs) for name, icon, obis in derivative_elements
    ]

    async_add_entities(entities)

    def update_entities_telegram(telegram):
        _LOGGER.debug(telegram)

        # Make all device entities aware of the new telegram
        for entity in entities:
            entity.setTelegram(telegram)

            hass.async_create_task(entity.async_update_ha_state())

    # Call MQTT subscribe function
    def telegram_callback(message):
        # Call callback
        if message is not None:
            update_entities_telegram(message.payload)

    hass.async_create_task(mqtt.async_subscribe(entry.data[TOPIC], telegram_callback, 0))


class DSMREntity(DSMRDevice, RestoreEntity):
    def __init__(self, name, icon, obis, precision, telegram_specs):
        # Initialize the sensor
        self._name = name
        self._icon = icon
        self._obis = obis
        self._precision = precision
        self._parser = TelegramParser(telegram_specs)

        self._raw = ''
        self._telegram = ''
        self._state = '-'

    def get_dsmr_object_attr(self, attribute):
        # Read attribute from last received telegram for this DSMR object
        # Make sure telegram contains an object for this entities obis

        # Get the attribute value if the object has it
        dsmr_object = self._telegram[self._obis]

        return getattr(dsmr_object, attribute, None)

    def setTelegram(self, telegram):
        self._raw = telegram
        self._telegram = self._parser.parse(self._raw)

    @property
    def unique_id(self) -> str:
        """Return the unique ID for this sensor."""
        return f"{UUID}.sensor.{self._name}"

    @property
    def name(self):
        # Return the name of the sensor
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        # Return the state of sensor, if available, translate if needed
        try:
            value = self.get_dsmr_object_attr('value')
        except:
            return '-'

        if self._name == 'Dutch Smart Meter Reader Power Consumption (both)':
            value = value + self._telegram[obis_ref.ELECTRICITY_USED_TARIFF_2].value
        elif self._obis == obis_ref.ELECTRICITY_ACTIVE_TARIFF:
            return self.translate_tariff(value)

        try:
            value = round(float(value), self._precision)
        except TypeError:
            pass

        if value is not None:
            return value

        return '-'

    @property
    def unit_of_measurement(self):
        # Return the unit of measurement of this entity, if any
        try:
            return self.get_dsmr_object_attr('unit')
        except Exception:
            pass

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


class DerivativeDSMREntity(DSMREntity):
    # Calculated derivative for values where the DSMR doesn't offer one.
    # Gas readings are only reported per hour and don't offer a rate only
    # the current meter reading. This entity converts subsequents readings
    # into a hourly rate.

    def __init__(self, name, icon, obis, precision, telegram_specs):
        super().__init__(name, icon, obis, precision, telegram_specs)

        self._previous_reading = None
        self._previous_timestamp = None
        self._state = None

    @property
    def device_state_attributes(self):
        return {'raw': self._raw}

    @property
    def state(self):
        # Return the calculated current hourly rate
        return self._state

    async def async_update(self):
        # Recalculate hourly rate if timestamp has changed.

        # DSMR updates gas meter reading every hour. Along with the new
        # value a timestamp is provided for the reading. Test if the last
        # known timestamp differs from the current one then calculate a
        # new rate for the previous hour.

        # check if the timestamp for the object differs from the previous one
        timestamp = self.get_dsmr_object_attr('datetime')
        timestamp = timestamp.astimezone(AMS_TIMEZONE)

        if timestamp and timestamp != self._previous_timestamp:
            current_reading = self.get_dsmr_object_attr('value')

            if self._previous_reading is None:
                # Can't calculate rate without previous datapoint
                # just store current point
                pass
            else:
                # Recalculate the rate
                diff = current_reading - self._previous_reading
                timediff = timestamp - self._previous_timestamp
                total_seconds = timediff.total_seconds()

                if self._name == 'Dutch Smart Meter Reader Hourly Gas Consumption':
                    self._state = round(float(diff) / total_seconds * 3600, self._precision)
                else:
                    self._state = timestamp.strftime('%X')

            self._previous_reading = current_reading
            self._previous_timestamp = timestamp

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, per hour, if any."""
        try:
            unit = self.get_dsmr_object_attr("unit")

            if self._name == 'Dutch Smart Meter Reader Hourly Gas Consumption' and unit:
                return f"{unit}/h"
        except:
            return ""

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        state = await self.async_get_last_state()

        if state:
            try:
                self._raw = state.attributes['raw']

                if self._raw:
                    self._telegram = self._parser.parse(self._raw)
                    self._state = state.state
                else:
                    self._telegram = ''
                    self._state = '-'
            except ValueError as err:
                _LOGGER.warning("Could not restore last state: %s", err)
