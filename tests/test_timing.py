# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""When do the icons hide: what counts as activity, and what postpones."""

import time
import unittest

from tests.fakes import FakeTidy

from plasma_tidy.consts import MODE_ACTIVITY


class Watcher:
    """Plays the idle watcher: hands Tidy the lines it would print."""

    def __init__(self):
        self.lines = b""

    def readAllStandardOutput(self):
        lines, self.lines = self.lines, b""
        return lines


def say(tidy, line):
    tidy.idle.lines = line.encode() + b"\n"
    tidy.on_idle_output()


def fake(**settings):
    tidy = FakeTidy(**settings)
    tidy.idle = Watcher()
    return tidy


class AtTheDesktop(unittest.TestCase):
    def test_moving_postpones(self):
        tidy = fake()
        say(tidy, "idle")
        self.assertIsNotNone(tidy.idle_since)
        say(tidy, "active")
        self.assertIsNone(tidy.idle_since)
        self.assertEqual(tidy.remaining(), 5)

    def test_time_counts_from_when_you_stopped(self):
        tidy = fake()
        say(tidy, "idle")
        self.assertAlmostEqual(tidy.remaining(), 4, delta=0.2)  # the watcher tells after 1 s

    def test_fixed_time_ignores_movement(self):
        tidy = fake(rehide="fixed")
        tidy.shown_at = time.monotonic() - 3
        say(tidy, "active")
        self.assertAlmostEqual(tidy.remaining(), 2, delta=0.2)


class InAnotherWindow(unittest.TestCase):
    def setUp(self):
        self.tidy = fake()
        self.tidy.on_desktop_active(False)
        self.left_at = self.tidy.idle_since

    def test_the_time_starts_when_you_leave_the_desktop(self):
        self.assertIsNotNone(self.left_at)

    def test_what_you_do_there_does_not_count(self):
        say(self.tidy, "idle")
        say(self.tidy, "active")
        self.assertEqual(self.tidy.idle_since, self.left_at)

    def test_moving_over_the_desktop_postpones(self):
        time.sleep(0.02)
        self.tidy.on_desktop_motion()
        self.assertGreater(self.tidy.idle_since, self.left_at)

    def test_typing_with_the_pointer_resting_on_the_desktop_does_not_count(self):
        self.tidy.on_desktop_motion()
        moved_at = self.tidy.idle_since
        say(self.tidy, "active")
        say(self.tidy, "idle")
        self.assertEqual(self.tidy.idle_since, moved_at)

    def test_back_at_the_desktop_everything_counts_again(self):
        self.tidy.on_desktop_active(True)
        self.assertIsNone(self.tidy.idle_since)

    def test_with_the_setting_off_everything_counts(self):
        self.tidy.settings.setValue("only_desktop", False)
        say(self.tidy, "active")
        self.assertIsNone(self.tidy.idle_since)


class BringingTheIconsBack(unittest.TestCase):
    def test_click_mode_ignores_movement(self):
        tidy = fake()
        tidy.hidden = True
        say(tidy, "active")
        tidy.on_desktop_active(False)
        tidy.on_desktop_motion()
        self.assertEqual(tidy.shown, 0)

    def test_movement_mode_shows_on_movement(self):
        tidy = fake(mode=MODE_ACTIVITY)
        tidy.hidden = True
        say(tidy, "active")
        self.assertEqual(tidy.shown, 1)

    def test_movement_mode_shows_when_the_pointer_reaches_the_desktop(self):
        tidy = fake(mode=MODE_ACTIVITY)
        tidy.on_desktop_active(False)
        tidy.hidden = True
        say(tidy, "active")
        self.assertEqual(tidy.shown, 0)
        tidy.on_desktop_motion()
        self.assertEqual(tidy.shown, 1)

    def test_focus_mode_keeps_them_away(self):
        tidy = fake(mode=MODE_ACTIVITY)
        tidy.hidden = tidy.hold_icons = True
        say(tidy, "active")
        self.assertEqual(tidy.shown, 0)


class TheIdleWatcher(unittest.TestCase):
    """It only has to run while there is something to learn from it."""

    def test_needed_while_the_icons_are_in_view(self):
        self.assertTrue(fake().idle_needed())

    def test_not_needed_hidden_until_a_click(self):
        tidy = fake()
        tidy.hidden = True
        self.assertFalse(tidy.idle_needed())

    def test_needed_hidden_until_movement(self):
        tidy = fake(mode=MODE_ACTIVITY)
        tidy.hidden = True
        self.assertTrue(tidy.idle_needed())

    def test_not_needed_when_switched_off(self):
        tidy = fake()
        tidy.enabled_action.on = False
        self.assertFalse(tidy.idle_needed())

    def test_not_needed_while_you_work_in_another_window(self):
        tidy = fake()
        tidy.desktop_active = False
        self.assertFalse(tidy.idle_needed())
        tidy.hidden = True
        tidy.settings.setValue("mode", MODE_ACTIVITY)
        self.assertFalse(tidy.idle_needed())

    def test_needed_in_another_window_when_everything_counts(self):
        tidy = fake(only_desktop=False)
        tidy.desktop_active = False
        self.assertTrue(tidy.idle_needed())

    def test_not_needed_with_a_fixed_time(self):
        self.assertFalse(fake(rehide="fixed").idle_needed())


if __name__ == "__main__":
    unittest.main()
