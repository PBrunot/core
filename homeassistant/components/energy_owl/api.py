"""API Placeholder.

You should create your api seperately and have it hosted on PYPI.  This is included here for the sole purpose
of making this example code executable.
"""

from dataclasses import dataclass
from enum import StrEnum
import logging
from random import randrange

_LOGGER = logging.getLogger(__name__)


class DeviceType(StrEnum):
    """Device types."""

    CM160_I = "CM 160 - Current"


DEVICES = [
    {"id": 1, "type": DeviceType.CM160_I},
]


@dataclass
class Device:
    """API device."""

    device_id: int
    device_unique_id: str
    device_type: DeviceType
    name: str
    state: int | bool


class API:
    """Class for example API."""

    def __init__(self, port: str) -> None:
        """Initialise."""
        self.port = port
        self.connected: bool = False

    @property
    def controller_name(self) -> str:
        """Return the name of the controller."""
        return self.port.replace(".", "_")

    def connect(self) -> bool:
        """Connect to api."""
        if self.port == "test":
            self.connected = True
            return True
        raise APIConnectionError(
            "Error connecting to device. Check USB port and delete/recreate integration."
        )

    def disconnect(self) -> bool:
        """Disconnect from api."""
        self.connected = False
        return True

    def get_devices(self) -> list[Device]:
        """Get devices on api."""
        return [
            Device(
                device_id=device.get("id"),
                device_unique_id=self.get_device_unique_id(
                    device.get("id"), device.get("type")
                ),
                device_type=device.get("type"),
                name=self.get_device_name(device.get("id"), device.get("type")),
                state=self.get_device_value(device.get("id"), device.get("type")),
            )
            for device in DEVICES
        ]

    def get_device_unique_id(self, device_id: str, device_type: DeviceType) -> str:
        """Return a unique device id."""
        if device_type == DeviceType.CM160_I:
            return f"{self.controller_name}_I_{device_id}"
        return f"{self.controller_name}_Z{device_id}"

    def get_device_name(self, device_id: str, device_type: DeviceType) -> str:
        """Return the device name."""
        if device_type == DeviceType.CM160_I:
            return f"CM160 Current {device_id}"
        return f"CM160 Other {device_id}"

    def get_device_value(self, device_id: str, device_type: DeviceType) -> int | bool:
        """Get device random value."""
        if device_type == DeviceType.CM160_I:
            return randrange(15, 28)
        return randrange(15, 28)


class APIConnectionError(Exception):
    """Exception class for connection error."""
