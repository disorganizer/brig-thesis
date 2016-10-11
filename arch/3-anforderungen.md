# Anforderungen {#sec:requirements}

Im Folgenden wird auf die Anforderungen eingegangen, welche ``brig`` in
Zukunft erfüllen soll. Diese sind weitreichender als der Umfang der
aktuellen Implementierung. Die Anforderungen lassen sich in drei Kategorien
unterteilen:

- **Anforderungen an die Integrität:** ``brig`` muss die Daten die es speichert
  versionieren, auf Integrität prüfen können und korrekt wiedergeben.
- **Anforderungen an die Sicherheit:** Alle Daten die ``brig`` anvertraut werden,
  sollten sowohl bei der Speicherung auf der Festplatte als auch bei der
  Übertragung zwischen Partnern verschlüsselt werden. Die Implementierung
  der Sicherheitstechniken sollte transparent von Nutzern und Experten
  nachvollzogen werden können.
- **Anforderungen an die Usability:** Die Software soll möglichst einfach zu
  nutzen und zu installieren sein. Der Nutzer soll ``brig`` auf den populärsten
  Betriebssystemen nutzen können und auch Daten mit Nutzern anderer
  Betriebssysteme austauschen können.

Die Kategorien beinhalten einzelne, konkretere Anforderungen, die im Folgenden
aufgelistet und erklärt werden. Dabei wird jeweils im ersten Paragraphen die
eigentliche Anforderung formuliert und danach kurz beispielhaft erklärt.
Ob und wie die Anforderung letztlich erfüllt wurde, wird in [@sec:evaluation]
betrachtet.

Nicht jede Anforderung kann dabei voll umgesetzt werden. Teils überschneiden
oder widersprechen sich Anforderungen an die Sicherheit und an die Effizienz,
da beispielsweise verschlüsselte Speicherung mehr Prozessor--Ressourcen in Anspruch nimmt.
Auch ist hohe Usability bei gleichzeitig hohen
Sicherheitsanforderungen schwierig umzusetzen. Das Neueingeben eines Passworts
bei jedem Zugriff mag sicherer sein, aber eben kaum benutzerfreundlich.
Daher muss bei der Erfüllung der Anforderungen eine Priorisierung erfolgen.
Im Zweifel wurde sich beim Entwurf von ``brig`` primär für die Usability entschieden.
Zwar kann ein sehr sicheres System den Nutzer beschützen, doch wird der
Nutzer es ungern einsetzen wollen, wenn es aufwendig zu bedienen ist.
Das heißt allerdings keineswegs dass ``brig`` »per Entwurf« unsicher
ist. Es wurde darauf geachtet, dass Sicherheitstechniken den
Benutzer möglichst wenig im Weg stehen und eher in den Hintergrund treten.
Rob Pike hat diesen
Punkt überspitzt, aber prägnant dargestellt:

> *Weak security that's easy to use will help more people than strong
> security that's hard to use. Door locks are a good example.*

--- Rob Pike ([@pike2001security] S.24)

Die unten stehenden Anforderungen sind teilweise an die Eigenschaften des
verteilten Dateisystems *Infinit* (beschrieben in [@quintard2012towards], siehe
S.39) angelehnt und an die Ausrichtung von ``brig`` angepasst worden.

## Anforderungen an die Integrität

**Entkopplung von Metadaten und Daten:** Statt einem zentralen Dienst, soll
``brig`` die Basis eines dezentralen Netzwerkes bilden. Dabei stellt jeder
Teilnehmer einen Knoten in diesem Netzwerk dar. Nutzer des Netzwerkes können
Dateien untereinander synchronisieren. Dabei muss nicht
zwangsweise die gesamte Datei übertragen werden, jeder Nutzer verwaltet
lediglich eine Liste der Metadaten der Dateien, die jeder Teilnehmer besitzt.
Durch die Entkopplung zwischen Metadaten und tatsächlichen Daten ist es
möglich bestimmte Dateien »on-demand« und für den Nutzer transparent zu
übertragen.

Der Hauptvorteil einer dezentralen Architektur ist die erhöhte
Ausfallsicherheit (kein *Single--Point--of--Failure*) und der Fakt, dass das
Netzwerk durch seine Nutzer entsteht und keine besondere Infrastruktur
benötigt. Stattdessen funktioniert ``brig`` als *Overlay--Netzwerk* (Siehe
[@peer2peer], S.8) über das Internet.

**Pinning:** Der Nutzer soll Kontrolle darüber haben, welche Dateien er lokal
auf seinem Rechner speichert und welche er von anderen Teilnehmern dynamisch
empfangen will. Dazu wird das Konzept des »Pinnings« und der »Quota«
eingeführt. Ein Nutzer kann eine Datei manuell *pinnen*, um sie auf seinem
lokalen Rechner zu behalten oder um ``brig`` anzuweisen sie aus dem Netzwerk zu holen und
lokal zwischenzulagern. Dateien, die ``brig`` explizit hinzugefügt wurden,
werden implizit mit einem *Pin* versehen. Die *Quota* hingegen beschreibt ein
Limit an Bytes, die lokal zwischengespeichert werden dürfen. Wird dies überschritten,
so werden Daten gelöscht, die keinen Pin haben.

Das manuelle Pinnen von Dateien ist insbesondere nützlich, wenn eine bestimmte
Datei zu einer Zeit ohne Internetzugang benötigt wird. Ein typisches Beispiel
wäre ein Zugpendler der ein Dokument auf dem Weg zur Arbeit
editieren möchte. Er kann dieses vorher *pinnen* um es lokal auf seinem Laptop
zwischenzulagern.

**Langlebigkeit:** Daten die ``brig`` anvertraut werden, müssen solange ohne
Veränderung und Datenverlust gespeichert werden bis kein Nutzer mehr
diese Datei benötigt.

Dabei ist zu beachten, dass diese Anforderung nur mit einer gewissen
Wahrscheinlichkeit erfüllt werden kann, da heutige Hardware nicht die
Integrität der Daten gewährleisten kann. So können beispielsweise Bitfehler[^BITROT]
bei der Verarbeitung im Hauptspeicher oder konventionelle
Festplatten mit beschädigten Platten die geschriebenen Daten verändern. Ist die
Datei nur einmal gespeichert worden, kann sie von Softwareseite aus nicht mehr
fehlerfrei hergestellt werden. Um diese Fehlerquelle zu verkleinern sollte eine
Möglichkeit zur redundanten Speicherung geschaffen werden, bei der eine
minimale Anzahl von Kopien einer Datei konfiguriert werden kann.

[^BITROT]: Auch als *Bitrot* bekannt, siehe <https://en.wikipedia.org/wiki/Data_degradation>

**Verfügbarkeit:** Alle Daten die ``brig`` verwaltet sollen stets erreichbar
sein und bleiben. In der Praxis ist dies natürlich nur möglich, wenn alle
Netzwerkteilnehmer ohne Unterbrechung zur Verfügung stehen oder wenn alle
Dateien lokal zwischengelagert worden sind.

Oft sind viele Nutzer zu unterschiedlichen Zeiten online oder leben in komplett
verschiedenen Zeitzonen. Aufgrund der Zeitverschiebung wäre eine Zusammenarbeit
zwischen einem chinesischen und einem deutschen Nutzer schwierig. Eine mögliche
Lösung wäre die Einrichtung eines automatisierten Knoten der ständig verfügbar
ist. Statt Dateien direkt miteinander zu teilen, könnten Nutzer diesen Knoten
als Zwischenlager benutzen.
Falls nötig, soll es also auch möglich sein den Vorteil eines zentralen
Ansatzes (also seine permanente Erreichbarkeit) mit ``brig`` zu kombinieren.

**Integrität:** Es muss sichergestellt werden, dass absichtliche oder
unabsichtliche Veränderungen an den Daten festgestellt werden können.

Unabsichtliche Änderungen können wie oben beschrieben beispielsweise durch
fehlerhafte Hardware geschehen. Absichtliche Änderungen können durch
Angriffe von außen passieren, bei denen gezielt Dateien von einem
Angreifer manipuliert werden. Als Beispiel könnte man an einen Schüler denken,
welcher unbemerkt seine Noten in der Datenbank seiner Schule manipulieren will.
Aus diesem Grund sollte das Dateiformat von ``brig`` mittels *Message Authentication
Codes* (MACs) sicherstellen können, dass die gespeicherten Daten den ursprünglichen
Daten entsprechen.

## Anforderungen an die Sicherheit

**Verschlüsselte Speicherung:** Die Daten sollten verschlüsselt auf der
Festplatte abgelegt werden und nur bei Bedarf wieder entschlüsselt werden.
Kryptografische Schlüssel sollten aus denselben Gründen nicht unverschlüsselt
auf der Platte, sondern nur im Hauptspeicher abgelegt werden.

Wie in [@sec:stand-der-technik] beleuchtet wurde, speichern die meisten Dienste und
Anwendungen zum Dateiaustausch ihre Dateien in keiner verschlüsselten Form. Es
gibt allerdings eine Reihe von Angriffsszenarien ([@cpiechula], Kapitel TODO), die
durch eine Vollverschlüsselung der Daten verhindert werden können.

**Verschlüsselte Übertragung:** Bei der Synchronisation zwischen Teilnehmern
sollte der gesamte Verkehr ebenfalls verschlüsselt erfolgen. Nicht nur die
Dateien selbst, sondern auch die dazugehörigen Metadaten sollen Ende--zu--Ende
verschlüsselt werden.

Die Verschlüsselung der Metadaten erscheint vor allem im Lichte der
Enthüllungen zur NSA--Affäre geboten[^snowdenWiki]. Eine Ende--zu--Ende
Verschlüsselung ist in diesem Fall vor allem deswegen wichtig, weil der
Datenverkehr unter Umständen auch über andere, ansonsten unbeteiligte, Knoten
im Netzwerk gehen kann.

[^snowdenWiki]: Siehe auch: <https://de.wikipedia.org/wiki/Globale_%C3%9Cberwachungs-_und_Spionageaff%C3%A4re>

**Authentifizierung:** ``brig`` sollte die Möglichkeit bieten zu überprüfen, ob
Synchronisationspartner wirklich diejenigen sind, die sie vorgeben zu sein.
Dabei muss zwischen der initialen Authentifizierung und der fortlaufenden
Authentifizierung unterschieden werden. Bei der initialen Authentifizierung
wird neben einigen Sicherheitsfragen ein Fingerprint des Kommunikationspartners
übertragen, welcher bei der fortlaufenden Authentifizierung auf Änderung
überprüft wird.

Mit welchen Partnern synchronisiert werden soll und wie vertrauenswürdig diese
sind kann ``brig`` nicht selbstständig ermessen. Man kann allerdings dem Nutzer
Hilfsmittel geben, um die Identität des Gegenüber zu überprüfen. So könnten
Werkzeuge angeboten werden, mithilfe deren der Nutzer dem potenziellen Partner
eine Frage (mit vordefinierter Antwort) schicken kann, die dieser dann
beantworten muss. Alternativ können sich beide Partner vorher auf einen
separaten Kanal auf ein gemeinsames Geheimnis einigen, welches dann über
``brig`` ausgetauscht und überprüft werden kann. Diese beiden Möglichkeiten
sind inspiriert von der OTR--Implementierung des Instant-Messanger Pidgin[^PIDGIN].

[^PIDGIN]: Webseite: <https://www.pidgin.im>

<!-- Die Nummer der Seite 23 ist komisch :D -->

**Identität:** Jeder Benutzer des Netzwerks muss eine öffentliche Identität
besitzen, welche ihn eindeutig identifiziert. Gekoppelt mit der öffentlichen
Identität soll jeder Nutzer ein überprüfbares Geheimnis kennen, mithilfe dessen er sich
gegenüber anderen authentifizieren kann. Zusätzlich dazu sollte es
einen menschenlesbaren Nutzernamen für jeden Teilnehmer geben.
Dieser sollte zur öffentlichen Identität des jeweiligen Nutzers auflösbar sein.
Eine Registrierung bei einer zentralen Stelle soll nicht benötigt werden.

**Transparenz:** Die Implementierung aller oben genannten Sicherheitsfeatures
muss für Anwender und Entwickler nachvollziehbar und verständlich sein. Durch
die Öffnung des gesamten Quelltextes können Entwickler den Code auf Fehler
überprüfen. Normale Anwender können die Arbeit von Herrn Piechula[@cpiechula]
lesen, um für die Themantik der Sicherheit sensibilisiert zu werden und ein
Überblick über die Sicherheit von ``brig`` zu bekommen. Dort wird auch das
Entwicklungsmodell besprochen, welches helfen soll sichere Software zu
entwickeln.

## Anforderungen an die Usability

*Anmerkung:* In [@sec:usability] werden weitere Anforderungen zur
Usability in Bezug auf eine grafische Oberfläche definiert. Da diese nicht
für die Gesamtheit der Software relevant sind, werden sie hier ausgelassen.

**Automatische Versionierung:** Die Dateien die ``brig`` verwaltet, sollen
automatisch versioniert werden. Die Versionierung soll dabei in Form von
*Checkpoints* bei jeder Dateiänderung erfolgen. Mehrere von Checkpoints
können manuell oder per *Timer* in einem zusammenhängenden *Commit*
zusammengefasst werden. Die Menge an Dateien die in alter Version vorhanden
sind, sollen durch eine Speicher-Quota geregelt werden, die nicht überschritten werden darf.
Wird dieses Limit überschritten, so werden die ältesten Dateien von der lokalen
Maschine gelöscht. Die jeweiligen Checkpoints sind aber noch  vorhanden und der
darin referenzierte Stand kann von anderen Teilnehmern aus dem Netzwerk geholt
werden, falls verfügbar.

Nutzer tendieren oft dazu mehrere Kopien einer Datei unter verschiedenen Orten
als Backup anzulegen. Leider artet dies erfahrungsgemäß in der Praxis oft dazu
aus, dass Dateinamen wie ``FINAL-rev2.pdf`` oder ``FINAL-rev7.comments.pdf``
entstehen. Daher wäre für viele Nutzer eine automatisierte und
robuste Versionierung wünschenswert.

**Portabilität:** ``brig`` sollte in möglichst portabler Weise implementiert
werden, um die zunehmende Fragmentierung des
Betriebssystemmarkts[@statistaFragOS] zu berücksichtigen. Dabei sollten neben
den populärsten Betriebssystemen wie Windows, Mac OSX und GNU/Linux auch auf lange
Sicht mobile Plattformen unterstützt werden.

**Einfache Installation:** ``brig`` sollte möglichst einfach und ohne
Vorkenntnisse installierbar sein. Zur Installation gehört dabei nicht nur die
Beschaffung der Software und deren eigentliche Installation, sondern auch die
initiale Konfiguration. Die Erfahrungen des Autors haben gezeigt, dass Nutzer
oft eine einfach zu installierende Software bevorzugen, obwohl eine schwerer zu
installierende Software, ihr Problem möglicherweise besser löst.

**Keine künstlichen Limitierungen:** Mit ``brig`` sollten die gleichen für den
Nutzer gewohnten Operationen und Limitierungen gelten, wie bei einem normalen
Dateisystem. Als Datei wird in diesem Kontext ein Datenstrom verstanden, der
unter einem bestimmten Pfad im Dateisystem ausgelesen oder beschrieben werden
kann. Ihm zugeordnet sind Metadaten, wie Größe, Änderungsdatum und
Zugriffsdatum. Dateien sollen kopiert, verschoben und gelöscht werden können.
Zudem sollten keine Limitierungen der Pfadlänge durch ``brig`` erfolgen, auch
keine bestimmte Enkodierung des Pfadnamens soll forciert werden. Ebenfalls soll
die Dateigröße nur durch das darunter liegende System begrenzt werden.

**Generalität:** Die Nutzung von Techniken die den Nutzerstamm auf bestimmte
Plattformen einschränkt oder den Kauf zusätzlicher, spezieller Hardware
benötigt ist nicht erlaubt. Beispielsweise der Einsatz von
plattformspezifischen Dateisystemen wie btrfs[^BTRFS] oder ZFS[^ZFS] zur
Speicherung  entfällt daher. Auch darf nicht vorausgesetzt werden, dass alle
Nutzer ``brig`` verwenden, da dies ein Lock--in wie bei anderen Produkten
bedeuten würde.

[^BTRFS]: Siehe auch: <https://de.wikipedia.org/wiki/Btrfs>
[^ZFS]: Siehe auch: <https://de.wikipedia.org/wiki/ZFS_(Dateisystem)>

Ein häufiger Anwendungsfall ist ein Nutzer, der ein bestimmtes Dokument seinen
Mitmenschen zu Verfügung stellen möchte. Optimalerweise müssen dabei die
Empfänger des Dokuments keine weitere Software installiert haben, sondern
können die Datei einfach mittels eines Hyperlinks in ihrem Browser
herunterladen. Zentrale Dienste können dies relativ einfach leisten, indem sie
einen Webservice anbieten, welcher die Datei von einer zentralen Stelle
herunterladbar macht. Ein dezentrales Netzwerk wie ``brig`` muss hingegen
*Gateways* anbieten, also eine handvoll Dienste, welche zwischen den »normalen
Internet« und dem ``brig``--Netzwerk vermitteln (siehe [@fig:gateway]). Die
Nutzer, welche die Dateien verteilen wollen, können ein solches Gateway selbst
betreiben oder können ein von Freiwilligen betriebenes Gateway benutzen.

![Schematischer Aufbau eines HTTPS--Gateway](images/7/gateway.pdf){#fig:gateway}

**Stabilität:** Die Software muss bei normaler Benutzung ohne Abstürze und
offensichtliche Fehler funktionieren. Eine umfangreiche Testsuite soll die
Fehlerquote der Software minimieren, quantisierbar machen und die
Weiterentwicklung erleichtern. Spätestens nach der Veröffentlichung der Software,
sollten auch Regressionstests[^REGRESSION] das erneute Auftreten von bereits reparierten
Fehlern vermeiden.

[^REGRESSION]: Siehe auch: <https://de.wikipedia.org/wiki/Regressionstest>

**Effizienz:** Die Geschwindigkeit der Software auf durchschnittlicher Hardware
(siehe [@sec:assumptions]) soll schnell genug sein, um den Anwender ein flüssiges
Arbeiten ermöglichen zu können. Die Geschwindigkeit sollte durch eine
Benchmarksuite messbar gemacht werden und bei jedem neuen Release mit dem
Vorgänger verglichen werden.
