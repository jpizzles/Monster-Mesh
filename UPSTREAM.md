# Upstream Relationship

Monster Mesh is built on existing open-source work and keeps that lineage explicit.

## Immediate upstream

DigitainoMeshCore by pesqair:

```text
https://github.com/pesqair/DigitainoMeshCore
```

Pinned Monster Mesh base revision:

```text
6d090074973262b549bcfa9b7ca64226307ca688
```

## MeshCore

DigitainoMeshCore is itself based on MeshCore.

Current MeshCore project:

```text
https://github.com/meshcore-dev/MeshCore
```

## Why Monster Mesh pins an upstream commit

The Monster Mesh customization layer currently patches exact upstream source locations. Pinning a known-good commit provides:

- reproducible builds
- predictable UI behavior
- fewer surprise regressions
- a clear point from which future upstream rebases can be reviewed

## Updating upstream

Do not simply replace the commit hash on `main`.

Use a development branch, rebuild, inspect all patch markers, test on hardware, and verify at least:

- advertising
- contacts and favorites
- Rooms filtering
- messaging
- radio preference storage
- frequency/SF/BW/CR editing
- GPS and Navigation
- repeater signal tools
- companion-app behavior

Only merge the new upstream revision after the Monster Mesh feature set passes those checks.

## Credits

Monster Mesh customizations and project branding: jPizZleS.

Upstream credit remains with DigitainoMeshCore, MeshCore, and their respective contributors.
