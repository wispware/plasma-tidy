# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""The peek key: a global shortcut that tells when it is pressed and let go."""

import re

from PyQt6.QtCore import QMetaType, QObject, Qt, pyqtSlot
from PyQt6.QtDBus import QDBusArgument, QDBusConnection, QDBusInterface
from PyQt6.QtGui import QKeySequence

from .consts import APP, PEEK_ACTION


class PeekKey(QObject):
    """A global shortcut that tells both when it is pressed and when it is let go."""

    def __init__(self, on_change):
        super().__init__()
        self.on_change = on_change
        self.bus = QDBusConnection.sessionBus()
        self.accel = QDBusInterface("org.kde.kglobalaccel", "/kglobalaccel",
                                    "org.kde.KGlobalAccel", self.bus)
        self.registered = False

    @staticmethod
    def action():
        """The action's name the way the shortcut service wants it: as a list of texts."""
        name = QDBusArgument()
        name.add(PEEK_ACTION, QMetaType.Type.QStringList.value)
        return name

    def set(self, text):
        keys = QKeySequence(text or "")
        if not keys.count() and not self.registered:
            return
        self.accel.call("doRegister", self.action())
        codes = QDBusArgument()
        codes.beginArray(QMetaType.Type.Int.value)
        for i in range(keys.count()):
            codes.add(keys[i].toCombined(), QMetaType.Type.Int.value)
        codes.endArray()
        # 2 | 4: the action is there now, and this key counts rather than an older one.
        flags = QDBusArgument()
        flags.add(6, QMetaType.Type.UInt.value)
        self.accel.call("setShortcut", self.action(), codes, flags)
        if not self.registered:
            path = "/component/" + re.sub(r"[^A-Za-z0-9]", "_", APP)
            for name, slot in (("globalShortcutPressed", self.pressed),
                               ("globalShortcutReleased", self.released)):
                self.bus.connect("org.kde.kglobalaccel", path,
                                 "org.kde.kglobalaccel.Component", name, slot)
            self.registered = True
        if not keys.count():
            self.accel.call("unRegister", self.action())

    def release(self):
        """Tidy stops: the key is free again until the next start."""
        if self.registered:
            self.accel.call("setInactive", self.action())

    @pyqtSlot(str, str, "qlonglong")
    def pressed(self, _component, action, _time):
        if action == PEEK_ACTION[1]:
            # Pressed while a peek is still on: the letting go was missed, so this press
            # ends it. That way the key can never leave everything stuck in view.
            self.on_change(None)

    @pyqtSlot(str, str, "qlonglong")
    def released(self, _component, action, _time):
        if action == PEEK_ACTION[1]:
            self.on_change(False)


def bare_key(sequence):
    """Is this a key that programs need themselves: one without Ctrl, Alt or Meta, and not a
    function key or a special key such as Pause or a media key?"""
    if not sequence.count():
        return False
    combo = sequence[0]
    held = combo.keyboardModifiers() & (Qt.KeyboardModifier.ControlModifier
                                        | Qt.KeyboardModifier.AltModifier
                                        | Qt.KeyboardModifier.MetaModifier)
    if held != Qt.KeyboardModifier.NoModifier:
        return False
    key = combo.key().value
    spare = [k.value for k in (Qt.Key.Key_Pause, Qt.Key.Key_ScrollLock, Qt.Key.Key_SysReq,
                               Qt.Key.Key_Menu, Qt.Key.Key_Help, Qt.Key.Key_Print)]
    special = (Qt.Key.Key_F1.value <= key <= Qt.Key.Key_F35.value or key in spare
               or key >= Qt.Key.Key_Back.value)
    return not special
