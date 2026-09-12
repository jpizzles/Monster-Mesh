# Monster Mesh Features

This file documents the custom behavior added on top of DigitainoMeshCore.

## 1. Local vs Flood advert

The Advert page supports two transmit modes directly from the Wio:

```text
ENTER: Local
DOWN: Flood
```

- Local uses zero-hop advertising.
- Flood sends the advert through the mesh using flood routing.

## 2. Favorite / Unfavorite contacts

The contact action menu adds:

```text
Favorite
Unfavorite
```

Behavior:

- favorites are stored persistently
- favorites show `*`
- favorites sort to the top of the contact list

## 3. Rooms filter

Contacts now support four filters:

```text
All | Contacts | Repeaters | Rooms
```

Room servers are identified by MeshCore advert type `ADV_TYPE_ROOM` and continue to display `[Rm]` in the list.

## 4. On-device radio controls

The Wio can edit these without the phone app:

- Frequency
- Spreading Factor
- Bandwidth
- Coding Rate
- TX power through the existing control

Changes are applied to the SX1262 and persisted.

## 5. Per-digit frequency editor

Frequency editing is designed for fast field changes.

Enter edit mode with ENTER on the Frequency row.

Controls:

```text
LEFT / RIGHT  move selected digit
UP / DOWN     change selected digit
ENTER         save and retune
CANCEL        discard changes
```

Example:

```text
[9]15.000
9[1]5.000
91[5].000
915.[0]00
915.0[0]0
915.00[0]
```

## 6. Version info screen

Settings now has a clickable `Version >` row. Opening it shows:

```text
Monster Mesh
v0.2.0  -  2026-09-12
A jPizZleS
Meshterpiece!
It's ALLLiVE!!
```

Any key returns to the settings list. (Only the Name row stays read-only now; FREQ/SF/BW/CR are directly editable on-device — see #4/#5.)

## 7. Boot splash flip-in animation

The startup splash is now an animated split-flap "flip-in": line 1 reveals `Monster Mesh`, line 2 reveals the device/node name (each character cycles through glyphs and settles left-to-right), then the firmware version and build date fade in beneath. Replaces the static MeshCore-logo splash.

## 8. Navigation retained

Monster Mesh keeps Digitaino's Navigation page and waypoint functionality, including:

- target name
- distance
- bearing arrow
- ETA
- GPS heading / movement data

## 9. Existing Digitaino functionality retained

The custom build is intended to preserve the broader Digitaino feature set, including:

- on-device messaging
- quick messages
- contacts
- repeater path discovery
- telemetry
- GPS
- signal tracking
- packets
- Nearby discovery
- companion-app compatibility
- motion-aware repeater checks
- Auto TX checks

## Design goal

Monster Mesh is intended to make the Wio Tracker L1 Pro more standalone and field-usable, especially for users who do not want to reach for the companion app for common tasks.
