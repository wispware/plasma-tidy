# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""What ships inside Tidy, and the single file that build.py makes of it."""

import json
import pathlib
import re
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


class WidgetNames(unittest.TestCase):
    """A widget is only read by Plasma when it starts, and a name that is not there only
    fails at the moment it is used. So: everything a widget asks of itself must exist."""

    # What every widget has without saying so.
    BUILT_IN = {"parent", "width", "height", "Window"}

    def own_names(self, source):
        names = set(re.findall(
            r"^\s*(?:readonly\s+|default\s+|required\s+)*property\s+[\w<>.]+\s+(\w+)", source, re.M))
        names |= set(re.findall(r"^\s*function\s+(\w+)", source, re.M))
        return names | set(re.findall(r"^\s*signal\s+(\w+)", source, re.M))

    def test_everything_a_widget_asks_of_itself_exists(self):
        for source in (resources.DRAWER_QML, resources.FADE_QML):
            used = set(re.findall(r"\broot\.(\w+)", source))
            self.assertEqual(used - self.own_names(source) - self.BUILT_IN, set())

    def test_every_change_handler_has_its_property(self):
        for source in (resources.DRAWER_QML, resources.FADE_QML):
            names = self.own_names(source) | self.BUILT_IN
            for handler in re.findall(r"^    on(\w+)Changed:", source, re.M):
                self.assertIn(handler[0].lower() + handler[1:], names)

    def test_every_setting_a_widget_reads_is_in_its_schema(self):
        for source, schema in ((resources.DRAWER_QML, resources.DRAWER_CONFIG_XML),
                               (resources.FADE_QML, resources.FADE_CONFIG_XML)):
            known = {e.getAttribute("name")
                     for e in xml.dom.minidom.parseString(schema).getElementsByTagName("entry")}
            used = set(re.findall(r"\bcfg\.(\w+)", source))
            self.assertEqual(used - known, set())


if __name__ == "__main__":
    unittest.main()
