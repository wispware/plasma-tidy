# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""Loading Tidy's helper script into KWin."""

from PyQt6.QtDBus import QDBusConnection, QDBusInterface

from .consts import APP, CATCHER_PREFIX, CORNERS, DBUS_NAME, KWIN_SCRIPT, KWIN_SCRIPT_NAME
from .resources import KWIN_EDGE_JS, KWIN_INFO_JS, KWIN_JS, KWIN_POINTER_JS, KWIN_RULES_JS


class KWin:
    """Loads the KWin script for the catchers and the screen corner."""

    def __init__(self):
        bus = QDBusConnection.sessionBus()
        self.scripting = QDBusInterface("org.kde.KWin", "/Scripting",
                                        "org.kde.kwin.Scripting", bus)
        self.kwin = QDBusInterface("org.kde.KWin", "/KWin", "org.kde.KWin", bus)

    def load(self, corner, pointer=False, panel=False, windows=False):
        script = KWIN_JS % {"app": APP, "prefix": CATCHER_PREFIX, "name": DBUS_NAME}
        script += KWIN_INFO_JS % {"app": APP, "name": DBUS_NAME}
        if windows:
            script += KWIN_RULES_JS % {"name": DBUS_NAME}
        if pointer:
            script += KWIN_POINTER_JS % {"name": DBUS_NAME,
                                         "panel": "true" if panel else "false"}
        edge = dict((key, js) for key, _, js in CORNERS).get(corner)
        if edge:
            script += KWIN_EDGE_JS % {"edge": edge, "name": DBUS_NAME}
        with open(KWIN_SCRIPT, "w") as f:
            f.write(script)
        self.unload()
        self.scripting.call("loadScript", KWIN_SCRIPT, KWIN_SCRIPT_NAME)
        self.scripting.call("start")

    def unload(self):
        self.scripting.call("unloadScript", KWIN_SCRIPT_NAME)

    def showing_desktop(self):
        return bool(self.kwin.property("showingDesktop"))
