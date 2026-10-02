function isCatcher(w) {
    return w && w.resourceClass == "%(app)s" && w.caption.indexOf("%(prefix)s") == 0;
}

// Last real active window, to hand focus back to when a catcher takes it.
var lastActive = workspace.activeWindow;
var freshUntil = 0;  // catcher just appeared: a focus change is then never caused by a click

function giveFocusBack() {
    if (lastActive && !lastActive.deleted && !lastActive.minimized && !isCatcher(lastActive))
        workspace.activeWindow = lastActive;
}

// A click on a catcher is a click on the desktop: afterwards the desktop of that
// screen should be active, not the window you were in before.
var clicked = false;

function activateDesktop(output) {
    var desk = workspace.windowList().find(function (d) {
        return d.desktopWindow && (!output || d.output === output);
    });
    if (desk) workspace.activeWindow = desk;
}

function setup(w) {
    if (!isCatcher(w)) return;
    freshUntil = Date.now() + 1000;
    if (workspace.activeWindow === w) giveFocusBack();
    w.closed.connect(function () {
        if (clicked) {
            clicked = false;
            activateDesktop(w.output);
        }
    });
    var name = w.caption.substring("%(prefix)s".length);
    w.keepBelow = true;
    w.skipTaskbar = true;
    w.skipSwitcher = true;
    w.skipPager = true;
    w.onAllDesktops = true;
    w.noBorder = true;
    var out = workspace.screens.find(function (s) { return s.name == name; });
    if (out) {
        var g = out.geometry;
        w.frameGeometry = {x: g.x, y: g.y, width: g.width, height: g.height};
    }
}
workspace.windowList().forEach(setup);
workspace.windowAdded.connect(setup);

function reportActive() {
    var w = workspace.activeWindow;
    if (isCatcher(w) && (Date.now() < freshUntil || !w.readyForPainting)) {
        // Safety net: a catcher that has just appeared must not keep the focus.
        giveFocusBack();
        return;
    }
    if (isCatcher(w)) clicked = true;  // became active through a click by the user
    if (w && !isCatcher(w)) lastActive = w;
    var desktop = !w || w.desktopWindow ||
        (w.resourceClass == "%(app)s" && w.caption.indexOf("%(prefix)s") == 0);
    if (desktop === toldDesktop) return;  // only a change is news
    toldDesktop = desktop;
    callDBus("%(name)s", "/", "%(name)s", "DesktopActive", desktop);
}
var toldDesktop = null;
workspace.windowActivated.connect(reportActive);
reportActive();

var popups = 0;
var toldPopups = null;
function reportPopups() {
    if ((popups > 0) === toldPopups) return;
    toldPopups = popups > 0;
    callDBus("%(name)s", "/", "%(name)s", "PopupOpen", popups > 0);
}
function trackPopup(w) {
    if (!w.popupWindow) return;
    popups++;
    reportPopups();
    w.closed.connect(function () { popups = Math.max(0, popups - 1); reportPopups(); });
}
workspace.windowList().forEach(trackPopup);
workspace.windowAdded.connect(trackPopup);
reportPopups();

// A panel that slides out of view (auto-hide, dodge windows): told with its screen and the
// edge it is on, for the drawers that close then. Its coming back is not told.
function trackPanel(w) {
    if (!w.dock) return;
    w.hiddenChanged.connect(function () {
        if (!w.hidden || !w.output) return;
        var g = w.frameGeometry, o = w.output.geometry;
        var edge = g.width >= g.height
            ? (g.y + g.height / 2 < o.y + o.height / 2 ? "top" : "bottom")
            : (g.x + g.width / 2 < o.x + o.width / 2 ? "left" : "right");
        callDBus("%(name)s", "/", "%(name)s", "PanelHidden", w.output.name, edge);
    });
}
workspace.windowList().forEach(trackPanel);
workspace.windowAdded.connect(trackPanel);
