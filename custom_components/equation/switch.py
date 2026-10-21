"""Fork: radiator on/off settings as switch entities (beep, keypad lock, open-window detection, anti-frost)."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .fork_entities import SWITCHES, EquationFieldEntity, constructors


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    coordinator.add_entities_for_seen_keys(async_add_entities, constructors(SWITCHES, EquationSwitch), Platform.SWITCH)


class EquationSwitch(EquationFieldEntity, SwitchEntity):
    """A boolean radiator setting."""

    @property
    def is_on(self) -> bool | None:
        v = self.raw_value
        return None if v is None else bool(v)

    async def async_turn_on(self, **kwargs) -> None:
        await self.write(True)

    async def async_turn_off(self, **kwargs) -> None:
        await self.write(False)
