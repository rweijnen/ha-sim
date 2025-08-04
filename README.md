# Home Assistant Integration Monitor (HA-SIM)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

HA-SIM is a custom Home Assistant integration that monitors the health and performance of other integrations in your Home Assistant instance.

## Features

- Monitor integration status and health
- Track integration performance metrics
- Alert on integration failures
- Display integration resource usage

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add `https://github.com/rweijnen/ha-sim` with category "Integration"
5. Click "Install" on the HA-SIM card
6. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/ha_sim` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "Home Assistant Integration Monitor"
4. Follow the configuration flow

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/rweijnen/ha-sim/issues).

## License

This project is licensed under the MIT License.