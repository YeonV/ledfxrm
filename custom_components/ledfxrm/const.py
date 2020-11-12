"""Constants for ledfxrm."""
# Base component constants
NAME = "LedFX ReMote"
DOMAIN = "ledfxrm"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.7"
MANUFACTURER = "YeonV"

ISSUE_URL = "https://github.com/YeonV/ledfxrm/issues"

# Icons
ICON_STRIP = "mdi:led-strip-variant"
ICON_SCENE = "mdi:image-multiple-outline"
ICON_POWER = "mdi:power"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
INPUT_SELECT = "input_select"
SENSOR = "sensor"
SWITCH = "switch"
PLATFORMS = [BINARY_SENSOR, SENSOR, SWITCH]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_HOST = "host"
CONF_PORT = "port"

# Defaults
DEFAULT_NAME = DOMAIN

NUMBER_SCENES = "Number of Scenes"
NUMBER_DEVICES = "Number of Devices"
START_KILL_SERVER = "Start/Stop Server"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""