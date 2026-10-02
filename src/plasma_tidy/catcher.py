# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""The invisible window that catches a click on the desktop."""

from PyQt6.QtCore import QRect, QTimer, Qt
from PyQt6.QtGui import QBackingStore, QColor, QPainter, QRegion, QWindow

from .consts import CATCHER_PREFIX


class Catcher(QWindow):
    """Invisible window over one screen's desktop that catches clicks.

    A window as large as the screen needs a picture as large as the screen, and a few of them
    while it is being drawn: tens of megabytes. The picture never changes, so it is drawn once
    and the memory for drawing is given back; the compositor keeps the one copy it shows."""

    def __init__(self, screen, on_click):
        super().__init__()
        # Must never get focus: that would close menus and interrupt your typing.
        self.setFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowDoesNotAcceptFocus)
        self.on_click = on_click
        look = self.format()
        look.setAlphaBufferSize(8)
        self.setFormat(look)
        self.setTitle(CATCHER_PREFIX + screen.name())
        self.setScreen(screen)
        self.setGeometry(screen.geometry())
        self.store = None
        self.release = QTimer(self, interval=500, singleShot=True)
        self.release.timeout.connect(self.drop_store)

    def exposeEvent(self, event):
        if not self.isExposed():
            return
        self.store = self.store or QBackingStore(self)
        self.store.resize(self.size())
        whole = QRect(0, 0, self.width(), self.height())
        self.store.beginPaint(QRegion(whole))
        painter = QPainter(self.store.paintDevice())
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        # Almost fully transparent: there is something to show, and nothing to see.
        painter.fillRect(whole, QColor(0, 0, 0, 1))
        painter.end()
        self.store.endPaint()
        self.store.flush(QRegion(whole))
        self.release.start()

    def drop_store(self):
        self.store = None

    def mousePressEvent(self, event):
        self.on_click(event.button(), False)

    def mouseDoubleClickEvent(self, event):
        self.on_click(event.button(), True)
