# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""The small things: tray rules, the warning for a bare key, reading a drawer's settings."""

import tempfile
import unittest
from unittest import mock

from tests import SRC  # noqa: F401

from PyQt6.QtGui import QKeySequence

from plasma_tidy.consts import TRAY_HIDDEN, TRAY_SHOWN
from plasma_tidy.peek import bare_key
from plasma_tidy.plasma import config_value, plasma_balloons, set_plasma_balloons
from plasma_tidy.tray import tray_minimal, tray_rule_mode
from plasma_tidy.widgets import drawer_value


class TrayRules(unittest.TestCase):
    RULES = [{"match": "disc", "mode": TRAY_HIDDEN}, {"match": "Tele", "mode": TRAY_SHOWN}]

    def test_matches_part_of_the_name_whatever_the_case(self):
        self.assertEqual(tray_rule_mode(self.RULES, "discord_status_icon_1", ""), TRAY_HIDDEN)
        self.assertEqual(tray_rule_mode(self.RULES, "x", "Telegram Desktop"), TRAY_SHOWN)

    def test_no_rule_no_answer(self):
        self.assertIsNone(tray_rule_mode(self.RULES, "steam", "Steam"))

    def test_minimal_keeps_what_was_off_switched_off(self):
        config = {"known": ["org.kde.plasma.volume", "org.kde.plasma.clipboard"],
                  "extra": ["org.kde.plasma.volume"], "shown": [], "hidden": []}
        extra, shown, hidden = tray_minimal(config, {"steam": "Steam"})
        self.assertEqual(extra, ["org.kde.plasma.volume"])
        self.assertEqual(shown, ["org.kde.plasma.volume"])
        self.assertEqual(hidden, ["steam"])


class BareKeys(unittest.TestCase):
    def test_a_key_programs_need_themselves(self):
        for key in ("Right", "Space", "A", "Shift+A"):
            self.assertTrue(bare_key(QKeySequence(key)), key)

    def test_a_key_that_is_free_to_take(self):
        for key in ("Meta+Z", "Ctrl+Right", "Alt+A", "F12", "Pause", ""):
            self.assertFalse(bare_key(QKeySequence(key)), key)


class DrawerSettings(unittest.TestCase):
    """Plasma hands every setting over as text."""

    def test_types_follow_the_defaults(self):
        self.assertIs(drawer_value("closed", "true"), True)
        self.assertIs(drawer_value("closed", "false"), False)
        self.assertEqual(drawer_value("hoverDelay", "250"), 250)
        self.assertEqual(drawer_value("targets", "5,7"), ["5", "7"])
        self.assertEqual(drawer_value("targets", ["5", 7]), ["5", "7"])
        self.assertEqual(drawer_value("name", "left"), "left")

    def test_nothing_gives_the_default(self):
        self.assertEqual(drawer_value("hoverDelay", ""), 200)
        self.assertEqual(drawer_value("targets", None), [])
        self.assertEqual(drawer_value("hoverDelay", "nonsense"), 200)


class Balloons(unittest.TestCase):
    """Plasma's own switch for its text balloons: no delay above zero means off."""

    def read(self, text):
        with mock.patch("plasma_tidy.plasma.plasmarc_delay", return_value=text):
            return plasma_balloons()

    def test_a_delay_is_on_and_none_or_below_zero_is_off(self):
        self.assertTrue(self.read("700"))
        self.assertTrue(self.read("0,3"))
        self.assertFalse(self.read("0"))
        self.assertFalse(self.read("-1"))

    def test_nonsense_is_on(self):
        self.assertTrue(self.read("soon"))

    def test_reading_the_settings_file(self):
        with tempfile.NamedTemporaryFile("w", suffix="rc") as f:
            f.write("[Other]\nDelay=5\n\n[PlasmaToolTips]\nDelay=-1\n\n[Theme]\nname=x\n")
            f.flush()
            self.assertEqual(config_value(f.name, "PlasmaToolTips", "Delay"), "-1")
            self.assertEqual(config_value(f.name, "Theme", "name"), "x")
            self.assertIsNone(config_value(f.name, "Theme", "Delay"))
        self.assertIsNone(config_value("/nonexistent/plasmarc", "PlasmaToolTips", "Delay"))

    def test_on_removes_the_setting_and_off_writes_it(self):
        with mock.patch("plasma_tidy.plasma.QProcess") as process:
            start = process.return_value.start
            set_plasma_balloons(True)
            self.assertEqual(start.call_args[0][1][-1], "--delete")
            set_plasma_balloons(False)
            self.assertEqual(start.call_args[0][1][-2:], ["--", "-1"])
            self.assertIn("--notify", start.call_args[0][1])  # or Plasma only sees it after a restart


if __name__ == "__main__":
    unittest.main()
