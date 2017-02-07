# Anforderungen {#sec:SEC03_ANFORDERUNGEN}

## Einleitung {#sec:SEC03_EINLEITUNG}

Die Betrachtung des aktuellen wissenschaftlichen und technischen Standes zeigt,
dass die Thematik im Detail komplex und kompliziert ist. Nichtsdestotrotz
ergeben sich gewissen Mindestanforderungen, die für die Entwicklung einer
sicheren und dezentralen Dateisynchronisationslösung nötig sind. Um eine
möglichst gute Sicherheit und Usability zu gewährleisten, muss die Software und
der Softwareentwicklungsprozess gewissen Mindestanforderungen genügen.

## Usability {#sec:SEC03_USABILITY}

Die Usability von Software ist teilweise subjektiv und ist stark von dem
Erfahrungshorizont des Nutzers abhängig. Unter Usability ist im Allgemeinen die
Gebrauchstauglichkeit/Benutzerfreundlichkeit[^FN_BENUTZERFREUNDLICHKEIT][^FN_GEBRAUCHSTAUGLICHKEIT]
eines Systems zu verstehen. Bereits bekannte Konzepte werden oft als »intuitiv«
empfunden, neue Konzepte hingegen oft nur mühsam vom Benutzer angenommen. Die
Umstellung des »User Interfaces« von Windows 7 zu Windows 8 (vgl.
[@nielsen2012windows]) ist hierfür ein gutes Beispiel.

[^FN_BENUTZERFREUNDLICHKEIT]: Benutzerfreundlichkeit: <https://de.wikipedia.org/w/index.php?title=Benutzerfreundlichkeit&oldid=159056605>

[^FN_GEBRAUCHSTAUGLICHKEIT]: Gebrauchstauglichkeit: <https://de.wikipedia.org/w/index.php?title=Gebrauchstauglichkeit_(Produkt)&oldid=159056626>

Einen weiteren Punkt zeigt die Praxis. Zwar gibt es seit Jahrzehnten Software
zur sicheren Kommunikation, wie beispielsweise OpenPGP, jedoch hat sich das
Konzept wenig durchgesetzt. Über die genauen Gründe, warum sich PGP nicht
durchgesetzt hat, kann man sich streiten. Laut Meinung des Autors, liegt es
einerseits an der hohen Komplexität beziehungsweise Einstiegshürde,
andererseits zeigen Umfragen, dass eine gewisse Gleichgültigkeit gegenüber dem
Schutz der eigenen Privatsphäre vorherrscht[^FN_PRIVACY_SURVEY].

[^FN_PRIVACY_SURVEY]: Umfrage DIVSI: <https://www.divsi.de/abhoeren-egal-ich-habe-nichts-zu-verbergen/>

Um dieser Problematik möglichst aus dem Weg zu gehen, sollen folgende
Anforderungen umgesetzt werden:

**Bekannte Umgebung:** Der Benutzer soll nach der Installation der Software
weiterhin seine bekannte Umgebung in Form eines Ordners vorfinden. In welcher
er seine Daten sicher speichern und synchronisieren kann, wie er es bereits von
bekannten Cloud--Storage--Diensten, wie beispielsweise Dropbox, kennt.

**Versteckte Sicherheit:** Die Sicherheitskomplexität soll möglichst hinter nur
»einem Passwort« versteckt werden. Dies soll sicherstellen, dass der Benutzer
nicht unnötig mit einer unangenehmen, beziehungsweise vorgangsfremden Thematik
konfrontiert wird.

**Entkopplung der Metadaten:** Die Datenübertragung soll entkoppelt von der
Metadatenübertragung passieren. Dies ermöglicht eine gezielte Synchronisation
bestimmter Daten und ermöglicht dem Benutzer so Ressourcen (Speicherplatz und
Zeit) zu sparen. Dabei sollen die Daten bei der Übertragung und Speicherung
verschlüsselt sein.

## Sicherheit {#sec:SEC03_SICHERHEIT}

Wie bereits unter [@sec:SEC02_DER_SICHERHEITSBEGRIFF] erwähnt, ist Sicherheit
ein sehr weitläufiger Begriff und stark von einem bestimmten »Angriffsszenario«
abhängig.

Eine Software zur dezentralen Dateiverteilung benötigt Sicherheitskonzepte
welche folgende Punkte gewährleisten:

* *Vertraulichkeit:* Kein Zugriff auf Daten durch unbefugte Personen.
* *Integrität:* Manipulation von Daten sind erkennbar.
* *Authentizität:* Kommunikationspartner sind eindeutig identifizierbar.

Die beiden unter [@sec:SEC02_DER_SICHERHEITSBEGRIFF] gelisteten Punkte
Autorisierung und Verfügbarkeit stellen keine erfüllbaren Sicherheitsaspekte
für eine dezentrale Softwarelösung dar.

Weiterhin sollen sich die Anforderungen an die Sicherheit an den aktuell
vorherrschenden und bewährten Sicherheitsstandards orientieren (vgl. @bsi).

Die Entwicklung einer sicheren Software setzt einen sicheren und transparenten
Entwicklungsprozess voraus. Wird eine Software produktiv eingesetzt, so ist ein
stetiges Patchmanagement essentiell. Bei einer dezentralen sicheren
Synchronisationslösung, wie »brig«, ist es weiterhin essentiell, dass ein
durchdachtes Sicherheitskonzept existiert.

Bei Open--Source--Projekten kommt erschwerend hinzu, dass Benutzern und
Entwicklern neben dem Vertrauen in die Software auch eine akzeptable Möglichkeit
geboten werden muss, den Entwicklungsprozess sicher und transparent
mitgestalten zu können.

Aus diesen Herausforderungen ergeben sich bezogen auf das Projekt folgende
Mindestanforderungen sowie Fragestellungen:

* *Passwortmanagement* -- Wie sieht für Benutzer und Entwickler ein sicheres
  Passwortmanagement aus?
* *Schlüsselmanagement* -- Welche Konzepte sollen für die Verwaltung
  kryptographischer Schlüssel verwendet werden?
* *Authentifizierung* -- Wie kann eine sichere Authentifizierung von Benutzern in
  einem dezentralen Netzwerk erfolgen?
* *Sichere Softwareverteilung* -- Wie kann der Benutzer/Entwickler sicherstellen,
  keine Schadsoftware erhalten zu haben?
* *Sichere und transparente Entwicklungsumgebung* -- Wie sieht eine transparente
  und sichere Entwicklungsumgebung aus?

Diese Anforderungen resultieren aus bestimmten Angriffsszenarien, welche im @sec:SEC05_ANGRIFFSFLAECHE_BEI_BRIG detaillierter behandelt werden.
