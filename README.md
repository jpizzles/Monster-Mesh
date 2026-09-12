# Monster Mesh by jPizZleS

Custom Wio Tracker L1 Pro firmware based on DigitainoMeshCore and MeshCore, focused on making the device much more useful without needing the phone app for everyday mesh operations.

## Download firmware

### [Open the latest Monster Mesh build](https://github.com/jpizzles/Monster-Mesh/actions/workflows/build.yml)

Open the newest successful build and download the `Monster-Mesh-WioTracker-L1-Pro` artifact. It contains:

- `Monster-Mesh-WioTracker-L1-Pro.uf2` — flashable firmware
- `Monster-Mesh-WioTracker-L1-Pro-SHA256.txt` — checksum

Build artifacts are retained for 90 days, and every push to `main` automatically produces a fresh downloadable UF2.

Target device: Seeed Studio Wio Tracker L1 Pro (nRF52840 + SX1262).

## What's new in Monster Mesh

### Local or Flood advert from the device

The Advert screen no longer forces a local-only advertisement.

- ENTER sends a Local / zero-hop advert
- DOWN sends a true Flood advert through the mesh/repeaters

### Favorite / Unfavorite contacts

The Contacts action menu now includes Favorite / Unfavorite.

- favorites are marked with `*`
- favorites automatically sort to the top
- favorite state is saved persistently

### Dedicated Rooms filter

Contacts now cycle through:

`All | Contacts | Repeaters | Rooms`

Advertised MeshCore room servers remain marked `[Rm]`, but you no longer have to hunt through the All list to find them.

### Standalone radio controls

Radio parameters can now be changed directly on the Wio instead of requiring the companion app:

- Frequency
- Spreading Factor (SF)
- Bandwidth (BW)
- Coding Rate (CR)
- TX power remains available through the existing radio controls

SF, BW and CR can be adjusted from the device UI and are applied to the radio and saved.

### Fast per-digit frequency editor

Press ENTER on Frequency to enter digit-edit mode.

- LEFT / RIGHT moves between individual digits
- UP / DOWN changes only the selected digit
- ENTER saves and retunes the SX1262
- CANCEL discards the edit

Example:

```text
[9]15.000
9[1]5.000
91[5].000
915.[0]00
915.0[0]0
915.00[0]
```

This is much faster than stepping frequency in tiny fixed increments.

### Navigation retained

Monster Mesh keeps the Digitaino navigation functionality, including:

- full Navigation screen
- waypoint / contact navigation
- target bearing arrow
- distance and ETA information
- GPS-based motion behavior

### Existing Digitaino features retained

Monster Mesh is not a stripped-down rewrite. Existing standalone messaging, GPS, signals, repeater tools, telemetry, packets, Nearby discovery, quick messages and companion-app functionality remain part of the build.

## Flashing

1. Open the [Monster Mesh build page](https://github.com/jpizzles/Monster-Mesh/actions/workflows/build.yml).
2. Open the newest successful build.
3. Download the `Monster-Mesh-WioTracker-L1-Pro` artifact.
4. Extract `Monster-Mesh-WioTracker-L1-Pro.uf2`.
5. Double-press RESET on the Wio Tracker L1 Pro.
6. The device should mount as the `TRACKER L1` bootloader drive.
7. Drag the UF2 onto that drive and wait for the Wio to reboot.

Changing Frequency, SF, BW or CR can immediately take the device off your current mesh. Nodes that need to communicate must use compatible LoRa radio parameters.

## Reproducible build

The repository pins the DigitainoMeshCore base revision used for Monster Mesh and applies the Monster Mesh customization patch during CI, so the downloadable UF2 is reproducible from the files in this repository.

The Wio Tracker L1 Pro build command is:

```bash
pio run -e WioTrackerL1_companion_radio_ble -t create_uf2
```

## Upstream / credits

Monster Mesh is derived from:

- DigitainoMeshCore by pesqair: https://github.com/pesqair/DigitainoMeshCore
- MeshCore and its contributors: https://github.com/meshcore-dev/MeshCore

The DigitainoMeshCore project states that it inherits the MIT license from upstream MeshCore. Monster Mesh preserves upstream attribution and is intended to remain compatible with the MeshCore ecosystem.

Monster Mesh customizations and branding: jPizZleS.

## Status

This is enthusiast firmware. Use radio settings that are legal for your region and appropriate for the mesh network you intend to join.
