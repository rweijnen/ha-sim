"""DataUpdateCoordinator for Home Assistant Integration Monitor."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class IntegrationMonitorCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching integration status."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        self.config_entry = entry
        
        scan_interval = entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL)
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        failed_integrations = []
        
        # Get all config entries
        for entry in self.hass.config_entries.async_entries():
            # Skip disabled integrations
            if entry.state == "disabled":
                continue
                
            # Check if integration failed to load
            if entry.state in ["setup_error", "setup_retry", "migration_error", "failed_unload"]:
                failed_integrations.append({
                    "domain": entry.domain,
                    "title": entry.title,
                    "state": entry.state,
                })
        
        return {
            "failed_integrations": failed_integrations,
            "failed_count": len(failed_integrations),
            "has_failures": len(failed_integrations) > 0,
        }