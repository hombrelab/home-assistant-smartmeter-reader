#  Copyright (c) 2021 Hombrelab <me@hombrelab.com>

# The Smartmeter Reader component for Home Assistant.

import asyncio
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType, HomeAssistantType

from .const import (
    DOMAIN,
    UUID,
    SW_MANUFACTURER,
    SW_NAME,
    SW_VERSION
)

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistantType, config: ConfigType):
    """Set up component"""
    hass.data[DOMAIN] = {}

    if DOMAIN not in config:
        return True

    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Load config entries"""

    hass.data[DOMAIN][entry.entry_id] = "1531923f-ed21-4e72-8def-a7e900c71c8e"

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigType):
    """Unload config entries"""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class SmartmeterDevice():
    @property
    def device_info(self):
        """Return device information"""
        return {
            "identifiers": {
                (DOMAIN,
                 UUID)
            },
            "name": SW_NAME,
            "manufacturer": SW_MANUFACTURER,
            "model": "",
            "sw_version": SW_VERSION,
        }
