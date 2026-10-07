# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""Tidy's look at itself: what the widgets and KWin report, and what Tidy makes of it."""

import json
import unittest

from tests import SRC  # noqa: F401
from tests.fakes import FakeTidy

from plasma_tidy.checks import KWIN_PARTS, MISSING, OK, UNUSED, Checks
from plasma_tidy.core import Tidy
from plasma_tidy.i18n import set_language


class Reports(unittest.TestCase):
    def setUp(self):
        set_language("en")
        self.checks = Checks()

    def test_all_well_says_nothing(self):
        self.checks.take("kwin", "", {part: OK for part in KWIN_PARTS})
        self.checks.take("drawer", "39", {"panel": OK, "tasks": OK, "tray": UNUSED})
        self.assertEqual(self.checks.problems(), [])
        self.assertEqual(self.checks.notice("6.7.5"), "")

    def test_each_part_that_does_not_work_is_named_once(self):
        self.checks.take("drawer", "39", {"panel": OK, "tasks": MISSING})
        self.checks.take("drawer", "40", {"panel": OK, "tasks": MISSING, "tray": MISSING})
        self.checks.take("helper", "1", {"icons": MISSING})
        self.assertEqual(self.checks.problems(), [
            "the desktop helper",
            "hiding programs in a drawer", "the system tray in a drawer"])
        notice = self.checks.notice("6.8.0")
        self.assertIn("6.8.0", notice)
        self.assertIn("hiding programs in a drawer", notice)

    def test_nonsense_is_ignored(self):
        self.checks.take("drawer", "39", "not a table")
        self.checks.take("drawer", "40", {"panel": 3})
        self.assertEqual(self.checks.problems(), [])

    def test_the_full_report(self):
        self.checks.take("kwin", "", {"active": OK, "panels": MISSING})
        self.checks.take("drawer", "39", {"panel": OK})
        text = self.checks.report("0.2.0", "6.7.5", {"39": "programs left"})
        self.assertIn("Tidy 0.2.0 on Plasma 6.7.5", text)
        self.assertIn("Drawer: programs left", text)
        self.assertIn("drawers closing when the panel hides: does not work in this version", text)
        self.assertIn("Desktop helper\n  has not reported (yet)", text)


class Telling(unittest.TestCase):
    """Tidy says it once per Plasma version and set of problems."""

    def setUp(self):
        set_language("en")
        self.tidy = FakeTidy()
        self.tidy.checks = Checks()
        self.tidy.check_timer = type("T", (), {"start": lambda self: None})()
        self.tidy.plasma_version = lambda: self.version
        self.tidy.plasma = type("Plasma", (), {"drawers": lambda _: [{"id": 39, "config": {}}],
                                               "desktops_on_screen": lambda _: {"1"}})()
        self.told = []
        self.tidy.tray = type("Tray", (), {"showMessage": lambda _, *a: self.told.append(a[1])})()
        self.version = "6.7.5"

    def report(self, found):
        Tidy.on_check(self.tidy, "drawer", "39", json.dumps(found))
        Tidy.review_checks(self.tidy)

    def test_once_per_version(self):
        self.report({"tasks": MISSING})
        self.report({"tasks": MISSING})
        self.assertEqual(len(self.told), 1)
        self.version = "6.8.0"
        self.report({"tasks": MISSING})
        self.assertEqual(len(self.told), 2)

    def test_a_drawer_that_is_gone_is_forgotten(self):
        Tidy.on_check(self.tidy, "drawer", "77", json.dumps({"tasks": MISSING}))
        Tidy.review_checks(self.tidy)
        self.assertEqual(self.told, [])
        self.assertNotIn("77", self.tidy.checks.drawers)

    def test_a_desktop_without_a_screen_is_left_out(self):
        # A second screen was unplugged: its desktop stays, with nothing in it to find.
        Tidy.on_check(self.tidy, "helper", "29", json.dumps({"view": MISSING}))
        Tidy.on_check(self.tidy, "helper", "1", json.dumps({"view": OK}))
        Tidy.review_checks(self.tidy)
        self.assertEqual(self.told, [])
        self.assertEqual(list(self.tidy.checks.helpers), ["1"])

    def test_nothing_when_all_is_well(self):
        self.report({"tasks": OK})
        self.assertEqual(self.told, [])


if __name__ == "__main__":
    unittest.main()
