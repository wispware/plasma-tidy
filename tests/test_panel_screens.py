# SPDX-FileCopyrightText: 2026 seanmamasde
# SPDX-License-Identifier: GPL-3.0-or-later
"""A panel on a screen that is gone (a dock unplugged): plasmashell 6.8 crashes when a script
reads or sets its hiding or lengthMode. Tidy's own scripts run here against panels that throw
where plasmashell would crash."""

import unittest

from tests import SRC  # noqa: F401

from PyQt6.QtWidgets import QApplication

from plasma_tidy.plasma import Plasma

try:
    from PyQt6.QtQml import QJSEngine
except ImportError:  # a PyQt6 without its QML part
    QJSEngine = None

app = QApplication.instance() or QApplication([])

# plasmashell's scripting, as far as these scripts use it: one screen, panel 82 on it, and
# panel 148 that still says screen 1, which is unplugged.
SHELL = """
var screenCount = 1, printed = "", wrote = {};
function print(text) { printed += text; }
function panel(id, screen) {
    var p = {id: id, screen: screen, location: "bottom", widgets: function () { return []; }};
    var now = {hiding: "autohide", lengthMode: "fit"};
    Object.keys(now).forEach(function (name) {
        Object.defineProperty(p, name, {
            get: function () {
                if (screen >= screenCount) throw new Error("plasmashell crashed reading " + name);
                return now[name];
            },
            set: function (v) {
                if (screen >= screenCount) throw new Error("plasmashell crashed setting " + name);
                wrote[id] = v;
            }});
    });
    return p;
}
function panels() { return [panel(82, 0), panel(148, 1)]; }
"""


@unittest.skipIf(QJSEngine is None, "needs PyQt6.QtQml to run the scripts")
class PanelOnAScreenThatIsGone(unittest.TestCase):
    def setUp(self):
        self.engine = QJSEngine()
        self.plasma = Plasma()
        self.plasma.run = self.fake_run   # never the real Plasma

    def fake_run(self, script):
        out = self.engine.evaluate(SHELL + script + "\nprinted")
        self.assertFalse(out.isError(), out.toString())
        return out.toString()

    def test_its_mode_is_not_asked(self):
        self.assertEqual(self.plasma.panel_modes(), {82: "autohide"})

    def test_its_mode_is_not_set(self):
        self.plasma.set_panel_modes({82: "none", 148: "none"})
        self.assertEqual(self.engine.evaluate("JSON.stringify(wrote)").toString(), '{"82":"none"}')

    def test_it_is_listed_but_not_asked_whether_it_fits(self):
        found = self.plasma.panel_widgets()
        self.assertEqual([(p["panel"], p["fit"]) for p in found], [(82, True), (148, False)])


if __name__ == "__main__":
    unittest.main()
