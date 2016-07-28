# Benutzerhandbuch

Die Funktionalität des ``brig``--Prototypen ist im momentanen Zustand nur über
eine Kommandozeilenanwendung erreichbar. Die Hilfe dieser Anwendung wird unten
gezeigt. Im Folgenden werden die einzelnen zur Verfügung stehenden Optionen und
Kommandos erklärt. Daneben wird auch eine Anleitung zur Installation gegeben
und es werden Ratschläge zur optimalen Nutzung erteilt.

```
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
     add	Transer file into brig's control
     rm		Remove the file and optionally old versions of it
     mv		Move a specific file
     cat	Concatenates a file

GLOBAL OPTIONS:
   --nodaemon, -n		Don't run the daemon
   --password value, -x value	Supply user password
   --path value			Path of the repository (default: ".") [$BRIG_PATH]
   --help, -h			show help
   --version, -v		print the version
```

## Installation

``brig`` kann momentan nur aus den Quellen installiert werden. Zudem wurde
der Prototyp nur auf Linux Systemen[^SYSTEM] getestet.

[^SYSTEM]: Im Falle der Autoren ist das: ArchLinux mit Kernel 4.4 und Go in Version 1.5 bis 1.6.

### Cross-Compiling

## Basics

## Anwendungsbeispiele
