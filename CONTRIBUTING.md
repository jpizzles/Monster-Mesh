# Contributing to Monster Mesh

Monster Mesh is a focused Wio Tracker L1 Pro firmware fork. Contributions should preserve the project's main goal: make the device more standalone and field-usable while remaining compatible with the MeshCore ecosystem.

## Before changing code

Read:

1. `HANDOFF.md`
2. `BUILD.md`
3. `DEVELOPMENT.md`
4. `FEATURES.md`

## Development rules

- Keep the Wio Tracker L1 Pro BLE companion build working.
- Do not silently remove existing Digitaino functionality.
- Keep radio-setting changes persistent and explicit to the user.
- Prefer deterministic changes in `.monster/monster_patch.py`.
- Add or update CI verification checks for important UI strings or behavior markers.
- Update `FEATURES.md` and `CHANGELOG.md` for user-visible changes.
- Test the resulting UF2 on actual hardware before declaring a feature stable.

## Build target

```bash
pio run -e WioTrackerL1_companion_radio_ble -t create_uf2
```

## Pull requests

A useful pull request should explain:

- what problem it solves
- what Wio UI behavior changes
- whether radio/network behavior changes
- how it was tested
- whether it changes compatibility with standard MeshCore nodes or companion apps

## Attribution

Preserve upstream attribution to DigitainoMeshCore, MeshCore and their contributors.
