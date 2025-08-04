"""Sensor platform for Home Assistant Integration Monitor."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import IntegrationMonitorCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    async_add_entities([
        IntegrationFailureCountSensor(coordinator),
        FailedIntegrationsListSensor(coordinator),
    ])


class IntegrationFailureCountSensor(CoordinatorEntity[IntegrationMonitorCoordinator], SensorEntity):
    """Sensor for counting failed integrations."""

    _attr_has_entity_name = True
    _attr_name = "Failed Integration Count"
    _attr_icon = "mdi:numeric"

    def __init__(self, coordinator: IntegrationMonitorCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_failed_count"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            manufacturer="HA-SIM",
            model="Integration Monitor",
            name="HA-SIM Monitor",
        )

    @property
    def native_value(self) -> int:
        """Return the number of failed integrations."""
        return self.coordinator.data.get("failed_count", 0)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity state attributes."""
        return {
            "has_failures": self.coordinator.data.get("has_failures", False),
        }


class FailedIntegrationsListSensor(CoordinatorEntity[IntegrationMonitorCoordinator], SensorEntity):
    """Sensor listing failed integrations."""

    _attr_has_entity_name = True
    _attr_name = "Failed Integrations"
    _attr_icon = "mdi:alert-box-outline"

    def __init__(self, coordinator: IntegrationMonitorCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_failed_list"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            manufacturer="HA-SIM",
            model="Integration Monitor",
            name="HA-SIM Monitor",
        )

    @property
    def native_value(self) -> str:
        """Return comma-separated list of failed integrations."""
        failed = self.coordinator.data.get("failed_integrations", [])
        if not failed:
            return "none"
        return ", ".join([f"{item['title']} ({item['domain']})" for item in failed])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity state attributes."""
        failed = self.coordinator.data.get("failed_integrations", [])
        return {
            "failed_integrations": failed,
            "count": len(failed),
        }