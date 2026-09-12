# Building Monster Mesh

This guide is intended for a fresh computer with no prior Monster Mesh setup.

## Target hardware

- Seeed Studio Wio Tracker L1 Pro
- nRF52840 MCU
- SX1262 LoRa radio
- BLE companion-radio build

## Prerequisites

Install:

- Git
- Python 3.11 or newer
- PlatformIO

PlatformIO can be installed with:

```bash
python -m pip install --upgrade platformio
```

Verify:

```bash
git --version
python --version
pio --version
```

## Clone Monster Mesh

```bash
git clone https://github.com/jpizzles/Monster-Mesh.git
cd Monster-Mesh
```

## Current source model

Monster Mesh currently uses a pinned DigitainoMeshCore base and applies the Monster Mesh customization patch during the build workflow.

Pinned upstream Digitaino commit:

```text
6d090074973262b549bcfa9b7ca64226307ca688
```

The customization patch lives at:

```text
.monster/monster_patch.py
```

## Manual local build

Clone the pinned upstream source:

```bash
git clone https://github.com/pesqair/DigitainoMeshCore.git firmware
cd firmware
git checkout 6d090074973262b549bcfa9b7ca64226307ca688
```

Apply the Monster Mesh patch from the repository root:

Linux/macOS:

```bash
python ../.monster/monster_patch.py
```

Windows PowerShell:

```powershell
python ..\.monster\monster_patch.py
```

Build the Wio Tracker L1 Pro UF2:

```bash
pio run -e WioTrackerL1_companion_radio_ble -t create_uf2
```

Expected UF2 output:

```text
.pio/build/WioTrackerL1_companion_radio_ble/firmware.uf2
```

## GitHub Actions build

The repository also builds automatically on every push to `main`.

Workflow:

```text
.github/workflows/build.yml
```

Open:

https://github.com/jpizzles/Monster-Mesh/actions/workflows/build.yml

Then open the newest successful run and download the artifact:

```text
Monster-Mesh-WioTracker-L1-Pro
```

It contains the UF2 and SHA-256 checksum.

## Flashing

1. Double-press RESET on the Wio Tracker L1 Pro.
2. Wait for the bootloader drive named `TRACKER L1`.
3. Copy the UF2 onto that drive.
4. Wait for the device to reboot.

## Troubleshooting

If the build fails after an upstream update, first check whether strings used by `.monster/monster_patch.py` still exist in the upstream source. Monster Mesh intentionally pins a known-good upstream commit so normal builds remain reproducible.

If PlatformIO cannot find dependencies, delete `.pio` and rebuild:

```bash
rm -rf .pio
pio run -e WioTrackerL1_companion_radio_ble -t create_uf2
```

On Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .pio
pio run -e WioTrackerL1_companion_radio_ble -t create_uf2
```
