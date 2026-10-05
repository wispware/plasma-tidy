// For "show the panel after a window is minimised or closed": tells when that happens, and
// whether the pointer is over a panel, which then stays in view for as long as it is.
function tellGone(w, how) {
    if (w.skipTaskbar || isCatcher(w) || w.resourceClass == "%(app)s") return;
    callDBus("%(name)s", "/", "%(name)s", "WindowGone", how);
}
function trackGone(w) {
    if (!w.normalWindow) return;
    w.minimizedChanged.connect(function () { if (w.minimized) tellGone(w, "minimized"); });
    // (A window that was minimised already is not one you were just working in.)
    w.closed.connect(function () { if (!w.minimized) tellGone(w, "closed"); });
}
workspace.windowList().forEach(trackGone);
workspace.windowAdded.connect(trackGone);

// KWin tells every single movement of the pointer. After one is looked at, the listening
// stops for a moment; when it starts again one more look tells where the pointer came to rest.
var overPanel = null;      // not told yet: the first look always tells
function lookForPanel() {
    var top = workspace.windowAt(workspace.cursorPos, 1)[0];
    var on = !!top && top.dock === true;
    if (on === overPanel) return;
    overPanel = on;
    callDBus("%(name)s", "/", "%(name)s", "PanelPointer", on);
}
function panelPointerMoved() {
    try {
        workspace.cursorPosChanged.disconnect(panelPointerMoved);
        panelWait.start();
    } catch (e) {}
    lookForPanel();
}
var panelWait = new QTimer();
panelWait.interval = 300;
panelWait.singleShot = true;
panelWait.timeout.connect(function () {
    workspace.cursorPosChanged.connect(panelPointerMoved);
    lookForPanel();
});
workspace.cursorPosChanged.connect(panelPointerMoved);
lookForPanel();
