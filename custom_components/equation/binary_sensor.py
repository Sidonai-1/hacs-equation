"""Fork: radiator alarms and cloud connection as binary sensors."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .fork_entities import BINARY_SENSORS, EquationFieldEntity, constructors


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    coordinator.add_entities_for_seen_keys(
        async_add_entities, constructors(BINARY_SENSORS, EquationBinarySensor), Platform.BINARY_SENSOR
    )


class EquationBinarySensor(EquationFieldEntity, BinarySensorEntity):
    """A read-only radiator flag."""

    def __init__(self, radiator, coordinator, field) -> None:
        super().__init__(radiator, coordinator, field)
        self._attr_device_class = field.device_class

    @property
    def is_on(self) -> bool | None:
        v = self.raw_value
        return None if v is None else bool(v) != self.field.invert

    @property
    def available(self) -> bool:
        # The connection sensor must stay available to show "disconnected".
        return self.coordinator.last_update_success and self.raw_value is not None
