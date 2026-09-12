# Monster Mesh Handoff

This file is the quick continuation document for moving development to another computer, another developer, or another AI session.

## Project

```text
Monster Mesh by jPizZleS
Repository: https://github.com/jpizzles/Monster-Mesh
Primary target: Seeed Studio Wio Tracker L1 Pro
Build environment: WioTrackerL1_companion_radio_ble
```

## Known-good upstream base

```text
Repository: https://github.com/pesqair/DigitainoMeshCore
Commit: 6d090074973262b549bcfa9b7ca64226307ca688
```

This commit was used for the working Monster Mesh frequency-digit UF2.

## Monster Mesh patch

All custom modifications are currently applied by:

```text
.monster/monster_patch.py
```

It patches:

```text
examples/companion_radio/MyMesh.h
examples/companion_radio/MyMesh.cpp
examples/companion_radio/ui-new/UITask.cpp
```

## Implemented custom features

1. Advert page
   - ENTER = Local / zero-hop advert
   - DOWN = Flood advert

2. Contact favorites
   - `Favorite` / `Unfavorite` in contact actions
   - saved through the contact database
   - favorites continue sorting to the top

3. Rooms filter
   - `All | Contacts | Repeaters | Rooms`
   - Rooms filter uses `ADV_TYPE_ROOM`

4. Radio controls
   - Frequency editable on device
   - SF editable on device
   - BW editable on device
   - CR editable on device
   - TX power remains supported

5. Frequency digit editor
   - LEFT / RIGHT selects digit
   - UP / DOWN changes digit
   - ENTER saves and retunes
   - CANCEL restores original frequency
   - editing is performed in integer kHz to avoid awkward float stepping

6. Digitaino navigation retained
   - Navigation screen
   - waypoint arrow
   - contact navigation
   - distance / ETA behavior

## Build automation

Workflow:

```text
.github/workflows/build.yml
```

It:

1. checks out Monster Mesh
2. clones pinned Digitaino source
3. applies `.monster/monster_patch.py`
4. verifies important Monster Mesh source strings
5. builds the Wio Tracker L1 Pro UF2
6. uploads a GitHub Actions artifact containing:

```text
Monster-Mesh-WioTracker-L1-Pro.uf2
Monster-Mesh-WioTracker-L1-Pro-SHA256.txt
```

## Existing known-good local firmware

The custom build previously produced a working artifact named:

```text
Digitaino-WioTracker-L1-Pro-Frequency-Digit-Editor.uf2
```

SHA-256 from that successful build:

```text
48ac28476cd1b395fdd11ac3f2cf11647717ff74a30734faea2b686d2a2d026a
```

That file predates the Monster Mesh repository name, but it represents the feature set being reproduced here.

## Next things to check after opening on another computer

Run through this sequence:

```bash
git clone https://github.com/jpizzles/Monster-Mesh.git
cd Monster-Mesh
```

Read in this order:

```text
README.md
HANDOFF.md
BUILD.md
FEATURES.md
DEVELOPMENT.md
CHANGELOG.md
```

Then verify the latest GitHub Actions build succeeded.

If making source changes, edit the patch deterministically, update documentation, and verify the resulting UF2 on hardware before considering the change stable.

## Important behavior notes

- The physical Advert UI originally sent only zero-hop adverts; Monster Mesh adds the explicit flood option.
- Digitaino already understood favorite flags but did not expose a favorite toggle in the on-device contact menu.
- Digitaino already recognized room servers as `ADV_TYPE_ROOM` and displayed `[Rm]`; Monster Mesh adds the dedicated Rooms filter.
- Digitaino stored radio parameters and could update them through the companion-app protocol; Monster Mesh exposes frequency/SF/BW/CR editing directly on the Wio.
- The Wio Tracker L1 Pro build used here is the BLE companion-radio environment.

## Goal

Keep Monster Mesh standalone-friendly, field-usable, compatible with the MeshCore ecosystem, and easy to rebuild from a clean computer without requiring undocumented chat history.
