> **Fork (Sidonai-1)** of [Ieshaj/hacs-equation](https://github.com/Ieshaj/hacs-equation), maintained for a home with Equation HERA radiators.
> Changes in 0.2.0:
> - the Equation SDK (MIT, [equation-sdk](https://github.com/Ieshaj/equation-sdk) 1.0.7) is bundled in `custom_components/equation/equationsdk`, no PyPI dependency;
> - **setting the temperature works**: while the radiator heats it is sent with `"status": "none"` (without it the radiator ignored it);
>   while it is off the value is stored as its *comfort* temperature (stays off; the next "heat" uses it), and HA shows that as the target;
> - no more crashes of the whole refresh when the cloud returns nothing for one radiator (`ApiResponse` missing argument);
> - unique device names (`Rad. F0DA7A` instead of several `Rad. C964EC`).

# 🌞 equation-hacs 
A minimal integration for Equation radiators in Home Assistant. 🏡

### Supported Devices
* Hera Radiators

## Features
* Ability to control the temperature
* Provides a sensor with the current temperature, as measured by the device.
* Choose between presets (Eco, Comfort) or Manual Mode
* Notification of firmware updates available
* Energy data (Current power and consumed energy)

## Upcoming features
* Configure preset temperatures
* Control screen brightness (for elegible devices)
* Control screen color.
