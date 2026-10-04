# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""plasma-tidy --report: everything that helps with a bug report, in one block to copy.

It holds versions, Tidy's own look at itself (--check), the settings and the drawers, and the
last errors. Nothing personal goes in: no file names under your home folder, no user or
computer name, no program names from your rules or tray, no window titles."""

import getpass
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys

from .consts import APP, DBUS_NAME, DRAWER_DEFAULTS, PROFILE_SETTINGS, VERSION

# Settings that can go in as they are.
PLAIN = sorted(set(PROFILE_SETTINGS) - {"tray_rules"}
               | {"enabled", "language", "welcomed", "checks_told"})
# Settings that hold names of programs, folders or panels of your own: only how many.
COUNTED = ("rules", "profiles", "tray_rules")
# Notes Tidy keeps for putting things back: only whether they are there.
PRESENT = ("saved_state", "focus_state", "peek_panels", "tips_original", "tray_original",
           "launchers_backup", "suspended")
# A drawer's own settings that hold something of your own.
DRAWER_PRIVATE = ("name", "iconCustom", "taskKeep", "taskList")


def scrub(text, home=None, user=None, host=None):
    """Take out what points at you: your home folder, your user name, your computer's name."""
    home = home if home is not None else os.path.expanduser("~")
    user = user if user is not None else getpass.getuser()
    host = host if host is not None else socket.gethostname()
    if home and home != "/":
        text = text.replace(home, "~")
    if host in ("fedora", "localhost", "localhost-live", "ubuntu", "debian", "archlinux"):
        host = ""  # a name every such computer has: nothing of yours, and "fedora" stays readable
    # The computer's name first: it often holds the user's name ("anna-laptop").
    for word, stand_in in ((host, "<host>"), (user, "<user>")):
        if word and len(word) > 1:
            text = re.sub(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(word), stand_in, text)
    return text


def settings_lines(values):
    """The settings, as far as they say nothing about you. `values`: {key: value as stored}."""
    lines = []
    for key in PLAIN:
        if key in values:
            lines.append("  %s = %s" % (key, values[key]))
    for key in COUNTED:
        if key in values:
            try:
                found = json.loads(values[key] or "null")
            except (ValueError, TypeError):
                found = None
            count = len(found) if isinstance(found, (list, dict)) else 0
            detail = ""
            if key == "rules" and isinstance(found, list):
                kinds = sorted({str(r.get("when")) for r in found if isinstance(r, dict)})
                detail = " (%s)" % ", ".join(kinds) if kinds else ""
            lines.append("  %s: %d%s" % (key, count, detail))
    for key in PRESENT:
        if values.get(key) not in (None, "", "false", False):
            lines.append("  %s: kept" % key)
    return lines


def drawer_lines(drawers, panels):
    """Each drawer's settings, its panel and what it holds (by kind of widget)."""
    kinds, places = {}, {}
    for panel in panels:
        for widget in panel.get("widgets", []):
            kinds[str(widget.get("id"))] = str(widget.get("type", "?")).replace("org.kde.plasma.", "")
            places[str(widget.get("id"))] = panel.get("location", "?")
    lines = []
    for drawer in drawers:
        config = drawer.get("config", {})
        targets = [kinds.get(str(t), "?") for t in config.get("targets", [])]
        lines.append("  drawer %s (panel %s): holds %s" % (
            drawer.get("id"), places.get(str(drawer.get("id")), "?"), ", ".join(targets) or "nothing"))
        rest = ["%s=%s" % (k, json.dumps(config[k])) for k in DRAWER_DEFAULTS
                if k in config and k not in DRAWER_PRIVATE and k != "targets"]
        while rest:
            lines.append("    " + " ".join(rest[:6]))
            rest = rest[6:]
    return lines or ["  none"]


def without_names(line, drawers):
    """A drawer is called by its number: the name you gave it is your own."""
    for drawer in drawers:
        name = drawer.get("config", {}).get("name", "")
        if name:
            line = line.replace(": " + name, ": %s" % drawer.get("id"))
    return line


def first_line(command):
    try:
        out = subprocess.run(command, capture_output=True, text=True, timeout=10)
        return (out.stdout or out.stderr).strip().splitlines()[0]
    except (OSError, subprocess.SubprocessError, IndexError):
        return "not found"


def error_lines(entries, limit=20):
    """From journal entries [(time, message)]: the errors of Tidy and of its widgets."""
    found = []
    for when, line in entries:
        if not re.search(r"plasmatidy|plasma_tidy|plasma-tidy|Tidy", line):
            continue
        if re.search(r"TIDYDRAWER|TIDYHELPER|TIDYTAP|TIDYTIP|Start|Stop|Consumed", line):
            continue  # test reports and service lines: no errors, and full of your own names
        if re.search(r"error|warning|traceback|exception|cannot|failed", line, re.I):
            found.append("  %s %s" % (when, line.strip()[:300]))
    return found[-limit:] or ["  none"]


def recent_errors():
    """The last errors of Tidy and of its widgets inside Plasma, since the computer started."""
    import datetime
    try:
        out = subprocess.run(["journalctl", "--user", "-b", "--no-pager", "-n", "4000", "-o", "json",
                              "--output-fields=MESSAGE"],
                             capture_output=True, text=True, timeout=15).stdout
    except (OSError, subprocess.SubprocessError):
        return ["  (the journal could not be read)"]
    entries = []
    for raw in out.splitlines():
        try:
            entry = json.loads(raw)
            when = datetime.datetime.fromtimestamp(int(entry["__REALTIME_TIMESTAMP"]) / 1e6)
            message = entry.get("MESSAGE")
        except (ValueError, KeyError, TypeError):
            continue
        if isinstance(message, str):
            entries.append((when.strftime("%H:%M:%S"), message))
    return error_lines(entries)


def gather():
    """Collect everything; the parts that need Plasma or the running Tidy say so when absent."""
    from PyQt6.QtCore import PYQT_VERSION_STR, QT_VERSION_STR, QCoreApplication, QSettings
    from PyQt6.QtDBus import QDBusConnection, QDBusMessage

    app = QCoreApplication.instance() or QCoreApplication(sys.argv)  # noqa: F841 (D-Bus needs it)
    from .plasma import Plasma

    lines = ["Tidy %s" % VERSION]
    os_name = platform.freedesktop_os_release().get("PRETTY_NAME", "?") if hasattr(
        platform, "freedesktop_os_release") else "?"
    lines += [
        "",
        "System",
        "  %s, %s session (%s)" % (os_name, os.environ.get("XDG_SESSION_TYPE", "?"),
                                   os.environ.get("XDG_CURRENT_DESKTOP", "?")),
        "  %s, %s" % (first_line(["plasmashell", "--version"]), first_line(["kwin_wayland", "--version"])),
        "  Qt %s, PyQt %s, Python %s" % (QT_VERSION_STR, PYQT_VERSION_STR, platform.python_version()),
        "  swayidle: %s" % ("found" if shutil.which("swayidle") else "missing"),
        "  Tidy installed in: %s" % os.path.dirname(os.path.abspath(sys.argv[0])),
    ]
    plasma = Plasma()
    screens = plasma.run("print(screenCount);").strip()
    lines.append("  screens: %s" % (screens or "? (Plasma did not answer)"))

    drawers = plasma.drawers()
    bus = QDBusConnection.sessionBus()
    lines += ["", "What works (plasma-tidy --check)"]
    if bus.interface().isServiceRegistered(DBUS_NAME).value():
        reply = bus.call(QDBusMessage.createMethodCall(DBUS_NAME, "/", DBUS_NAME, "Check"))
        text = reply.arguments()[0] if reply.arguments() else "  (no answer)"
        lines += ["  " + without_names(line, drawers) for line in text.splitlines()[1:] if line.strip()]
    else:
        lines.append("  Tidy is not running")

    settings = QSettings(APP, APP)
    values = {key: settings.value(key) for key in settings.allKeys()}
    lines += ["", "Settings"] + settings_lines(values)
    lines += ["", "Drawers"] + drawer_lines(drawers, plasma.panel_widgets())
    lines += ["", "Recent errors"] + recent_errors()
    return scrub("\n".join(lines))


def print_report():
    rule = "-" * 72
    print("Copy everything between the lines into your bug report. It holds no personal data:")
    print("no file names in your home folder, no user or computer name, no program names.")
    print(rule)
    print(gather())
    print(rule)
    return 0
