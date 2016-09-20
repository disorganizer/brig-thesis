# Motivation {#sec:motivation}

Einfache und sichere Dateisynchronisation ist trotz vieler Lösungsansätze im
Jahre 2016 noch immer kein Standard. Versucht man beispielsweise eine Datei
zwischen zwei Personen zu teilen (oder noch schwieriger: synchron zu halten),
so kann man unter anderem zwischen den folgenden Möglichkeiten wählen:

- Übertragung mittels USB--Stick, Speicherkarte oder Ähnlichem
- Übertragung über einen zentralen Dienst, entweder im lokalen Netz (wie FTP oder *ownCloud*[^ownCloud]) 
* Übertragung über das Internet mit zentralen Diensten wie Dropbox.
- Direkte Übertragung im Netzwerk mittels Protokollen wie ``ssh``.
- ...oder sehr häufig auch einfach via E--Mail.

Jede dieser Ansätze »funktioniert« auf seine Weise, doch ergeben sich in der
Praxis meist sehr unterschiedliche Probleme. Bei E--Mails kann oft nur eine
maximale Dateigröße übermittelt werden, die Übertragung von Dateien mittels
``ssh`` ist für die meisten Nutzer zu kompliziert und zentrale Dienste rufen
einerseits Sicherheitsbedenken hervor, andererseits sind sie meist nur bedingt
kostenlos und können unvermittelt ausfallen. Wie in [@fig:xkcd-sync] gezeigt,
muss also für jeden neuen Kontakt stets erst aufwendig der kleinste gemeinsame
Nenner ausgehandelt werden.

![Humorvolle Darstellung der Suche nach dem »kleinsten gemeinsamen Nenner«.[^SOURCE_XKCD]](images/1/xkcd-file-transfer.png){#fig:xkcd-sync width=50%}

[^SOURCE_XKCD]: Quelle: xkcd (<https://xkcd.com/949>)
[^ownCloud]: Eine Filehosting--Software für den Heimgebrauch; siehe auch <https://owncloud.org>

Zahlreiche Ansätze haben versucht diese Probleme in der Praxis abzumildern oder
zu lösen. Viele dieser Ansätze basieren nicht mehr auf einer zentralen
Infrastruktur, sondern benutzen als Gegenentwurf einen dezentralen Ansatz.
Dabei werden nicht alle Dateien an einem zentralen Punkt gespeichert, sondern
können verteilt (ganz oder nur einzelne Blöcke einer Datei) im Netzwerk
vorhanden sein. Dass dabei Dokumente auch durchaus doppelt oder öfters gespeichert werden
dürfen, erhöht die Ausfallsicherheit und vermeidet den Flaschenhals zentraler
Dienste, da der Ausfall einzelner Netzwerkknoten durch andere abgefangen werden kann.
Anwender sind auch oft davon betroffen, dass viele Filehoster nur für einen bestimmten Zeitraum
speichern. Ist dieser Zeitraum vorbei oder wird der Dienst eingestellt, entstehen vielfach
tote Links. Hier könnte eine Lösung ansetzen, bei denen die Dateien von jedem Interessenten
gespiegelt werden und auch von diesen beziehbar sind.

Abseits der Dateisynchronisation konnte sich in anderen Bereichen sichere
Open--Source--Software erfolgreich etablieren. Ein gutes Beispiel hierfür ist
die Messenger--Anwendung *Signal*[^SIGNAL], welche sichere und einfache
Kommunikation auf dem Smartphone ermöglicht. Wir sind der Meinung, dass diese
Software nicht nur durch seine hohen Sicherheitsversprechen eine gewisse
Verbreitung[^SIGNAL_VERBREITUNG] erfahren hat, sondern schlicht weil es genauso
leicht benutzbar und zugänglich war, wie die unsichereren Alternativen (wie *SMS*
oder frühere Versionen von *WhatsApp*). Letztendlich führte dies sogar dazu,
dass die von *Signal* genutzte Technik auch im populäreren
*WhatsApp*--Messenger eingesetzt wurde. Gleichzeitig muss
fairerweise auch gesagt werden, dass die gute Benutzbarkeit durch einige
Vereinfachungen im Sicherheitsmodell erreicht wurden[^SIGNAL_WIKI].

[^SIGNAL]: Mehr Informationen unter: <https://whispersystems.org>
[^SIGNAL_VERBREITUNG]: Zwischen 1 bis 5 Millionen Installationen im PlayStore (<https://play.google.com/store/apps/details?id=org.thoughtcrime.securesms&hl=de>)
[^SIGNAL_WIKI]: Mehr Informationen unter: <https://de.wikipedia.org/wiki/Signal_(Software)#Kritik>

Erwähnenswert ist *Signal*, da auch viele Dateisynchronisationsdienste in der
Praxis entweder an der Benutzbarkeit oder an den Sicherheitsanforderungen
kranken, die insbesondere Unternehmen an eine solche Lösung stellen. Die vorliegende
Arbeit versucht einen dezentralen Ansatz zur Dateisynchronisation vorzustellen,
der eine Balance zwischen Sicherheit und Benutzbarkeit herstellt. Die hier
vorgestellte und quelloffene Lösung trägt den Namen »``brig``«.
Der jeweils aktuelle Quelltext findet sich auf der Code--Hosting--Plattform *GitHub*[^GITHUB].

[^GITHUB]: Offizielles GitHub Repository: <http://github.com/disorganizer/brig>

## Der Name

Eine »Brigg« (englisch »brig«) ist ein kleines und wendiges
Zweimaster--Segelschiff aus dem 18-ten Jahrhundert. Passend erschien uns der
Name einerseits, weil wir flexibel »Güter« (in Form von Dateien) in der ganzen
Welt verteilen, andererseits weil ``brig`` auf (Datei-)Strömen operiert.

Dass der Name ähnlich klingt und kurz ist wie ``git``[^GIT_REF], ist kein
Zufall. Das Versionsverwaltungssystem hat durch seine sehr flexible und
dezentrale Arbeitsweise bestehende zentrale Alternativen wie ``svn`` oder
``cvs`` fast vollständig abgelöst. Zusätzlich ist der Gesamteinsatz von
Versionsverwaltungssystemen durch die verhältnismäßige einfache Anwendung
gestiegen. Wir hoffen mit ``brig`` eine ähnlich flexible Lösung für »große«
Dateien etablieren zu können.

[^GIT_REF]: Ein dezentrales Versionsverwaltungssystem; siehe auch: <https://git-scm.com>

## Lizenz

Eine sicherheitskritische Lösung sollte den Nutzern die Möglichkeit geben zu
validieren, wie die Sicherheitskonzepte implementieren sind. Aus diesem Grund
und um eine freie Weiterentwicklung zu gewährleisten wird die entwickelte
Software unter die ``AGPLv3`` (*Affero General Public License, Version
3*[^AGPL]) gestellt. Diese stellt sicher, dass Verbesserungen am Projekt auch
wieder in dieses zurückfließen müssen. Das Open--Source Modell bietet aus
unserer Sicht hierbei einige grundlegende Vorteile:

- Schnellere Verbreitung durch fehlende Kostenbarriere auf Nutzerseite.
- Kann von Nutzern und Unternehmen ihren Bedürfnissen angepasst werden.
- Transparenz in puncto Sicherheit (keine offensichtlichen Backdoors möglich).
- Fehlerkorrekturen, Weiterentwicklung und Testing aus der Community.

[^AGPL]: Voller Lizenztext unter: <http://www.gnu.org/licenses/agpl-3.0.de.html>

## Gliederung der Arbeit

Diese Arbeit wird einen Überblick über die aktuelle Implementierung sowie die
Techniken und Designentscheidungen dahinter geben, um sie anschließend kritisch
zu reflektieren. Sicherheitsaspekte werden in dieser Arbeit nur oberflächlich
angeschnitten, da Herr Piechula in seiner Arbeit »*Sicherheitskonzepte und
Evaluation dezentraler Dateisynchronisationssysteme am Beispiel
brig*«[@cpiechula] die Sicherheitskonzepte der Software im Detail beleuchtet.

Die vorliegende Arbeit ist in drei größere logische Blöcke gegliedert:

- [@sec:motivation] -- [@sec:eigenschaften] *(Motivation, Einleitung, Stand der Technik):* Eine **Hinführung zum Thema**
  wird gegeben. Neben einer Analyse der Wettbewerber und Einsatzmöglichkeiten wird auch das nötige Grundlagenwissen vermittelt,
  um die nächsten Kapitel zu verstehen.
- [@sec:architektur] -- [@sec:benutzbarkeit] *(Architektur, Implementierung):* In diesen beiden Kapiteln wird das
  **technisches Design des Prototypen** erläutert und Begründen zu den Designentscheidungen gegeben. Zuletzt wird noch ein Konzept
  für eine grafische Benutzeroberfläche vorgestellt.
- [@sec:evaluation] -- [@sec:fazit] *(Evaluation, Fazit):* Der **aktuelle Prototyp wird auf Schwächen untersucht** und mögliche
  Lösungen werden diskutiert. Zudem werden Möglichkeiten zur weiteren Entwicklung aufgezeigt.

Im [@sec:benutzerhandbuch] findet sich zudem ein Benutzerhandbuch, das
losgekoppelt vom Rest gelesen werden und dazu dienen soll ein Eindruck von der
Implementierung zu bekommen.

## Über die Autoren

Die Autoren sind zwei Master--Studenten an der Hochschule Augsburg, die von
Freier Software begeistert sind und mit ihr die Welt ein klein bisschen besser machen
wollen. Momentan entwickeln wir ``brig`` im Rahmen unserer Masterarbeiten bei
Prof. Dr.-Ing. Thorsten Schöler in der
Distributed--Systems--Group[^DSG] und wollen auch nach unserem Abschluss daran
weiter arbeiten. Beide Autoren haben Erfahrung und Spaß darin
Open--Source--Software zu entwickeln und zu betreuen, was neben dem Eigennutzen
einen großen Teil unserer Motivation ausmacht.

Unsere sonstigen Projekte finden sich der Vollständigkeit halber auf GitHub:

* <https://github.com/sahib> (Projekte von Christopher Pahl)
* <https://github.com/qitta> (Projekte von Christoph Piechula)
* <https://github.com/studentkittens> (gemeinsame Projekte und Studienarbeiten)

[^DSG]: Siehe auch: <http://dsg.hs-augsburg.de>

## Typografische Konventionen

TODO: Angebracht?

- ``Monospaced``: Programmnamen.
* *Hervorgehoben*
* **Absatz:**

Diagramme nutzen monospaced als font.

