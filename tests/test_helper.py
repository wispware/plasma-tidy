# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""Hiding through the helper on the desktop: when it is used, and what the helper is told."""

import json
import unittest

from tests.fakes import FakeTidy


class WhichWay(unittest.TestCase):
    def test_not_before_a_helper_has_reported(self):
        tidy = FakeTidy()
        tidy.helper_count = 1
        self.assertFalse(tidy.helper_way())

    def test_once_every_desktop_has_one(self):
        tidy = FakeTidy()
        tidy.helper_count = 2
        tidy.on_helper_ready("1")
        self.assertFalse(tidy.helper_way())
        tidy.on_helper_ready("29")
        self.assertTrue(tidy.helper_way())

    def test_icons_hidden_the_other_way_are_handed_over(self):
        tidy = FakeTidy()
        tidy.helper_count = 1
        tidy.hidden = True  # hidden before the helper was there
        tidy.on_helper_ready("1")
        self.assertEqual((tidy.shown, tidy.hidden_times), (1, 1))
        tidy.hidden_by_helper = True
        tidy.on_helper_ready("1")  # reporting again changes nothing
        self.assertEqual((tidy.shown, tidy.hidden_times), (1, 1))

    def test_not_when_switched_off(self):
        tidy = FakeTidy(use_helper=False)
        tidy.helper_count = 1
        tidy.helpers = {"1"}
        self.assertFalse(tidy.helper_way())


class WhatTheHelperHears(unittest.TestCase):
    def setUp(self):
        self.tidy = FakeTidy(buttons="left,middle", fade_icons=True, fade_duration=250)
        self.tidy.helper_count = 1
        self.tidy.on_helper_ready("1")

    def last(self):
        signal, args = self.tidy.told[-1]
        self.assertEqual(signal, "DesktopState")
        return json.loads(args[0])

    def test_a_new_helper_is_told_how_things_are(self):
        self.assertFalse(self.last()["hidden"])

    def test_hidden_only_counts_when_the_helper_did_it(self):
        self.tidy.hidden = True
        self.assertFalse(self.tidy.desktop_state()["hidden"])
        self.tidy.hidden_by_helper = True
        self.assertTrue(self.tidy.desktop_state()["hidden"])

    def test_the_click_that_brings_them_back(self):
        state = self.tidy.desktop_state()
        self.assertTrue(state["catch"])
        self.assertEqual(state["buttons"], 1 + 4)  # left and middle, as Qt numbers them
        self.assertFalse(state["double"])

    def test_no_click_in_focus_mode_or_with_showing_on_movement(self):
        self.tidy.hold_icons = True
        self.assertFalse(self.tidy.desktop_state()["catch"])
        self.tidy.hold_icons = False
        self.tidy.settings.setValue("mode", "activity")
        self.assertFalse(self.tidy.desktop_state()["catch"])

    def test_fade_time_only_with_fading_on(self):
        self.assertEqual(self.tidy.desktop_state()["duration"], 250)
        self.tidy.settings.setValue("fade_icons", False)
        self.assertEqual(self.tidy.desktop_state()["duration"], 0)

    def test_a_click_shows_unless_focus_mode_holds_them(self):
        self.tidy.hidden = True
        self.tidy.hold_icons = True
        self.tidy.on_desktop_click()
        self.assertEqual(self.tidy.shown, 0)
        self.tidy.hold_icons = False
        self.tidy.on_desktop_click()
        self.assertEqual(self.tidy.shown, 1)


if __name__ == "__main__":
    unittest.main()
