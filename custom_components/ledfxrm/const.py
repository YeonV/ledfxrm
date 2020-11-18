"""Constants for ledfxrm."""
# Base component constants
NAME = "LedFX ReMote"
DOMAIN = "ledfxrm"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.1.7"
MANUFACTURER = "YeonV"

ISSUE_URL = "https://github.com/YeonV/ledfxrm/issues"

# Icons
ICON_STRIP = "mdi:led-strip-variant"
ICON_STRIP_DEVICE = "mdi:led-strip"
ICON_SCENE = "mdi:image-multiple-outline"
ICON_ASCENE = "mdi:image-outline"
ICON_POWER = "mdi:power"
ICON_LED = "mdi:led-variant-outline"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"
SWITCH_DEVICE_CLASS = "outlet"

# Platforms
BINARY_SENSOR = "binary_sensor"
INPUT_SELECT = "input_select"
SENSOR = "sensor"
SWITCH = "switch"
LIGHT = "light"
PLATFORMS = [BINARY_SENSOR, SENSOR, SWITCH, LIGHT]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_HOST = "host"
CONF_PORT = "port"
CONF_START = "start"
CONF_STOP = "stop"
CONF_ADVANCED = "advanced"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_SHOW_SUBDEVICES = "show_subdevices"


# Defaults
DEFAULT_NAME = DOMAIN

NUMBER_SCENES = "Number of Scenes"
NUMBER_DEVICES = "Number of Devices"
NUMBER_PIXELS = "Number of Pixels"
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