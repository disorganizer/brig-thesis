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

### Metadatenindex

Problem: Unterschiedliche Pfadkonventionen auf verschiedenen Betriebssystemen.

Virtueller Wurzelknoten.

(/home/sahib/x.png -> /x.png)

TODO: Datenentkopplung.

Alle Metadaten werden in einer einzigen Key--Value basierten Datenbank gespeichert.
Die Basis eines Key--Value--Stores sind sogenannte *Buckets* (dt. Eimer).
In diesem können wie bei einer Hashtabelle einzelne Werte einzigartigen
Schlüsseln zugeordnet werden. Die Werte können wieder *Buckets* sein,
wodurch die Bildung einer verschachtelten Hierarchie möglich ist.
Die verwendete Hierarchie ist dabei schematisch in [@fig:brig-store-layout] abgebildet.

![Hierarchie innerhalb der Key--Value--Datenbank](images/4/tree-store-layout.pdf){#fig:brig-store-layout width=100%}

Anmerkung: Die Struktur ist momentan auf Einfachheit und nicht auf Speichereffizienz ausgelegt.
Es wäre beispielsweise leicht möglich im ``index``--Bucket einen Präfixbaum (TODO: ref) zu speichern.
Dieser würde verhindern, dass Pfade teilweise doppelt abgespeichert werden.

(TODO: In Grafik umwandeln)

### Serialisierung

Protobuf Store Protokoll beschreiben

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

### Versionsverwaltung

Commit/Checkpoint erklären!

### Benutzermanagement

![Überprüfung eines Benutzernamens](images/4/id-resolving.pdf){#fig:arch-overview}

### Synchronisation

Das Synchronisationsmodell von ``brig`` basiert auf einer stark vereinfachter Variante von ``git``.

Unterschied:

- kein gemeinsamer Root nötig (-> lösung: merge points)
- History ist linear für jeden Benutzer. 


Im Gegensatz zu Timed Vector Pair Sync, informierter Austausch, daher muss nicht jedesmal
der gesamte Metadatenindex übertragen werden.

Merge-Commit = Tüte mit allen Checkpoints des Gegenübers

Problem: Metadaten wachsen schnell, Angreifer könnte sehr viele kleine änderungen sehr schnell machen.
Mögliche Lösung : Delayed Checkpoints, Directory Checkpoints.

Kompatible änderungen: A modifiziert, B moved.

### Gateway

### Sonstiges

Logging

Konfiguration
