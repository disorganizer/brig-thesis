# Benutzerhandbuch {#sec:benutzerhandbuch}

Die Funktionalität des ``brig``--Prototypen ist im momentanen Zustand nur über
eine Kommandozeilenanwendung erreichbar. Die Hilfe dieser Anwendung wird unten
gezeigt. Im Folgenden werden die einzelnen zur Verfügung stehenden Optionen und
Kommandos erklärt. Daneben wird auch eine Anleitung zur Installation gegeben
und es werden Ratschläge zur optimalen Nutzung erteilt. Vorausgesetzt wird
dabei nur die Lektüre von [@sec:motivation] und [@sec:einleitung], damit dieses Kapitel auch als Tutorial
gelesen werden kann.

```bash
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

## Basics

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

## Anlegen eines Repositories

Repository erklären.

```bash
$ export BRIG_PATH=/tmp/alice
$ brig init alice@wonderland.lit/desktop
```

- Frage nach Passphrase.
- Passphrase mindest komplexität, ref. auf kitteh.
- Wiederholung des Passphrases.

```bash
tree $BRIG_PATH/.brig
```

## Dateien hinzufügen, löschen und verschieben

## Mounten

## Dateien teilen
