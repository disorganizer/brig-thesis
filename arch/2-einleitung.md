# Einleitung {#sec:einleitung}

In diesem Kapitel werden das Projektziel definiert und die  Anforderungen an
eine moderne Dateisynchronisationslösung festgelegt.

## Projektziel

Ziel des Projektes ist die Entwicklung einer sicheren und dezentralen
Alternative zu Cloud--Storage Lösungen wie Dropbox, die sowohl für Unternehmen,
als auch für Heimanwender nutzbar ist. Trotz der Prämisse, einfache Nutzbarkeit
zu gewährleisten, wird auf Sicherheit sehr großen Wert gelegt.  Aus Gründen der
Transparenz wird die Software dabei quelloffen unter der »``AGPLv3``« Lizenz
entwickelt.

Nutzbar soll das resultierende Produkt, neben dem Standardanwendungsfall der
Dateisynchronisation, auch als Backup- bzw. Archivierungs--Lösung sein. Des
Weiteren kann es auch als verschlüsselter Daten--Safe oder als Plattform für
andere, verteilte Anwendungen dienen -- wie beispielsweise aus dem Industrie 4.0
Umfeld.

Als weiteres Abgrenzungsmerkmal setzt ``brig`` nicht auf möglichst hohe
Effizienz (wie es typischerweise verteilte Dateisysteme tun) sondern versucht
möglichst generell anwendbar sein und über Netzwerkgrenzen hinweg funktioneren.
Dadurch soll es zu einer Art »Standard« werden, auf denen sich möglichst viele
Anwender einigen können.

Um ein Eindruck von ``brig`` und seinen (angestrebten) Fähigkeiten in der
Praxis zu bekommen, ist die Lektüre des *Benutzerhandbuch* in
[@sec:benutzerhandbuch] empfohlen.

## Eigenschaften und Anforderungen

Im Folgenden werden auf die Anforderungen eingegangen, welche ``brig`` erfüllen soll.
Die Anforderungen lassen sich in drei grobe Kategorien unterteilen:

- **Anforderungen an die Integrität:** ``brig`` muss die Daten die es speichert
  versionieren, auf Integrität prüfen können und korrekt wiedergeben können.
- **Anforderungen an die Sicherheit:** Alle Daten die ``brig`` anvertraut werden,
  sollten sowohl bei der Speicherung "auf der Festplatte" als auch bei der
  Übertragung zwischen Partnern verschlüsselt werden. Die Implementierung
  der Sicherheitstechniken sollte transparent von Nutzern und Experten
  nachvollzogen werden können.
- **Anforderungen an die Benutzbarkeit:** Die Software soll möglichst einfach zu
  nutzen und zu installieren sein. Der Nutzer soll ``brig`` auf den populärsten
  Betriebssystemen nutzen können und auch Daten mit Nutzern anderer
  Betriebssysteme austauschen können.

Die Kategorien beinhalten einzelne, konkretere Anforderungen, die im Folgenden
aufgelistet und erklärt werden. Dabei wird jeweils im ersten Paragraphen die
eigentliche Anforderung formuliert und danach beispielhaft erklärt.
Ob und wie die Anforderung letztlich erfüllt wurde, wird in [@sec:evaluation]
betrachtet.

Nicht jede Anforderung kann dabei voll umgesetzt werden. Teils überschneiden
oder widersprechen sich Anforderungen an die Sicherheit und an die Effizienz,
da beispielsweise verschlüsselte Speicherung mit effizienter Dekodierung
kollidiert. Auch ist hohe Benutzbarkeit bei gleichzeitig hohen
Sicherheitsanforderungen schwierig umzusetzen. Das Neueingeben eines Passworts
bei jedem Zugriff mag sicherer sein, aber eben leider kaum benutzerfreundlich.
Die Anforderungen werden daher nach dieser Faustregel in [@eq:faustregel] priorisiert:

$$Benutzbarkeit \ge Sicherheit \geq Effizienz$$ {#eq:faustregel}

Im Zweifel wurde sich also beim Entwurf also für die Benutzbarkeit entschieden,
da ein sehr sicheres System zwar den Nutzer beschützen kann, er wird es aber
ungern nutzen wollen und eventuell dazu tendieren um ``brig`` herum zu arbeiten.
Das heißt allerdings keineswegs dass ``brig`` »per Entwurf« unsicher ist.
Es wurden lediglich auf zu invasive Sicherheitstechniken verzichtet, welche den
Nutzer stören könnten. Oder um Rob Pike[@pike2001security, S.24] zu zitieren:

```
	Weak security that's easy to use will help more people than strong
	security that's hard to use. Door locks are a good example.
```

Bei Fragen zwischen Effizienz und Sicherheit wird allerdings eher zugunsten der
Sicherheit entschieden. Man könnte hier argumentieren, dass die Effizienz durch
bessere Hardware von alleine steigt, die Sicherheit hingegen nicht.
(TODO: srsly?)

Die unten stehenden Anforderungen sind teilweise an die Eigenschaften des
verteilten Dateisystems *Infinit* (beschrieben in [@quintard2012towards], siehe
S.39) angelehnt und an die Ausrichtung von ``brig`` angepasst wurden.

### Anforderungen die Integrität

**Entkopplung von Metadaten und Daten:** Statt einem zentralen Dienst, soll
``brig`` die Basis eines dezentralen Netzwerkes bilden. Dabei stellt jeder
Teilnehmer einen Knoten in diesem Netzwerk dar. Nutzer des Netzwerkes können
Dateien zwischen verschiedenen Teilnehmern synchronisieren. Dabei muss nicht
zwangsweise die gesamte Datei übertragen werden, jeder Nutzer verwaltet
lediglich eine Liste der Metadaten der Dateien, die jeder Teilnehmer besitzt.
Durch die Entkopplung zwischen Metadaten und tatsächlichen Metadaten ist es
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
lokalen Rechner zu behalten oder um ``brig`` anzuweisen sie aus dem Netzwerk
lokal zwischenzulagern. Dateien, die der Nutzer ``brig`` hinzugefügt hat,
werden implizit mit einem *Pin* versehen. Die *Quota* hingegen beschreibt ein
Limit an Bytes, die lokal zwischengespeichert werden dürfen. Dabei gibt es ein
hartes und ein weiches Limit. Wird das weiche Limit erreicht oder übertreten,
so dürfen keine weiteren Dateien automatisch von ``brig`` gepinnt werden. Nach
Erreichen des harten Limits funktioniert auch das manuelle Pinnen durch den
Benutzer nicht mehr.

Das manuelle Pinnen von Dateien ist insbesondere nützlich, wenn eine bestimmte Datei
zu einer Zeit ohne Internetzugang benötigt wird. Ein typisches Beispiel wäre ein Zug--Pendler
der ein Spreadsheet--Dokument auf dem Weg zur Arbeit editieren möchte. Er kann dieses vorher *pinnen*
um es lokal auf seinem Laptop zwischenzulagern.

**Langlebigkeit:** Daten die ``brig`` anvertraut werden, müssen solange ohne
Veränderung und Datenverlust gespeichert werden bis kein Nutzer mehr
diese Datei benötigt.

Dabei ist zu beachten, dass diese Anforderung nur mit einer gewissen
Wahrscheinlichkeit erfüllt werden kann, da heutige Hardware nicht die Integrität
der Daten gewährleisten kann. So können beispielsweise Bitfehler bei der
Verarbeitung im Hauptspeicher, SSDs die Strahlung ausgesetzt sind oder
konventionelle Festplatten mit beschädigten Platten die geschriebenen Daten
verändern. Ist die Datei nur einmal gespeichert worden, kann sie von
Softwareseite aus nicht mehr fehlerfrei hergestellt werden.
Um diese Fehlerquelle zu verkleinern sollte eine Möglichkeit zur redundanten
Speicherung geschaffen werden, bei der eine minimale Anzahl von Kopien einer
Datei konfiguriert werden kann.

**Verfügbarkeit:** Alle Daten die ``brig`` verwaltet sollen stets erreichbar
sein und bleiben. In der Praxis ist dies natürlich nur möglich, wenn alle
Netzwerkteilnehmer ohne Unterbrechung zur Verfügung stehen oder wenn alle
Dateien lokal zwischengelagert worden sind.

In der Praxis sind viele Nutzer zu unterschiedlichen Zeiten online oder
zu komplett verschiedenen Zeiten. Aufgrund der Zeitverschiebung wäre eine
Zusammenarbeit zwischen einem chinesischen Nutzer und einem deutschen Nutzer
schwierig. Eine mögliche Lösung wäre die Einrichtung eines automatsierten Knoten
der ständig verfügbar ist. Statt Dateien direkt miteinander zu teilen, könnte Nutzer
diesen Knoten als Zwischenlager benutzen, wie in [@fig:temp-datahold]

![Temporäre Datenhalde](images/temp-datahold.png){#fig:temp-datahold width=50%}

**Integrität:** Es muss sichergestellt werden, dass absichtliche oder
unabsichtliche Veränderungen an den Daten festgestellt werden können.

Unabsichtliche Änderungen können wie oben beschrieben beispielsweise durch
fehlerhafte Hardware geschehen. Absichtliche Änderungen können durch
Angriffe von außen passieren, bei denen gezielt Dateien gezielt von einem
Angreifer manipuliert werden. Als Beispiel könnte man an einen Schüler denken,
welcher unbemerkt seine Noten in der Datenbank seiner Schule manipulieren will.

Aus diesem Grund sollte das Dateiformat von ``brig`` mittels *Message Authentication
Codes* (MACs) sicherstellen können, dass die gespeicherten Daten denen
entsprechen, welche ursprünglich hinzugefügt worden sind.

### Anforderungen an die Sicherheit

**Verschlüsselte Speicherung:** Die Daten sollten verschlüsselt auf der
Festplatte abgelegt werden und nur bei Bedarf wieder entschlüsselt werden.
Kryptografische Schlüssel sollten aus denselben Gründen nicht unverschlüsselt
auf der Platte abgelegt werden und sonst nur im Hauptspeicher abgelegt werden.

Wie in [@sec:stand-der-technik] beleuchtet wird, speichern die meisten Dienste und
Anwendungen zum Dateiaustausch ihre Dateien in keiner verschlüsselten Form. Es
gibt allerdings eine Reihe von Angriffsszenarien (TODO: ref kitteh arbeit), die
durch eine Vollverschlüsselung der Daten verhindert werden können.

**Verschlüsselte Übertragung:** Bei der Synchronisation zwischen Teilnehmern
sollte der gesamte Verkehr ebenfalls verschlüsselt erfolgen. Nicht nur die
Dateien selbst, sondern auch die dazugehörigen Metadaten sollen Ende--zu--Ende
verschlüsselt werden.

Die Verschlüsselung der Metadaten erscheint vor allen im Lichte der
Enthüllungen zur NSA--Affäre geboten[@snowdenWiki]. Eine Ende--zu--Ende
Verschlüsselung ist in diesem Fall vor allem deswegen wichtig, weil der
Datenverkehr unter Umständen auch über andere, ansonsten unbeteiligte, Knoten
im Netzwerk gehen kann.

**Authentifizierung:** ``brig`` sollte die Möglichkeit bieten zu überprüfen, ob
Synchronisationspartner wirklich diejenigen sind die sie vorgeben zu sein.
Dabei muss zwischen der initialen Authentifizierung und der fortlaufenden
Authentifizierung unterschieden werden. Bei der initialen Authentifizierung
wird neben einigen Sicherheitsfragen ein Fingerprint des Kommunikationspartners
übertragen, welcher bei der fortlaufenden Authentifizierung auf Änderung
überprüft wird.

Mit welchen Partnern synchronisiert werden soll und wie vertrauenswürdig diese
sind kann ``brig`` nicht selbstständig ermessen. Es kann allerdings dem Nutzer
Hilfsmitteln geben, um die Identität des Gegenübers zu überprüfen. So könnten
Werkzeuge angeboten werden, mithilfe dessen der Nutzer dem potenziellen Partner
eine Frage (mit vordefinierter Antwort) schicken können, die dieser dann
beantworten muss. Alternativ können sich beide Partner vorher auf einen
separaten Kanal auf ein gemeinsames Geheimnis einigen, welches dann über
``brig`` ausgetauscht und überprüft werden kann. Diese beiden Möglichkeiten
sind inspiriert von der OTR Implementierung des Instant-Messangers Pidgin. Eine
modernere Variante wäre die Generierung eines QR--Codes aus der geheimen
Identität beider Partner. Diese könnten beide Partner dann beispielsweise über
ihr Smartphone scannen, austauschen und manuell vergleichen.

**Identität:** Jeder Benutzer des Netzwerks muss eine öffentliche Identität besitzen welche ihn eindeutig
kennzeichnet. Gekoppelt mit der öffentlichen Identität soll jeder Nutzer ein Geheimnis kennen, mithilfe
dessen er sich gegenüber anderen authentifizieren kann. Die öffentliche Identität soll menschenlesbar sein
und keine Registrierung an einer zentralen Stelle benötigen.

Eine mögliches Format für eine menschenlesbare Identität wäre eine abgeschwächte Form der Jabber--ID[^JID] (*JID*).
Diese hat, ähnlich wie eine E--Mail Adresse, die Form ``Nutzer@Domäne.tld/Ressource``.
Beim Jabber/XMPP Protokoll ist der Teil hinter dem ``/`` optional, der Rest ist zwingend erforderlich.
Als Abschwächung wird vorgeschlagen, auch den Teil hinter dem ``@`` optional zu machen.

Darüber hinaus sollen folgende Regeln gelten:

- Es sind keine Leerzeichen erlaubt.
- Ein leerer String ist nicht valide.
- Der String muss valides UTF8 (TODO: ref) sein.
- Der String muss der »UTF-8 Shortest Form[^SHORTEST]« entsprechen
- Der String darf durch die »UTF-8 NKFC Normalisierung[^NORMALIZATION]« nicht verändert werden.
- Alle Charaktere müssen druckbar und auf dem Bildschirm darstellbar sein.

Insbesondere die letzten vier Punkte dienen der Sicherheit, da ein Angreifer versuchen könnte
eine Unicode--Sequenz zu generieren, welche visuell genauso ausschaut wie die eines anderen Nutzers,
aber einer anderen Byte--Reihenfolge und somit einer anderen Identität entspricht.

[^SHORTEST]: Siehe auch: <http://unicode.org/versions/corrigendum1.html>
[^NORMALIZATION]: Siehe auch: <http://www.unicode.org/reports/tr15/\#Norm_Forms>

Valide Identitätsbezeichner wären also beispielsweise:

- ``alice``
- ``alice@company``
- ``alice@company.de``
- ``alice@company.de/laptop``
- ``böb@subdomain.company.de/desktop``

Dies hat aus unserer Sich folgende wesentlichen Vorteile:

- Eine E--Mail Adresse  oder eine JID ist gleichzeitig ein valider Identitätsbezeichner.
- Der Nutzer kann eine fast beliebige Unicode Sequenz als Name verwenden, was beispielsweise
  für Nutzer des kyrillischen Alphabetes nützlich ist.
- Unternehmen können die Identifikationsbezeichner hierarchisch gliedern. So kann *Alice* der
  Bezeichner ``alice@security.google.com`` zugewiesen werden, wenn sie im Sicherheitsteam arbeitet.
- Der *Ressourcen*--Teil hinter dem ``/`` ermöglicht die Nutzung desselben Nutzernamens auf verschiedenen Geräten,
  wie ``desktop`` oder ``laptop``.

[^JID]: Mehr Details unter: <https://de.wikipedia.org/wiki/Jabber_Identifier>

**Transparenz:** Die Implementierung aller oben genannten Sicherheitsfeatures
muss für Anwender und Entwickler nachvollziehbar und verständlich sein. Durch
die Öffnung des gesamten Quelltextes können Entwickler den Code auf Fehler
überprüfen. Normale Anwender können die Arbeit von Herrn Piechula lesen, um
einen Überblick über die Funktionsweise und Architektur der Sicherheitsfeatures
zu bekommen. Desweiteren wird auch die Weiterentwicklung der Software offen gehalten[^SECNOTE].

[^SECNOTE]: TODO: Sicherheitslücken sollten vertraulich gemeldet werden. (TODO: ref kitteh arbeit?)

### Anforderung an die Benutzbarkeit

*Anmerkung:* In [@sec:benutzbarkeit] werden weitere Anforderungen zur
Benutzbarkeit in Bezug auf eine grafische Oberfläche definiert. Da diese nicht
für die Gesamtheit der Software relevant sind, werden sie hier ausgelassen.

**Automatische Versionierung:** Die Dateien die ``brig`` verwaltet, sollen automatisch versioniert
werden. Die Versionierung soll dabei in Form von *Checkpoints* bei jeder Dateiänderung
erfolgen. Größere Mengen von Checkpoints können manuell oder per *Timer* in einem
zusammenhängenden *Commit* zusammengefasst werden. Die Menge an Dateien die in alter Version
vorhanden sind werden durch eine Speicher-Quota geregelt, die nicht überschritten wird.
Wird dieses Limit überschritten, so werden die ältesten Dateien von der lokalen Maschine
gelöscht. Die jeweiligen Checkpoints sind aber noch  vorhanden und der darin verwiesene
Stand kann von anderen Teilnehmern aus dem Netzwerk geholt werden, falls verfügbar.

Nutzer tendieren oft dazu mehrere Kopien einer Datei unter verschiedenen Orten als Backup
anzulegen. Leider artet dies erfahrungsgemäß in der Praxis oft dazu aus, dass Dateinamen
wie ``FINAL-rev2.pdf`` oder ``FINAL-rev7.comments.pdf`` entstehen (TODO: ref?). Daher wäre
für viele Nutzer eine automatisierte und robuste Versionierung wünschenswert. Auch wenn
ein Vorbild von ``brig`` das Versionsverwaltungssystem ``git`` ist, so kann es dessen
detaillierte und manuelle Herangehensweise an  die Versionierung nicht nachbilden.

**Portabilität:** ``brig`` sollte in möglichst portabler Weise implementiert werden, um
die zunehmende Fragmentierung des Betriebssystemmarkts zu berücksichtigen (TODO: ref
statistiken). Dabei sollten neben den populärsten Betriebssystemen wie Windows, Mac OSX
und Linux auch auf lange Sicht mobile Plattformen unterstützt werden.

Der in dieser Arbeit vorgestellte Prototyp wurde auf einem Linux--System entwickelt und
ist momentan nur unter unixoiden Betriebssystemen lauffähig.

**Einfache Installation:** ``brig`` sollte möglichst einfach und ohne Vorkenntnisse
installierbar sein. Zur Installation gehört dabei nicht nur die Beschaffung der Software
und deren Installation im System, sondern auch die initiale Konfiguration.

Die Erfahrungen des Autors haben gezeigt, dass Nutzer verständlicherweise oft eine einfache
zu installierende Software zur einer schwerer zu installierenden Software bevorzugen (die
aber möglicherweise ihr Problem besser löst).

**Keine künstlichen Limitierungen:** Mit ``brig`` sollten die gleichen für den
Nutzer gewohnten Operationen und Limitierungen gelten wie in einem normalen
Dateisystem. Als Datei verstehen wir in diesem Kontext ein Datenstrom, der
unter einem bestimmten Pfad im Dateisystem ausgelesen oder beschrieben werden
kann. Ihm zugeordnet sind Metadaten, wie Größe, Änderungsdatum und
Zugriffsdatum. Dateien sollen kopiert, verschoben und gelöscht werden können.
Zudem sollten keine Limitierungen der Pfadlänge durch ``brig`` erfolgen, auch
keine bestimmte Enkodierung des Pfadnamens soll forciert werden. Ebenfalls soll
die Dateigröße nur durch das darunter liegende System begrenzt werden.

**Generalität:** Keine Nutzung von Techniken die den Nutzerstamm auf bestimmte Plattformen
einschränken würde oder den Kauf zusätzlicherHardware bedingt. Der Einsatz von
plattformspezifischen Dateisystemen btrfs oder ZFS zur Speicherung oder die Annahme eines
bestimmten RAID--Verbundes entfällt daher. Auch darf nicht vorausgesetzt werden, dass
alle Nutzer ``brig`` verwenden, da dies ein Lock--in wie bei anderen Produkten bedeuten würde.

Ein häufiger Anwendungsfall ist ein Nutzer, der ein bestimmtes Dokument seinen Mitmenschen
zu Verfügung stellen möchte. Optimalerweise müssen dabei die Empfänger des Dokuments
keine weitere Software installiert haben, sondern können die Datei einfach als Hyperlink
in ihrem Browser herunterladen. Zentrale Dienste können dies relativ einfach leisten, indem
sie einen Webservice anbieten, welcher die Datei von einer zentralen Stelle herunterladbar macht.
Ein dezentrales Netzwerk wie ``brig`` muss hingegen »Gateways« anbieten, also eine handvoll
Dienste, welche zwischen den »normalen Internet« und dem ``brig``--Netzwerk vermitteln.
Die Nutzer, welche die Dateien verteilen wollen, können ein solches Gateway selbst betreiben.
Alternativ können sie die entsprechende Datei mit einem öffentlichen Gateway teilen, welches
von Freiwilligen betrieben wird. Solche öffentlichen Gateways wären die einzige
öffentlich getragene  Infrastruktur.

**Stabilität:** Die Software muss ohne Abstürze und offensichtliche Fehler
funktionieren. Eine umfangreiche Testsuite soll die Fehlerfreiheit der Software
beweisen, quantisierbar machen und die Weiterentwicklung erleichtern.

**Effizienz:** Die Geschwindigkeit der Software auf durchschnittlicher Hardware
schnell genug sein, um den Anwender ein flüssiges Arbeiten ermöglichen zu
können. Die Geschwindigkeit sollte durch eine Benchmarksuite messbar gemacht
werden und bei jedem neuen Release mit dem Vorgänger verglichen werden.


## Zielgruppen

Auch wenn ``brig`` extrem flexibel einsetzbar ist, sind die primären
Zielgruppen Unternehmen und Heimanwender.  Aufgrund der starken Ende-zu-Ende
Verschlüsselung ist ``brig`` allerdings auch insbesondre für Berufsgruppen
attraktiv, bei denen eine hohe Diskretion bezüglich Datenschutz gewahrt werden
muss. Hier wären in erster Linie Journalisten, Anwälte, Ärzte mit
Schweigepflicht auch Aktivisten und politisch verfolgte Minderheiten, zu
nennen.

Im Folgenden werden die verschiedenen Zielgruppen und Plattformen genauer
besprochen und wie diese von ``brig`` profitieren können.

### Unternehmen

Unternehmen können ``brig`` nutzen, um ihre Daten und Dokumente intern zu
verwalten. Besonders sicherheitskritische Dateien entgehen so der Lagerung in
Cloud--Services oder der Gefahr von Kopien auf unsicheren
Mitarbeiter--Endgeräten. Größere Unternehmen verwalten dabei meist ein
Rechenzentrum in dem firmeninterne Dokumente gespeichert werden. Von den
Nutzern werden diese dann meist mittels Diensten wie *ownCloud*[^NEXTCLOUD] oder *Samba*
»händisch« heruntergeladen.

[^NEXTCLOUD]: Siehe auch <https://owncloud.org}, bzw. dessen Fork *Nextcloud* <https://nextcloud.com>

In diesem Fall könnte man ``brig`` im Rechenzentrum und auf allen Endgeräten
installieren. Das Rechenzentrum würde die Datei mit tiefer Versionierung
vorhalten. Endanwender würden alle Daten sehen, aber auf ihrem Gerät nur die
Daten tatsächlich speichern, die sie auch benötigen. Hat beispielsweise ein
Kollege im selben Büro die Datei bereits vorliegen, kann ``brig`` diese dann
direkt transparent vom Endgerät des Kollegen holen. Das »intelligente Routing«
erlaubt den Einsatz von ``brig`` auf Smartphones, Tablets und anderen
speicherplatz-limitierten Geräten. Nutzer, die eine physikalische Kopie der Datei
auf ihrem Gerät haben wollen, können das entsprechende Dokument »pinnen«. Ist
ein Außendienstmitarbeiter beispielsweise im Zug unterwegs, kann er vorher eine
benötigtes Dokument pinnen, damit ``brig`` die Datei persistent verfügbar macht.

Indirekt sorgt auch die einfache Benutzbarkeit von ``brig`` für höhere
Sicherheit, da Mitarbeiter sich weniger durch die Sicherheitsrichtlinien ihres
Unternehmens gegängelt fühlen und nicht die Notwenigkeit sehen, wichtige
Dokumente auf private Geräte oder Speicher zu kopieren. Dies wirkt ebenfalls
Gefahren wie Industriespionage entgegen.

Da ``brig`` auch das Teilen von Dateien mittels Hyperlinks über ein »Gateway«
erlaubt, ist beispielsweise ein Kunde eines Ingenieurbüros nicht genötigt
``brig`` ebenso installieren zu müssen.


### Privatpersonen / Heimanwender

Heimanwender können ``brig`` für ihren Datenbestand aus Fotos, Filmen, Musik und
sonstigen Dokumenten nutzen. Ein typischer Anwendungsfall wäre dabei ein
NAS--Server, der alle Dateien mit niedriger Versionierung speichert. Endgeräte,
wie Laptops und Smartphones, würden dann ebenfalls ``brig`` nutzen, aber mit
deutlich geringeren Speicherquotas (maximales Speicherlimit), so dass nur die
aktuell benötigten Dateien physikalisch auf dem Gerät vorhanden sind. Die
anderen Dateien lagern »im Netz« und können transparent von ``brig`` von anderen
verfügbaren Knoten geholt werden.

### Plattform für industrielle Anwendungen

Da ``brig`` auch komplett automatisiert und ohne Interaktion nutzbar sein soll,
kann es auch als Plattform für jede andere Anwendung genutzt werden, die Dateien
sicher austauschen und synchronisieren müssen. Eine Anwendung in der Industrie 4.0
wäre beispielsweise die Synchronisierung von Konfigurationsdateien im gesamten Netzwerk.

### Einsatz im öffentlichen Bereich

Aufgrund der Ende-zu-Ende Verschlüsselung und einfachen Benutzbarkeit ist eine
Nutzung an Schulen, Universitäten sowie auch in Behörden zum Dokumentenaustausch
denkbar. Vorteilhaft wäre für die jeweiligen Institutionen hierbei vor allem,
dass man sich aufgrund des Open--Source Modells an keinen Hersteller bindet
(Stichwort: *Vendor Lock--In*) und keine behördlichen Daten in der »Cloud«
landen. Eine praktische Anwendung im universitären Bereich wäre die Verteilung
von Studienunterlagen an die Studenten. Mangels einer »Standardlösung« ist es
heutzutage schwierig Dokumente sicher mit Behörden auszutauschen. ``brig``
könnte hier einen »Standard« etablieren und in Zukunft als eine »Plattform«
dienen, um beispielsweise medizinische Unterlagen mit dem Hospital auszutauschen.

### Berufsgruppen mit hohen Sicherheitsanforderungen

Hier wären in erster Linie Berufsgruppen mit Schweigepflicht zu nennen wie Ärzte,
Notare und Anwälte aber auch Journalisten und politisch verfolgte Aktivisten.
Leider ist zum jetzigen Zeitpunkt keine zusätzliche Anonymisierung vorgesehen,
die es erlauben würde auch die Quelle der Daten unkenntlich zu machen. Dies
könnte allerdings später mit Hilfe des Tor Netzwerks (Tor Onion Routing Projekt)
realisiert werden.

## Einsatszenarien

Zusammengefasst soll ``brig`` also in folgenden Einsatszenarien praktikabel nutzbar sein:

**Synchronisationslösung:** Spiegelung von zwei oder mehr Ordnern und das
Teilen desselben zwischen ein oder mehreren Nutzern. Ein häufiger
Anwendungsfall ist dabei die Synchronisation zwischen mehreren Geräten eines
einzigen Nutzers. Eine selektive Synchronisation bestimmter Ordner ist vorerst
nicht vorgesehen.

**Transferlösung:** »Veröffentlichen« von Dateien nach Außen mittels *Gateways* über den Browser.
Eine beliebige Anzahl an bekannten und unbekannten Teilnehmern können die Datei herunterladen.

**Versionsverwaltung:** Alle Modifikationen an den bekannten Dateien werden aufgezeichnet.
Bis zu einer gewissen Mindestiefe können Dateien wiederhergestellt werden. Die Tiefe hängt
dabei von der *Quota* ab und ob andere Teilnehmer die Datei noch speichern.

**Backup- und Archivierungslösung:** Es ist möglich Knoten so zu konfigurieren, dass
(nach Möglichkeit) alle Dateien gepinned werden. Ein solcher Knoten kann dann
anderen Teilnehmern automatisch als Archiv für alte Dateien dienen.

**Verschlüsselter Safe:** Da alle Dateien verschlüsselt sind, müssen sie beim Start
der Software erst »aufgeschlossen« werden. Da die entschlüsselten Daten nur
im Hauptspeicher vorgehalten werden, ist nach Beenden der Software kein
Zugriff mehr möglich.

**Plattform:** Die momentane Implementierung ist als Werkzeugkasten für
Dateisynchronisation ausgelegt. Sofern keine Echtzeitbedingungen benötigt
werden, kann ``brig`` beispielsweise zum Synchronisieren von Log--Dateien im
Industrie--4.0 Umfeld oder zum Verteilen von Konfigurations--Dateien eingesetzt
werden.

Es gibt natürlich auch einige Einsattzzwecke, für die ``brig`` eher bis gar
nicht geeignet ist. Diese werden im [@sec:evaluation] beleuchtet, da die
dortige Argumentation teilweise ein Verständnis von der internen Architektur
benötigen.
