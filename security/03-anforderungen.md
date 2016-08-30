# Anforderungen

Die Betrachtung des aktuellen wissenschaftlichen und technischen Standes zeigt,
dass die Thematik im Detail komplex und kompliziert ist. Nichtsdestotrotz ergeben
sich gewissen Mindestanforderungen, die für die Entwicklung einer »sicheren«
und dezentralen Dateisynchronisationslösung nötig sind. Um eine möglichst gute
Sicherheit und Usability zu gewährleisten, muss die Software und der
Softwareentwicklungsprozess gewissen Mindestanforderungen genügen. Da die
Anforderungen von der Zielgruppe abhängig sind, werden folgend grundsätzliche
Anforderungen definiert, welche Zielgruppen--übergreifend sind.

## Anforderungen an die Software

### Sicherheit

Wie bereits unter [@sec:sicherheit] erwähnt, ist »Sicherheit« ein sehr
weitläufiger Begriff und immer von einem bestimmten »Angriffsszenario«
abhängig.

Eine Software zur dezentralen Dateiverteilung benötigt Sicherheitskonzepte welche folgende Punkte gewährleisten:

* Vertraulichkeit: Kein Zugriff auf Daten durch unbefugte Personen.
* Integrität: Manipulation von Daten erkennen.
* Authentizität: Kommunikationspartner eindeutig identifizierbar.

Weiterhin sollen sich die Anforderungen an die Sicherheit an den aktuell
vorherrschenden und bewährten »Sicherheitsstandards« orientieren.


### Usability

Die Usability von Software ist teilweise subjektiv und ist stark von den
Erfahrungshorizont des Nutzers abhängig. Bereits bekannte Konzepte werden oft
als »intuitiv« empfunden, neue Konzepte hingegen oft nur mühsam vom Benutzer
angenommen. Die Umstellung des »User Interfaces« von Windows 7 zu Windows 8
(vgl. [@nielsen2012windows]) ist hierfür ein gutes Beispiel.

Ein weiteren Punkt zeigt die Praxis. Zwar gibt es seit Jahrzehnten Software zur
»sicheren« Kommunikation, wie beispielsweise OpenPGP, jedoch hat sich das
Konzept nicht durchgesetzt. Über die genauen Gründe, warum sich PGP nicht
durchgesetzt hat, kann man sich streiten. Laut Meinung des Autors, liegt es
einerseits an der hohen Komplexität beziehungsweise Einstiegshürde,
andererseits zeigen Umfragen, dass eine gewisse Gleichgültigkeit gegenüber dem
Schutz der eigenen Privatsphäre vorherrscht[^umfrage]. 

[^umfrage]: Umfrage DIVSI: <https://www.divsi.de/abhoeren-egal-ich-habe-nichts-zu-verbergen/>

Um dieser Problematik möglichst aus dem Weg zu gehen, sollen folgende
Anforderungen umgesetzt werden:

**Bekannte Umgebung:** Der Benutzer soll nach der Installation der Software
weiterhin seine »bekannte« Umgebung in Form eines Ordners vorfinden, in welchem
er seine Daten »sicher« speichern und synchronisieren kann, wie er von bereits
vor bekannten Cloud--Storage--Diensten, wie beispielsweise Dropbox, kennt.

**Versteckte Sicherheit:** Die Sicherheitskomplexität soll möglichst hinter nur
»einem Passwort« versteckt werden. Dies soll sicherstellen, dass der Benutzer
nicht unnötig mit einer »unangenehmen« beziehungsweise vorgangsfremden Thematik
konfrontiert wird.

Die Datenübertragung soll entkoppelt von der Metadatenübertragung passieren.
Dies ermöglicht eine gezielte Synchronisation bestimmter Daten und ermöglicht
dem Benutzer so Ressourcen (Speicherplatz und Zeit) zu sparen. Dabei sollen die
Daten bei der Übertragung und Speicherung verschlüsselt sein.

## Anforderungen an die Softwareentwicklung

* Transparentes Entwicklungsmodell
* »Sichere« Softwareentwicklung
* Signatur von Software--Releases
