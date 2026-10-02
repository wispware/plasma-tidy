# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""Starting Tidy, or passing a command to the copy that is running.

Passing a command is what a keyboard shortcut does, so it is kept quick: the rest of Tidy,
and the part of Qt that draws windows, are only loaded when Tidy really starts."""

import os
import shutil
import signal
import socket
import sys

from PyQt6.QtCore import QSettings, QSocketNotifier, QTimer
from PyQt6.QtDBus import QDBusConnection, QDBusMessage

from .consts import APP, APP_NAME, DBUS_NAME, OLD_APP, VERSION
from .i18n import tr

COMMANDS = {"--show": "Show", "--hide": "Hide", "--toggle": "Toggle", "--settings": "Settings",
            "--peek": "Peek", "--welcome": "Welcome",
            "--drawer-open": "DrawerOpen", "--drawer-close": "DrawerClose",
            "--drawer-toggle": "DrawerToggle", "--restore": "Restore", "--focus": "Focus"}
USAGE = ("Usage: plasma-tidy [--show | --hide | --toggle | --settings | --focus | --peek | "
         "--drawer-open | --drawer-close | --drawer-toggle | --restore | --version]")


def migrate_old_config():
    """One-off: carry over the settings from the old name (AutoHide Desktop Icons)."""
    old = os.path.expanduser(f"~/.config/{OLD_APP}/{OLD_APP}.conf")
    new = os.path.expanduser(f"~/.config/{APP}/{APP}.conf")
    if os.path.exists(old) and not os.path.exists(new):
        os.makedirs(os.path.dirname(new), exist_ok=True)
        shutil.copy2(old, new)


def pass_on(bus, command):
    """Give the command to the copy that is running (default: open the settings)."""
    bus.call(QDBusMessage.createMethodCall(DBUS_NAME, "/", DBUS_NAME, command or "Settings"))


def main():
    command = None
    for arg in sys.argv[1:]:
        if arg == "--version":
            print(f"{APP_NAME} (plasma-tidy) {VERSION}")
            return 0
        if arg in COMMANDS:
            command = COMMANDS[arg]
        else:
            print(tr(USAGE), file=sys.stderr)
            return 2

    bus = QDBusConnection.sessionBus()
    if bus.interface().isServiceRegistered(DBUS_NAME).value():
        pass_on(bus, command)
        return 0
    return start(bus, command)


def start(bus, command):
    from PyQt6.QtWidgets import QApplication, QMessageBox

    from .core import Tidy
    from .dbus import DBusAdaptor

    migrate_old_config()
    fresh = not QSettings(APP, APP).allKeys()  # the very first start
    app = QApplication(sys.argv)
    app.setApplicationName(APP)
    app.setDesktopFileName(APP)
    app.setQuitOnLastWindowClosed(False)

    if not bus.registerService(DBUS_NAME):
        pass_on(bus, command)  # another copy started in the same moment
        return 0

    if not shutil.which("swayidle"):
        QMessageBox.critical(None, APP_NAME,
                             tr("swayidle is missing.\n\nInstall it with:\n"
                                "sudo dnf install swayidle"))
        return 1

    autohide = Tidy(app)
    adaptor = DBusAdaptor(autohide)
    autohide.adaptor = adaptor
    bus.registerObject("/", autohide)
    # Load only now: the KWin script reports the active window over D-Bus right away.
    autohide.load_kwin()
    # Helpers that were there before Tidy (Tidy restarted, Plasma did not) report on this.
    autohide.tell("Started")
    if command and command != "Toggle":
        QTimer.singleShot(0, getattr(adaptor, command))
    if fresh and not command:
        QTimer.singleShot(800, autohide.welcome)

    # Restore cleanly on logout/shutdown (SIGTERM) or Ctrl+C.
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: autohide.quit())
    # Python only handles a signal when its own code runs: let the signal wake Qt up.
    reader, writer = socket.socketpair()
    reader.setblocking(False)
    writer.setblocking(False)
    signal.set_wakeup_fd(writer.fileno())
    notifier = QSocketNotifier(reader.fileno(), QSocketNotifier.Type.Read)
    notifier.activated.connect(lambda *_: reader.recv(64))
    return app.exec()
