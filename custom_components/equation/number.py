"""Fork: radiator settings as number entities (comfort/eco/anti-frost temperatures, probe offset, display)."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .fork_entities import NUMBERS, EquationFieldEntity, constructors


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    coordinator.add_entities_for_seen_keys(async_add_entities, constructors(NUMBERS, EquationNumber), Platform.NUMBER)


class EquationNumber(EquationFieldEntity, NumberEntity):
    """A numeric radiator setting."""

    _attr_mode = NumberMode.BOX

    @property
    def native_min_value(self) -> float:
        return self.field.min

    @property
    def native_max_value(self) -> float:
        return self.field.max

    @property
    def native_step(self) -> float:
        return self.field.step

    @property
    def native_unit_of_measurement(self) -> str | None:
        return self.field.unit

    @property
    def native_value(self) -> float | None:
        v = self.raw_value
        return None if v is None else float(v)

    async def async_set_native_value(self, value: float) -> None:
        value = int(value) if self.field.step >= 1 else round(value * 2) / 2
        await self.write(value)
