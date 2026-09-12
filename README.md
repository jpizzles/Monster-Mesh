# Monster Mesh by jPizZleS

Custom Wio Tracker L1 Pro firmware based on DigitainoMeshCore and MeshCore, focused on making the device much more useful without needing the phone app for everyday mesh operations.

## Download firmware

### [Download the latest Monster Mesh UF2](https://github.com/jpizzles/Monster-Mesh/releases/latest/download/Monster-Mesh-WioTracker-L1-Pro.uf2)

Latest releases are also available from the repository's [Releases page](https://github.com/jpizzles/Monster-Mesh/releases).

Target device: Seeed Studio Wio Tracker L1 Pro (nRF52840 + SX1262).

## Monster Mesh additions

- On-device Local vs Flood advert control
  - ENTER sends a local / zero-hop advert
  - DOWN sends a true mesh flood advert through repeaters
- Favorite / Unfavorite directly from the Contacts action menu
  - favorite contacts are marked with `*`
  - favorites sort to the top
  - favorite state persists
- Dedicated Rooms contact filter
  - Contacts filters are now `All | Contacts | Repeaters | Rooms`
  - advertised MeshCore room servers remain marked `[Rm]`
- Standalone radio controls directly on the Wio
  - Frequency
  - Spreading Factor (SF)
  - Bandwidth (BW)
  - Coding Rate (CR)
  - TX power remains available from the existing radio controls
- Fast per-digit frequency editor
  - ENTER on Frequency starts editing
  - LEFT / RIGHT moves between digits
  - UP / DOWN changes only the selected digit
  - ENTER saves and retunes the SX1262
  - CANCEL discards changes
  - frequency editor is constrained to the SX1262 operating range used by this build
- Digitaino navigation features retained
  - full Navigation screen
  - waypoint / contact navigation
  - target bearing arrow
  - distance and ETA information
- Existing Digitaino standalone messaging, GPS, signal, repeater, telemetry and companion-app functionality retained

## Frequency editor example

A frequency such as `915.000 MHz` is edited one digit at a time:

```text
[9]15.000
9[1]5.000
91[5].000
915.[0]00
915.0[0]0
915.00[0]
```

This is substantially faster than stepping frequency in small fixed increments.

## Flashing

1. Download `Monster-Mesh-WioTracker-L1-Pro.uf2` from the Latest Release link above.
2. Double-press RESET on the Wio Tracker L1 Pro.
3. The device should mount as the `TRACKER L1` bootloader drive.
4. Drag the UF2 onto that drive.
5. Wait for the Wio to reboot.

Changing Frequency, SF, BW or CR can immediately take the device off your current mesh. Nodes that need to communicate must use compatible LoRa radio parameters.

## Building

Monster Mesh uses PlatformIO. For the Wio Tracker L1 Pro BLE companion build:

```bash
pio run -e WioTrackerL1_companion_radio_ble -t create_uf2
```

The GitHub Actions workflow also builds the UF2 automatically and publishes the current main build to GitHub Releases.

## Upstream / credits

Monster Mesh is derived from:

- DigitainoMeshCore by pesqair: https://github.com/pesqair/DigitainoMeshCore
- MeshCore and its contributors: https://github.com/meshcore-dev/MeshCore

The original project README states that DigitainoMeshCore inherits the MIT license from upstream MeshCore. Monster Mesh preserves upstream attribution and is intended to remain compatible with the MeshCore ecosystem.

Monster Mesh customizations and branding: jPizZleS.

## Status

This project is an enthusiast firmware fork. Use radio settings that are legal for your region and appropriate for the mesh network you intend to join.
