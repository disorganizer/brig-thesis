# Architektur {#sec:architektur}

In diesem Kapitel wird die Architektur des Prototypen von ``brig`` erklärt.
Dabei wird weniger auf die genaue Funktionsweise der Komponenten eingegangen
(das passiert im [@sec:implementierung], *Implementierung*), sondern das
Zusammenspiel der einzelnen Komponenten wird spezifiziert und welche Eingaben
sie entgegennehmen und welche Ausgaben sie produzieren. Die Berührungspunkte
mit dem Nutzer werden ebenfalls diskutiert.

## Architektur von IPFS

Da ``brig`` eine Art »Frontend« für das »Backend« ``IPFS`` ist, wird dessen
Architektur hier kurz schematisch erklärt.

![Übersicht über die Architektur von ``brig``](images/4/architecture-overview.pdf){#fig:arch-overview}

- Bitswap
- For the swarm!

TODO: Komponentendiagramm

-----

Aufbau der Software aus funktionaler Sicht.
Eher blackbox, was kommt rein was kommt raus.

- Berührungspunkte mit Nutzer.

## Architekturübersicht

TODO: Komponentendiagramm

TODO: Repository begriff irgendwo einführen?

``brig`` ist architektonisch in einem langlebigen Daemon--Prozess und einem
kurzlebigen Kontroll--Prozess aufgeteilt, welche im Folgenden jeweils ``brigd``
und ``brigctl`` genannt werden.[^BRIGCTL_NOTE] Beide Prozesse kommunizieren
dabei über Netzwerk mit einem speziellen Protokoll, welches auf einen
Serialisierungsmechanismus  von Google namens *Protobuf*[^PROTOBUF] basiert.
Dabei wird basierend auf einer textuellen Beschreibung des Protokolls (in einer
``.proto``--Datei mit eigener Syntax) Quelltext generiert in der gewünschten
Zielsprache generiert. Dieser Quelltext ist dann in der Lage Datenstrukturen
von der Zielsprache in ein serialisiertes Format zu überführen, beziehungsweise
dieses wieder einzulesen. Als Format steht dabei wahlweise eine
speichereffiziente, binäre Repräsentation der Daten zur Verfügung, oder eine
menschenlesbare Darstellung als JSON--Dokument.

Die Aufteilung in zwei Programmteile ist dabei inspiriert von ``MPD`` und
``IPFS``. (TODO) Nötig ist die Aufteilung vor allem, da ``brigd`` im
Hintergrund als Netzwerkdienst laufen muss, um Anfragen von außen verarbeiten
zu können. Abgesehen davon ist es aus Effizienz--Gründen förderlich, wenn nicht
bei jedem eingetippten Kommando das gesamte Repository geladen werden muss.
Auch ist es durch die Trennung möglich, dass ``brigd`` auch von anderen
Programmiersprachen und Prozessen auf dem selben Rechner aus gesteuert werden
kann.

[^BRIGCTL_NOTE]: Tatsächlich gibt es derzeit keine ausführbaren Dateien mit
diesen Namen. Die Bezeichnungen ``brigctl`` und ``brigd`` dienen lediglich der
Veranschaulichung.
[^PROTOBUF]: Mehr Informationen unter: <https://developers.google.com/protocol-buffers>

### Aufbau von ``brigctl``

Kurz gesagt ist ``brigctl`` eine »Fernbedienung« für ``brigd``, welche momentan
exklusiv von der Kommandozeile aus bedient wird. In den meisten Fällen
verbindet sich der Kommando--Prozess ``brigctl`` sich beim Start zu ``brigd``,
sendet ein mittels *Protobuf* serialisiertes Kommando und wartet auf die
dazugehörige Antwort welche er dann deserialisiert. Nachdem die empfangene
Antwort je nach Art ausgewertet wurde, beendet sich der Prozess wieder.

**Protobuf Protokoll:** Das Protokoll ist dabei so, aufgebaut, dass
für jede Aufgabe, die ``brigd`` erledigen soll ein separates Kommando
existiert. Neben einer allgemeinen Typbezeichnung, können auch vom Kommando
abhängige optionale und erforderliche Parameter enthalten sein. Ein gekürzter
Auszug aus der Protokollspezifikation veranschaulicht dies in [@lst:proto-command].

```{#lst:proto-command .protobuf}
enum MessageType {
	ADD = 0;
	// ...
}

message Command {
	// Type identifier of the Command
	required MessageType command_type = 1;

	message AddCmd {
		// Absolute path to the file on the user's disk.
		required string file_path = 1;

		// Path inside the brig repo (e.g. /photos/me.png)
		required string repo_path = 2;

		// Add directories recursively? Defaults to true.
		optional bool recursive = 3;
	}
	// ... more subcommands ...

	// If command_type is ADD, read from this field:
	optional AddCmd add_command = 2;
	// ... more command entries ...
}
```

Analog dazu kann ``brigd`` mit einer *Response* auf ein *Command* antworten. In
[@lst:proto-response] wird beispielhaft die Antwortspezifikation
(``OnlineStatusResp``) auf ein ``OnlineStatusCmd``--Kommando gezeigt, welches
prüft, ob ``brigd`` Verbindungen von Außen annimmt.

```{#lst:proto-response .protobuf}
message Response {
	// Type identifier to the response;
	// matches the associated command.
    required MessageType response_type = 1;

	// Everything fine?
    required bool success = 2;

	// If not, an optional error description might be provided.
	optional string error = 3;

	// Detailed error code (not yet used)
	optional id errno = 4;

	message OnlineStatusResp {
		// True if brigd is in online mode.
    	required bool is_online = 1;
	}
	// ... more sub responses ...

	optional OnlineStatusResp online_status_resp = 5;
	// ... more response entries ...
}
```

Neben der Kommunikation mit  ``brigd`` muss ``brigctl`` noch drei andere Aufgaben erledigen:

**Initiales Anlegen eines Repositories:** Bevor ``brigd`` gestatertet werden kann,
muss die in TODO: ref gezeigte Verzeichnisstruktur angelegt werden.

**Bereitstellung des User--Interfaces:** Das zugrundeliegende Protokoll wird so gut
es geht vom Nutzer versteckt und Fehlermeldungen müssen möglichst gut beschrieben werden.

**Autostart von ``brigd``:** Damit der Nutzer nicht explizit ``brigd`` starten
muss, sollte der Daemon--Prozess automatisch im Hintergrund gestartet werden,
falls er noch nicht erreichbar ist. Dies besorgt ``brigctl`` indem es dem
Nutzer nach dem Passwort zum Entsperren eines Repositories fragt und das
Passwort beim Start an ``brigd`` weitergibt, damit der Daemon--Prozess das
Repository entsperren kann.

### Aufbau von ``brigd``

Der Daemon--Prozess implementiert alle sonstigen Funktionalitäten, die nicht
von ``brigctl`` erfüllt werden. Die einzelnen Komponenten werden in
[@sec:einzelkomponenten] beschrieben. In diesem Abschnitt werden nur
die Eigenschaften von ``brigd`` als Hintergrundprozess beschrieben.

Ist gleichzeitig IPFS im selben Prozess.

Nach Start des Daemons, lauscht dieser als Netzwerkdienst auf einem
Port  

Global config zur Bestimmung des Ports.

## Einzelkomponenten {#sec:einzelkomponenten}


### Dateiströme

https://en.wikipedia.org/wiki/Convergent_encryption

Schaubild mit den relevanten io.Reader/io.Writer

#### Verschlüsselung

![Aufbau des Verschlüsselungs--Dateiformats](images/4/format-encryption.pdf){#fig:format-encryption}

TODO: NaCL Secretbox erwähnen, Unterschiede

#### Kompression

![Aufgbau des Kompressions--Dateiformat](images/4/format-compression.pdf){#fig:format-compression}

### Dateisystemordner

FUSE

### Deduplizierung

- Miller Rabin Chunking
- Rolling Hash

### Benutzermanagement

![Überprüfung eines Benutzernamens](images/4/id-resolving.pdf){#fig:arch-overview}

### Synchronisation

**Synchronisation einzelner Dateien:** In seiner einfachsten Form nimmt ein Synchronisationsalgorithmus als Eingabe
die Metadaten zweier Dateien von zwei Synchronisationspartnern und trifft als
auf dieser Basis als Ausgabe eine der folgenden Entscheidungen:

1) Die Datei existiert nur bei Partner A.
2) Die Datei existiert nur bei Partner B.
3) Die Datei existiert bei beiden und ist gleich.
4) Die Datei existiert bei beiden und ist verschieden.


Je nach Entscheidung kann für diese Datei eine entsprechende Aktion ausgeführt werden:

1) Die Datei muss zu Partner B übertragen werden.
2) Die Datei muss zu Partner A übertragen werden.
3) Es muss nichts weiter gemacht werden.
4) Konfliktsituation: Eventuell Eingabe vom Nutzer erforderlich.

Bis auf den vierten Schritt ist die Implementierung trivial und kann leicht von
einem Computer erledigt werden. Das Kriterium, ob die Datei gleich ist, kann
entweder durch einen direkten Vergleich gelöst werden (aufwendig) oder durch
den Vergleich der Prüfsummen beider Dateien (schnell, aber vernachlässigbares
Restrisiko durch Kollision TODO: ref). Manche Werkzeuge wie ``rsync`` setzen
sogar auf probabilistische Ansätze, indem sie in der Standardkonfiguration aus Geschwindigkeitsgründen nur
ein Teil des Dateipfades, eventuell das Änderungsdatum und die Dateigröße vergleichen.

Für die Konfliktsituation hingegen kann es keine perfekte, allumfassende Lösung
geben, da die optimale Lösung von der jeweiligen Datei und der Absicht des
Nutzers abhängt. Bei Quelltext--Dateien möchte der Anwender vermutlich, dass
beide Stände automatisch zusammengeführt werden, bei großen Videodateien ist
das vermutlich nicht seine Absicht. Selbst wenn die Dateien nicht automatisch zusammengeführt werden sollen
(englisch >>to merge<<), ist fraglich was mit der Konfliktdatei des Partners geschehen soll.
Soll die eigene oder die fremde Version behalten werden? Dazwischen sind auch weitere Lösungen denkbar,
wie das Anlegen einer Konfliktdatei (``photo.png:conflict-by-bob-2015-10-04_14:45``), so wie es beispielsweise
Dropbox macht.[^DROPBOX_CONFLICT_FILE]
Alternativ könnte der Nutzer auch bei jedem Konflikt befragt werden. Dies wäre
allerdings im Falle von ``brig`` nach Meinung des Autors der Benutzbarkeit
stark abträglich.

Im Falle von ``brig`` müssen nur die Änderung von ganzen Dateien betrachtet werden, aber keine partiellen Änderungen
darin. Eine Änderung der ganzen Datei kann dabei durch folgende Aktionen des Nutzers entstehen:

1) Der Dateinhalt wurde modifiziert, ergo muss sich die Prüfsumme geändert haben (``MODIFY``).
2) Die Datei wurde verschoben (``MOVE``).
3) Die Datei wurde gelöscht (``REMOVE``).
4) Die Datei wurde (initial oder erneut) hinzugefügt (``ADD``).

Der vierte Zustand (``ADD``) ist dabei der Initialisierungszustand. Nicht alle dieser
Zustände führen dabei automatisch zu Konflikten. So sollte ein guter
Algorithmus kein Problem, erkennen, wenn ein Partner die Datei modifiziert und
der andere sie lediglich umbenennt. Eine Synchronisation der entsprechenden
Datei sollte den neuen Inhalt mit dem neuen Dateipfad zusammenführen.
[@tbl:sync-conflicts] zeigt welche Operationen zu Konflikten führen und welche
verträglich sind.


|     A/B    | ``ADD`` | ``REMOVE`` | ``MOVE`` | ``MODIFY`` |
|:----------:|---------|------------|----------|------------|
|   ``ADD``  | ?       | ?          | ?        | ?          |
| ``REMOVE`` | ?       | \cmark     | \xmark   | \xmark     |
|  ``MOVE``  | ?       | \xmark     | ?        | \xmark     |
| ``MODIFY`` | ?       | \xmark     | \cmark   | \xmark     |

: Verträglichkeit {#tbl:sync-conflicts}

TODO: Fragezeichen in Tabelle erklären.

[^RSYNC]: <https://de.wikipedia.org/wiki/Rsync>
[^DROPBOX_CONFLICT_FILE]: Siehe <https://www.dropbox.com/help/36>

**Synchronisation von Verzeichnissen:** Prinzipiell lässt sich die
Synchronisation einer Datei auf Verzeichnisse übertragen, indem einfach obiger
Algorithmus auf jede darin befindliche Datei angewandt wird. In der
Fachliteratur (vergleiche unter anderem [@cox2005file]) findet sich zudem die
Unterscheidung zwischen *informierter* und *uninformierter* Synchronisation.
Der Hauptunterschied ist, dass bei ersterer die Änderungshistorie jeder Datei
als zusätzliche Eingabe zur Verfügung steht. Auf dieser Basis können dann
intelligentere Entscheidungen bezüglich der Konflikterkennung getroffen werden.
Insbesondere können dadurch aber leichter die Differenzen zwischen den
einzelnen Ständen ausgemacht werden: Für jede Datei muss dabei lediglich die in
[@lst:file-sync] gezeigte Sequenz abgelaufen werden, die von beiden
Synchronisationspartnern unabhängig ausgeführt werden muss. Unten stehender
Go--Pseudocode ist eine modifizierte Version aus Russ Cox' Arbeit »File
Synchronization with Vector Time Pairs«[@cox2005file], welcher für ``brig``
angepasst wurde.

```{#lst:file-sync .go caption="Synchronisationsalgorithmus für eine einzelne Datei"}
// historyA ist die Historie der eigenen Datei A.
// historyB ist die Historie der fremden Datei B mit gleichem Pfad.
func sync(historyA, historyB History) Result {
	if historyA.Equal(historyB) {
		// Keine weitere Aktion nötig.
		return NoConflict
	}

	if historyA.IsPrefix(historyB) {
		// B hängt A hinterher.
		return NoConflict
	}

	if historyB.IsPrefix(historyA) {
		// A hängt B hinterher. Kopiere B zu A.
		copy(B, A)
		return NoConflict
	}

	if root := historyA.FindCommonRoot(historyB); root != nil {
		// A und B haben trotzdem eine gemeinsame Historie,
		// haben sich aber auseinanderentwickelt.
		if !historyA.HasConflictingChanges(historyB, root) {
			// Die Änderungen sind verträglich und
			/  können automatisch aufgelöst werden.
			ResolveConflict(historyA, historyB, root)
			return NoConflict
		}
	}

	// Keine gemeinsame Historie.
	// -> Nicht automatisch zusammenführbar.
	// -> Konfliktstrategie muss angewandt werden.
	return Conflict
}
```

Werkzeuge wie ``rsync`` betreiben eher eine *uninformierte Synchronisation*.
Sie müssen bei jedem Programmlauf Metadaten über beide Verzeichnisse sammeln
und darauf arbeiten. TODO: mehr worte verlieren
Im Gegensatz zu Timed Vector Pair Sync, informierter Austausch, daher muss nicht jedesmal
der gesamte Metadatenindex übertragen werden.


**Aufbau der Historie:** ``brig`` nutzt ein Modell zur Abbildung der
Dateihistorie, welches insbesondere ``git`` Nutzern vertraut vorkommen sollte.
Das Modell von ``git`` basiert auf einem Merkle-DAG und ähnelt anschaulich dem
in [@fig:merkle-tree] gezeigten Beispiel. Dabei übernimmt ``brig`` den Begriff
des *Commits* und erweitert und vereinfacht das Modell von ``git``
folgendermaßen:

1) Es ist sind keine *Branches* möglich. Jeder *Commit* hat exakt einen
   Vorgänger. Die einzige Ausnahme bildet der leere *Commit*, welcher beim Anlegen
   eines Repositories erstellt wird. Mit anderen Worten: Die Commit--Historie ist
   immer linear.
2) Synchronisationspartner müssen **keine gemeinsame Vergangenheit** haben.
   In diesem Fall werden einfach alle Dateien als Änderungen erkannt.
   Ein separates Klonen eines Repositories ist daher nicht nötig. Es kann einfach
   ein neues, leeres Repository angelegt werden, in das dann alle Daten des gewünschten
   Partners synchronisiert werden.
3) Es werden keine partiellen Änderungen gespeichert, sondern lediglich die oben
   erklärten Änderungszustände ``ADD``, ``MODIFY``, ``REMOVE`` und ``MOVE``.
   Eine solche atomare Änderung wird *Checkpoint* genannt. Jeder *Checkpoint*
   kennt den Zustand der Datei zum Zeitpunkt der Modifikation, sowie einige Metadaten
   wie ein Zeitstempel, der Dateigröße, dem Änderungstyp, dem Urheber der Änderung
   und seinem Vorgänger. Kurz gesagt hat jede Datei also eine eigene, unabhängige Änderungshistorie,
   ohne, dass diese aus den Commits extrahiert werden muss.
4) Da ein *Commit* nur ein Vorgänger haben kann, musste ein anderer Mechanismus eingeführt werden,
   um die Synchronisation zwischen zwei Partnern festzuhalten. Bei ``git`` wird
   dies mittels eines Merge--Commit gelöst, welcher aus den Änderungen der
   Gegenseite besteht. Hier wird das Konzept eines *Merge--Points* eingeführt.
   Innerhalb eines *Commit* ist das ein spezieller Marker, der festhält mit wem synchronisiert wurde
   und mit welchen Stand er zu diesem Zeitpunkt hatte. Bei einer späteren Synchronisation muss
   daher lediglich der Stand zwischen dem aktuellen *Commit* (nach ``git``--Terminologie ``HEAD`` genannt),
5) Ein *Commit* muss bei ``brig`` nicht zwangsweise ein logisches Paket mit zusammengehörigen Änderungen sein.
   Die Funktionalität gleich eher einem *Snapshot* (bekannt aus vielen Backup--Programmen), welche
   eher einen Sicherungspunkt zu einem gewissen Zeitpunkt bieten. Entsprechend werden in der Praxis viele
   *Commits* bei ``brig`` automatisch gemacht, nachdem einige Zeit lang keine Änderung mehr stattfand.
6) Anders als bei ``git`` kennt jedes ``brig``--Repository den Stand aller
   Teilnehmer (beziehungsweise den zuletzt verfügbaren), die ein Nutzer in seiner
   Remote--Liste gespeichert hat. Da es sich dabei nur um Metadaten handelt, wird
   dabei nicht viel Speicherplatz in Anspruch genommen.


Merge-Commit = Tüte mit allen Checkpoints des Gegenübers

Problem: Metadaten wachsen schnell, Angreifer könnte sehr viele kleine änderungen sehr schnell machen.
Mögliche Lösung : Delayed Checkpoints, Directory Checkpoints.

TODO: Internas von Checkpoint/Commit erklären, was die Hashes bedeuten.


**Synchronisation über das Netzwerk:** Um die Metadaten nun tatsächlich
austauschen zu können, muss ein Protokoll etabliert werden, mit dem diese
zwischen zwei Partnern übertragen werden. Aus Zeitgründen ist dieses Protokoll
im Moment sehr einfach und wird bei größeren Datenmengen nicht optimal
funktionieren. Für einen Proof--of--Concept reicht es aber aus. Wie in Grafik TODO gezeigt besteht das Protokoll
aus drei Teilen.

* encode
- fetch.
- decode

Nachteilig ist dabei natürlich, dass momentan der gesamte Metadatenindex
übertragen werden muss. Mit etwas mehr Aufwand könnte vorher der eigentlichen
Übertragung der letzte gemeinsame Stand ausgehandelt werden, um nur die
Änderungen seit diesem Stand zu übertragen zu müssen.

Auch sind zum momentanen Stand noch keine *Live*--Updates möglich. Hierfür müssten sich die
einzelnen Knoten bei jeder Änderung kleine *Update*--Pakete schicken, welche prinzipiell
einen einzelnen *Checkpoint* beeinhalten würden. Dies ist technisch bereits möglich,
wurde aus Zeitgründen aber noch nicht umgesetzt.

### Versionsverwaltung

Die Historiedaten sind natürlich nicht nur zum Synchronisieren nützlich. Sie können auch verwendet werden,
um die häufigsten Funktionalitäten von Versionsverwaltungssystemen umzusetzen.

- checkout
* commit
- Staging Bereich (status)

Zukunft:

- tag

### Gateway

### Sonstiges

Logging

Konfiguration
