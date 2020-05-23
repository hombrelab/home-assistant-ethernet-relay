#  Copyright (c) 2020 Hombrelab <me@hombrelab.com>

# Switch for the Ethernet Relay component.

from homeassistant.config_entries import ConfigEntry

from homeassistant.helpers import config_validation as cv, entity_platform, service
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.components.switch import SwitchEntity

import logging
import socket

import voluptuous as vol

from . import EthernetRelayDevice
from .const import (
    UUID,
    NAME,
    HOST,
    PORT,
    ICON,
    MODEL,
    RELAYS,
    DEFAULT_PULSE,
    SERVICE_SET_PULSE,
    ATTR_PULSE
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry, async_add_entities):
    """Set up entities based on a config entry."""

    platform = entity_platform.current_platform.get()

    platform.async_register_entity_service(
        SERVICE_SET_PULSE,
        {
            vol.Required(ATTR_PULSE, DEFAULT_PULSE): cv.positive_int,
        },
        "set_pulse"
    )

    relays = entry.data[RELAYS]

    entities = []

    relay = 1
    while relay <= relays:
        entities += [EthernetRelaySwitch(
            entry.data[NAME],
            entry.data[MODEL],
            entry.data[ICON],
            entry.data[HOST],
            entry.data[PORT],
            relay)]
        relay += 1

    async_add_entities(entities)


class EthernetRelaySwitch(EthernetRelayDevice, SwitchEntity):
    def __init__(self, device, model, icon, host, port, relay):
        # Initialize the switch
        super().__init__(device, model)

        self._name = f"{device} {relay}"
        self._relay = relay
        self._icon = icon
        self._host = host
        self._port = port

        self._attributes = {}
        self._is_on = False

        self._pulse = DEFAULT_PULSE

    @property
    def unique_id(self) -> str:
        """Return the unique ID for this switch."""
        return f"{UUID}.switch.{self._device}-{self._name}"

    @property
    def device_state_attributes(self):
        return self._attributes

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self._switch_relay(True)

    async def async_turn_off(self, **kwargs):
        self._switch_relay(False)

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        self._check_relay()

    def _check_relay(self):
        relay = self._relay

        data = self._send_command('GR %s' % str(relay))

        if data is not None:
            if data.decode('utf-8').lower().find('inactive') > -1:
                self._is_on = False
            elif data.decode('utf-8').lower().find('active') > -1:
                self._is_on = True

    def _switch_relay(self, switch_on):
        if switch_on:
            data = self._send_command('SR %s on %s' % (str(self._relay), str(self._pulse)))
        else:
            data = self._send_command('SR %s off %s' % (str(self._relay), str(self._pulse)))

        if data is not None and data.decode('utf-8').lower().find('ok') > -1:
            if self._pulse == 0:
                self._is_on = switch_on
            else:
                self._is_on = False

    def _send_command(self, command):
        data = None

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                sock.connect((self._host, self._port))
                sock.settimeout(None)

                sock.sendall(command.encode('utf-8'))

                data = sock.recv(1024)

                _LOGGER.debug('Result for \'%s\' is %s' % (command, repr(data.decode('utf-8'))))
        except socket.error as msg:
            _LOGGER.warning("Caught exception socket.error : %s" % msg)
        finally:
            sock.close()

        return data

    def set_pulse(self, pulse):
        self._pulse = pulse
