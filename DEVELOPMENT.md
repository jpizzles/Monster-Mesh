# Monster Mesh Development Guide

This document explains how to continue Monster Mesh development on another computer without needing prior chat context.

## Repository layout

Important files:

```text
README.md                     user-facing overview and download instructions
BUILD.md                      clean-machine build instructions
FEATURES.md                   Monster Mesh feature documentation
DEVELOPMENT.md                developer workflow
CHANGELOG.md                  project change history
HANDOFF.md                    current implementation state and continuation notes
.monster/monster_patch.py     Monster Mesh source modifications
.github/workflows/build.yml   automatic UF2 build
```

## Upstream base

Monster Mesh currently builds from DigitainoMeshCore commit:

```text
6d090074973262b549bcfa9b7ca64226307ca688
```

Upstream repository:

```text
https://github.com/pesqair/DigitainoMeshCore
```

Do not casually change the pinned upstream commit. The patch uses exact source markers and an upstream update may require the patch to be rebased.

## Customization strategy

Monster Mesh currently stores its changes in:

```text
.monster/monster_patch.py
```

That script modifies these upstream files during a build:

```text
examples/companion_radio/MyMesh.h
examples/companion_radio/MyMesh.cpp
examples/companion_radio/ui-new/UITask.cpp
```

The approach makes the custom changes auditable while keeping a known upstream base.

## Main custom areas

### Advertising

`MyMesh::advert(bool flood)` supports both:

- zero-hop local advert
- scoped flood advert

The Advert screen maps:

```text
ENTER -> local
DOWN  -> flood
```

### Contact favorites

`MyMesh::setContactFavorite(...)` updates the contact favorite flag and saves contacts.

The contact actions dynamically show either `Favorite` or `Unfavorite`.

### Rooms

Contact filter values:

```text
0 = All
1 = Contacts
2 = Repeaters
3 = Rooms
```

Rooms match:

```cpp
ADV_TYPE_ROOM
```

### Radio settings

The Settings / Radio screen makes frequency, SF, BW and CR selectable instead of app-only information rows.

SF, BW and CR currently use LEFT / RIGHT adjustment.

### Frequency editor

Frequency has a dedicated edit mode.

State added to the UI task:

```text
_freq_edit_mode
_freq_orig
_freq_digit
```

The displayed frequency is converted to integer kHz for digit-safe editing.

Digit positions correspond to:

```text
100 MHz
10 MHz
1 MHz
100 kHz
10 kHz
1 kHz
```

ENTER applies the selected frequency with `radio_set_params(...)` and persists preferences.

CANCEL restores the original value.

## Testing a change

At minimum after each code modification:

1. Run the patch against the pinned Digitaino source.
2. Confirm the patch completes without a missing-marker error.
3. Build `WioTrackerL1_companion_radio_ble` with the `create_uf2` target.
4. Verify the expected strings exist in the source or binary.
5. Flash a test device before treating the build as stable.

## Adding another Monster Mesh feature

Recommended process:

1. Identify the relevant upstream source behavior.
2. Modify `.monster/monster_patch.py` so the change is deterministic.
3. Add a verification check to `.github/workflows/build.yml` when practical.
4. Update `FEATURES.md`.
5. Update `CHANGELOG.md`.
6. Update `HANDOFF.md` if the architecture or important state changed.
7. Confirm GitHub Actions succeeds and produces the UF2 artifact.

## Updating upstream Digitaino

When moving to a newer Digitaino commit:

1. Create a temporary development branch.
2. Change the pinned commit only on that branch.
3. Run `.monster/monster_patch.py` against the new source.
4. Repair any failed source markers.
5. Compile successfully.
6. Test core functions on hardware.
7. Compare relevant upstream changes for navigation, contacts, radio prefs and advert routing.
8. Only then move the new commit to `main`.

## Naming

Project display name:

```text
Monster Mesh by jPizZleS
```

Primary hardware target:

```text
Wio Tracker L1 Pro
```
