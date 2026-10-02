# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""What ships inside Tidy, and the single file that build.py makes of it."""

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
import xml.dom.minidom

from tests import ROOT

from plasma_tidy import resources
from plasma_tidy.consts import DRAWER_DEFAULTS, VERSION
from plasma_tidy.widgets import drawer_files, fade_files


class Widgets(unittest.TestCase):
    def test_a_widget_has_what_plasma_needs(self):
        for files in (drawer_files(), fade_files()):
            self.assertIn("metadata.json", files)
            self.assertIn("contents/ui/main.qml", files)
            self.assertIn("contents/config/main.xml", files)
            self.assertEqual(json.loads(files["metadata.json"])["KPlugin"]["Version"], VERSION)
            xml.dom.minidom.parseString(files["contents/config/main.xml"])

    def test_every_drawer_setting_is_known_to_the_widget(self):
        schema = xml.dom.minidom.parseString(resources.DRAWER_CONFIG_XML)
        known = {entry.getAttribute("name") for entry in schema.getElementsByTagName("entry")}
        self.assertEqual(sorted(set(DRAWER_DEFAULTS) - known), [])

    def test_the_kwin_scripts_take_their_names(self):
        names = {"app": "a", "prefix": "p", "name": "n", "panel": "true", "edge": "1"}
        for script in (resources.KWIN_JS, resources.KWIN_INFO_JS, resources.KWIN_RULES_JS,
                       resources.KWIN_POINTER_JS, resources.KWIN_EDGE_JS):
            self.assertNotIn("%(", script % names)


class Build(unittest.TestCase):
    def test_the_single_file_runs(self):
        with tempfile.TemporaryDirectory() as folder:
            target = pathlib.Path(folder) / "plasma-tidy"
            subprocess.run([sys.executable, str(ROOT / "build.py"), str(target)], check=True,
                           capture_output=True)
            answer = subprocess.run([str(target), "--version"], capture_output=True, text=True)
            self.assertEqual(answer.returncode, 0)
            self.assertIn(VERSION, answer.stdout)
            wrong = subprocess.run([str(target), "--nonsense"], capture_output=True, text=True)
            self.assertEqual(wrong.returncode, 2)


if __name__ == "__main__":
    unittest.main()
