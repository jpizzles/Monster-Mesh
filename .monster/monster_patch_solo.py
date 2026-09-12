from pathlib import Path

# ===================================================================================
# Monster Mesh customizations, applied over MeshCore-Solo (the new base) in CI.
# Mirrors the guarded string-patch approach of the Digitaino patch: every change
# is anchored on an exact upstream string and fails the build loudly if that anchor
# ever drifts, so a silent no-op can never ship.
#
# Roadmap (built incrementally, each verified in CI + on device):
#   [x] Silent by default (no beeping)
#   [ ] SOS-style status bar (username / horizontal battery / GPS-only-when-on)
#   [ ] SOS font
#   [ ] Digitaino navigation features, ported 1:1
#   [ ] Monster Snake, Version screen, boot flip animation
# ===================================================================================


def require(hay, needle, what):
    if needle not in hay:
        raise SystemExit('Monster Mesh Solo patch marker missing: ' + what)


# ---- (1) Silent by default -------------------------------------------------------
# Stock Solo leaves buzzer_quiet at its memset(0) default (= NOT quiet) and sounds
# every advert at max volume; on a busy mesh that is near-constant beeping. Monster
# Mesh ships silent. A saved prefs file still wins (loadPrefs runs after this
# defaults block), and the on-device Buzzer toggle still works normally.
p = Path('examples/companion_radio/MyMesh.cpp')
s = p.read_text()

anchor = '  _prefs.buzzer_volume = 4;      // max volume by default\n'
require(s, anchor, 'buzzer defaults block')
s = s.replace(
    anchor,
    anchor + '  _prefs.buzzer_quiet = 1;       // Monster Mesh: silent by default (no beeping)\n',
    1,
)

p.write_text(s)
print('Monster Mesh Solo patch applied: silent by default.')
