# SPDX-FileCopyrightText: 2026 Ivar
# SPDX-License-Identifier: GPL-3.0-or-later
"""Translations: the texts are English in the code; this holds the other languages."""

from PyQt6.QtCore import QLocale, QSettings

from .consts import APP

# Translations. The texts in the code are English; to add a language, add a table here
# and a line in LANGUAGES. A text missing from a table stays English.
TRANSLATIONS = {
    "nl": {
        "Keeps your KDE Plasma desktop, panel and system tray clean.":
            "Houdt je KDE Plasma-bureaublad, paneel en systeemvak opgeruimd.",
        # screen corners
        "None": "Geen",
        "Top left": "Linksboven",
        "Top right": "Rechtsboven",
        "Bottom left": "Linksonder",
        "Bottom right": "Rechtsonder",
        # system tray
        "Automatic": "Automatisch",
        "Only visible when relevant": "Alleen zichtbaar als het relevant is",
        "Show": "Tonen",
        "Always visible in the panel": "Altijd zichtbaar in de taakbalk",
        "Hide": "Verbergen",
        "Only reachable through the ^ arrow": "Alleen bereikbaar via het pijltje ^",
        "Off": "Uit",
        "Switched off completely": "Helemaal uitgeschakeld",
        "Battery": "Batterij",
        "Brightness": "Helderheid",
        "Camera indicator": "Camera-indicator",
        "Clipboard": "Klembord",
        "Devices (USB)": "Apparaten (usb)",
        "Caps Lock indicator": "Caps Lock-indicator",
        "Keyboard layout": "Toetsenbordindeling",
        "Input method": "Invoermethode",
        "Network (Wi-Fi)": "Netwerk (wifi)",
        "Notifications": "Meldingen",
        "Vaults": "Kluizen",
        "Weather": "Weer",
        "Displays": "Beeldschermen",
        "Media controls": "Mediabediening",
        "Xwayland screen sharing": "Xwayland-schermdelen",
        "Tidy (this program)": "Tidy (dit programma)",
        "No system tray found in the panel.": "Geen systeemvak gevonden in het paneel.",
        "Choose for each icon how it appears in the system tray.\n"
        "Automatic: only when relevant · Hide: under the ^ arrow":
            "Kies per pictogram hoe het rechts in de taakbalk staat.\n"
            "Automatisch: alleen als het relevant is · Verbergen: onder het pijltje ^",
        "System items": "Systeemonderdelen",
        "Applications": "Programma's",
        "Minimal": "Minimaal",
        "Show all": "Alles tonen",
        "Every icon always visible in the panel; what is switched off stays off.":
            "Elk pictogram altijd zichtbaar in de taakbalk; wat uit staat blijft uit.",
        "Hide all": "Alles verbergen",
        "Every icon under the ^ arrow; what is switched off stays off.":
            "Elk pictogram onder het pijltje ^; wat uit staat blijft uit.",
        "Only network, volume and battery visible; notifications and devices when relevant; "
        "the rest under ^.":
            "Alleen netwerk, volume en batterij in beeld; meldingen en "
            "apparaten als ze relevant zijn; de rest onder ^.",
        # panel drawers
        "Application launcher": "Startmenu",
        "Application menu": "Toepassingenmenu",
        "Application dashboard": "Toepassingendashboard",
        "Virtual desktops": "Virtuele bureaubladen",
        "Task manager (icons)": "Taakbeheer (pictogrammen)",
        "Task manager": "Taakbeheer",
        "Clock": "Klok",
        "Show desktop": "Bureaublad tonen",
        "Minimize all": "Alles minimaliseren",
        "Quick launch": "Snelstarter",
        "Program icon": "Programmapictogram",
        "Trash": "Prullenbak",
        "Global menu": "Globaal menu",
        "Top panel": "Paneel boven",
        "Bottom panel": "Paneel onder",
        "Left panel": "Paneel links",
        "Right panel": "Paneel rechts",
        "Panel": "Paneel",
        "A drawer is an arrow in the panel. It tucks the widgets you choose away and "
        "brings them back when you click or point at the arrow.":
            "Een la is een pijltje in het paneel. Die bergt de onderdelen op die je kiest "
            "en haalt ze terug als je op het pijltje klikt of het aanwijst.",
        "Drawer:": "La:",
        "Drawer {n}": "La {n}",
        "Name:": "Naam:",
        "A name of your own for this drawer. Without one it is called after what is in it.":
            "Een eigen naam voor deze la. Zonder naam heet hij naar wat erin zit.",
        "Add a drawer": "La toevoegen",
        "Remove": "Verwijderen",
        "No drawer yet. Add one to hide panel icons behind an arrow.":
            "Nog geen la. Voeg er een toe om paneelpictogrammen achter een pijltje te verbergen.",
        "The drawer could not be added to the panel.":
            "De la kon niet aan het paneel worden toegevoegd.",
        "No panel found.": "Geen paneel gevonden.",
        "In this drawer": "In deze la",
        "Hide all programs, open ones too": "Alle programma's verbergen, ook geopende",
        "Hide only pinned programs that are not open":
            "Alleen vastgemaakte programma's verbergen die niet open zijn",
        "Open programs are windows: with the second choice they stay in the panel and only "
        "the pinned icons of programs that are not running disappear.":
            "Geopende programma's zijn vensters: bij de tweede keuze blijven ze in het paneel "
            "staan en verdwijnen alleen de vastgemaakte pictogrammen van programma's die niet "
            "draaien.",
        "Task manager:": "Taakbeheer:",
        "A click on the arrow": "Een klik op het pijltje",
        "Pointing at the arrow (a click works too)":
            "Het pijltje aanwijzen (klikken werkt ook)",
        "Open with:": "Openen met:",
        "Pointing opens after:": "Aanwijzen opent na:",
        "Close by itself:": "Vanzelf sluiten:",
        "Never": "Nooit",
        "When the pointer leaves the drawer": "Als de muis de la verlaat",
        "When the pointer leaves the panel": "Als de muis het paneel verlaat",
        "The drawer is the arrow and the items it shows; empty panel space next to them "
        "is outside it.":
            "De la is het pijltje met de onderdelen die het toont; lege ruimte in het "
            "paneel ernaast valt erbuiten.",
        "Closes after:": "Sluit na:",
        "Close with a click on an empty spot in the panel":
            "Sluiten met een klik op een lege plek in het paneel",
        "Open when a program asks for attention": "Openen als een programma om aandacht vraagt",
        "Animation:": "Animatie:",
        "Slide": "Schuiven",
        "One by one": "Eén voor één",
        "Fade": "Vervagen",
        "Slide: the icons slide out from under the arrow at their normal size, like a drawer. "
        "Grow: they grow from small to their normal size. One by one: they come and go one "
        "after the other. Fade: they fade together and the rest closes up.":
            "Schuiven: de pictogrammen schuiven op normale grootte onder het pijltje vandaan, "
            "als een la. Groeien: ze groeien van klein naar hun normale grootte. Eén voor één: "
            "ze komen en gaan na elkaar. Vervagen: ze vervagen tegelijk en de rest sluit aan.",
        "Grow": "Groeien",
        "Speed:": "Snelheid:",
        "How long the movement takes; one by one, how long each icon takes.":
            "Hoe lang de beweging duurt; bij één voor één, hoe lang elk pictogram erover doet.",
        "Appearance": "Uiterlijk",
        "Open programs:": "Open programma's:",
        "On their pinned spot": "Op hun vaste plek",
        "All in front": "Allemaal vooraan",
        "All at the back": "Allemaal achteraan",
        "A pinned program that is open normally stays on its pinned spot, between the others. "
        "In front or at the back, the open programs stand together and the pinned ones slide "
        "out next to them.":
            "Een vastgemaakt programma dat open is, blijft normaal op zijn vaste plek staan, "
            "tussen de andere. Vooraan of achteraan staan de open programma's bij elkaar en "
            "schuiven de vastgemaakte ernaast uit.",
        "Arrow points the other way": "Pijltje wijst de andere kant op",
        "Contents": "Inhoud",
        "Opening and closing": "Openen en sluiten",
        "Arrow": "Pijltje",
        "Opening": "Openen",
        "Closing": "Sluiten",
        "Shortcut:": "Sneltoets:",
        "A shortcut for this drawer alone. The shortcut for all drawers at once is set in "
        "System Settings.":
            "Een sneltoets voor alleen deze la. De sneltoets voor alle laden tegelijk stel je "
            "in bij Systeeminstellingen.",
        "Open when the desktop is shown": "Openen als het bureaublad wordt getoond",
        "Works while Tidy is running.": "Werkt zolang Tidy draait.",
        "Close after a click on something in the drawer": "Sluiten na een klik op iets in de la",
        "Close when a window that fills the screen comes to the front":
            "Sluiten als een schermvullend venster naar voren komt",
        "Icon:": "Pictogram:",
        "Double arrow": "Dubbel pijltje",
        "Triangle": "Driehoekje",
        "Dots": "Puntjes",
        "Menu lines": "Menustreepjes",
        "Grip": "Greep",
        "My own icon": "Eigen pictogram",
        "No icon": "Geen pictogram",
        "Without an icon the spot stays clickable and lights up under the pointer.":
            "Zonder pictogram blijft de plek aanklikbaar en licht hij op onder de muis.",
        "Icon name or image file": "Pictogramnaam of afbeeldingsbestand",
        "Choose…": "Kiezen…",
        "Choose an image": "Kies een afbeelding",
        "The place of the arrow is set in Tidy.": "De plaats van het pijltje stel je in Tidy in.",
        "Mark on the closed drawer:": "Teken op een gesloten la:",
        "A dot when programs are open": "Een stip als er programma's open zijn",
        "The number of open programs": "Het aantal open programma's",
        "A dot only when a program asks for attention":
            "Alleen een stip als een programma om aandacht vraagt",
        "Shown on the arrow while the drawer is closed and hides a task manager with all its "
        "programs. The dot changes colour when a program asks for attention.":
            "Staat op het pijltje zolang de la dicht is en een taakbeheer met al zijn "
            "programma's verbergt. De stip verandert van kleur als een programma om aandacht "
            "vraagt.",
        "Place of the arrow:": "Plaats van het pijltje:",
        "Just before the items it hides": "Direct vóór de onderdelen die het verbergt",
        "Just after the items it hides": "Direct na de onderdelen die het verbergt",
        "Where I put it myself": "Waar ik het zelf neerzet",
        "After a task manager the arrow sits right behind the last program. The task manager "
        "then no longer fills the panel; the drawer does that instead.":
            "Na een taakbeheer staat het pijltje direct achter het laatste programma. "
            "Taakbeheer vult het paneel dan niet meer op; dat doet de la.",
        "All drawers": "Alle laden",
        "Close and open together with the desktop icons":
            "Sluiten en openen samen met de bureaubladpictogrammen",
        "The arrow sits next to the items it hides. To place it yourself, choose \"Where I "
        "put it myself\", right-click the panel, choose Enter Edit Mode and drag it.":
            "Het pijltje staat naast de onderdelen die het verbergt. Zelf plaatsen: kies "
            "\"Waar ik het zelf neerzet\", klik met rechts op het paneel, kies Bewerkmodus "
            "en sleep het.",
        "Show the hidden items": "Verborgen onderdelen tonen",
        "Hide the items": "Onderdelen verbergen",
        "{app} settings…": "{app}-instellingen…",
        "Paused. Click to resume": "Gepauzeerd. Klik om te hervatten",
        # focus mode
        "Focus mode": "Focusmodus",
        "Focus mode tucks everything away at once and keeps it away: nothing comes back on "
        "mouse movement or a click on the desktop. Switching it off puts everything back as "
        "it was.":
            "De focusmodus bergt alles in één keer op en houdt het weg: er komt niets terug "
            "bij een muisbeweging of een klik op het bureaublad. Zet je hem uit, dan staat "
            "alles weer zoals het was.",
        "In focus mode": "In de focusmodus",
        "Hide the desktop icons": "Bureaubladpictogrammen verbergen",
        "Close the panel drawers": "Paneelladen sluiten",
        "Set the system tray to Minimal": "Systeemvak op Minimaal zetten",
        "Auto-hide the panel": "Paneel automatisch verbergen",
        "Switch focus mode off": "Focusmodus uitzetten",
        "Save and switch focus mode on": "Opslaan en focusmodus aanzetten",
        "Focus mode is also in the tray menu, and you can give it a shortcut (see the General "
        "tab). A closed drawer still opens when you click or point at its arrow.":
            "De focusmodus staat ook in het systeemvakmenu, en je kunt er een sneltoets aan "
            "geven (zie het tabblad Algemeen). Een gesloten la gaat nog steeds open als je op "
            "het pijltje klikt of het aanwijst.",
        "Focus mode — everything stays away until you switch it off":
            "Focusmodus — alles blijft weg tot je hem uitzet",
        "{app} — focus mode": "{app} — focusmodus",
        # restore everything
        "Restore everything…": "Alles terugzetten…",
        "Restore everything?": "Alles terugzetten?",
        "This shows your desktop icons, your panel and everything in the drawers again, and "
        "puts back the Plasma settings that {app} changed. {app} is switched off and the "
        "drawers are paused until you switch {app} on again.":
            "Dit toont je bureaubladpictogrammen, je paneel en alles in de laden weer, en zet "
            "de Plasma-instellingen terug die {app} heeft aangepast. {app} wordt uitgeschakeld "
            "en de laden pauzeren tot je {app} weer inschakelt.",
        "Also put the system tray back as it was before {app} changed it":
            "Ook het systeemvak terugzetten zoals het was voordat {app} het aanpaste",
        "Restore": "Terugzetten",
        # about
        "Version {version}": "Versie {version}",
        "Hides your desktop icons when you don't need them, tucks the programs and icons "
        "in your panel away behind an arrow, and lets you choose per icon what shows in the "
        "system tray.":
            "Verbergt je bureaubladpictogrammen als je ze niet nodig hebt, bergt de "
            "programma's en pictogrammen in je paneel op achter een pijltje, en laat je per "
            "pictogram kiezen wat er in het systeemvak staat.",
        "coming with the first release": "volgt bij de eerste release",
        "Made by {author}": "Gemaakt door {author}",
        "License: {license}": "Licentie: {license}",
        "Website and source code": "Website en broncode",
        "Report a problem or share an idea": "Probleem melden of idee delen",
        "Support {app}": "Steun {app}",
        "{app} is free and open source. Find it useful? "
        "A small donation helps further development.":
            "{app} is gratis en open source. Vind je het handig? "
            "Met een kleine donatie help je de verdere ontwikkeling.",
        "♥  Donate": "♥  Doneren",
        "The donation page is coming with the first release.":
            "De doneerpagina volgt bij de eerste release.",
        # settings
        "{app} — settings": "{app} — instellingen",
        "Desktop": "Bureaublad",
        "System tray": "Systeemvak",
        "About {app}": "Over {app}",
        "Hide now": "Nu verbergen",
        "Hide after:": "Verbergen na:",
        "On any mouse movement or key press": "Bij elke muisbeweging of toets",
        "Only on a click on the desktop": "Alleen bij een klik op het bureaublad",
        "Show again:": "Weer tonen:",
        "Left": "Links",
        "Middle": "Midden",
        "Right": "Rechts",
        "With mouse button:": "Met muisknop:",
        "After that time without movement (moving postpones)":
            "Na die tijd stilstand (bewegen stelt uit)",
        "After that time, even while you move": "Na die tijd, ook als je beweegt",
        "With a fixed time the icons can disappear just as you are about to click "
        "something; 10 s or more works well.":
            "Bij een vaste tijd kunnen de pictogrammen verdwijnen terwijl je "
            "net iets wilt aanklikken; 10 s of meer is prettig.",
        "Hide again:": "Weer verbergen:",
        "Moving the mouse into this screen corner brings the icons back.\n"
        "Note: KDE may already have an action on that corner "
        "(System Settings → Screen Edges).":
            "Muis in deze schermhoek haalt de pictogrammen terug.\n"
            "Let op: KDE kan zelf al een actie op die hoek hebben "
            "(Systeeminstellingen → Schermranden).",
        "Screen corner shows:": "Schermhoek toont:",
        "Activity in other windows doesn't count": "Activiteit in andere vensters telt niet mee",
        "On: while you work in another window the timer keeps running "
        "and the icons disappear behind your window. Moving the mouse over "
        "the desktop itself always counts.\n"
        "Off: every mouse movement or key press, anywhere, counts.":
            "Aan: werk je in een ander venster, dan loopt de teller door "
            "en verdwijnen de pictogrammen achter je venster. De muis bewegen "
            "boven het bureaublad zelf telt altijd mee.\n"
            "Uit: elke muisbeweging of toets, waar dan ook, telt.",
        "Moving over the panel does count": "Bewegen boven het paneel telt wel mee",
        "On: moving the mouse over the panel (taskbar) keeps the icons, "
        "like moving over the desktop.\n"
        "Off: only the desktop itself counts.":
            "Aan: de muis bewegen boven het paneel (de taakbalk) houdt de pictogrammen "
            "in beeld, net als bewegen boven het bureaublad.\n"
            "Uit: alleen het bureaublad zelf telt.",
        "Also hide the panel (taskbar)": "Paneel (taakbalk) ook verbergen",
        "Start at login": "Starten bij inloggen",
        "Language:": "Taal:",
        "System language": "Systeemtaal",
        "General": "Algemeen",
        "Hide the icons on:": "Pictogrammen verbergen op:",
        "Fade the icons in and out": "Pictogrammen laten vervagen bij verbergen en tonen",
        "Needs the helper widget on the desktop.":
            "Heeft de hulpwidget op het bureaublad nodig.",
        "Hide with a helper widget on the desktop (lighter)":
            "Verbergen met een hulpwidget op het bureaublad (lichter)",
        "On: an invisible widget on the desktop makes the icons go and come. That is at once, "
        "costs no memory and writes nothing to disk; fading, hiding widgets and the "
        "double-click need it.\n"
        "Off: Tidy swaps the desktop's folder for an empty one and lays an invisible window "
        "over the desktop for your click. That needs nothing inside Plasma.\n"
        "Tidy also falls back on the second way by itself when the helper does not work.":
            "Aan: een onzichtbare widget op het bureaublad laat de pictogrammen verdwijnen en "
            "verschijnen. Dat gaat direct, kost geen geheugen en schrijft niets naar schijf; "
            "vervagen, widgets verbergen en de dubbelklik hebben hem nodig.\n"
            "Uit: Tidy wisselt de map van het bureaublad voor een lege en legt een onzichtbaar "
            "venster over het bureaublad voor je klik. Daar is niets binnen Plasma voor nodig.\n"
            "Tidy valt ook vanzelf terug op de tweede manier als de hulpwidget niet werkt.",
        "New icons go under the ^ arrow by themselves":
            "Nieuwe pictogrammen gaan vanzelf onder het pijltje ^",
        "An application that shows a tray icon for the first time gets it hidden. Works while "
        "Tidy is running.":
            "Een programma dat voor het eerst een pictogram in het systeemvak zet, krijgt het "
            "verborgen. Werkt zolang Tidy draait.",
        "Profiles": "Profielen",
        "A profile keeps all settings together: desktop, drawers, system tray and focus mode. "
        "Switch between them here or in the tray menu.":
            "Een profiel houdt alle instellingen bij elkaar: bureaublad, laden, systeemvak en "
            "focusmodus. Wissel hier of in het systeemvakmenu.",
        "Apply": "Toepassen",
        "Cancel": "Annuleren",
        "Save current as…": "Huidige bewaren als…",
        "Delete": "Verwijderen",
        "Name of the profile:": "Naam van het profiel:",
        "None yet: save one in the settings": "Nog geen: bewaar er een in de instellingen",
        "All settings": "Alle instellingen",
        "Export…": "Exporteren…",
        "Saves all settings and profiles in a file.":
            "Bewaart alle instellingen en profielen in een bestand.",
        "Import…": "Importeren…",
        "Reads settings and profiles from a file and applies them.":
            "Leest instellingen en profielen uit een bestand en past ze toe.",
        "Defaults…": "Standaardwaarden…",
        "Puts every setting back to how Tidy comes. Your drawers stay, with what is in them; "
        "the system tray is left alone.":
            "Zet elke instelling terug naar hoe Tidy geleverd wordt. Je laden blijven, met wat "
            "erin zit; het systeemvak blijft ongemoeid.",
        "Export settings": "Instellingen exporteren",
        "Import settings": "Instellingen importeren",
        "This is not a file with Tidy settings.": "Dit is geen bestand met Tidy-instellingen.",
        "Put every setting back to how Tidy comes?":
            "Elke instelling terugzetten naar hoe Tidy geleverd wordt?",
        "Shortcuts: System Settings → Keyboard → Shortcuts → Add New → Application… → Tidy. "
        "There you can give a key to showing and hiding the icons, switching Tidy on or off, "
        "focus mode, opening or closing the drawers, and restoring everything.":
            "Sneltoetsen: Systeeminstellingen → Toetsenbord → Sneltoetsen → Nieuwe toevoegen → "
            "Toepassing… → Tidy. Daar geef je een toets aan het tonen en verbergen van de "
            "pictogrammen, Tidy in- of uitschakelen, de focusmodus, de laden openen of sluiten, "
            "en alles terugzetten.",
        "Shows everything again, puts back the Plasma settings that Tidy changed, and switches "
        "Tidy off.":
            "Toont alles weer, zet de Plasma-instellingen terug die Tidy heeft aangepast, en "
            "schakelt Tidy uit.",
        "Search…": "Zoeken…",
        "All automatic": "Alles automatisch",
        "Plasma decides for every icon; what is switched off stays off.":
            "Plasma bepaalt het per pictogram; wat uit staat blijft uit.",
        "Plasma default": "Plasma-standaard",
        "Everything switched on and automatic, as a fresh Plasma has it.":
            "Alles ingeschakeld en automatisch, zoals een verse Plasma het heeft.",
        "My preset": "Mijn voorkeur",
        "Apply the arrangement you saved.": "Past de indeling toe die je hebt bewaard.",
        "Save as my preset": "Bewaren als mijn voorkeur",
        "Remember the choices as they are now.": "Onthoudt de keuzes zoals ze nu staan.",
        "Undo": "Ongedaan maken",
        "Back to how the list was when this window opened.":
            "Terug naar hoe de lijst stond toen dit venster openging.",
        "♥ Support {app}": "♥ Steun {app}",
        "Donate or more information": "Doneren of meer informatie",
        "Disabled": "Uitgeschakeld",
        "Hidden — waiting for a click on the desktop":
            "Verborgen — wacht op een klik op het bureaublad",
        "Hidden — waiting for mouse movement or a key press":
            "Verborgen — wacht op een muisbeweging of toets",
        "Paused — menu open or Plasma in edit mode":
            "Gepauzeerd — menu open of Plasma in bewerkingsmodus",
        "paused": "pauze",
        "Visible — hiding in:": "Zichtbaar — verbergen over:",
        # tray menu
        "Enabled": "Ingeschakeld",
        "Settings…": "Instellingen…",
        "♥ Donate…": "♥ Doneren…",
        "Quit": "Afsluiten",
        "{app} — disabled": "{app} — uitgeschakeld",
        "{app} — icons hidden": "{app} — pictogrammen verborgen",
        "{app} — icons visible": "{app} — pictogrammen zichtbaar",
        # command line
        "Usage: plasma-tidy [--show | --hide | --toggle | --settings | --focus | --peek | "
        "--drawer-open | --drawer-close | --drawer-toggle | --restore | --version]":
            "Gebruik: plasma-tidy [--show | --hide | --toggle | --settings | --focus | --peek | "
            "--drawer-open | --drawer-close | --drawer-toggle | --restore | --version]",
        "for example: discord":
            "bijvoorbeeld: discord",
        "Remove this rule":
            "Deze regel verwijderen",
        "Add a rule for a name":
            "Regel voor een naam toevoegen",
        "A rule decides by name how an application's icon appears: when the rule is made, and every time such an icon shows up for the first time. A rule goes before the choice on the left.":
            "Een regel bepaalt op naam hoe het pictogram van een programma verschijnt: op het moment dat je de regel maakt, en elke keer dat zo'n pictogram voor het eerst opduikt. Een regel gaat voor op de keuze links.",
        "Name contains:":
            "Naam bevat:",
        "Programs that go in the drawer":
            "Programma's die in de la gaan",
        "A program without a tick stays in the panel, also while the drawer is closed.":
            "Een programma zonder vinkje blijft in het paneel staan, ook als de la dicht is.",
        "The programs of the task manager appear here a moment after the drawer has one in it. Open this window again to see them.":
            "De programma's van het takenbeheer verschijnen hier kort nadat er een in de la zit. Open dit venster opnieuw om ze te zien.",
        "Program name":
            "Naam van het programma",
        "The list holds the programs that are open now. You can also type the name.":
            "In de lijst staan de programma's die nu open zijn. Je kunt de naam ook typen.",
        "A rule uses one of your profiles, or switches focus mode on, for as long as something is the case. For the profile the highest rule that applies decides. You make profiles on the General tab.":
            "Een regel gebruikt een van je profielen, of zet de focusmodus aan, zolang iets het geval is. Voor het profiel beslist de bovenste regel die geldt. Profielen maak je op het tabblad Algemeen.",
        "No rules yet.":
            "Nog geen regels.",
        "Add a rule":
            "Regel toevoegen",
        "The profile for when no rule with a profile applies.":
            "Het profiel voor als er geen regel met een profiel geldt.",
        "Otherwise:":
            "Anders:",
        "A ✓ marks the rules that apply right now. A profile is put to use at the moment the choice changes; what you change by hand afterwards stays until the next change, so save it in the profile to keep it. Rules work while Tidy is running and switched on.":
            "Een ✓ staat bij de regels die nu gelden. Een profiel wordt gebruikt op het moment dat de keuze verandert; wat je daarna met de hand wijzigt blijft tot de volgende wissel, dus sla het op in het profiel om het te houden. Regels werken zolang Tidy draait en aan staat.",
        "Leave everything as it is":
            "Alles laten zoals het is",
        "Hide the icons after:":
            "Pictogrammen verbergen na:",
        "Start":
            "Starten",
        "More settings…":
            "Meer instellingen…",
        "Rules":
            "Regels",
        "One click":
            "Eén klik",
        "A double-click":
            "Een dubbelklik",
        "Number of clicks:":
            "Aantal klikken:",
        "A double-click on an empty spot of the desktop hides the icons":
            "Dubbelklikken op een lege plek van het bureaublad verbergt de pictogrammen",
        "Also hide the widgets on the desktop":
            "Widgets op het bureaublad ook verbergen",
        "Without a tick this widget stays in view.":
            "Zonder vinkje blijft deze widget in beeld.",
        "Clocks, notes and other widgets on the desktop go and come with the icons. Needs the "
        "helper widget on the desktop.":
            "Klokken, notities en andere widgets op het bureaublad verdwijnen en verschijnen "
            "samen met de pictogrammen. Heeft de hulpwidget op het bureaublad nodig.",
        "While you hold this key, the desktop icons and everything in the drawers are shown; let go and they are away again. Works in focus mode too.":
            "Zolang je deze toets ingedrukt houdt, zijn de bureaubladpictogrammen en alles in de la's te zien; laat los en ze zijn weer weg. Werkt ook in de focusmodus.",
        "Hold to peek:":
            "Ingedrukt houden om te gluren:",
        "This key has no Ctrl, Alt or Meta with it. While Tidy runs it would no longer work in "
        "any program, not for typing or moving either. Better choose a combination, such as "
        "Meta+Z.":
            "Deze toets heeft geen Ctrl, Alt of Meta erbij. Zolang Tidy draait werkt hij dan in "
            "geen enkel programma meer, ook niet om te typen of te bewegen. Kies liever een "
            "combinatie, zoals Meta+Z.",
        "A peek also shows the panel, on top of your windows":
            "Gluren laat ook het paneel zien, boven je vensters",
        "A panel that hides by itself or sits behind a window comes into view while you hold "
        "the key. Your windows keep their size. A program in full screen stays on top of the "
        "panel.":
            "Een paneel dat zichzelf verbergt of achter een venster zit komt in beeld zolang je "
            "de toets vasthoudt. Je vensters houden hun grootte. Een programma op volledig "
            "scherm blijft boven het paneel.",
        "Open with a click on an empty spot in the panel":
            "Openen met een klik op een lege plek in het paneel",
        "A left click where the panel is empty opens this drawer. If a drawer that closes on "
        "such a click is open, the click only closes; it opens when none is.":
            "Een linkerklik waar het paneel leeg is opent deze la. Staat er een la open die op "
            "zo'n klik sluit, dan sluit de klik alleen; openen gebeurt als er geen open staat.",
        "and":
            "en",
        "Applies right now":
            "Geldt nu",
        "Welcome to {app}":
            "Welkom bij {app}",
        "{app} keeps your desktop clean. It hides the desktop icons when you don't need them and brings them back when you do. Three choices to start with; everything can be changed later.":
            "{app} houdt je bureaublad schoon. Het verbergt de bureaubladpictogrammen als je ze niet nodig hebt en haalt ze terug als je ze wel nodig hebt. Drie keuzes om mee te beginnen; alles is later te wijzigen.",
        "There is more in the settings: drawers that tuck panel icons away, a tidy system tray, focus mode, rules and profiles. {app} lives in the system tray: click its eye icon to open the settings.":
            "In de instellingen zit meer: la's die paneelpictogrammen wegstoppen, een opgeruimd systeemvak, focusmodus, regels en profielen. {app} staat in het systeemvak: klik op het oog-pictogram om de instellingen te openen.",
        "Profile: {name}":
            "Profiel: {name}",
        "Desktop {n}":
            "Bureaublad {n}",
        "Higher: goes before the rules below it":
            "Hoger: gaat voor op de regels eronder",
        "Lower":
            "Lager",
        "On battery":
            "Op de accu",
        "On mains power":
            "Op netstroom",
        "An external screen is connected":
            "Er is een extern scherm aangesloten",
        "Between these times":
            "Tussen deze tijden",
        "This program is in front":
            "Dit programma staat vooraan",
        "A program fills the whole screen":
            "Een programma vult het hele scherm",
        "On this virtual desktop":
            "Op dit virtuele bureaublad",
        "In this activity":
            "In deze activiteit",
        "swayidle is missing.\n\nInstall it with:\nsudo dnf install swayidle":
            "swayidle ontbreekt.\n\nInstalleer het met:\nsudo dnf install swayidle",
    },
}
# Choices for the language setting. Languages go by their own name; "auto" follows the system.
LANGUAGES = [("auto", "System language"), ("en", "English"), ("nl", "Nederlands")]


def pick_catalog(choice):
    """Table for the chosen language; with "auto", for the first system language we know.
    English needs no table."""
    if choice in TRANSLATIONS:
        return TRANSLATIONS[choice]
    if choice == "en":
        return {}
    for language in QLocale.system().uiLanguages():
        code = language.replace("_", "-").split("-")[0].lower()
        if code == "en":
            break
        if code in TRANSLATIONS:
            return TRANSLATIONS[code]
    return {}


CATALOG = pick_catalog(QSettings(APP, APP).value("language", "auto"))


def set_language(choice):
    global CATALOG
    CATALOG = pick_catalog(choice)


def tr(text):
    return CATALOG.get(text, text)


def speaks_dutch():
    return CATALOG is TRANSLATIONS.get("nl")
