// While another window is the active one: tell when the pointer moves over the desktop
// itself (or over a panel, if that is set to count). Only the movement is told, twice a
// second at most; what you type or do in the other window never counts.
var pointerChecked = 0;
workspace.cursorPosChanged.connect(function () {
    var now = Date.now();
    if (now - pointerChecked < 500) return;
    pointerChecked = now;
    var active = workspace.activeWindow;
    if (!active || active.desktopWindow || isCatcher(active)) return;  // the desktop is in use anyway
    var top = workspace.windowAt(workspace.cursorPos, 1)[0];
    if (!top || top.desktopWindow || (%(panel)s && top.dock))
        callDBus("%(name)s", "/", "%(name)s", "DesktopMotion");
});
