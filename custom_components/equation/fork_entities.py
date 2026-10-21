"""Fork (Sidonai-1): generic settings entities backed by the radiator's raw cloud fields.

Every entity reads radiator.raw[field] and writes by PATCHing {field: value} to the device data path, the same way the
Equation app does. Added 2026-10-21, tested on Equation HERA (v2, fw 2_1_1).
"""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import EntityCategory, UnitOfTemperature
from homeassistant.exceptions import HomeAssistantError

from .coordinator import EquationDataUpdateCoordinator
from .equation_entity import EquationRadiatorEntity
from .equationsdk.device import EquationDevice


@dataclass(frozen=True)
class Field:
    """A raw cloud field exposed as an entity."""

    key: str
    name: str
    icon: str | None = None
    category: EntityCategory | None = EntityCategory.CONFIG
    enabled: bool = True
    # number only
    min: float = 0
    max: float = 0
    step: float = 0.5
    unit: str | None = UnitOfTemperature.CELSIUS
    # binary_sensor only
    device_class: BinarySensorDeviceClass | None = None
    invert: bool = False


NUMBERS = [
    Field("comfort", "Comfort temperature", "mdi:sun-thermometer", min=7, max=30),
    Field("eco", "Eco temperature", "mdi:leaf", min=7, max=30),
    Field("ice", "Anti-frost temperature", "mdi:snowflake-thermometer", min=7, max=15),
    Field("offset_probe", "Probe offset", "mdi:thermometer-plus", min=-5, max=5),
    Field("backlight_time", "Display timeout", "mdi:timer-outline", enabled=False, min=0, max=60, step=1, unit="s"),
    Field("backlight", "Display brightness (idle)", "mdi:brightness-4", enabled=False, min=0, max=10, step=1, unit=None),
    Field("backlight_on", "Display brightness (active)", "mdi:brightness-6", enabled=False, min=0, max=10, step=1, unit=None),
]

SWITCHES = [
    Field("buzzer", "Beep", "mdi:volume-high"),
    Field("block_local", "Keypad lock", "mdi:lock"),
    Field("windows_open_mode", "Open window detection", "mdi:window-open-variant"),
    Field("ice_mode", "Anti-frost protection", "mdi:snowflake-alert"),
    Field("pir_mode", "Presence sensor", "mdi:motion-sensor", enabled=False),
]

BINARY_SENSORS = [
    Field("is_alive", "Cloud connection", None, EntityCategory.DIAGNOSTIC, device_class=BinarySensorDeviceClass.CONNECTIVITY),
    Field("error_heating", "Heating fault", None, EntityCategory.DIAGNOSTIC, device_class=BinarySensorDeviceClass.PROBLEM),
    Field("error_temperature_probe", "Probe fault", None, EntityCategory.DIAGNOSTIC, device_class=BinarySensorDeviceClass.PROBLEM),
    Field("error_low_wifi", "Weak Wi-Fi", None, EntityCategory.DIAGNOSTIC, device_class=BinarySensorDeviceClass.PROBLEM),
]


class EquationFieldEntity(EquationRadiatorEntity):
    """Base for raw-field entities."""

    def __init__(self, radiator: EquationDevice, coordinator: EquationDataUpdateCoordinator, field: Field) -> None:
        super().__init__(coordinator, radiator, name=f"{radiator.name} {field.name}", unique_id=f"{radiator.id}-{field.key}")
        self.field = field
        self._attr_icon = field.icon
        self._attr_entity_category = field.category
        self._attr_entity_registry_enabled_default = field.enabled

    @property
    def raw_value(self):
        return (getattr(self._radiator, "raw", None) or {}).get(self.field.key)

    @property
    def available(self) -> bool:
        return super().available and self.raw_value is not None

    async def write(self, value) -> None:
        if not await self.device_manager.async_set_fields(self._radiator, {self.field.key: value}):
            raise HomeAssistantError(f"Failed to set {self.field.name} on {self._radiator.name}")
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()


def constructors(fields: list[Field], cls):
    """Entity constructors for coordinator.add_entities_for_seen_keys (called as constructor(device, coordinator))."""
    return [lambda dev, coord, f=f: cls(dev, coord, f) for f in fields]
