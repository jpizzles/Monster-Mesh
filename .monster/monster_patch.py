from pathlib import Path

p = Path('examples/companion_radio/MyMesh.h')
s = p.read_text()
s = s.replace('  bool advert();', '  bool advert(bool flood=false);\n  bool setContactFavorite(const uint8_t* pub_key, bool favorite);')
p.write_text(s)

p = Path('examples/companion_radio/MyMesh.cpp')
s = p.read_text()
s = s.replace('bool MyMesh::advert() {', 'bool MyMesh::advert(bool flood) {', 1)
s = s.replace('    sendZeroHop(pkt);\n    return true;', '    if (flood) {\n      TransportKey default_scope;\n      memcpy(&default_scope.key, _prefs.default_scope_key, sizeof(default_scope.key));\n      sendFloodScoped(default_scope, pkt, 0);\n    } else {\n      sendZeroHop(pkt);\n    }\n    return true;', 1)
idx = s.find('bool MyMesh::advert(bool flood) {')
end = s.find('\n}\n', idx) + 3
insert = '\nbool MyMesh::setContactFavorite(const uint8_t* pub_key, bool favorite) {\n  ContactInfo* contact = lookupContactByPubKey(pub_key, PUB_KEY_SIZE);\n  if (contact == NULL) return false;\n  if (favorite) contact->flags |= 0x01;\n  else contact->flags &= (uint8_t)~0x01;\n  saveContacts();\n  return true;\n}\n'
s = s[:end] + insert + s[end:]
p.write_text(s)

p = Path('examples/companion_radio/ui-new/UITask.cpp')
s = p.read_text()

s = s.replace(
    '  int8_t _radio_orig_power;       // saved before edit; restored on CANCEL\n',
    '  int8_t _radio_orig_power;       // saved before edit; restored on CANCEL\n'
    '  bool _freq_edit_mode;           // per-digit frequency editor active\n'
    '  float _freq_orig;               // value restored on CANCEL\n'
    '  uint8_t _freq_digit;            // 0..5 = 100MHz,10MHz,1MHz,100k,10k,1k\n',
    1,
)
s = s.replace(
    '_page_active(false), _settings_sel(0), _radio_edit_mode(false), _radio_orig_power(0), _ct_filter(0),',
    '_page_active(false), _settings_sel(0), _radio_edit_mode(false), _radio_orig_power(0), _freq_edit_mode(false), _freq_orig(0), _freq_digit(0), _ct_filter(0),',
    1,
)

s = s.replace(
    '      display.setColor(DisplayDriver::GREEN);\n      display.drawXbm((display.width() - 32) / 2, TOP_BAR_H + 4, advert_icon, 32, 32);\n      display.drawTextCentered(display.width() / 2, TOP_BAR_H + 40, "advert: " PRESS_LABEL);',
    '      display.setColor(DisplayDriver::GREEN);\n      display.drawTextCentered(display.width() / 2, TOP_BAR_H + 7, "Send advert");\n      display.setColor(DisplayDriver::LIGHT);\n      display.drawTextCentered(display.width() / 2, TOP_BAR_H + 23, "ENTER: Local");\n      display.drawTextCentered(display.width() / 2, TOP_BAR_H + 39, "DOWN: Flood");',
    1,
)
s = s.replace(
    '    if (c == KEY_ENTER && _page == HomePage::ADVERT) {\n      _task->notify(UIEventType::ack);\n      if (the_mesh.advert()) {\n        _task->showAlert("Advert sent!", 1000);\n      } else {\n        _task->showAlert("Advert failed..", 1000);\n      }\n      return true;\n    }',
    '    if (_page == HomePage::ADVERT && (c == KEY_ENTER || c == KEY_DOWN)) {\n      const bool flood = (c == KEY_DOWN);\n      _task->notify(UIEventType::ack);\n      if (the_mesh.advert(flood)) {\n        _task->showAlert(flood ? "Flood advert sent!" : "Local advert sent!", 1000);\n      } else {\n        _task->showAlert("Advert failed..", 1000);\n      }\n      return true;\n    }',
    1,
)

s = s.replace(
    '          // Actions\n          if (ci.type == ADV_TYPE_CHAT) {',
    '          // Actions\n          bool is_fav = (ci.flags & 0x01) != 0;\n          items[item_count] = is_fav ? "Unfavorite" : "Favorite"; item_is_action[item_count++] = true;\n          if (ci.type == ADV_TYPE_CHAT) {',
    1,
)
s = s.replace(
    '            const char* actions[8];\n            uint8_t act_count = 0;\n            if (ci.type == ADV_TYPE_CHAT) {',
    '            const char* actions[8];\n            uint8_t act_count = 0;\n            bool is_fav = (ci.flags & 0x01) != 0;\n            actions[act_count++] = is_fav ? "Unfavorite" : "Favorite";\n            if (ci.type == ADV_TYPE_CHAT) {',
    1,
)
s = s.replace(
    '            const char* chosen = actions[_ct_action_sel];\n            if (strcmp(chosen, "Ping") == 0) {',
    '            const char* chosen = actions[_ct_action_sel];\n            if (strcmp(chosen, "Favorite") == 0 || strcmp(chosen, "Unfavorite") == 0) {\n              bool make_favorite = (strcmp(chosen, "Favorite") == 0);\n              if (the_mesh.setContactFavorite(ci.id.pub_key, make_favorite)) {\n                rebuildContactsSorted();\n                _ct_action_sel = 0;\n                _task->showAlert(make_favorite ? "Favorited" : "Unfavorited", 800);\n              } else {\n                _task->showAlert("Update failed", 800);\n              }\n            } else if (strcmp(chosen, "Ping") == 0) {',
    1,
)

s = s.replace('uint8_t _ct_filter;  // 0=All, 1=Contacts, 2=Repeaters', 'uint8_t _ct_filter;  // 0=All, 1=Contacts, 2=Repeaters, 3=Rooms', 1)
s = s.replace('        if (_ct_filter == 2 && ci.type != ADV_TYPE_REPEATER) continue;', '        if (_ct_filter == 2 && ci.type != ADV_TYPE_REPEATER) continue;\n        if (_ct_filter == 3 && ci.type != ADV_TYPE_ROOM) continue;')
s = s.replace('        const char* filter_name = _ct_filter == 0 ? "All" : _ct_filter == 1 ? "Contacts" : "Repeaters";', '        const char* filter_name = _ct_filter == 0 ? "All" : _ct_filter == 1 ? "Contacts" : _ct_filter == 2 ? "Repeaters" : "Rooms";', 1)
s = s.replace('_ct_filter = (_ct_filter + 2) % 3;', '_ct_filter = (_ct_filter + 3) % 4;', 1)
s = s.replace('_ct_filter = (_ct_filter + 1) % 3;', '_ct_filter = (_ct_filter + 1) % 4;', 1)

# Make the Radio rows (FREQ/SF/BW/CR) selectable so they can be edited on-device,
# and make Version clickable (it opens the Version info screen). Only Name stays
# read-only. Guarded: if upstream ever changes this predicate, the build fails loudly
# instead of silently leaving Radio navigation stuck (that was the "stuck at TX" bug).
_readonly_old = '    return id == SG_FREQ || id == SG_SF || id == SG_BW || id == SG_CR ||\n           id == SG_NAME || id == SG_VER;'
if _readonly_old not in s:
    raise SystemExit('settingIsReadonly predicate marker missing')
s = s.replace(_readonly_old, '    return id == SG_NAME;', 1)

old = 'case SG_FREQ:    snprintf(buf, len, "Freq %.3f (app)", _node_prefs->freq); break;'
new = '''case SG_FREQ: {
        uint32_t khz = (uint32_t)lroundf(_node_prefs->freq * 1000.0f);
        char f[8];
        snprintf(f, sizeof(f), "%03lu.%03lu", (unsigned long)(khz / 1000UL), (unsigned long)(khz % 1000UL));
        if (_freq_edit_mode) {
          static const uint8_t pos[6] = {0,1,2,4,5,6};
          char out[24];
          int o = 0;
          for (int i = 0; f[i] && o < (int)sizeof(out)-4; i++) {
            bool sel = (i == pos[_freq_digit]);
            if (sel) out[o++] = '[';
            out[o++] = f[i];
            if (sel) out[o++] = ']';
          }
          out[o] = 0;
          snprintf(buf, len, "Freq %s", out);
        } else {
          snprintf(buf, len, "Freq [%s] MHz", f);
        }
      } break;'''
if old not in s:
    raise SystemExit('freq row marker missing')
s = s.replace(old, new, 1)
s = s.replace('case SG_SF:      snprintf(buf, len, "SF %d (app)", _node_prefs->sf); break;', 'case SG_SF:      snprintf(buf, len, "SF [%d]", _node_prefs->sf); break;', 1)
s = s.replace('case SG_BW:      snprintf(buf, len, "BW %.0f (app)", _node_prefs->bw); break;', 'case SG_BW:      snprintf(buf, len, "BW [%.2f] kHz", _node_prefs->bw); break;', 1)
s = s.replace('case SG_CR:      snprintf(buf, len, "CR %d (app)", _node_prefs->cr); break;', 'case SG_CR:      snprintf(buf, len, "CR [4/%d]", _node_prefs->cr); break;', 1)

nav = '      // Navigation skips section headers and read-only info rows\n'
freq = '''      // Per-digit frequency editor. ENTER saves; CANCEL restores.
      if (_freq_edit_mode) {
        if (c == KEY_LEFT) {
          if (_freq_digit > 0) _freq_digit--; else _freq_digit = 5;
          return true;
        }
        if (c == KEY_RIGHT) {
          _freq_digit = (_freq_digit + 1) % 6;
          return true;
        }
        if (c == KEY_UP || c == KEY_DOWN) {
          static const uint32_t place_khz[6] = {100000UL,10000UL,1000UL,100UL,10UL,1UL};
          uint32_t khz = (uint32_t)lroundf(_node_prefs->freq * 1000.0f);
          uint32_t place = place_khz[_freq_digit];
          int oldd = (khz / place) % 10;
          int nd = (oldd + (c == KEY_UP ? 1 : 9)) % 10;
          uint32_t next = khz - (uint32_t)oldd * place + (uint32_t)nd * place;
          if (next >= 150000UL && next <= 960000UL) {
            _node_prefs->freq = next / 1000.0f;
          } else {
            _task->showAlert("150-960 MHz", 500);
          }
          return true;
        }
        if (c == KEY_ENTER) {
          radio_set_params(_node_prefs->freq, _node_prefs->bw, _node_prefs->sf, _node_prefs->cr);
          the_mesh.savePrefs();
          _freq_edit_mode = false;
          char a[24];
          snprintf(a, sizeof(a), "Freq %.3f saved", _node_prefs->freq);
          _task->showAlert(a, 700);
          return true;
        }
        if (c == KEY_CANCEL) {
          _node_prefs->freq = _freq_orig;
          _freq_edit_mode = false;
          _task->showAlert("Freq cancelled", 600);
          return true;
        }
        return true;
      }

'''
if nav not in s:
    raise SystemExit('settings nav marker missing')
s = s.replace(nav, freq + nav, 1)

gmt = '      // GMT offset: LEFT/RIGHT to adjust\n'
other = '''      // Other radio parameters: LEFT/RIGHT adjusts immediately and persists.
      if ((cur == SG_SF || cur == SG_BW || cur == SG_CR) && (c == KEY_LEFT || c == KEY_RIGHT)) {
        const int dir = (c == KEY_RIGHT) ? 1 : -1;
        if (cur == SG_SF) {
          int v = (int)_node_prefs->sf + dir;
          if (v < 5) v = 5;
          if (v > 12) v = 12;
          _node_prefs->sf = v;
        } else if (cur == SG_CR) {
          int v = (int)_node_prefs->cr + dir;
          if (v < 5) v = 5;
          if (v > 8) v = 8;
          _node_prefs->cr = v;
        } else {
          static const float bws[] = {7.8f,10.4f,15.6f,20.8f,31.25f,41.7f,62.5f,125.0f,250.0f,500.0f};
          const int nbw = sizeof(bws)/sizeof(bws[0]);
          int nearest = 0;
          float best = fabsf(_node_prefs->bw-bws[0]);
          for (int i=1; i<nbw; i++) {
            float d=fabsf(_node_prefs->bw-bws[i]);
            if (d<best) { best=d; nearest=i; }
          }
          nearest += dir;
          if (nearest<0) nearest=0;
          if (nearest>=nbw) nearest=nbw-1;
          _node_prefs->bw=bws[nearest];
        }
        radio_set_params(_node_prefs->freq, _node_prefs->bw, _node_prefs->sf, _node_prefs->cr);
        the_mesh.savePrefs();
        return true;
      }

'''
if gmt not in s:
    raise SystemExit('gmt marker missing')
s = s.replace(gmt, other + gmt, 1)

s = s.replace(
    '          case SG_TXPOWER:\n            _radio_orig_power = _node_prefs->tx_power_dbm; _radio_edit_mode = true;\n            break;',
    '          case SG_TXPOWER:\n            _radio_orig_power = _node_prefs->tx_power_dbm; _radio_edit_mode = true;\n            break;\n'
    '          case SG_FREQ:\n            _freq_orig = _node_prefs->freq; _freq_digit = 0; _freq_edit_mode = true;\n            _task->showAlert("L/R digit  U/D value", 900);\n            break;\n'
    '          case SG_SF:\n          case SG_BW:\n          case SG_CR:\n            _task->showAlert("Use LEFT / RIGHT", 800);\n            break;',
    1,
)
s = s.replace('// read-only info rows (freq/SF/BW/CR/name/version): editable via companion app', '// read-only info rows (name)', 1)


# ===================================================================================
# Monster Mesh v0.2.0 additions
#   (1) Settings -> Version: clickable row that opens a Version info screen
#   (2) Boot splash: split-flap "flip-in" animation (line 1 brand, line 2 node name)
# Each replacement below is guarded so a silent no-op can never ship.
# ===================================================================================

def _require(hay, needle, what):
    if needle not in hay:
        raise SystemExit('Monster Mesh patch marker missing: ' + what)

# ---- (1) Version info screen -------------------------------------------------------

# HomeScreen member flag for the overlay (anchored on the freq-editor member added above).
_ver_mem = '  uint8_t _freq_digit;            // 0..5 = 100MHz,10MHz,1MHz,100k,10k,1k\n'
_require(s, _ver_mem, 'version-info member anchor')
s = s.replace(
    _ver_mem,
    _ver_mem + '  bool _ver_info_active;          // Version info overlay active\n',
    1,
)

# HomeScreen ctor init (anchored on the freq-editor init added above).
_ver_ctor = '_radio_orig_power(0), _freq_edit_mode(false), _freq_orig(0), _freq_digit(0), _ct_filter(0),'
_require(s, _ver_ctor, 'version-info ctor anchor')
s = s.replace(
    _ver_ctor,
    '_radio_orig_power(0), _freq_edit_mode(false), _freq_orig(0), _freq_digit(0), _ver_info_active(false), _ct_filter(0),',
    1,
)

# Relabel the Version row as a drill-in ("Version >") instead of showing the raw
# build-version string inline; the details live on the screen it opens.
_ver_row_old = '      case SG_VER:     snprintf(buf, len, "v%s", FIRMWARE_VERSION); break;'
_require(s, _ver_row_old, 'version row-label anchor')
s = s.replace(_ver_row_old, '      case SG_VER:     snprintf(buf, len, "Version >"); break;', 1)

# ENTER on the Version row opens the overlay (inserted before the default case).
_ver_enter_old = '          default:\n            // read-only info rows (name)\n'
_require(s, _ver_enter_old, 'version-info ENTER-case anchor')
s = s.replace(
    _ver_enter_old,
    '          case SG_VER:\n'
    '            _ver_info_active = true;\n'
    '            break;\n'
    '          default:\n'
    '            // read-only info rows (name)\n',
    1,
)

# Render the overlay instead of the settings list while it is active.
_ver_render_old = (
    '    } else if (_page == HomePage::SETTINGS) {\n'
    '      display.setTextSize(1);\n'
    '      display.setColor(DisplayDriver::YELLOW);\n'
    '      display.drawTextCentered(display.width() / 2, TOP_BAR_H, "-- Settings --");\n'
)
_require(s, _ver_render_old, 'version-info render anchor')
s = s.replace(
    _ver_render_old,
    '    } else if (_page == HomePage::SETTINGS) {\n'
    '      if (_ver_info_active) {\n'
    '        display.setTextSize(1);\n'
    '        display.setColor(DisplayDriver::GREEN);\n'
    '        display.drawTextCentered(display.width() / 2, TOP_BAR_H, "Monster Mesh");\n'
    '        display.setColor(DisplayDriver::LIGHT);\n'
    '        display.drawTextCentered(display.width() / 2, TOP_BAR_H + 10, "v0.2.0  -  2026-09-12");\n'
    '        display.setColor(DisplayDriver::YELLOW);\n'
    '        display.drawTextCentered(display.width() / 2, TOP_BAR_H + 24, "A jPizZleS");\n'
    '        display.drawTextCentered(display.width() / 2, TOP_BAR_H + 34, "Meshterpiece!");\n'
    "        display.drawTextCentered(display.width() / 2, TOP_BAR_H + 44, \"It's ALLLiVE!!\");\n"
    '        return 1000;\n'
    '      }\n'
    '      display.setTextSize(1);\n'
    '      display.setColor(DisplayDriver::YELLOW);\n'
    '      display.drawTextCentered(display.width() / 2, TOP_BAR_H, "-- Settings --");\n',
    1,
)

# Any key dismisses the overlay (inserted at the top of the settings input handler).
_ver_input_old = (
    '    if (_page == HomePage::SETTINGS) {\n'
    '      uint8_t items[32];\n'
    '      int n = buildSettings(items);\n'
    '      clampSettingsSel(items, n);\n'
    '      uint8_t cur = items[_settings_sel];\n'
)
_require(s, _ver_input_old, 'version-info input anchor')
s = s.replace(
    _ver_input_old,
    _ver_input_old +
    '\n'
    '      // Version info overlay: any key dismisses and returns to the list.\n'
    '      if (_ver_info_active) {\n'
    '        if (c == KEY_ENTER || c == KEY_CANCEL || c == KEY_UP || c == KEY_DOWN ||\n'
    '            c == KEY_LEFT || c == KEY_RIGHT) {\n'
    '          _ver_info_active = false;\n'
    '        }\n'
    '        return true;\n'
    '      }\n',
    1,
)

# ---- (2) Boot splash flip-in animation ---------------------------------------------

# Add the animation clock + a split-flap reveal helper to SplashScreen.
_splash_mem_old = '  char _version_info[12];\n\npublic:\n'
_require(s, _splash_mem_old, 'splash member anchor')
s = s.replace(
    _splash_mem_old,
    '  char _version_info[12];\n'
    '  unsigned long _start_ms = 0;\n'
    '\n'
    '  // Split-flap reveal: fills `out` with `text`, each glyph settling left-to-right;\n'
    '  // returns true once all have settled. Spaces pass through unchanged.\n'
    '  static bool flipReveal(const char* text, char* out, size_t out_sz, unsigned long elapsed) {\n'
    '    static const char GLYPHS[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#%&*+=?";\n'
    '    const int nG = sizeof(GLYPHS) - 1;\n'
    '    const unsigned long PER_CHAR = 75;   // stagger between adjacent characters\n'
    '    const unsigned long FLIP_MS  = 45;   // glyph cycling speed while unsettled\n'
    '    size_t i = 0;\n'
    '    bool done = true;\n'
    '    for (; text[i] && i + 1 < out_sz; i++) {\n'
    "      if (text[i] == ' ') { out[i] = ' '; continue; }\n"
    '      unsigned long settle = (unsigned long)(i + 1) * PER_CHAR;\n'
    '      if (elapsed >= settle) {\n'
    '        out[i] = text[i];\n'
    '      } else {\n'
    '        done = false;\n'
    '        out[i] = GLYPHS[((elapsed / FLIP_MS) + i * 7) % nG];\n'
    '      }\n'
    '    }\n'
    '    out[i] = 0;\n'
    '    return done;\n'
    '  }\n'
    '\n'
    'public:\n',
    1,
)

# Record the start time in the constructor.
_splash_ctor_old = '    dismiss_after = millis() + BOOT_SCREEN_MILLIS;\n'
_require(s, _splash_ctor_old, 'splash ctor anchor')
s = s.replace(
    _splash_ctor_old,
    '    _start_ms = millis();\n'
    '    dismiss_after = _start_ms + BOOT_SCREEN_MILLIS;\n',
    1,
)

# Replace the static splash body with the animated two-line flip-in.
_splash_render_old = (
    '  int render(DisplayDriver& display) override {\n'
    '    // meshcore logo\n'
    '    display.setColor(DisplayDriver::BLUE);\n'
    '    int logoWidth = 128;\n'
    '    display.drawXbm((display.width() - logoWidth) / 2, 3, meshcore_logo, logoWidth, 13);\n'
    '\n'
    '    // version info\n'
    '    display.setColor(DisplayDriver::LIGHT);\n'
    '    display.setTextSize(2);\n'
    '    display.drawTextCentered(display.width()/2, 22, _version_info);\n'
    '\n'
    '    display.setTextSize(1);\n'
    '    display.drawTextCentered(display.width()/2, 42, FIRMWARE_BUILD_DATE);\n'
    '\n'
    '    display.setColor(DisplayDriver::YELLOW);\n'
    '    display.drawTextCentered(display.width()/2, 54, "custom digitaino fw");\n'
    '\n'
    '    return 1000;\n'
    '  }\n'
)
_require(s, _splash_render_old, 'splash render anchor')
s = s.replace(
    _splash_render_old,
    '  int render(DisplayDriver& display) override {\n'
    '    unsigned long elapsed = millis() - _start_ms;\n'
    '\n'
    '    char line1[24], line2[24];\n'
    '    const char* name = the_mesh.getNodePrefs()->node_name;\n'
    '    if (!name || !name[0]) name = "Monster";\n'
    '    bool done1 = flipReveal("Monster Mesh", line1, sizeof(line1), elapsed);\n'
    '    const unsigned long LINE2_LAG = 450;   // line 2 begins a beat after line 1\n'
    '    bool done2 = flipReveal(name, line2, sizeof(line2),\n'
    '                            elapsed > LINE2_LAG ? elapsed - LINE2_LAG : 0);\n'
    '\n'
    '    display.setTextSize(1);\n'
    '    display.setColor(DisplayDriver::GREEN);\n'
    '    display.drawTextCentered(display.width()/2, 16, line1);\n'
    '    display.setColor(DisplayDriver::LIGHT);\n'
    '    display.drawTextCentered(display.width()/2, 30, line2);\n'
    '\n'
    '    // Once both lines settle, reveal version + build date beneath.\n'
    '    if (done1 && done2) {\n'
    '      display.setColor(DisplayDriver::YELLOW);\n'
    '      display.drawTextCentered(display.width()/2, 46, _version_info);\n'
    '      display.drawTextCentered(display.width()/2, 56, FIRMWARE_BUILD_DATE);\n'
    '      return 250;\n'
    '    }\n'
    '    return 45;   // keep animating the flip\n'
    '  }\n',
    1,
)

p.write_text(s)
