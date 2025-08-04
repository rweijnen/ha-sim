"""Binary sensor platform for Home Assistant Integration Monitor."""
from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import IntegrationMonitorCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    async_add_entities([
        IntegrationFailureBinarySensor(coordinator),
    ])


class IntegrationFailureBinarySensor(CoordinatorEntity[IntegrationMonitorCoordinator], BinarySensorEntity):
    """Binary sensor for integration failures."""

    _attr_has_entity_name = True
    _attr_name = "Integration Failures Detected"
    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, coordinator: IntegrationMonitorCoordinator) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_has_failures"

    @property
    def is_on(self) -> bool:
        """Return true if any integrations have failed."""
        return self.coordinator.data.get("has_failures", False)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity state attributes."""
        failed = self.coordinator.data.get("failed_integrations", [])
        return {
            "failed_count": len(failed),
            "failed_domains": [item["domain"] for item in failed],
        }