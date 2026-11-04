# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""How a panel is set: Plasma reports "windows go below" as "none", and its settings file,
which knows better, is written some seconds late."""

import json
import os
import pathlib
import tempfile
import time
import unittest
from unittest import mock

from tests import SRC  # noqa: F401

from plasma_tidy.plasma import Plasma


class Memory:
    """Tidy's settings, as far as Plasma uses them."""

    def __init__(self):
        self.values = {}

    def value(self, key, default=None):
        return self.values.get(key, default)

    def setValue(self, key, value):
        self.values[key] = value

    def sync(self):
        pass


class PanelModes(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.TemporaryDirectory()
        self.addCleanup(self.home.cleanup)
        patch = mock.patch.dict(os.environ, {"HOME": self.home.name})
        patch.start()
        self.addCleanup(patch.stop)
        self.rc = pathlib.Path(self.home.name, ".config", "plasmashellrc")
        self.rc.parent.mkdir()
        self.reported = {"2": "none"}   # what Plasma's scripting says
        self.memory = Memory()
        self.plasma = Plasma(self.memory)
        self.plasma.run = self.fake_run   # never the real Plasma

    def fake_run(self, script):
        self.plasma.reached = True
        if "p.hiding = m[p.id]" in script:
            return ""
        return json.dumps(self.reported)

    def write_rc(self, visibility, age=0):
        self.rc.write_text("[PlasmaViews][Panel 2]\npanelVisibility=%d\n" % visibility)
        then = time.time() - age
        os.utime(self.rc, (then, then))

    def test_the_settings_file_tells_windows_go_below(self):
        self.write_rc(3)
        self.assertEqual(self.plasma.panel_modes(), {2: "windowsgobelow"})
        self.write_rc(0)
        self.assertEqual(self.plasma.panel_modes(), {2: "none"})

    def test_just_set_counts_before_the_file_catches_up(self):
        # Tidy puts the panel back on "windows go below" and is started again at once:
        # Plasma has not written its file yet, which still says "always visible".
        self.write_rc(0, age=60)
        self.plasma.set_panel_modes({2: "windowsgobelow"})
        self.assertEqual(self.plasma.panel_modes(), {2: "windowsgobelow"})
        # A new Tidy reads the same from its settings.
        again = Plasma(self.memory)
        again.run = self.fake_run
        self.assertEqual(again.panel_modes(), {2: "windowsgobelow"})

    def test_the_other_way_round(self):
        self.write_rc(3, age=60)
        self.plasma.set_panel_modes({2: "none"})
        self.assertEqual(self.plasma.panel_modes(), {2: "none"})

    def test_once_the_file_is_written_it_counts(self):
        self.write_rc(0, age=60)
        self.plasma.set_panel_modes({2: "windowsgobelow"})
        self.write_rc(0)   # written after: someone set it back to always visible
        self.assertEqual(self.plasma.panel_modes(), {2: "none"})

    def test_other_modes_are_told_by_plasma_itself(self):
        self.write_rc(0, age=60)
        self.plasma.set_panel_modes({2: "windowsgobelow"})
        self.reported = {"2": "autohide"}
        self.assertEqual(self.plasma.panel_modes(), {2: "autohide"})

    def test_without_settings_as_before(self):
        plasma = Plasma()
        plasma.run = self.fake_run
        self.write_rc(0, age=60)
        plasma.set_panel_modes({2: "windowsgobelow"})
        self.assertEqual(plasma.panel_modes(), {2: "none"})

    def test_a_damaged_memory_is_ignored(self):
        self.write_rc(3)
        self.memory.values["panels_set"] = "{not json"
        self.assertEqual(self.plasma.panel_modes(), {2: "windowsgobelow"})
        self.memory.values["panels_set"] = json.dumps({"2": "windowsgobelow"})
        self.assertEqual(self.plasma.panel_modes(), {2: "windowsgobelow"})


if __name__ == "__main__":
    unittest.main()
