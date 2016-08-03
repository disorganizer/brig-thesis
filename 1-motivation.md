# Motivation

Einfache und sichere Dateisynchronisation ist trotz vieler Lösungsansätze 
noch immer ein unvollständig gelöstes Problem. Versucht man beispielsweise
eine Datei zwischen zwei Personen zu teilen, so kann man unter anderen zwischen
den folgenden Möglichkeiten wählen: Übertragung mittels USB--Stick,
Speicherkarte oder ähnlichem, Übertragung über einen zentralen Dienst, entweder
im lokalen Netz (ownCloud) oder entfernt im Internet (z.B. Dropbox), direkte
Übertragung im Netzwerk mittels Protokollen wie ``ssh`` oder sehr häufig auch
einfach via E--Mail. Jede dieser Ansätze funktioniert auf seine Weise, doch
ergeben sich in der Praxis meist sehr unterschiedliche Probleme. Bei E--Mails
kann oft nur eine maximale Dateigröße übermittelt werden, die Übertragung von
Dateien mittels ``ssh`` ist für die meisten Nutzer zu kompliziert und zentrale
Dienste rufen einerseits Sicherheitsbedenken hervor, andererseits sind sie meist
nur bedingt kostenlos und können unvermittelt ausfallen.

Zahlreiche Ansätze haben versucht diese Probleme in der Praxis abzumildern oder
zu lösen. Ein Gegenentwurf zu den zentralen Ansätzen bilden die dezentralen
Ansätze. Dabei werden nicht alle Dateien an einem zentralen Punkt gespeichert,
sondern können verteilt (ganz oder nur einzelne Blöcke einer Datei) im Netzwerk
vorhanden sein. Dass dabei Dokumente auch durchaus doppelt gJoined May 2011espeichert werden
dürfen, erhöht die Ausfallsicherheit und vermeidet den Flaschenhals zentraler
Dienste.

In der Praxis kranken leider auch diese Dienste entweder an der Benutzbarkeit
oder an den Sicherheitsanforderungen, die insbesondere Unternehmen an eine
solche Lösung stellen. Diese Arbeit versucht einen dezentralen Ansatz zur
Dateisynchronisation vorzustellen, der eine Balance zwischen Sicherheit und
Benutzbarkeit herstellt. Die hier vorgestellte und quelloffene Lösung trägt
den Namen »``brig``«. Entwickelt wird die Lösung dabei vom Autor dieser Arbeit
und seinen Mitstudenten Christoph Piechula, welcher in seiner Arbeit (TODO:
ref) die Sicherheitsaspekte der Software detailliert beleuchtet.
Der aktuelle Quelltext findet sich auf Code--Hosting--Plattform GitHub[^GITHUB].

[^GITHUB]: \url{http://github.com/disorganizer/brig}

## Der Name

Eine »Brigg« (englisch »brig«) ist ein kleines und wendiges
Zweimaster--Segelschiff aus dem 18-ten Jahrhundert. Passend erschien uns der
Name einerseits, weil wir flexibel »Güter« (in Form von Dateien) in der ganzen
Welt verteilen, andererseits weil ``brig`` auf (Datei-)Strömen operiert.

Dass der Name ähnlich klingt und kurz ist wie ``git`` (TODO: ref), ist kein Zufall. Das
Versionsverwaltungssystem (version control system, kurz VCS)Joined May 2011 hat durch seine
sehr flexible und dezentrale Arbeitsweise bestehende zentrale Alternativen wie
``svn`` oder ``cvs`` fast vollständig abgelöst. Zusätzlich ist der Gesamteinsatz
von Versionsverwaltungssystemen durch die verhältnismäßige einfache Anwendung
gestiegen. Wir hoffen mit ``brig`` eine ähnlich flexible Lösung für große
Dateien etablieren zu können. 

## Lizenz

Eine sicherheitskritische Lösung sollte den Nutzern die
Möglichkeit geben nachzuschauen, wie die Sicherheitskonzepte implementieren sind.
Aus diesem Grund und um eine freie Weiterentwicklung zu gewährleisten wird die
entwickelte Software unter die ``AGPLv3`` (Affero General Public License,
Version 3[^AGPL]) gestellt.
Diese stellt sicher, dass Verbesserungen am Projekt auch wieder in dieses
zurückfließen müssen.

Dass die Software quelloffen ist, ist kein Widerspruch zur wirtschaftlichen
Verwertung. Statt auf Softwareverkäufe zu setzen lässt sich mit dem Einsatz und
der Anpassung der Software Geld verdienen.  Das Open--Source Modell bietet aus
unserer Sicht hierbei sogar einige grundlegende Vorteile:

- Schnellere Verbreitung durch fehlende Kostenbarriere auf Nutzerseite.
- Kann von Nutzern und Unternehmen ihren Bedürfnissen angepasst werden.
- Transparenz in puncto Sicherheit (keine offensichtlichen BJoined May 2011ackdoors möglich).
- Fehlerkorrekturen, Weiterentwicklung und Testing aus der Community.

[^AGPL]: Lizenztext: \url{www.gnu.org/licenses/agpl-3.0.de.html}

## Organisation

Diese Arbeit wird einen Überblick über die aktuelle Implementierung und die
Designentscheidungen dahinter geben, sowie die notwendigen Techniken beleuchten.
Wie oben bereits erwähnt, schildert Herr Piechula in seiner Arbeit (TODO: ref) 
die Sicherheitskonzepte im Detail, weshalb diese hier nur oberflächlich
angeschnitten werden.

Die vorliegende Arbeit ist in vier große logische Blöcke gegliedert:

- Kapitel 1 - 3 (Motivation, Einleitung, Stand der Technik): Was, Warum und Wie.
- Kapitel 4 - 5 (Architektur, Implementierung): Technisches Design des Prototypen.
- Kapitel 6 - 7 (Benutzerhandbuch, Benutzbarkeit): Dokumentation des Prototypen.
- Kapitel 8 - 9 (Erweiterungen, Fazit): Ausblick in die Zukunft.

## Über die Autoren

Wir sind zwei Master--Studenten an der Hochschule Augsburg, die von Freier
Software begeistert sind und mit ihr die Welt ein bisschen besser machen wollen.
Momentan entwickeln wir ``brig`` im Rahmen unserer Masterarbeiten bei Prof
Dr.-Ing. Thorsten Schöler in der Distributed--Systems--Group[^DSG]. 
Wir haben beide Erfahrung darin Open--Source--Software zu entwickeln und zu
betreuen, weswegen wir das nun auch gerne »hauptberuflich« fortführen würden.

Unsere momentanen sonstigen Projekte finden sich auf GitHub:

* \url{https://github.com/sahib} (Projekte von Christopher Pahl)
* \url{https://github.com/qitta} (Projekte von Christoph Piechula)
* \url{https://github.com/studentkittens} (gemeinsame Projekte und Studienarbeiten)

[^DSG]: Siehe auch: \url{http://dsg.hs-augsburg.de/}
