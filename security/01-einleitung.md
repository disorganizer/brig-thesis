# Einleitung

## Motivation

Der Austausch von Dokumenten beziehungsweise Dateien wurde früher hauptsächlich
über Datenträger (Diskette, USB--Stick) oder E--Mail durchgeführt. Mit dem
Aufkommen der Cloud--Lösungen der letzten Jahre, werden Dateien immer öfters
über Cloud--Dienste wie beispielsweise »Apple iCloud«, »Dropbox«, »Microsoft
OneDrive« oder »Google--Drive« ausgetauscht.

Diese Dienste basieren auf einer zentralen Architektur und ermöglichen dem

Benutzer seine Dateien über mehrere Computer hinweg zu synchronisieren und mit
Freunden --- oder im geschäftlichen Umfeld mit Partnern --- auszutauschen.
Hierbei ist man in der Regel stets auf die Verfügbarkeit des jeweiligen
Dienstes angewiesen --- fällt der Dienst aus oder wird beispielsweise
Strafverfolgungsbehörden geschlossen (Megaupload[^FN_MEGAUPLOAD_TAKEDOWN]),
bleibt einem der Zugriff auf die eigenen Dateien verwehrt.

[^FN_MEGAUPLOAD_TAKEDOWN]: Hinweise zur Schließung: <https://de.wikipedia.org/wiki/Megaupload>

Auch wenn das Aufkommen dieser Dienste auf den ersten Blick eine Abhilfe sein
mag, so werden beim genaueren Hinsehen Risiken und Nachteile --- welche erst
durch Aufkommen dieser Dienste entstanden sind --- deutlich sichtbar. Eins der
Hauptprobleme ist, aufgrund mangelnder Transparenz, der Schutz der Daten
beziehungswiese der Privatsphäre.

Hier muss dem Dienstanbieter vollständig vertraut werden, da nicht bekannt ist
welche Drittparteien Zugriff auf die Daten haben. Dies mag bei der persönlichen
Musik--Sammlung --- im im Gegensatz zur Speicherung sensibler medizinischer
oder finanzieller Unterlagen --- weniger ein Problem sein. Spätestens seit den
Snowden--Enthüllungen und der Bekanntheit des PRISM--Überwachungsprogramms ist
offiziell bekannt[@bibgreenwald2013nsa], dass der Zugriff auf persönliche Daten
durch Drittparteien erfolgt ist beziehungswiese erzwungen wurde. Neben dem
geduldeten oder rechtlich erzwungenen Zugriff durch Drittparteien, haben
Cloud--Storage--Anbieter wie beispielsweise »Dropbox« in der Vergangenheit
immer wieder für Schlagzeilen gesorgt. 

Durch diverse Softwarefehler war beispielsweise der Zugriff über mehrere
Stunden mit beliebigen Passwörtern möglich[^FN_DROPBOX_AUTH_BUG]. Ein weiterer
Softwarefehler hat bei der Aktivierung bestimmter Features Daten unwiderruflich
gelöscht[^FN_DROPBOX_DATA_CORRUPTION]. Daneben wird die Sicherheit von
Cloud--Storage--Services in Studien bemängelt[@bibfisitcloudsec].

[^FN_DROPBOX_AUTH_BUG]: Authentifizierungs--Bug: <https://blogs.dropbox.com/dropbox/2011/06/yesterdays-authentication-bug/>
[^FN_DROPBOX_DATA_CORRUPTION]: Selective--Sync--Bug: <https://plus.google.com/+MichaelArmogan/posts/E9sVnrLTB5C>

Will man Daten privat oder geschäftlich austauschen so muss man sich in der
Regel auf einen Anbieter einigen. Hierbei stellt die
Fragmentierung[^FN_PROVIDER_FRAGMENTATION] der Cloud--Storage--Anbieter den
Benutzer oft vor weitere Herausforderungen.

[^FN_PROVIDER_FRAGMENTATION]: Übersicht Online--Backup--Provider: <https://en.wikipedia.org/wiki/Comparison_of_online_backup_services>

Will man persönlichen Bedenken auf den Einsatz von Cloud--Storage--Anbietern
verzichten, bleibt einem immer noch die Möglichkeit Dateien über E--Mail zu
versenden. Hier erschließt sich aber bei näherer Betrachtung ein ähnliches
Problem wie bei den Cloud--Storage--Anbietern, die Privatsphäre beziehungswiese
der Schutz der Daten vorm Zugriff durch Dritte, sind mangelhaft. Es gibt die
Möglichkeit E-Mails beispielsweise mittels *Pretty Good Privacy* zu
verschlüsseln, jedoch ist der Einsatz und Aufwand für den Otto
Normalverbraucher schlichtweg zu kompliziert und wird daher kaum genutzt.

Der Austausch über Cloud--Storage--Service oder E-Mail ist nichtsdestotrotz der
Quasi--Standard. Es gibt zwar technisch gesehen weitere Möglichkeiten Daten,
auch ohne eine zentrale Instanz, auszutauschen, jedoch sind diese entweder
recht unbekannt, für den Otto Normalverbraucher unbenutzbar oder unsicher. Zu
den bekanntesten Vertretern gehören hier wahrscheinlich
*Syncthing*[^FN_SYNCTHING], *git--annex*[^FN_GIT_ANNEX] oder auch
*Resilio*[^FN_RESILIO].

[^FN_SYNCTHING]: Syncthing: <https://syncthing.net/>
[^FN_RESILIO]: Resilio: <https://getsync.com/>
[^FN_GIT_ANNEX]: git--annex: <https://git-annex.branchable.com/>

Diese Ausgangssituation hat letztendlich nicht nur aus persönlichem Interesse
und mangels Alternativen dazu geführt, sich mit der Thematik näher zu befassen
und weitere Möglichkeiten zu erschließen. In Zusammenarbeit mit meinem
Kommilitonen, Christopher Pahl, wurde die Entwicklung an dem dezentralen
Dateisynchronisationswerkzeug *brig* gestartet, welches aktuelle Situation
verbessern soll.

## Organisation und Schwerpunkt der Arbeit

**Projektschwerpunkte:** Ziel ist es eine Software zu entwickeln, welche
aktuelle Sicherheitsstandards und Usability möglichst gut vereint und dabei
ohne zentrale Instanzen auskommt.

Aufgegliedert liegen die Schwerpunkte wie folgt:

**Vollständige Transparenz:** Der Benutzer soll vollständige Transparenz
bezüglich die Software und den Entwicklungsprozess haben --- nur so lässt ich
eine vertrauenswürdige Implementierung gewährleisten.

**Aktuelle Sicherheitsstandards:** Die Software soll die Daten des Benutzers zu
jeder Zeit möglichst gut schützen. Hierzu sollen bewährte Sicherheitsstandards
verwendet werden.

**Möglichst intuitive Benutzung:** Der Benutzer soll von der
Sicherheitskomplexität so wenig wie nötig mitbekommen. Die Software soll dabei
jedoch mindestens so einfach nutzbar sein wie die heutzutage gängige
Cloud--Dienste.

**Organisation:**

Die Basis für die Entwicklung der Software, Validierung einzelner Komponenten
und Prozesse, sowie die Ausarbeitung möglicher zukünftiger Konzepte stellen die
beiden Arbeiten

1) »brig«: Ein Werkzeug zur sicheren und verteilten Dateisynchronisation,
   *Christopher Pahl*
2) Sicherheitskonzepte und Evaluation dezentraler Dateisynchronisationssysteme
   am Beispiel »brig«, *Christoph Piechula*

an der Hochschule Augsburg bei *Prof. Dr.-Ing. Honorary Doctor of ONPU Thorsten
Schöler* dar.

Die vorliegende Arbeit hat aufgrund des Umfangs des Gesamtprojekts folgende
Schwerpunkte:

* Betrachtung von Sicherheitskonzepten (hier wird zwischen Datensicherheit und
  Datenintegrität unterschieden) zentraler und dezentraler Lösungen.
* Betrachtung der Vor-- und Nachteile zentraler und dezentraler Lösungen.
* Betrachtung von Sicherheitskonzepten welche für eine »sichere« und
  »vertrauenswürdige« Softwareentwicklung essentiell sind
* Evaluation bisherige Ansätze (Sicherheit, Usability) und Definition möglicher
  Verbesserungen, welche in die Weiterentwicklung und in den
  Entwicklungsprozess einfließen sollen.

## Zielgruppen und Einsatzszenarien

Da die Software nicht auf ein bestimmtes Fachgebiet begrenzt werden kann, ist
die Nutzung sowohl durch Individuen, Unternehmen als auch öffentliche
Einrichtungen möglich.

Aufgrund der Ausrichtung der Projektziele, sollen jedoch vor allem Benutzer mit
erhöhten Sicherheitsanforderungen von der Software profitieren. Hierzu gehören
neben einzelnen Individuen vor allem bestimmte Personengruppen wie
beispielsweise:

* Journalisten, Aktivisten
* Medizinischer Bereich
* Öffentliche Einrichtungen

TODO: Ref Elch.

## Projektname und Lizenzierung

Der Name brig stellt eine Anlehnung an das zweimastige Handelsschiff
*brigg*[^FN_BRIGG], welches gegen Ende des 18. Jahrhunderts zum Einsatz kam.
Die Namensanlehnung soll analog den dezentralen Transport von Daten darstellen.

[^FN_BRIGG]: Brigg Handelsschiff: <https://de.wikipedia.org/wiki/Brigg>

Aufgrund der Projektziele kommt als Lizenzierung die Open--Source--die
Open--Source--Lizenz *AGPLv3*[^FN_AGPL] zum Einsatz. Denkbar wären jedoch im
späteren Verlauf des Projektes kombinierte Lizenzen für Unternehmen.

[^FN_AGPL]: AGPLv3 Lizenz: <https://www.gnu.org/licenses/agpl-3.0.de.html>
