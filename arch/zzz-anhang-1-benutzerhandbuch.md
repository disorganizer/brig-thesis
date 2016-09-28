# Anhang: Benutzerhandbuch {#sec:benutzerhandbuch}

TODO: rename brig add -> brig stage
             brig unstage einführen
			 brig status/checkout/log?

Die Funktionalität des ``brig``--Prototypen ist im momentanen Zustand nur über
eine Kommandozeilenanwendung erreichbar. Die Hilfe dieser Anwendung wird unten
gezeigt. Im Folgenden werden die einzelnen zur Verfügung stehenden Optionen und
Kommandos erklärt. Daneben wird auch eine Anleitung zur Installation gegeben
und es werden Ratschläge zur optimalen Nutzung erteilt. Vorausgesetzt wird
dabei nur die Lektüre von [@sec:motivation] und [@sec:eigenschaften], damit
dieses Kapitel auch als Tutorial gelesen werden kann.

```{#lst:brig-help .bash .numberLines}
NAME:
   brig - Secure and dezentralized file synchronization

USAGE:
   brig [global options] command [command options] [arguments...]

VERSION:
   v0.1.0-alpha+cd50f68 [buildtime: 2016-07-28T12:55:29+0000]

COMMANDS:
   ADVANCED COMMANDS:
     daemon	Manually run the daemon process

   MISC COMMANDS:
     config	Access, list and modify configuration values
     mount	Mount a brig repository

   REPOSITORY COMMANDS:
     init	Initialize an empty repository
     open	Open an encrypted repository
     close	Close an encrypted repository
     history	Show the history of the given brig file
     pin	Pin a file locally to this machine
     net	Query and modify network status
     remote	Remote management.

   VERSION CONTROL COMMANDS:
     status	Print which file are in the staging area
     diff	Show what changed between two commits
     log	Show all commits in a certain range
     commit	Print which file are in the staging area

   WORKING COMMANDS:
     tree	List files in a tree
     ls		List files
     mkdir	Create an empty directory
     add	Transer file into brig`s control
     rm		Remove the file and optionally old versions of it
     mv		Move a specific file
     cat	Concatenates a file

GLOBAL OPTIONS:
   --nodaemon, -n		Don`t run the daemon
   --password value, -x value	Supply user password
   --path value			Path of the repository (default: ".") [$BRIG_PATH]
   --help, -h			show help
   --version, -v		print the version
```

## Installation {#sec:installation}

``brig`` kann momentan nur aus den Quellen installiert werden. Zudem wurde
der Prototyp nur auf Linux Systemen[^SYSTEM] getestet, sollte aber prinzipiell
auch unter *Mac OS X* funktionieren. Die Installation aus den Quellen ist in beiden
Fällen vergleichsweise einfach und besteht aus maximal zwei Schritten:

**Installation von Go:** Falls noch nicht geschehen, muss der *Go*--Compiler
und die mitgelieferte Standardbibliothek installiert werden. Dazu kann in Linux
Distribution der mitgelieferte Paketmanager genutzt werden. Unter ArchLinux ist
der Befehl etwa ``pacman -S go`` unter Debian/Ubuntu ``apt-get install
golang``. In allen anderen Fällen kann ein Installationspaket von
``golang.org``[^GOLANG_DOWNLOAD] heruntergeladen werden.
Ist *Go* installiert, muss noch der Pfad definiert werden, in dem alle *Go*--Quellen
landen. Dazu ist das Setzen der Umgebungsvariable ``GOPATH`` nötig:

```bash
$ mkdir ~/go
$ export GOPATH=~/go
$ export PATH=$PATH:~/go/bin
```

Die letzten beiden ``export`` Kommandos sollte man in eine Datei wie
``.bashrc`` einfügen, um zu gewährleisten, dass die Umgebungsvariablen in jeder
Sitzung erneut gesetzt werden.

[^GOLANG_DOWNLOAD]: <https://golang.org/dl/>

**Übersetzen der Quellen:** Ist *Go* installiert, kann mittels des ``go
get``--Werkzeugs ``brig`` kompiliert werden:

```bash
$ go get github.com/disorganizer/brig
```

Nach erfolgreicher Ausführung (kann je nach Rechner zwischen etwa einer bis
zehn Minuten dauern) sollte eine *brig* Kommando auf der Kommandozeile verfügbar sein.
Ohne weitere Argumente sollte das Kommando den oben stehenden Hilfetext produzieren.

[^SYSTEM]: Im Falle der Autoren ist das: ArchLinux mit Kernel 4.4 und Go in Version 1.5 bis 1.6.

### Cross-Compiling

Sobald eine erste öffentliche Version von ``brig`` veröffentlicht wurde, wollen
wir vorgebaute Binärdateien für die populärsten Plattformen anbieten. Um von
einem einzigen Host--System aus Binärdateien für andere Plattformen zu
erstellen, kann der *Go*--Compiler mittels der Umgebungsvariablen ``GOOS`` und
``GOARCH`` dafür konfiguriert werden. ``GOOS`` steuert dabei, die Zielplattform
(z.B. *linux* oder *windows*), ``GOARCH`` hingegen steuert die Zielarchitektur
der CPU (``arm``, ``386``, ``amd64``). Folgendes Shellskript kann daher genutzt
werden, um für einen Großteil der Plattformen eine Binärdatei zu erzeugen:

```bash
#!/bin/sh
PLATFORMS=( linux darwin windows )
ARCHS=( 386 amd64 arm )
OUTDIR=/tmp/brig-binaries

mkdir -p "$OUTDIR"
cd "$GOPATH/src/github.com/disorganizer/brig" || exit 1

for platform in "${PLATFORMS[@]}"; do
    for arch in "${ARCHS[@]}"; do
        printf "## Building %s-%s\n" $platform $arch
        export GOARCH=$arch; export GOOS=$platform

        # This calls `go install` with some extras:
        make || exit 2
        cp $GOBIN/brig "$OUTDIR/brig-$platform-arch"
    done
done
```

[^GOENV]: <https://golang.org/doc/install/source#environment>

## Grundlegende Benutzung

TODO: Umbenennen: brig add -> brig stage
TODO: Implementieren: brig unstage

Die Bedienung von ``brig`` ist an das Versionsverwaltungssystem ``git``
angelehnt. Genau wie dieses, bietet ``brig`` für jede Unterfunktionalität ein
einzelnes Subkommando an. Damit ``git``--Nutzer die Bedienung leichter fällt,
wurden viele Subkommandos ähnlich benannt, wenn sie in etwa dasselbe tun. So
fügen sowohl ``git add``, als auch ``brig add`` Dateien dem Repository hinzu.

Es wird allerdings empfohlen nicht nur aufgrund des Namens auf die
Funktionalität zu schließen. So fügt ``brig add`` Dateien von überall aus dem
Dateisystem hinzu, bei ``git add`` müssen sie unterhalb des
Repository--Wurzelverzeichnises liegen. Die Nahmensähnlichkeit soll nur als
Anknüpfungspunkt für erfahrene Anwender dienen.

### Eingebaute Hilfe

Neben diesem Dokument und der eingebauten Hilfe gibt es im Moment keine weitere
Dokumentation zu den vorgestellten Kommandos. Die eingebaute Hilfe kann
entweder allgemein über ``$ brig help``{.bash} aufgerufen werden (produziert
diesselbe Ausgabe, wie in {#lst:brig-help}) oder für ein spezifisches
Subkommando mittels ``$ brig help <subcommand>``{.bash}. Beispiel für ``$ brig
rm``{.bash}:

```bash
NAME:
   brig rm - Remove the file and optionally old versions of it.

USAGE:
   brig rm [command options] <file> [--recursive|-r]

CATEGORY:
   WORKING COMMANDS

DESCRIPTION:
   Remove a spcific file or directory

OPTIONS:
   --recursive, -r	Remove directories recursively
```

### Anlegen eines Repositories (``brig init``)

Alle von ``brig`` verwalteten Dateien werden in einem einzigen *Repository*
verwaltet. Dies speichert alle Daten und die dazugehörigen Metadaten
in einer Ordnerhierarchie.

Um ``brig`` zu nutzen, muss daher zuerst ein Repository angelegt werden:

```bash
$ export BRIG_PATH=/tmp/alice
$ brig init alice@wonderland.lit/desktop
```

Der Nutzer wird um die Eingabe einer Passphrase gebeten. Die Formulierung
*Passphrase* ist dabei bewusst anstatt dem Wort *Passwort* gewählt, da eine
gewisse Mindestkomplexität Voraussetzung zur erfolgreichen Eingabe ist. Die
Komplexität wird dabei von der ``zxcvbn``--Bibliothek überprüft[^zxcvbn].
Welche Kriterien es dabei anwendet, kann in Kapitel 8 von [@cpiechula]
nachgeschlagen\ werden.

[^zxcvbn]: Mehr Informationen hier: <https://github.com/dropbox/zxcvbn>

Nach wiederholter, erfolgreicher Eingabe der Passphrase wird ein Schlüsselpaar generiert,
und die in [@fig:brig-repo-tree] gezeigte Verzeichnisstruktur angelegt.

### Dateien hinzufügen, löschen und verschieben

Wurde ein Repository angelegt, können einzelne Dateien oder rekursiv ganze
Verzeichnisse hinzugefügt werden:

```bash
$ cd $BRIG_PATH
$ brig add ~/photos/cat.png
/cat.png
$ brig add ~/music/knorkator/
/knorkator
```

Das Hinzufügen größerer Verzeichnisse nimmt etwas Zeit in Anspruch, da die
Dateien komprimiert, verschlüsselt und gehasht werden. 

----

*Anmerkung:* Zum Ausführen dieser Kommandos muss man entweder im Ordner des ``brig``--Repositories
sein oder in einem Unterordner. Andernfalls wird ``brig`` eine Meldung wie diese ausgeben:

```bash
10.08.2016/17:33:11 I: Unable to find repo in path or any parents: "/home/sahib"
10.08.2016/17:33:11 W: Could not load config: open .brig/config: No such file or directory
10.08.2016/17:33:11 W: Falling back on config defaults...
```

Oft genug reichen die Standardwerte der Konfiguration aus, damit der Befehl korrekt funktioniert.
Alternativ kann auch die Umgebungsvariable ``BRIG_PATH`` wie oben gezeigt gesetzt werden, um
von überall im Dateisystem das Kommando absetzen zu können.

----

Die hinzugefügten Dateien werden von ``brig`` einem virtuellen Wurzelknoten ``/`` hinzugefügt (``/cat.png``),
anstatt den vollen Pfad zu erhalten (``~/photos/cat.png``) --- letzterer hätte nach der Synchronisation
auf andere Rechner keine sinnvolle Bedeutung mehr. Dieses Prinzip wird auch ersichtlich bei Benutzung
von ``$ brig ls``{.bash}:

```bash
$ brig ls
105 MB	4 seconds ago	/
2.1 MB	4 seconds ago	/photos/
2.1 MB  5 seconds ago   /photos/cat.png
103 MB	4 seconds ago	/knorkator/
 99 MB	4 seconds ago	/knorkator/hasenchartbreaker/
7.9 MB	1 minute ago	/knorkator/hasenchartbreaker/01 Ich bin ein ganz besond'rer Mann.mp3
...
```

Möchte man den Inhalt einer Datei von ``brig`` wieder ausgeben lassen,
so übergibt man den Pfad an das ``cat``--Subkommando[^BRIG_CAT_NOTE]:

[^BRIG_CAT_NOTE]: Benannt nach dem traditionellen Unix--Kommando ``cat`` zum Ausgeben und Konkatenieren von Dateien.

```bash
$ brig cat /photos/cat.png > some-cat.png
$ open ./some-cat.png  # Öffnet die Datei in einem Bildbetrachter.
```

Da ``brig cat``{.bash} die Datei als kontinuierlichen Strom ausgibt, ist es
möglich größere Dateien (wie Filme) ohne Zwischendatei direkt zu verwerten:

```bash
$ brig cat /movies/big-buck-bunny.mov | mpv -  # Zeige Film mit `mpv`
```

Auch die üblichen Unix--Kommandos zum Anlegen von Verzeichnissen, sowie dem
Löschen und Verschieben von Dateien sind verfügbar:

```bash
# Anmerkung: Der vordere '/' kann auch nach Belieben weggelassen werden.
$ brig mkdir seen-movies
$ brig mv movies/big-buck-bunny.mov seen-movies/
$ brig rm seen-movies/big-buck-bunny.mov
$ brig tree
```

### Nutzung des FUSE Filesystems (``brig mount``)

Die bisherige Nutzung von ``brig`` erinnert an ``git`` und ist für alltägliche
Aufgaben eher aufwendig und nicht kompatibel mit existierenden Dateimanagern.
Leichter wäre es für den Benutzer wenn er seine gewohnten Anwendungen einfach
weiterverwenden könnte. Das ist mit dem *FUSE*--Dateisystem möglich.
Zur Verwendung muss das Dateisystem »gemounted« werden:

```bash
$ mkdir /tmp/alice-mount
$ brig mount /tmp/alice-mount
```

Dies erstellt in ``/tmp/alice-mount`` einen speziellen Ordner, mit den bisher hinzugefügten
Dateien:

```bash
$ ls /tmp/alice-mount
photos  movies  knorkator
```

Es können wie gewohnt Dateien editiert werden, gelöscht und neu angelegt werden:

```bash
$ gimp /tmp/alice-moumt/photos/cat.png
$ cp ~/dog.png /tmp/alice-mount/photos
$ rm /tmp/alice/photos/dog.png
```

Der ``mount``--Befehl kann auch ohne Pfad aufgerufen werden. In diesem Fall wird das Dateisystem.
direkt über dem ``brig``--Repository unter ``$BRIG_PATH`` gelegt:

```bash
$ brig mount
$ ls $BRIG_PATH
photos  movies  knorkator
$ ls /tmp/alice-mount
photos  movies  knorkatoor
$ brig mount -u /tmp/alice-mount
```

Wie man sieht, ist auch der andere Ordner noch weiterhin benutzbar bis er »unmounted« wurde.
Eine Modifikation in dem einen Ordner wird auch im anderen Ordner angezeigt.

(TODO: Test that.)

### Versionsverwaltung

Alle genanten Operationen werden von ``brig`` im Hintergrund aufgezeichnet und
versioniert. Dabei muss zwischen *Checkpoints* und *Commits* unterschieden
werden. Erstere beschreiben eine atomare Änderung an einer Datei (also ob sie
hinzugefügt, gelöscht, modifiziert oder verschoben wurde). Ein *Commit* fasst
mehrere *Checkpoints* zu einem gemeinsamen, logischen Paket zusammen. Ähnlich
wie bei ``git``, gibt es zudem einen *Staging*--Bereich, der aus den
*Checkpoints* bestehen, die noch in keinem *Commit* verpackt worden sind. Ein
wichtiger Unterschied zu ``git`` ist allerdings, dass ``brig`` auch
automatisiert (in einem konfigurierten Zeitintevall) *Commits* erstellen kann.
Diese dienen dann eher als Sicherungspunkte eines Repositories, beziehungsweise
*Snapshots* wie in vielen Backup--Programmen und weniger als zusammenhänge
Einheit logischer Änderungen.

```bash
$ brig status
Changes by alice@wonderland.lit/desktop:

  Added:
		photos/kitten.png
  Removed:
		photos/dog.png
  Moved:
  		cat.png -> photos/cat.png
```

Die gemachten Änderungen können mit dem ``commit``--Unterkommando in einem *Commit* verpackt werden:

```bash
$ brig commit -m 'Moved my cat photos to the right place.'
3 changes committed
```

Die Nachricht, die man mittels ``-m (--message)`` angegeben hat beschreibt, was in diesem *Commit*
passiert ist und taucht später als hilfreiche Beschreibung im ``log`` auf. Mann kann diese
Nachricht auch weglassen, was ``brig`` dazu veranlasst eine automatische *Commit*--Nachricht zu verfassen:

```bash
$ brig add ~/garfield-small.png /photos/garfield.png
$ brig commit
1 change committed
```

Die gemachten *Commits* lassen sich mittels des ``log``--Unterkommandos anzeigen:

```bash
$ brig log
QmNLei78zW/QmNLei78zW by alice, Initial commit
QmPtprCMpd/Qma2Uquo9b by alice, Moved cat photos to the right place.
QmZNJPSbTE/QmbrpM6sKy by alice, Update on 2016-08-11 15:33:37.651 +0200 CEST
```

Die *Checkpoints* einer einzelnen Datei zeigt der ``history`` Befehl:

```bash
/photos/cat.png
 +-- Checkpoint #2 (moved by alice@jabber.nullcat.de/laptop)
 |   +- Hash: Qma2Uquo9bMyuRZ7Fw1oQ1v68Vm7hpCYLRsrQXoLFpZVoK
 |   +- What: /cat.png -> /photos/cat.png
 |   \_ Date: 2016-08-11 15:24:39.993907482 +0200 CEST
 \-- Checkpoint #1 (added by alice@jabber.nullcat.de/laptop)
     |- Hash: Qma2Uquo9bMyuRZ7Fw1oQ1v68Vm7hpCYLRsrQXoLFpZVoK
     \_ Date: 2016-08-11 15:24:15.301565687 +0200 CEST
```

TODO:

brig checkout implementieren...
brig unstage

TODO: Fügt das eigentlich einen neuen punkt in der historie hinzu oder löscht es diesen?
Da die History linear ist, wohl ersteres.

### Verwalten von Synchronisationspartnern (``brig remote``)

Um seine Dateien mit anderen Teilnehmern zu teilen müssen diese erst einmal
``brig`` bekannt gemacht werden und vom Nutzer authentifiziert werden. Für
diese Aufgabe bietet ``brig`` das ``remote``--Unterkommando. Jedes Repository
hat dabei eine eindeutige »Identität«, welches es im Netzwerk eindeutig
identifiziert. Diese besteht aus einem Hash--Wert, und einem menschenlesbaren
Nutzernamen. Für das eigene Repository kann er folgendermaßen angezeigt werden:

```bash
$ brig remote self
QmZyhL3VAAr35a9msSyhW4zfLPnx9Jn4gMSyMQR5VCBFnx online alice@wonderland.lit/desktop
```

Das Hinzufügen eines anderen Nutzers erfordert beide Werte: Sowohl sein Nutzername,
als auch der kryptografische Hash, der ihn unfälschbar identifiziert.
Kennt man den Namen seines Kommunikationspartners, so kann ``brig`` alle Teilnehmer
im Netzwerk mit diesen Namen abfragen. Im Beispiel möchte ``alice`` nun auch ein ``brig``--Repository
auf ihren Laptop einrichten und auf ihren Arbeitsrechner dieses als Partner eintragen:

```bash
$ brig remote locate alice@wonderland.lit/laptop
QmVszFHVNj6UYuPybU3rVXG5L6Jm6TVcvHi2ucDaAubfss
QmNwr8kJrnQdjwupCDLs2Fv8JknjWD7esrF81QDKT2Q2g6
```

Falls man nur den Teil hinter dem ``@`` kennt (also die *Domain*), so, können auch alle
Identitäten mit dieser Domain aufgelistet werden:

```bash
$ brig remote locate alice@wonderland.lit/laptop
QmZyhL3VAAr35a9msSyhW4zfLPnx9Jn4gMSyMQR5VCBFnx
QmVszFHVNj6UYuPybU3rVXG5L6Jm6TVcvHi2ucDaAubfss
QmNwr8kJrnQdjwupCDLs2Fv8JknjWD7esrF81QDKT2Q2g6
```

Für gewöhnlich taucht hier allerdings nur ein Hash--Wert auf, in diesem Fall
muss allerdings zwischen zwei verschiedenen Identitäten gewählt werden.
Mindestens eine davon könnte allerdings theoretisch ein Betrüger sein, der nur
den Nutzernamen *alice@wonderland.lit/laptop* verwendet. In diesem Fall ist es
nötig über einen Seitenkanal direkt Kontakt mit der Person aufzunehmen, mit der
man synchronisieren will und darüber die Identität abzugleichen. Ein möglicher
Seitenkanal wäre ein Telefonanruf, E--Mail oder auch ein Instant Messenger. Hat
man festgestellt was die richtige Identität ist,  kann man sie seiner
Kontaktliste hinzufügen:

```bash
$ brig remote add alice@wonderland.lit/laptop QmVszFHVNj6UYuPybU3rVXG5L6Jm6TVcvHi2ucDaAubfss
```

TODO: Check einbauen ob der Kontakt verfügbar ist und warnen falls nicht?

Der Unterbefehl ``list`` zeigt alle verfügbaren Kontakte an und ob diese online sind:

```bash
$ brig remote list
QmZyhL3VAAr35a9msSyhW4zfLPnx9Jn4gMSyMQR5VCBFnx online alice@wonderland.lit/laptop
```

Das Löschen eines Kontakts ist mit ``$ brig remove <username>``{.bash} möglich
und wird nicht weiter demonstriert.

### Synchronisieren (``brig sync``)

*Anmerkung zur* ``git`` *Analogie:* Es ist bei ``brig`` nicht nötig eine
gemeinsame Synchronisations--Vergangenheit zu haben. Es wird rein auf
Dateiebene synchronisiert. Mit anderen Worten: Konflikte entstehen nur dann
wenn mehre Teilnehmern unterschiedliche Checkpoints für einen einzelnen Pfad
einbringen.

TODO: brig sync

Automatische Synchronisation?

### Dateien pinnen (``brig pin``)

Ist man mit dem Zug unterwegs, so kann ein Pfad »gepinnt« werden, um
sicherzustellen dass sie lokal verfügbar ist:

```bash
$ brig pin /thesis/01-motivation.tex
```

Benötigt man später wieder den Speicherplatz, so kann die Datei wieder »unpinned« werden.
``brig`` wird diese Datei nach einiger Zeit aus dem lokalen Zwischenspeicher entfernt, sofern
ein Platzmangel vorherrscht.

TODO: brig automatisch den gc triggern lassen.

### Konfiguration (``brig config``)

``brig`` bietet momentan einige wenige Konfigurationswerte, um
das Verhalten der Software nach seinen Wünschen einzustellen.
Ein Überblick über die verfügbaren Optionen liefert das Unterkommando ``list`` von ``brig config list``:

```bash
$ brig config list
daemon:
  port: 6666                        # Der Port von brigd.
ipfs:
  path: /tmp/alice/.brig/ipfs       # Pfad zum IPFS-Store
  swarmport: 4001                   # Port des IPFS Swarm
repository:
  id: alice@wonderland.lit/desktop  # Nutzer-ID
```

Das verwendete Format zur Speicherung und Anzeige entspricht dem YAML--Format. (TODO: Ref)
Einzelne Werte können auch direkt angezeigt werden:

```bash
$ brig config get repository.id
alice@wonderland.lit/desktop
```

Möchte man die Werte editieren, so können diese einzeln gesetzt werden:

```bash
$ brig config set daemon.port 7777
```

TODO: Erklärung für bestimmte Konfigurationswerte liefern?

```bash
$ brig config doc daemon.port
Defines the port brigd is listening on locally.

Requires Restart: yes
Category:         daemon
```

## Fortgeschrittene Nutzung

Die obigen Kommandos reichen durchaus für die alltägliche Benutzung von
``brig`` aus. Es gibt ein paar weitere Kommandos, die besonders für technisch
versierte Nutzer und Entwickler interessant sind.

### Repository öffnen und schließen (``brig open/close``)

Um ein Repository als *Datensafe* zu nutzen, kann mit dem ``close``--Unterkommando
der ``brigd``--Daemon heruntergefahren werden. Danach ist das Repository nur
mit der erneuten Eingabe eines Passwortes zugreifbar. Das kann nützlich sein,
um Fremdzugriff auch bei physikalischer Abwesenheit am Rechner zu verhindern.

```bash
$ brig close
# Nach einiger Zeit ohne Netz:
$ brig open
Password: **********
```

Ein explizites ``brig open`` ist bei normaler Benutzung nicht nötig. Jedes
Kommando, das von ``brigd`` abhängt, versucht diesen zu starten, wenn der
Daemon nicht erreichbar ist. Dazu fragt es wie ``brig open``{.bash} auch nach
dem Passwort. Das ``open``--Unterkommando ist allerdings nützlich für
Skriptdateien, wenn der Passwort--Prompt an einer erwarteten Stelle auftauchen
soll.

### Status von ``brigd`` (``brig daemon``)

Das ``daemon``--Unterkommando bietet einige Optionen, um den Status von
``brigd`` zu überprüfen und zu verändern. Um zu überpüfen ob ``brigd`` läuft,
kann das ``ping``--Unterkommando genutzt werden:

```bash
$ brig daemon ping
#01 127.0.0.1:33024 => 127.0.0.1:6668: OK (517.310422ms)
#02 127.0.0.1:33024 => 127.0.0.1:6668: OK (522.751µs)
...
```

Das ``wait``--Unterkommando wartet bis ``brigd`` verfügbar ist und Kommandos entgegen nehmen kann.
Das ist für Skripte nützlich, die darauf warten müssen ohne Passwort--Prompt normale
``brig``--Kommandos abzusetzen:

```bash
$ echo 'Waiting for brig to start...'
$ brig daemon wait
$ echo 'Available! You can execute brig commands now.'
```

Auch das Starten und Beenden von ``brigd`` ist mit diesem Unterkommando direkt möglich:

```bash
$ brig daemon quit    # Momentan selbe Funktion wie `brig close`
$ brig daemon launch  # Momentan selbe Funktion wie `brig open`
```

### Netzwerkstatus (``brig net``)

Das ``net``--Unterkommando bietet die Möglichkeit sich vom Netzwerk zu trennen und wieder
zu verbinden:

```bash
$ brig net status
true
$ brig net offline
$ brig net status
false
$ brig net online
true
```

### Debugging (``brig debug``)

Unter dem ``debug``--Unterkommando finden sich einige Hilfsmittel, um die internen Abläufe
von ``brig`` nachvollziehen zu können:

* ``brig debug export``: Exportiert den aktuellen Metadatenindex auf ``stdout``. Standardmäßig ist das Format
  dabei die binäre Enkodierung von Protobuf. Mit der Option ``--json`` kann allerdings auch zu Debugging--Zwecken
  der Index als JSON exportiert werden.
* ``brig debug import``: Importiert die serialisierte Version eines Metadatenindex. Falls das Format JSON ist,
  sollte die Option ``--json`` benutzt werden.
* ``brig debug diff <StoreA> <StoreB>``: Zeigt Debug--Ausgaben und Differenzen zwischen zwei exportierten, serialisierten
  Indizes.

### Software--Version anzeigen (``brig version``)

Die Versionsnummer von ``brig`` folgt den Prinzipien des *Semantic
Versioning*[^SEMVER] (in der Version 2.0). Das Format entspricht dabei
``v<MAJOR>.<MINOR>.<PATCH>[-<TAG>][+<REV>]``, wobei die Platzhalter folgende
Bedeutung haben:

* ``MAJOR``: Oberste Versionsnummer. Wird nur bei inkompatiblen API--Änderungen inkrementiert.
* ``MINOR``: Wird bei Erweiterungen inkrementiert, welche nicht die Kompatibilität beeinflussen.
* ``PATCH``: Wird bei Berichtigung einzelner Fehler jeweils einmal inkrementiert.
* ``TAG``: Optional. Weißt spezielle Entwicklungsstände wie ``alpha``, ``beta``, ``final`` etc. aus.
* ``REV``: Falls bei Kompilierzeit verfügbar, der aktuelle ``git``--HEAD.

Nach der eigentliche Versionsnummer wird zusätzlich zur Information der Kompilierzeitpunkt angezeigt:

```bash
$ brig -v
v0.1.0-alpha+cd50f68 [buildtime: 2016-07-28T12:55:29+0000]
```

[^SEMVER]: Mehr Informationen unter <http://semver.org>
