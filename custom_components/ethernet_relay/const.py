"""
Constants for the Ethernet Relay component
"""

DOMAIN = "ethernet_relay"
UUID = "7d0450fb-f738-4884-afd1-39f8ba7d74cb"

SW_MANUFACTURER = "Hombrelab"
SW_NAME = "Ethernet Relay"
SW_VERSION = "1.0.1"

# labels
NAME = "name"
HOST = "host"
PORT = "port"
ICON = "icon"
MODEL = "model"
RELAY = "relay"
RELAYS = "relays"

# default values
DEFAULT_NAME = "Ethernet Relay"
DEFAULT_HOST = "192.168.0.90"
DEFAULT_PORT = 17123
DEFAULT_ICON = "mdi:electric-switch"
DEFAULT_MODEL = "DS378"
DEFAULT_RELAYS = 8
DEFAULT_PULSE = 500

SERVICE_SET_PULSE = "set_pulse"

ATTR_PULSE = "pulse"
