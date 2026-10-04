# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""plasma-tidy --report: what goes in, and above all what does not."""

import json
import unittest

from tests import SRC  # noqa: F401

from plasma_tidy.report import drawer_lines, error_lines, scrub, settings_lines, without_names


class NothingPersonal(unittest.TestCase):
    def test_home_user_and_computer_go(self):
        text = scrub("file:///home/anna/.local/x anna@laptop-anna laptop-anna annabel /tmp/-home-anna-x",
                     home="/home/anna", user="anna", host="laptop-anna")
        self.assertEqual(text, "file://~/.local/x <user>@<host> <host> annabel /tmp/-home-<user>-x")
        self.assertEqual(scrub("fedora on Fedora", home="/h", user="x", host="fedora"), "fedora on Fedora")

    def test_settings_with_names_of_your_own_are_only_counted(self):
        values = {"timeout": "10", "rules": json.dumps([{"when": "app", "arg": "secret-app"},
                                                        {"when": "battery"}]),
                  "profiles": json.dumps({"Work": {}, "Home": {}}),
                  "tray_rules": json.dumps([{"match": "secret-tray"}]),
                  "saved_state": json.dumps({"urls": {"1": "file:///home/anna/Desktop"}}),
                  "tray_seen": json.dumps(["secret-tray"])}
        text = "\n".join(settings_lines(values))
        self.assertIn("timeout = 10", text)
        self.assertIn("rules: 2 (app, battery)", text)
        self.assertIn("profiles: 2", text)
        self.assertIn("tray_rules: 1", text)
        self.assertIn("saved_state: kept", text)
        for secret in ("secret", "anna", "Work", "Home"):
            self.assertNotIn(secret, text)

    def test_a_drawer_without_its_name_and_programs(self):
        drawers = [{"id": 39, "config": {"name": "my secret drawer", "targets": ["5"],
                                         "taskKeep": ["secret.desktop"], "iconCustom": "/home/anna/i.png",
                                         "closed": True, "openOn": "hover"}}]
        panels = [{"location": "bottom", "widgets": [{"id": 5, "type": "org.kde.plasma.icontasks"},
                                                    {"id": 39, "type": "drawer"}]}]
        text = "\n".join(drawer_lines(drawers, panels))
        self.assertIn("drawer 39 (panel bottom): holds icontasks", text)
        self.assertIn('openOn="hover"', text)
        for secret in ("secret", "anna"):
            self.assertNotIn(secret, text)
        self.assertEqual(without_names("Drawer: my secret drawer", drawers), "Drawer: 39")

    def test_only_errors_of_tidy_and_never_its_test_reports(self):
        entries = [("10:00:00", "main.qml:12: ReferenceError: x is not defined (plasmatidy)"),
                   ("10:00:01", 'TIDYDRAWER {"tasks": ["secret window"]} error'),
                   ("10:00:02", "kwin: something else failed"),
                   ("10:00:03", "plasma-tidy: all fine")]
        self.assertEqual(error_lines(entries),
                         ["  10:00:00 main.qml:12: ReferenceError: x is not defined (plasmatidy)"])


if __name__ == "__main__":
    unittest.main()
