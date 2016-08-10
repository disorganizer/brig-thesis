# Benutzerhandbuch {#sec:benutzerhandbuch}

Die Funktionalität des ``brig``--Prototypen ist im momentanen Zustand nur über
eine Kommandozeilenanwendung erreichbar. Die Hilfe dieser Anwendung wird unten
gezeigt. Im Folgenden werden die einzelnen zur Verfügung stehenden Optionen und
Kommandos erklärt. Daneben wird auch eine Anleitung zur Installation gegeben
und es werden Ratschläge zur optimalen Nutzung erteilt. Vorausgesetzt wird
dabei nur die Lektüre von [@sec:motivation] und [@sec:einleitung], damit dieses Kapitel auch als Tutorial
gelesen werden kann.

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

## Installation

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

### Anlegen eines Repositories

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

![Test](images/tree-brig-repo.pdf){#fig:brig-repo-tree width=50%}

### Dateien hinzufügen, löschen und verschieben

Wurde ein Repository angelegt, können einzelne Dateien oder ganze Verzeichnisse hinzugefügt werden:

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

```
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
so übergibt man den Pfad an das ``cat``--Subkommando:

```bash
$ brig cat /photos/cat.png > some-cat.png
$ open ./some-cat.png  # Öffnet die Datei in einem Bildbetrachter.
```

brig cat
brig rm
brig mv
brig ls
brig tree
brig mkdir

### Nutzung des FUSE Filesystems

brig mount

### Versionsverwaltung

brig status
brig history
brig log
brig commit

### Synchronisieren

brig remote
brig sync

### Dateien pinnen

brig pin

## Fortgeschrittene Nutzung

### Repository öffnen und schließen

brig daemon

Fällt der Daemon weg (durch normales Beenden oder Absturz), so fragen alle
Kommandos, die mit ihm kommunizieren müssen nach dem Passwort. Dieses ist nötig,
um ihn neu zu starten.

brig net
brig debug export/import
brig config
brig open
brig close

### Version anzeigen

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
