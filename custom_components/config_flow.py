#  Copyright (c) 2021 Hombrelab <me@hombrelab.com>

import logging

from homeassistant import config_entries, exceptions
from homeassistant.config_entries import ConfigFlow

from .const import (
    DOMAIN,
    TITLE,

    CONFIG_SCHEMA,

    DSMRVERSION,
    PRECISION,
    TIMEZONE,

    DSMRVERSIONS,
)

_LOGGER = logging.getLogger(__name__)


class SmartmeterConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    CONNECTION_CLASS = config_entries.CONN_CLASS_UNKNOWN

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            return await self._show_setup_form(user_input)

        errors = {}

        try:
            await is_valid(user_input)
        except ValidationError:
            errors["base"] = "variables_error"
            return await self._show_setup_form(errors)

        data = {
            DSMRVERSION: user_input[DSMRVERSION],
            PRECISION: user_input[PRECISION],
            TIMEZONE: user_input[TIMEZONE],
        }

        return self.async_create_entry(
            title=TITLE,
            data=data,
        )

    async def _show_setup_form(self, errors=None):
        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA.schema[DOMAIN],
            errors=errors or {},
        )


async def is_valid(user_input):
    if not user_input[DSMRVERSION] in DSMRVERSIONS:
        raise ValidationError

    if user_input[PRECISION] < 0:
        raise ValidationError

    if not user_input[TIMEZONE].strip():
        raise ValidationError


class ValidationError(exceptions.HomeAssistantError):
    """Error to indicate that data is not valid"""
