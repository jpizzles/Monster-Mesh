# Changelog

All notable Monster Mesh changes are tracked here.

## 0.2.0 - 2026-09-12

Base: same pinned DigitainoMeshCore commit as 0.1.0.

Added:

- Settings `Version >` screen (Monster Mesh / v0.2.0 / release date / "A jPizZleS Meshterpiece! It's ALLLiVE!!")
- animated boot splash: split-flap flip-in of "Monster Mesh" + the device/node name

Fixed / hardened:

- the read-only predicate that makes FREQ/SF/BW/CR editable on-device is now
  guarded in the patch and verified in CI, so it can never silently no-op and
  leave Radio navigation "stuck at TX" again. (If your device can't move past
  TX power on the Radio page, you are running a build from before this fix —
  the `Version >` screen will confirm which build is flashed.)

## 0.1.0 - Initial Monster Mesh build

Base:

```text
DigitainoMeshCore commit 6d090074973262b549bcfa9b7ca64226307ca688
```

Added:

- Monster Mesh by jPizZleS branding
- on-device Local vs Flood advert selection
- Favorite / Unfavorite contact action
- persistent favorite flag handling
- dedicated Rooms contact filter
- direct on-device Frequency editing
- direct on-device SF editing
- direct on-device BW editing
- direct on-device CR editing
- per-digit frequency editor for fast field changes
- automatic GitHub Actions UF2 build
- downloadable firmware artifact and checksum
- build, development, feature and handoff documentation

Retained from Digitaino:

- Navigation page
- waypoint / contact bearing arrow
- on-device messaging
- quick messages
- GPS
- Nearby discovery
- repeater signal tools
- telemetry
- packet view
- companion-app support

## Planned / possible future work

Ideas that can be evaluated later:

- true GitHub Release publishing for one-click permanent UF2 downloads
- upstream Digitaino rebase workflow
- additional standalone settings normally exposed only through the companion app
- additional room-server UI improvements
- more explicit radio preset management
- hardware testing matrix and release versioning
