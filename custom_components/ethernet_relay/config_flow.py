"""
Config flow for the Ethernet Relay component.
"""

import logging

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.config_entries import ConfigFlow

from .const import (
    DOMAIN,
    NAME,
    HOST,
    PORT,
    ICON,
    MODEL,
    RELAYS,
    DEFAULT_NAME,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_ICON,
    DEFAULT_MODEL,
    DEFAULT_RELAYS
)

_LOGGER = logging.getLogger(__name__)


class EthernetRelayConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    CONNECTION_CLASS = config_entries.CONN_CLASS_UNKNOWN

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return await self._show_setup_form(user_input)

        errors = {}

        try:
            for entry in self._async_current_entries():
                if user_input[NAME] == entry.data[NAME]:
                    raise ValidationError
        except ValidationError:
            errors["base"] = "name_error"
            return await self._show_setup_form(errors)

        try:
            await is_valid(user_input)
        except ValidationError:
            errors["base"] = "variables_error"
            return await self._show_setup_form(errors)

        try:
            await has_connection(user_input)
        except ConnectionError:
            errors["base"] = "connection_error"
            return await self._show_setup_form(errors)

        data = {
            NAME: user_input[NAME],
            ICON: user_input[ICON],
            HOST: user_input[HOST],
            PORT: user_input[PORT],
            MODEL: user_input[MODEL],
            RELAYS: user_input[RELAYS],
        }

        return self.async_create_entry(
            title = user_input[NAME] + " " + user_input[MODEL],
            data = data,
        )

    async def _show_setup_form(self, errors=None):
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(NAME, default=DEFAULT_NAME): str,
                    vol.Optional(ICON, default=DEFAULT_ICON): str,
                    vol.Required(HOST, default=DEFAULT_HOST): str,
                    vol.Required(PORT, default=DEFAULT_PORT): int,
                    vol.Optional(MODEL, default=DEFAULT_MODEL): str,
                    vol.Required(RELAYS, default=DEFAULT_RELAYS): int,
                }
            ),
            errors=errors or {},
        )

async def is_valid(user_input):
    if not user_input[NAME].strip():
        user_input[NAME] = DEFAULT_NAME

    if not user_input[HOST].strip():
        raise ValidationError

    if user_input[RELAYS] < 1:
        raise ValidationError

    if user_input[ICON] and not ":" in user_input[ICON]:
        raise ValidationError


async def has_connection(user_input):
    try:
        return True
    except Exception:
        raise ConnectionError


class ValidationError(exceptions.HomeAssistantError):
    """Error to indicate that data is not valid"""


class ConnectionError(exceptions.HomeAssistantError):
    """Error to indicate that board can not be reached"""
