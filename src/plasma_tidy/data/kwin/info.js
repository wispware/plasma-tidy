// Which virtual desktop is shown: told when it changes.
function reportDesktop() {
    var names = workspace.desktops.map(function (d) { return d.name; });
    callDBus("%(name)s", "/", "%(name)s", "VirtualDesktop",
             workspace.desktops.indexOf(workspace.currentDesktop) + 1, names.join("\n"));
}
workspace.currentDesktopChanged.connect(reportDesktop);
workspace.desktopsChanged.connect(reportDesktop);
reportDesktop();

// Tidy's settings window opens: tell which programs are open, for it to choose from.
workspace.windowAdded.connect(function (w) {
    if (w.resourceClass != "%(app)s" || isCatcher(w) || !w.normalWindow) return;
    var seen = {};
    workspace.windowList().forEach(function (o) {
        if (o.normalWindow && o.resourceClass && o.resourceClass != "%(app)s")
            seen[String(o.resourceClass)] = true;
    });
    callDBus("%(name)s", "/", "%(name)s", "WindowClasses", Object.keys(seen).join("\n"));
});
