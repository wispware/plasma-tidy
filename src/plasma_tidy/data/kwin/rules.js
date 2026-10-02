// For the rules: which program is in front, and does it fill the screen.
function reportWindow() {
    var w = workspace.activeWindow;
    if (isCatcher(w)) return;
    callDBus("%(name)s", "/", "%(name)s", "ActiveWindow",
             w ? String(w.resourceClass) : "", !!(w && w.fullScreen));
}
function watchWindow(w) {
    w.fullScreenChanged.connect(function () {
        if (workspace.activeWindow === w) reportWindow();
    });
}
workspace.windowList().forEach(watchWindow);
workspace.windowAdded.connect(watchWindow);
workspace.windowActivated.connect(reportWindow);
reportWindow();
