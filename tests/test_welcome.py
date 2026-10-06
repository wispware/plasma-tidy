# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""The welcome window: what its choices set in motion."""

import unittest

from tests.fakes import FakeTidy

from PyQt6.QtWidgets import QApplication

from plasma_tidy import welcome
from plasma_tidy.consts import APP

app = QApplication.instance() or QApplication([])


class Plasma:
    """A panel with a start menu, a task manager and a system tray."""

    def __init__(self, drawers=()):
        self.found = list(drawers)
        self.added = []
        self.tray = None

    def drawers(self):
        return self.found

    def panel_widgets(self):
        return [{"panel": 2, "location": "bottom", "widgets": [
            {"id": 3, "type": "org.kde.plasma.kickoff", "index": 0},
            {"id": 5, "type": "org.kde.plasma.icontasks", "index": 1},
            {"id": 7, "type": "org.kde.plasma.systemtray", "index": 2}]}]

    def tray_config(self):
        return {"known": ["org.kde.plasma.volume", "org.kde.plasma.clipboard"],
                "extra": ["org.kde.plasma.volume", "org.kde.plasma.clipboard"],
                "shown": [], "hidden": []}

    def add_drawer(self, panel, config):
        self.added.append((panel, config["targets"]))
        self.closed = config.get("closed")

    def set_tray_config(self, extra, shown, hidden):
        self.tray = (extra, shown, hidden)


def window(plasma):
    tidy = FakeTidy()
    tidy.plasma = plasma
    tidy.autostart = None
    tidy.set_autostart = lambda on: setattr(tidy, "autostart", on)
    tidy.backup_launchers = lambda: None
    tidy.after_settings = lambda *args: None
    tidy.hidden_setup = lambda: ()
    welcome.install_drawer = lambda: None       # nothing is written to disk here
    welcome.tray_app_items = lambda: {APP: "Tidy", "steam": "Steam"}
    return tidy, welcome.Welcome(tidy)


class Choices(unittest.TestCase):
    def test_nothing_ticked_changes_only_the_three_settings(self):
        plasma = Plasma()
        tidy, dialog = window(plasma)
        dialog.timeout.setValue(20)
        dialog.save()
        self.assertEqual(tidy.settings.value("timeout"), 20)
        self.assertTrue(tidy.autostart)
        self.assertEqual(plasma.added, [])
        self.assertIsNone(plasma.tray)

    def test_a_drawer_for_the_task_manager(self):
        plasma = Plasma()
        tidy, dialog = window(plasma)
        self.assertTrue(dialog.drawer.isEnabled())
        dialog.drawer.setChecked(True)
        dialog.save()
        self.assertEqual(plasma.added, [(2, ["5"])])
        self.assertTrue(plasma.closed)   # the programs are tucked away at once

    def test_no_second_drawer_for_the_same_task_manager(self):
        plasma = Plasma(drawers=[{"id": 39, "config": {"targets": ["5"]}}])
        tidy, dialog = window(plasma)
        self.assertFalse(dialog.drawer.isEnabled())

    def test_the_tray_keeps_tidys_own_icon_in_view(self):
        plasma = Plasma()
        tidy, dialog = window(plasma)
        dialog.tray.setChecked(True)
        dialog.save()
        extra, shown, hidden = plasma.tray
        self.assertIn(APP, shown)
        self.assertNotIn(APP, hidden)
        self.assertIn("org.kde.plasma.volume", shown)
        self.assertIn("steam", hidden)
        self.assertIn("org.kde.plasma.clipboard", hidden)
        self.assertTrue(tidy.settings.value("tray_original"))  # for "Restore everything"


if __name__ == "__main__":
    unittest.main()
