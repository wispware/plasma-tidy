// While another window is the active one: tell when the pointer moves over the desktop
// itself (or over a panel, if that is set to count). Only the movement is told, twice a
// second at most; what you type or do in the other window never counts.
//
// KWin tells every single movement. After one is looked at, the listening stops for half a
// second, so that a moving pointer costs two looks a second and not one for every movement.
function pointerMoved() {
    try {
        workspace.cursorPosChanged.disconnect(pointerMoved);
        pointerWait.start();
    } catch (e) {}
    var active = workspace.activeWindow;
    if (!active || active.desktopWindow || isCatcher(active)) return;  // the desktop is in use anyway
    var top = workspace.windowAt(workspace.cursorPos, 1)[0];
    if (!top || top.desktopWindow || (%(panel)s && top.dock))
        callDBus("%(name)s", "/", "%(name)s", "DesktopMotion");
}
var pointerWait = new QTimer();
pointerWait.interval = 500;
pointerWait.singleShot = true;
pointerWait.timeout.connect(function () { workspace.cursorPosChanged.connect(pointerMoved); });
workspace.cursorPosChanged.connect(pointerMoved);
