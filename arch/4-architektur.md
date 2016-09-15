# Architektur {#sec:architektur}

In diesem Kapitel wird die grundlegende Architektur von ``brig`` erklärt.
Dabei wird vor allem das »Kernstück« beleuchtet: Das zugrundeliegende Datenmodell
in dem alle Metadaten abgespeichert und in Relation gesetzt werden. Basierend
darauf werden die umgebenden Komponenten beschrieben, die um diesen Kern
gelagert sind. Am Ende des Kapitels werden zudem noch einmal alle
Einzelkomponenten in einer Übersicht gezeigt. Es wird dabei stets vom Stand des
aktuellen Prototypen ausgegangen. Mögliche Erweiterungen werden in Kapitel
[@sec:evaluation] (*Evaluation*) diskutiert. Die technische Umsetzung der
jeweiligen Komponenten hingegen wird in [@sec:implementierung]
(*Implementierung*) besprochen.

## Architektur von git

Der interne Aufbau von ``brig`` ist relativ stark von ``git`` inspiriert.
Deshalb werden im Folgenden immer wieder Parallelen zwischen den beiden
Systemen gezogen, um die jeweiligen Unterschiede aufzuzeigen und zu erklären
warum ``brig`` letztlich einige wichtige Differenzen aus architektonischer
Sicht aufweist.

Kurz beschrieben sind beide Projekte »*stupid content
tracker*«[^TORVALDS_ZITAT], die Änderungen an tatsächlichen Dateien auf
Metadaten abbilden, welche in einer dafür geeigneten Datenbank ablegen. Die
eigentlichen Daten werden dabei nicht mittels eines Pfades abgespeichert,
sondern werden durch  eine Prüfsumme referenziert (im Falle von ``git`` mittels
``sha1``). Im Kern lösen beide Programme also Pfade in Prüfsummen auf und
umgekehrt. Um diese Auflösung einfach und effizient möglich zu machen nutzte
``git`` ein ausgeklügeltes Datenmodell, mit dem sich Änderungen natürlich
abbilden lassen. Dabei werden, anders als bei anderen
Versionsverwaltungssystemen (wie Subversion), Differenzen »on-the-fly«
berechnet und nicht separat abgespeichert (daher die Bezeichnung »stupid«).
Abgespeichert werden, wie in [@fig:git-data-model] gezeigt, nur vier
verschiedene *Objekte*:

![Vereinfachte Darstellung des Datenmodell von ``git``.](images/4/git-data-model.pdf){#fig:git-data-model}

[^TORVALDS_ZITAT]: Originalzitat von Linus Torvalds. Siehe auch: <https://git-scm.com/docs/git.html>

- **Blob:** Speichert Daten einer bestimmten Größe (möglicherweise) komprimiert
  ab und assoziiert diese mit einer ``sha1``--Prüfsumme des (unkomprimierten)
  Dateiinhaltes.
- **Tree:** Speichert *Blobs* oder weitere *Trees*, modelliert also eine Art »Verzeichnis«.
  Seine Prüfsumme ergibt sich, indem eine Prüfsumme aus den Prüfsummen der Kinder gebildet wird.
  Zusammen mit *Blobs* lässt sich bereits ein »unixoides Dateisystem« modellieren, bei dem alle
  Dateien von einem Wurzelknoten (ein *Tree* ohne Vorgänger) aus mittels eines Pfades erreichbar sind.
- **Commit:** Ein *Commit* speichert den Zustand des »Dateisystems«, indem es
  seinen Wurzelknoten referenziert. Zudem hat ein *Commit* mindestens einen
  Vorgänger (meist *Parent* genannt, kann beim initialen *Commit* leer sein) und
  speichert eine vom Nutzer verfasste Änderungszusammenfassung ab, sowie den
  Namen des Nutzers. Seine Prüfsumme ergibt sich indem eine Konkatenation von
  Wurzelprüfsumme, Vorgängerprüfsumme, Nutzernamen und
  Commit--Nachricht.[^COMMIT_HASH]
- **Ref:** Eine Referenz auf einen bestimmten *Commit*. Er speichert lediglich dessen
  Prüfsumme und wird von ``git`` separat zu den eigentlichen Objekten gespeichert.

[^COMMIT_HASH]: Mehr Details unter: <https://gist.github.com/masak/2415865>

Die ersten drei Objekte werden in einem gerichteten, azyklischen Graphen
(Merkle--DAG) (TODO: prüfen ob das vorher erklärt wurde) untereinander in
Relation gesetzt. Diese Struktur ergibt sich dadurch, dass bei Änderung einer
Datei in ``git`` sich sämtliche Prüfsummen der Verzeichnisse darüber ändern. In
Abbildung [@fig:git-data-model] wurde im zweiten Commit die Datei ``big.mkv``
verändert (Prüfsumme ändert sich von *QmR5AWs9* zu  *QmYYLnXi*). Als direkte
Konsequenz ändert sich die Prüfsumme des darüber liegenden Verzeichnisses (in
diesem Fall das Wurzelverzeichnis »``/``«). Bemerkenswert ist hier aber, dass auf
das das neue »``/``«--Verzeichnis trotzdem auf das ``/photos``--Verzeichnis des
vorherigen *Commits* verlinkt, da dieses sich in der Zwischenzeit nicht
geändert hat.

Jede Änderung bedingt daher eine Veränderung der Prüfsumme des »``/``«--Verzeichnisses.
Daher sichert dies die Integrität aller darin enthaltenen Dateien ab. Aufgrund dessen
kann ein darüber liegender *Commit* einfach ein *Wurzelverzeichnis* referenzieren, um
eine Momentaufnahme der Daten zu erzeugen. Jeder *Commit* lässt in seine eigene
Prüfsumme zudem die Prüfsumme seines Vorgänger einfließen, weshalb jegliche
(absichtliche oder versehentliche) Modifikation der von ``git`` gespeicherten Daten
aufgedeckt werden kann.

Möchte ``git`` nun die Unterschiede zwischen zwei Dateiständen in zwei
verschiedenen Commits anzeigen, so geht es folgendermaßen vor:

1) Löse die Prüfsummen der beiden zu untersuchenden *Commits* auf.
2) Löse die Prüfsummen der darin enthaltenen Wurzelverzeichnisse auf.
3) Traversiere in beiden Wurzelverzeichnisse zum gewünschten *Blob*.
4) Lade beide *Blobs* und wende ein Algorithmus an, der Differenzen findet (z. B. ``diff`` von Unix).
5) Gebe Differenzen aus.

Dies ist ein signifikanter Unterschied zu Versionsverwaltungssystemen wie ``svn``, die
jeweils die aktuellste Datei ganz und ein oder mehrere »Reverse-Diff« abspeichern. Mithilfe
des *Reverse-Diff* ist es möglich die alten Stände wiederherzustellen.
Obwohl das auf den ersten Blick wie ein Vorteil von ``svn`` wirkt, so nutzt dieses
in der Praxis deutlich mehr Speicherplatz für ein Repository[^MORE_SPACE] und ist signifikant
langsamer als ``git`` (insbesondere da Netzwerkzugriffe nötig sind, während ``git`` lokal arbeitet).
Insbesondere beim Erstellen von *Commits* und dem Wiederherstellen alter Stände ist ``git``
durch sein Datenmodell erstaunlich schnell. Tatsächlich speichert ``git`` auch nicht jeden *Blob*
einzeln, sondern fasst diese gelegentlich zu sogenannten *Packfiles* zusammen, welche
vergleichbar mit einem indizierten, komprimierten Archiv mehrerer Objekte sind[^PACK_FILES].

[^MORE_SPACE]: <https://git.wiki.kernel.org/index.php/GitSvnComparison#Smaller%20Space%20Requirements>
[^PACK_FILES]: Siehe auch: <https://git-scm.com/book/be/v2/Git-Internals-Packfiles>

Zusammengefasst hat ``git`` also aus architektonischer Sicht einige positive Eigenschaften:

* Objekte werden vollautomatisch und ohne weiteren Aufwand dedupliziert abgespeichert.
* Das Datenmodell ist minimalistisch gehalten und leicht für erfahrenere Benutzer verständlich.
* Nicht alle Objekte müssen beim Start von ``git`` geladen werden. Lediglich die benötigten Objekte werden von ``git`` geladen,
  was den Startvorgang beschleunigt.
* Das Bilden einer dezentralen Architektur liegt nahe, da das Datenmodell immer alle Objekte beinhalten muss.
* Alle Dateien liegen in einem separaten ``.git``--Verzeichnis und alle darin enthaltenen Internas sind
  durch die gute Dokumentation gut zugänglich und nötigenfalls reparierbar. Zudem ist das Arbeitsverzeichnis
  ein ganz normales Verzeichnis, in dem der Benutzer arbeiten kann ohne von ``git`` gestört zu werden.
* Die gespeicherten Daten sind durch kryptografische Prüfsummen gegen Veränderungen geschützt.
  Ein potentieller Angreifer müsste ein *Blob* generieren, der die von ihm gewünschten Daten enthält *und*
  die gleiche Prüfsumme, wie der bereits vorhandene *Blob* erzeugt. Obwohl ``sha1`` nicht mehr empfohlen wird[^SCHNEIER_SHA1],
  wäre das ein sehr rechenintensiver Angriff.

[^SCHNEIER_SHA1]: Siehe unter anderem: <https://www.schneier.com/blog/archives/2005/02/sha1_broken.html>

Aus Sicht des Autors hat ``git`` einige, kleinere Schwächen aus architektonischer Sicht:

1) **Prüfsummenalgorithmus nicht veränderbar:** Ein auf einem Merkle--DAG basierenden Versionsverwaltungssystem muss
   eine Abwägung zwischen der Prüfsummenlänge (länger ist typischerweise rechenaufwendiger, braucht mehr Speicher und
   ist unhandlicher für den Benutzer) und der Kollisionsresistenz der Prüfsumme. Tritt trotzdem eine Kollision auf,
   so können Daten überschrieben werden.[^VERSION_CONTROL_BY_EXAMPLE] Solche Kollisionen sind zwar heutzutage noch
   sehr unwahrscheinlicher, werden mit steigender Rechenleistungen aber wahrscheinlicher. Leider kann ``git``
   den genutzten Prüfsummenalgorithmus (``sha1``) nicht mehr ohne hohen Aufwand ändern[^LWM_HASH].
2) **Keine nativen Renames:** ``git`` behandelt das Verschieben einer Datei als eine Sequenz aus dem Löschen und anschließendem
   Hinzufügen der Datei[^GIT_FAQ_RENAME]. Der Nachteil dabei ist, dass ``git`` dem Nutzer die Umbenennung nicht mehr als solche präsentiert,
   was für diesen verwirrend sein kann wenn er nicht sieht, dass die Datei anderswo neu hinzugefügt wurde.
   Neuere ``git`` Versionen nutzen probabilistische Methoden, um Umbenennungen zu finden (Pfad wurde gelöscht, Prüfsumme der Datei tauchte
   aber anderswo auf). Diese können zwar nicht alle Fälle abdecken (umbenannt, dann modifiziert) leisten aber in der Praxis
   zugegebenermaßen gute Dienste.
3) **Probleme mit großen Dateien:** Da ``git`` für die Verwaltung von Quelltextdateien entwickelt wurde, ist es nicht auf die Verwaltung großer Dateien ausgelegt.
   Jede Datei muss dann einmal im ``.git``--Verzeichnis und einmal im
   Arbeitsverzeichnis gespeichert werden, was den Speicherverbrauch mindestens verdoppelt. Da Differenzen zwischen Binärdateien
   nur wenig Aussagekraft haben (da Differenz--Algorithmen normal zeilenbasiert arbeiten) wird bei jeder Modifikation
   jeweils noch eine Kopie angelegt. Nutzer, die ein solches Repository »*clonen*« (also sich eine eigene Arbeitskopie besorgen wollen),
   müssen zudem alle Kopien lokal zu sich kopieren. Werkzeuge wie ``git-annex`` versuchen das Problem zu lösen, indem sie statt den Dateien,
   nur symbolische Links versionieren, die zu den tatsächlichen Dateien zeigen[^GIT_ANNEX]. Symbolische Links sind allerdings wenig portabel,
   weshalb diese Lösung vom Autor eher als »Hack« angesehen wird.
4) **Kein Tracking von leeren Verzeichnissen:** Es können keine leeren
   Verzeichnisse zu ``git`` hinzugefügt werden. Damit ein Verzeichnis von ``git``
   verfolgt werden kann, muss sich mindestens eine Datei darin empfinden. Das ist
   weniger eine Einschränkung des Datenmodells von ``git``, als viel mehr ein
   kleinerer Designfehler[^GIT_FAQ_EMPTY_DIR], der bisher als zu unwichtig galt,
   um korrigiert zu werden.
5) **Keine einzelne History pro Datei:** Es gibt nur eine gesamte *History*,
   die durch die Verkettung von *Commits* erzeugt wird. Bei einem Befehl wie ``git
   log <filename>`` (»Zeige alle Commits, in denen ``<filename>`` verändert
   wurde«) müssen alle *Commits* betrachtet werden, auch wenn ``<filename>`` nur
   in wenigen davon tatsächlich geändert wurde. Eine mögliche Lösung wäre das
   Anlegen einer *History* für einzelne Dateien.

[^VERSION_CONTROL_BY_EXAMPLE]: Siehe auch: http://ericsink.com/vcbe/html/cryptographic_hashes.html
[^LWM_HASH]: Mehr zum Thema unter: <https://lwn.net/Articles/370907>
[^GIT_FAQ_RENAME]: <https://git.wiki.kernel.org/index.php/GitFaq#Why_does_Git_not_.22track.22_renames.3F>
[^GIT_FAQ_EMPTY_DIR]: <https://git.wiki.kernel.org/index.php/GitFaq#Can_I_add_empty_directories.3F>
[^GIT_FAQ_SLOW_LOG]: <https://git.wiki.kernel.org/index.php/GitFaq#Why_is_.22git_log_.3Cfilename.3E.22_slow.3F>
[^GIT_ANNEX]: <https://git-annex.branchable.com/direct_mode>

Zusammengefasst lässt sich sagen, dass ``git`` ein extrem flexibles und schnelles Werkzeug für die Verwaltung von Quelltext und kleinen Dateien ist,
aber weniger geeignet für eine allgemeine Dateisynchronisationssoftware ist, die auch große Dokumente effizient behandeln muss.

## Datenmodell von ``brig``

änderungen:

- checkpoints/inodes (uid)
* 3 statt 2 Möglichkeiten einen Knoten zu referenzieren: per hash (zustand zu bestimmten zeitpunkt); per pfad (lokation zu bestimmten zeitpunkt)
  per inode (neueste lokation *und* neuester zustand)


TODO: Vereinfachung: keine partiellen diffs, nur ganze änderungen.

**Aufbau der Historie:** ``brig`` nutzt ein Modell zur Abbildung der
Dateihistorie, welches insbesondere ``git`` Nutzern vertraut vorkommen sollte.
Das Modell von ``git`` basiert auf einem Merkle-DAG und ähnelt anschaulich dem
in [@fig:merkle-tree] gezeigten Beispiel. Dabei übernimmt ``brig`` den Begriff
des *Commits* und erweitert und vereinfacht das Modell von ``git``
folgendermaßen:

1) Rigorose Trennung zwischen Daten und Metadaten. Metadaten werden von ``brig``'s Datenmodell
   verwaltet. Die eigentlichen Daten werden lediglich per Prüfsumme referenziert und
   von einem Backend (aktuell *IPFS*) gespeichert. So gesehen ist ``brig`` ein ``git``--Aufsatz
   auf ``ipfs``.
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

TODO: Internas von Checkpoint/Commit erklären, was die Hashes bedeuten
TODO: Auflistung aller internen Typen (refs, commit, checkpoints, directories, files)


TODO: Volle Trennung zwischen Daten (IPFS) und Metadaten (Datenmodell)

TODO: Staging area

TODO: Merkle DAG erlaubt keine rückreferenzen.

TODO: Checkpoint Squashing (nicht implementiert, sähe aber so aus)

TODO: Herstellung von coreutils um dieses Datenmodell herum
	  coreutils beschreiben und auflisten

## Architektur von IPFS

TODO: Weiter nach hinten verschieben

Da ``brig`` eine Art »Frontend« für das »Backend« ``IPFS`` ist, wird dessen
Architektur hier kurz schematisch erklärt.

- Bitswap
- For the swarm!

TODO: Komponentendiagramm

-----

Aufbau der Software aus funktionaler Sicht.
Eher blackbox, was kommt rein was kommt raus.

- Berührungspunkte mit Nutzer.

## Architekturübersicht

![Übersicht über die Architektur von ``brig``](images/4/architecture-overview.pdf){#fig:arch-overview}

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

Verschlüsselung ist nur für einzelne Dateien. Verzeichnisse sind Metadaten.

Auf Schwäbisch: "Metadate is alls wasch nüscht koscht"

https://bcache.evilpiepirate.org/Encryption

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

TODO: Erkennung von renames?

TODO: Garbage collector

File_hash = hash aus inhalt
Directory_hash = hash(path) XOR FILE_HASH_1 XOR FILE_HASH_2 ...
COMMIT_HASH = hash(root_hash) XOR hash(parent) XOR Author XOR message

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
