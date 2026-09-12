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


# ---- (3) Monster Snake ------------------------------------------------------------
# Self-contained Snake game under Tools > System ("Monster Snake"). Writes a new
# UIScreen header and wires it in with minimal guarded patches (include, instance,
# goto, Tools enum/dispatch/entry). Draws only through the DisplayDriver API used
# elsewhere; modelled on the existing tool screens.

Path('examples/companion_radio/ui-new/MonsterSnakeScreen.h').write_text(r'''#pragma once
// Monster Mesh -- "Monster Snake": a self-contained Snake game under Tools.
// Custom screen, included by UITask.cpp after UITask is fully defined (like the
// other tool screens). Draws only through the DisplayDriver API.

#include "UIScreen.h"

class UITask;

class MonsterSnakeScreen : public UIScreen {
  UITask* _task;

  static const int CELL = 4;
  static const int GRID_X = 0;
  static const int GRID_Y = 10;   // below a one-line score header
  static const int COLS = 32;     // 128 / CELL
  static const int ROWS = 13;     // (64 - GRID_Y) / CELL
  static const int MAXLEN = 96;

  enum State : uint8_t { READY, RUNNING, OVER };
  State    _state = READY;
  uint8_t  _sx[MAXLEN], _sy[MAXLEN];
  int      _len = 3;
  uint8_t  _dir = 1, _next_dir = 1;   // 0=up 1=right 2=down 3=left
  uint8_t  _fx = 0, _fy = 0;
  int      _score = 0;
  uint32_t _last_step = 0;
  uint16_t _tick_ms = 180;

  void placeFood() {
    for (int t = 0; t < 60; t++) {
      uint8_t x = (uint8_t)random(COLS), y = (uint8_t)random(ROWS);
      bool hit = false;
      for (int i = 0; i < _len; i++) if (_sx[i] == x && _sy[i] == y) { hit = true; break; }
      if (!hit) { _fx = x; _fy = y; return; }
    }
    _fx = 0; _fy = 0;
  }

  void reset() {
    randomSeed(millis());
    _len = 3;
    _dir = _next_dir = 1;
    _sx[0] = COLS / 2;   _sy[0] = ROWS / 2;
    _sx[1] = _sx[0] - 1; _sy[1] = _sy[0];
    _sx[2] = _sx[0] - 2; _sy[2] = _sy[0];
    _score = 0;
    _tick_ms = 180;
    placeFood();
    _last_step = millis();
    _state = RUNNING;
  }

  void step() {
    _dir = _next_dir;
    int hx = _sx[0], hy = _sy[0];
    if (_dir == 0) hy--; else if (_dir == 1) hx++; else if (_dir == 2) hy++; else hx--;
    if (hx < 0 || hx >= COLS || hy < 0 || hy >= ROWS) { _state = OVER; return; }
    bool grow = ((uint8_t)hx == _fx && (uint8_t)hy == _fy);
    int body = grow ? _len : _len - 1;
    for (int i = 0; i < body; i++)
      if (_sx[i] == (uint8_t)hx && _sy[i] == (uint8_t)hy) { _state = OVER; return; }
    if (grow && _len < MAXLEN) _len++;
    for (int i = _len - 1; i > 0; i--) { _sx[i] = _sx[i-1]; _sy[i] = _sy[i-1]; }
    _sx[0] = (uint8_t)hx; _sy[0] = (uint8_t)hy;
    if (grow) {
      _score++;
      if (_tick_ms > 80) _tick_ms -= 6;
      placeFood();
    }
  }

public:
  MonsterSnakeScreen(UITask* task) : _task(task) { }

  void onShow() override { _state = READY; }

  int render(DisplayDriver& display) override {
    if (_state == RUNNING && (uint32_t)(millis() - _last_step) >= _tick_ms) {
      _last_step = millis();
      step();
    }

    display.setTextSize(1);
    display.setColor(DisplayDriver::YELLOW);
    char hdr[24];
    snprintf(hdr, sizeof(hdr), "Monster Snake  %d", _score);
    display.setCursor(2, 0);
    display.print(hdr);

    // playfield border (fillRect only -- guaranteed available)
    const int bw = COLS * CELL, bh = ROWS * CELL, by = GRID_Y - 1;
    display.setColor(DisplayDriver::LIGHT);
    display.fillRect(GRID_X, by, bw, 1);
    display.fillRect(GRID_X, by + bh, bw, 1);
    display.fillRect(GRID_X, by, 1, bh);
    display.fillRect(GRID_X + bw - 1, by, 1, bh);

    if (_state == READY) {
      display.setColor(DisplayDriver::GREEN);
      display.drawTextCentered(display.width() / 2, GRID_Y + 14, "Monster Snake");
      display.setColor(DisplayDriver::LIGHT);
      display.drawTextCentered(display.width() / 2, GRID_Y + 30, "ENTER to play");
      return 200;
    }

    display.setColor(DisplayDriver::YELLOW);
    display.fillRect(GRID_X + _fx * CELL, GRID_Y + _fy * CELL, CELL - 1, CELL - 1);

    display.setColor(DisplayDriver::GREEN);
    for (int i = 0; i < _len; i++)
      display.fillRect(GRID_X + _sx[i] * CELL, GRID_Y + _sy[i] * CELL, CELL - 1, CELL - 1);

    if (_state == OVER) {
      display.setColor(DisplayDriver::LIGHT);
      display.drawTextCentered(display.width() / 2, GRID_Y + 14, "Game Over");
      display.drawTextCentered(display.width() / 2, GRID_Y + 30, "ENTER = retry");
      return 300;
    }
    return 60;
  }

  bool handleInput(char c) override {
    if (c == KEY_CANCEL) { _task->gotoToolsScreen(); return true; }
    if (c == KEY_ENTER) { if (_state != RUNNING) reset(); return true; }
    if (_state == RUNNING) {
      if      (c == KEY_UP    && _dir != 2) _next_dir = 0;
      else if (c == KEY_RIGHT && _dir != 3) _next_dir = 1;
      else if (c == KEY_DOWN  && _dir != 0) _next_dir = 2;
      else if (c == KEY_LEFT  && _dir != 1) _next_dir = 3;
      return true;
    }
    return false;
  }
};
''')

# Wire the game into UITask.cpp (include + instance).
p = Path('examples/companion_radio/ui-new/UITask.cpp')
s = p.read_text()
# Anchor on the ASCII include directive only (the trailing comment contains a
# non-ASCII char); insert the snake include on its own line just above it.
snake_inc = '#include "ClockToolsScreen.h"'
require(s, snake_inc, 'Monster Snake: include anchor')
s = s.replace(snake_inc, '#include "MonsterSnakeScreen.h"   // Monster Mesh: Snake game (Tools)\n' + snake_inc, 1)
snake_new = '  clock_tools        = new ClockToolsScreen(this, node_prefs);\n'
require(s, snake_new, 'Monster Snake: begin() instance anchor')
s = s.replace(snake_new, snake_new + '  monster_snake      = new MonsterSnakeScreen(this);\n', 1)
p.write_text(s)

# UITask.h: screen member + goto.
p = Path('examples/companion_radio/ui-new/UITask.h')
s = p.read_text()
snake_mem = '  UIScreen* clock_tools = nullptr;\n'
require(s, snake_mem, 'Monster Snake: member anchor')
s = s.replace(snake_mem, snake_mem + '  UIScreen* monster_snake = nullptr;\n', 1)
snake_goto = '  void gotoHomeScreen() { setCurrScreen(home); }\n'
require(s, snake_goto, 'Monster Snake: goto anchor')
s = s.replace(snake_goto, snake_goto + '  void gotoMonsterSnake() { setCurrScreen(monster_snake); }\n', 1)
p.write_text(s)

# ToolsScreen.h: enum + dispatch + Tools entry (under System).
p = Path('examples/companion_radio/ui-new/ToolsScreen.h')
s = p.read_text()
snake_enum = '    ACT_CLOCK, ACT_RINGTONE, ACT_DIAGNOSTICS\n'
require(s, snake_enum, 'Monster Snake: enum anchor')
s = s.replace(snake_enum, '    ACT_CLOCK, ACT_RINGTONE, ACT_DIAGNOSTICS, ACT_SNAKE\n', 1)
snake_disp = '      case ACT_DIAGNOSTICS: _task->gotoDiagnosticsScreen(); break;\n'
require(s, snake_disp, 'Monster Snake: dispatch anchor')
s = s.replace(snake_disp, snake_disp + '      case ACT_SNAKE:       _task->gotoMonsterSnake();    break;\n', 1)
snake_tool = '  { "Diagnostics",     &ICON_CHART, ACT_DIAGNOSTICS },\n'
require(s, snake_tool, 'Monster Snake: Tools entry anchor')
s = s.replace(snake_tool, snake_tool + '  { "Monster Snake",   nullptr,     ACT_SNAKE },\n', 1)
p.write_text(s)

print('Monster Mesh Solo patch applied: silent + SOS status bar + Monster Snake.')
