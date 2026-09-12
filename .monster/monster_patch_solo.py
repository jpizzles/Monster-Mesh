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


# ---- (2) SOS-style status bar ----------------------------------------------------
# Match the SOS top bar: username left, horizontal battery right (already so in Solo),
# "GPS" text centred on the title row only when GPS is on, and a row of plain dots for
# the page indicator (current page = a larger filled square) instead of Solo's per-page
# icons + underline.
p = Path('examples/companion_radio/ui-new/UITask.cpp')
s = p.read_text()

# (2a) "GPS" text on the title row when GPS is on.
gps_anchor = (
    '          display.drawTextEllipsized(0, 0, rightEdge - 2, filtered_name);\n'
    '        }\n'
    '      }\n'
    '    }\n'
)
require(s, gps_anchor, 'SOS status bar: title-row anchor')
s = s.replace(
    gps_anchor,
    '          display.drawTextEllipsized(0, 0, rightEdge - 2, filtered_name);\n'
    '        }\n'
    '      }\n'
    '      // Monster Mesh (SOS look): "GPS" centred on the title row, only when GPS is on.\n'
    '      if (_page != LOCK && _task->getGPSState()) {\n'
    '        display.drawTextCentered(display.width() / 2, 0, "GPS");\n'
    '      }\n'
    '    }\n',
    1,
)

# (2b) SOS dots for the page indicator (current page = larger filled square).
dots_anchor = (
    '        const MiniIcon* ic = pageIcon(order[i]);\n'
    '        if (ic) miniIconDrawCentered(display, x, dots_y, *ic);\n'
    '        if (i == curr_vis)                              // underline the current page\n'
    '          display.fillRect(x - icon_w / 2, dots_y + pg_half + 1, icon_w, s);\n'
)
require(s, dots_anchor, 'SOS status bar: page-indicator anchor')
s = s.replace(
    dots_anchor,
    '        // Monster Mesh (SOS look): plain dots; current page = larger filled square.\n'
    '        int dot = (i == curr_vis) ? 3 * s : s;\n'
    '        display.fillRect(x - dot / 2, dots_y - dot / 2, dot, dot);\n',
    1,
)

p.write_text(s)
print('Monster Mesh Solo patch applied: silent + SOS status bar.')
