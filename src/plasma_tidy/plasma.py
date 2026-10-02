# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""Talking to plasmashell, and looking up names and icons of programs and widgets."""

import json
import os
import re

from PyQt6.QtCore import QLibraryInfo
from PyQt6.QtDBus import QDBusConnection, QDBusInterface
from PyQt6.QtGui import QIcon

from .consts import (DRAWER_DEFAULTS, DRAWER_ID, FADE_ID, PANEL_NAMES, PLACE_AFTER, PLACE_BEFORE,
                     TASK_PLUGINS, TRAY_NAMES)
from .i18n import speaks_dutch, tr
from .widgets import drawer_value


def app_icon(app_id):
    """The icon of a program, looked up in its .desktop file; an empty icon if not found."""
    name = app_id if app_id.endswith(".desktop") else app_id + ".desktop"
    bases = [os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")]
    bases += (os.environ.get("XDG_DATA_DIRS") or "/usr/local/share:/usr/share").split(":")
    for base in bases:
        try:
            with open(os.path.join(base, "applications", name), errors="replace") as f:
                for line in f:
                    if line.startswith("Icon="):
                        icon = line[5:].strip()
                        return QIcon(icon) if os.path.isabs(icon) else QIcon.fromTheme(icon)
        except OSError:
            continue
    return QIcon()


def widget_name(plugin):
    """What a widget is called, from its own description; in Dutch when Tidy speaks Dutch."""
    for base in (os.path.expanduser("~/.local/share"), "/usr/local/share", "/usr/share"):
        try:
            with open(os.path.join(base, "plasma/plasmoids", plugin, "metadata.json")) as f:
                about = json.load(f).get("KPlugin", {})
        except (OSError, ValueError):
            continue
        name = (about.get("Name[nl]") if speaks_dutch() else None) or about.get("Name")
        if name:
            return name
    return compiled_widget_name(plugin) or panel_widget_name(plugin)


def compiled_widget_name(plugin):
    """The name of a widget that Plasma ships as a compiled plugin. Its description sits in
    the file in Qt's packed form (CBOR); the name is picked out of it by hand."""
    path = os.path.join(QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath),
                        "plasma", "applets", plugin + ".so")
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        return None

    def text_at(pos):
        # A short text: one byte 0x60 + length, or 0x78 and a length byte; then the text.
        if pos >= len(data):
            return None, pos
        if 0x60 <= data[pos] < 0x78:
            length, pos = data[pos] - 0x60, pos + 1
        elif data[pos] == 0x78 and pos + 1 < len(data):
            length, pos = data[pos + 1], pos + 2
        else:
            return None, pos
        try:
            return data[pos:pos + length].decode(), pos + length
        except UnicodeDecodeError:
            return None, pos

    def value_of(key, start):
        head = bytes([0x60 + len(key)]) + key.encode()
        pos = data.find(head, start)
        return text_at(pos + len(head))[0] if pos >= 0 else None

    # The widget's own name comes after its license; the names before that are its authors.
    start = max(0, data.find(b"\x67License"))
    dutch = value_of("Name[nl]", start) if speaks_dutch() else None
    return dutch or value_of("Name", start)


def panels_below_windows():
    """The panels that Plasma's settings file has on "windows go below" (panelVisibility 3)."""
    found, panel = set(), None
    try:
        with open(os.path.expanduser("~/.config/plasmashellrc")) as f:
            for line in f:
                group = re.match(r"\[PlasmaViews\]\[Panel (\d+)\]$", line.strip())
                if line.startswith("["):
                    panel = int(group.group(1)) if group else None
                elif panel is not None and line.strip() == "panelVisibility=3":
                    found.add(panel)
    except OSError:
        pass
    return found


def panel_widget_name(plugin):
    if plugin in PANEL_NAMES:
        return tr(PANEL_NAMES[plugin])
    if plugin in TRAY_NAMES:
        return tr(TRAY_NAMES[plugin])
    return plugin.rsplit(".", 1)[-1]


class Plasma:
    """Talks to plasmashell through its scripting interface."""

    def __init__(self):
        self.iface = QDBusInterface("org.kde.plasmashell", "/PlasmaShell",
                                    "org.kde.PlasmaShell", QDBusConnection.sessionBus())
        # A Plasma that hangs must not make Tidy hang along for long.
        self.iface.setTimeout(3000)

    def run(self, script):
        reply = self.iface.call("evaluateScript", script)
        args = reply.arguments()
        return args[0] if args else ""

    def desktop_urls(self):
        out = self.run("""
            var r = {};
            desktops().forEach(function (d) {
                if (d.type != "org.kde.plasma.folder") return;
                d.currentConfigGroup = ["General"];
                r[d.id] = d.readConfig("url") || "desktop:/";
            });
            print(JSON.stringify(r));""")
        try:
            return {int(k): v for k, v in json.loads(out).items()}
        except ValueError:
            return {}

    def ensure_helpers(self, wanted):
        """Have a helper on every desktop that is on a screen, or none at all. Returns how
        many there are afterwards."""
        out = self.run("var type = %s, wanted = %s;" % (json.dumps(FADE_ID), json.dumps(wanted)) + """
            var n = 0;
            desktops().forEach(function (d) {
                if (d.type != "org.kde.plasma.folder") return;
                var have = d.widgets().filter(function (w) { return w.type == type; });
                if (!wanted) { have.forEach(function (w) { w.remove(); }); return; }
                if (d.screen < 0) return;  // not on a screen now: counted when it is
                if (!have.length) {
                    var w = d.addWidget(type);
                    if (w && w.id) n++;
                }
                n += have.length;
            });
            print(n);""")
        try:
            return int(out)
        except ValueError:
            return 0

    def desktop_widgets(self):
        """The widgets on the desktops, without our own helper: [{id, type}]."""
        out = self.run("var own = %s;" % json.dumps(FADE_ID) + """
            var r = [];
            desktops().forEach(function (d) { d.widgets().forEach(function (w) {
                if (w.type != own) r.push({id: w.id, type: w.type});
            }); });
            print(JSON.stringify(r));""")
        try:
            return json.loads(out)
        except ValueError:
            return []

    def set_helper_debug(self, text):
        """For testing: the helpers' own switch for telling what they see."""
        self.run("var type = %s, text = %s;" % (json.dumps(FADE_ID), json.dumps(text)) + """
            desktops().forEach(function (d) { d.widgets().forEach(function (w) {
                if (w.type != type) return;
                w.currentConfigGroup = ["General"];
                w.writeConfig("debug", text);
                w.reloadConfig();
            }); });""")

    def desktop_screens(self):
        """Where each desktop is shown: {desktop id: (x, y, width, height)}; desktops that are
        not on a screen right now are left out."""
        out = self.run("""
            var r = {};
            desktops().forEach(function (d) {
                if (d.type != "org.kde.plasma.folder" || d.screen < 0) return;
                var g = screenGeometry(d.screen);
                r[d.id] = [g.x, g.y, g.width, g.height];
            });
            print(JSON.stringify(r));""")
        try:
            return {int(k): tuple(int(round(i)) for i in v) for k, v in json.loads(out).items()}
        except (ValueError, TypeError):
            return {}

    def set_desktop_urls(self, urls):
        self.run("var urls = %s;" % json.dumps({str(k): v for k, v in urls.items()}) + """
            desktops().forEach(function (d) {
                if (!(d.id in urls)) return;
                d.currentConfigGroup = ["General"];
                d.writeConfig("url", urls[d.id]);
                d.reloadConfig();
            });""")

    def panel_modes(self):
        out = self.run("""
            var r = {};
            panels().forEach(function (p) { r[p.id] = p.hiding; });
            print(JSON.stringify(r));""")
        try:
            modes = {int(k): v for k, v in json.loads(out).items()}
        except ValueError:
            return {}
        # Plasma reports "windows go below" as "none". Its own settings file knows better.
        if "none" in modes.values():
            below = panels_below_windows()
            modes = {k: "windowsgobelow" if v == "none" and k in below else v
                     for k, v in modes.items()}
        return modes

    def tray_config(self):
        """System tray settings: its plasmoids and the shown/hidden lists."""
        out = self.run("""
            var r = null;
            panels().forEach(function (p) { p.widgets().forEach(function (w) {
                if (r || w.type != "org.kde.plasma.systemtray") return;
                w.currentConfigGroup = ["General"];
                var get = function (k) {
                    var v = w.readConfig(k);
                    if (!v) return [];
                    return Array.isArray(v) ? v : String(v).split(",");
                };
                r = {extra: get("extraItems"), known: get("knownItems"),
                     shown: get("shownItems"), hidden: get("hiddenItems")};
            }); });
            print(JSON.stringify(r));""")
        try:
            return json.loads(out) or None
        except ValueError:
            return None

    def set_tray_config(self, extra, shown, hidden):
        self.run("var c = %s;" % json.dumps({"extra": extra, "shown": shown, "hidden": hidden}) + """
            panels().forEach(function (p) { p.widgets().forEach(function (w) {
                if (w.type != "org.kde.plasma.systemtray") return;
                w.currentConfigGroup = ["General"];
                w.writeConfig("extraItems", c.extra);
                w.writeConfig("shownItems", c.shown);
                w.writeConfig("hiddenItems", c.hidden);
                w.reloadConfig();
            }); });""")

    def set_panel_modes(self, modes):
        self.run("var m = %s;" % json.dumps({str(k): v for k, v in modes.items()}) + """
            panels().forEach(function (p) { if (p.id in m) p.hiding = m[p.id]; });""")

    def panel_widgets(self):
        """The panels with their widgets, in the order they have in the panel."""
        out = self.run("""
            var r = [];
            panels().forEach(function (p) {
                // "fit": the panel is as long as its contents, and changes size with them
                r.push({panel: p.id, location: p.location, fit: p.lengthMode == "fit",
                        widgets: p.widgets().map(function (w) {
                            return {id: w.id, type: w.type, index: w.index};
                        })});
            });
            print(JSON.stringify(r));""")
        try:
            found = json.loads(out)
        except ValueError:
            return []
        for panel in found:
            panel["widgets"].sort(key=lambda w: w["index"])
        return found

    def drawers(self):
        """Every Tidy drawer in the panels, with its settings."""
        out = self.run("var keys = %s, type = %s;" % (json.dumps(list(DRAWER_DEFAULTS)),
                                                      json.dumps(DRAWER_ID)) + """
            var r = [];
            panels().forEach(function (p) { p.widgets().forEach(function (w) {
                if (w.type != type) return;
                w.currentConfigGroup = ["General"];
                var c = {};
                keys.forEach(function (k) { c[k] = w.readConfig(k); });
                r.push({id: w.id, panel: p.id, config: c, shortcut: String(w.globalShortcut || "")});
            }); });
            print(JSON.stringify(r));""")
        try:
            found = json.loads(out)
        except ValueError:
            return []
        for drawer in found:
            drawer["config"] = {k: drawer_value(k, drawer["config"].get(k))
                                for k in DRAWER_DEFAULTS}
        return found

    def set_drawer_config(self, drawer_id, config):
        """Write settings to one drawer, or to all of them with drawer_id None."""
        self.run("var id = %s, c = %s, type = %s;" % (json.dumps(drawer_id), json.dumps(config),
                                                      json.dumps(DRAWER_ID)) + """
            panels().forEach(function (p) { p.widgets().forEach(function (w) {
                if (w.type != type || (id !== null && w.id != id)) return;
                w.currentConfigGroup = ["General"];
                for (var k in c) w.writeConfig(k, c[k]);
                w.reloadConfig();
            }); });""")

    def add_drawer(self, panel_id, config):
        """Add a drawer to a panel and put it next to its widgets. Returns its id, or None."""
        out = self.run("var panel = %d, c = %s, type = %s;" % (panel_id, json.dumps(config),
                                                               json.dumps(DRAWER_ID)) + """
            var id = -1;
            panels().forEach(function (p) {
                if (p.id != panel) return;
                var w = p.addWidget(type);
                if (!w || !w.id) return;
                w.currentConfigGroup = ["General"];
                for (var k in c) w.writeConfig(k, c[k]);
                w.reloadConfig();
                id = w.id;
            });
            print(id);""")
        try:
            new_id = int(out)
        except ValueError:
            return None
        if new_id < 0:
            return None
        # In a call of its own: only then does the panel know the new widget's place.
        self.place_drawer(new_id, config.get("targets", []), config.get("place", PLACE_BEFORE))
        return new_id

    def place_drawer(self, drawer_id, targets, where):
        """Move a drawer's arrow next to the widgets it hides: just before the first of them
        or just after the last."""
        if where not in (PLACE_BEFORE, PLACE_AFTER) or not targets:
            return
        self.run("var id = %d, targets = %s, after = %s;" % (
            drawer_id, json.dumps([str(i) for i in targets]), json.dumps(where == PLACE_AFTER)) + """
            panels().forEach(function (p) {
                var me = null, anchor = null;
                p.widgets().forEach(function (w) {
                    if (w.id == id) { me = w; return; }
                    if (targets.indexOf(String(w.id)) < 0) return;
                    if (!anchor || (after ? w.index > anchor.index : w.index < anchor.index))
                        anchor = w;
                });
                if (!me || !anchor) return;
                // Our own slot disappears from the order when we move, so everything behind
                // us shifts one place.
                var want = anchor.index + (after ? 1 : 0) - (me.index < anchor.index ? 1 : 0);
                if (want != me.index) me.index = want;
            });""")

    def set_drawer_shortcut(self, drawer_id, shortcut):
        """The drawer's own keyboard shortcut, e.g. "Meta+D"; empty for none."""
        self.run("var id = %d, s = %s;" % (drawer_id, json.dumps(shortcut)) + """
            panels().forEach(function (p) { p.widgets().forEach(function (w) {
                if (w.id == id) w.globalShortcut = s;
            }); });""")

    def remove_drawer(self, drawer_id):
        # Open it first, so that everything it hides is back before it goes.
        self.set_drawer_config(drawer_id, {"closed": False})
        self.run("var id = %d, type = %s;" % (drawer_id, json.dumps(DRAWER_ID)) + """
            panels().forEach(function (p) { p.widgets().forEach(function (w) {
                if (w.type == type && w.id == id) w.remove();
            }); });""")

    def task_launchers(self):
        """The pinned programs of every task manager in the panels: {widget id: [urls]}."""
        out = self.run("var types = %s;" % json.dumps(TASK_PLUGINS) + """
            var r = {};
            panels().forEach(function (p) { p.widgets().forEach(function (w) {
                if (types.indexOf(w.type) < 0) return;
                w.currentConfigGroup = ["General"];
                var v = w.readConfig("launchers");
                r[w.id] = !v ? [] : (Array.isArray(v) ? v : String(v).split(","));
            }); });
            print(JSON.stringify(r));""")
        try:
            return {int(k): [i for i in v if i] for k, v in json.loads(out).items()}
        except ValueError:
            return {}

    def held_launchers(self):
        """Pinned programs that closed drawers are holding: {task manager id: [urls]}."""
        out = self.run("var type = %s;" % json.dumps(DRAWER_ID) + """
            var r = [];
            panels().forEach(function (p) { p.widgets().forEach(function (w) {
                if (w.type != type) return;
                w.currentConfigGroup = ["General"];
                r.push(String(w.readConfig("savedLaunchers") || "{}"));
            }); });
            print(JSON.stringify(r));""")
        held = {}
        try:
            for text in json.loads(out):
                for widget_id, launchers in json.loads(text).items():
                    held[int(widget_id)] = [i for i in launchers if i]
        except (ValueError, AttributeError, TypeError):
            pass
        return held

    def set_task_launchers(self, widget_id, launchers):
        self.run("var id = %d, list = %s;" % (widget_id, json.dumps(launchers)) + """
            panels().forEach(function (p) { p.widgets().forEach(function (w) {
                if (w.id != id) return;
                w.currentConfigGroup = ["General"];
                w.writeConfig("launchers", list);
                w.reloadConfig();
            }); });""")

    def set_drawers_closed(self, closed):
        """Close (True) or open (False) every drawer. None switches: close them all if one
        is open, otherwise open them all."""
        self.run("var want = %s, type = %s;" % (json.dumps(closed), json.dumps(DRAWER_ID)) + """
            var list = [];
            panels().forEach(function (p) { p.widgets().forEach(function (w) {
                if (w.type != type) return;
                w.currentConfigGroup = ["General"];
                list.push(w);
            }); });
            if (want === null)
                want = list.some(function (w) { return String(w.readConfig("closed")) != "true"; });
            list.forEach(function (w) { w.writeConfig("closed", want); w.reloadConfig(); });""")
