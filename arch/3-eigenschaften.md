# Anforderungen {#sec:eigenschaften}

In diesem Kapitel werden aus dem Stand der Technik die Anforderungen und
Eigenschaften abgeleitet, die ein modernes Dateisynchronisationssystem haben
sollte. Im Zuge dessen werden die Grundlagen erklärt,
die zum Verständnis der folgenden Kapitel notwendig sind.

XXX: passt noch?

## Anforderungen an ``brig`` {#sec:requirements}

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

### Anforderungen die Integrität

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

[^BITROT]: Auch *Bitrot* genannt, siehe <https://en.wikipedia.org/wiki/Data_degradation>

**Verfügbarkeit:** Alle Daten die ``brig`` verwaltet sollen stets erreichbar
sein und bleiben. In der Praxis ist dies natürlich nur möglich, wenn alle
Netzwerkteilnehmer ohne Unterbrechung zur Verfügung stehen oder wenn alle
Dateien lokal zwischengelagert worden sind.

Oft sind viele Nutzer zu unterschiedlichen Zeiten online oder
zu komplett verschiedenen Zeiten. Aufgrund der Zeitverschiebung wäre eine
Zusammenarbeit zwischen einem chinesischen und einem deutschen Nutzer
schwierig. Eine mögliche Lösung wäre die Einrichtung eines automatisierten Knoten
der ständig verfügbar ist. Statt Dateien direkt miteinander zu teilen, könnten Nutzer
diesen Knoten als Zwischenlager benutzen.

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

### Anforderungen an die Sicherheit

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

### Anforderungen an die Usability

*Anmerkung:* In [@sec:usability] werden weitere Anforderungen zur
Usability in Bezug auf eine grafische Oberfläche definiert. Da diese nicht
für die Gesamtheit der Software relevant sind, werden sie hier ausgelassen.

**Automatische Versionierung:** Die Dateien die ``brig`` verwaltet, sollen
automatisch versioniert werden. Die Versionierung soll dabei in Form von
*Checkpoints* bei jeder Dateiänderung erfolgen. Mehrere von Checkpoints
können manuell oder per *Timer* in einem zusammenhängenden *Commit*
zusammengefasst werden. Die Menge an Dateien die in alter Version vorhanden
sollen durch eine Speicher-Quota geregelt, die nicht überschritten werden darf.
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
verständlicherweise oft eine einfach zu installierende Software einer
schwer zu installierenden Software bevorzugen, die aber möglicherweise ihr
Problem besser löst.

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
können die Datei einfach mittels eines Hyperlinks in ihrem Browser herunterladen. Zentrale
Dienste können dies relativ einfach leisten, indem sie einen Webservice
anbieten, welcher die Datei von einer zentralen Stelle herunterladbar macht.
Ein dezentrales Netzwerk wie ``brig`` muss hingegen *Gateways* anbieten, also
eine handvoll Dienste, welche zwischen den »normalen Internet« und dem
``brig``--Netzwerk vermitteln. Die Nutzer, welche die Dateien verteilen wollen,
können ein solches Gateway selbst betreiben. Alternativ können sie die
entsprechende Datei mit einem öffentlichen Gateway teilen, welches von
Freiwilligen betrieben wird.

XXX: Gateway grafik hierhin verschieben.

**Stabilität:** Die Software muss bei normaler Benutzung ohne Abstürze und
offensichtliche Fehler funktionieren. Eine umfangreiche Testsuite soll die
Fehlerquote der Software minimieren, quantisierbar machen und die
Weiterentwicklung erleichtern. Spätestens nach der Veröffentlichung der Software,
sollten auch Regressionstests[^REGRESSION] das erneute Auftreten von bereits reparierten
Fehlern vermeiden.

[^REGRESSION]: Siehe auch: <https://de.wikipedia.org/wiki/Regressionstest>

**Effizienz:** Die Geschwindigkeit der Software auf durchschnittlicher Hardware
(siehe [@sec:assumptions]) schnell genug sein, um den Anwender ein flüssiges
Arbeiten ermöglichen zu können. Die Geschwindigkeit sollte durch eine
Benchmarksuite messbar gemacht werden und bei jedem neuen Release mit dem
Vorgänger verglichen werden.

## ``ipfs``: Das *Interplanetary Filesystem*

Anstatt das Rad neu zu erfinden, setzt ``brig`` auf das relativ junge
*Interplanetary Filesystem* (kurz ``ipfs``), welches von Juan Benet und seinen
Mitentwicklern unter der MIT--Lizenz in der Programmiersprache Go entwickelt
wird (siehe auch das Whitepaper[@benet2014ipfs]). Im Gegensatz zu den meisten
anderen verfügbaren Peer--to-Peer Netzwerken kann ``ipfs`` als
Software--Bibliothek genutzt werden. Dies ermöglicht es ``brig`` als,
vergleichsweise dünne Schicht, zwischen Benutzer und ``ipfs`` zu fungieren (wie in [@fig:fuse-brig-ipfs] dargestellt).

![Zusammenhang zwischen ``ipfs``, ``brig`` und FUSE.](images/3/fuse-brig-ipfs.pdf){#fig:fuse-brig-ipfs width=30%}

``ipfs`` stellt dabei ein *Content Addressed Network* (kurz *CAN*, [^CAN]) dar.
Dabei wird eine Datei, die in das Netzwerk gelegt wird nicht mittels eines
Dateinamen angesprochen, sondern mittels einer Prüfsumme, die durch eine vorher
festgelegte Hashfunktion berechnet wird. Andere Teilnehmer im Netzwerk können
mittels dieser Prüfsumme die Datei lokalisieren und empfangen. Anders als bei
einer HTTP--URL (*Unified Resource Locator*) steckt der Prüfsumme einer Datei
also nicht nur die Lokation der Datei, sondern sie dient auch
als eindeutiges Identifikationsmerkmal (ähnlich eines Pfads) und gleicht daher
eher einem Magnet Link[^MAGNET_LINK] als einer URL. Vereinfacht gesagt ist es
nun die Hauptaufgabe von ``brig`` dem Nutzer die gewohnte Abstraktionsschicht
eines Dateisystem zu geben, während im Hintergrund jede Datei zu einer
Prüfsumme aufgelöst wird.

[^MAGNET_LINK]: Mehr Informationen unter <https://de.wikipedia.org/wiki/Magnet-Link>

Im Vergleich zu zentralen Ansätzen (bei dem der zentrale Server einen *Single
Point of Failure* darstellt) können Dateien intelligent geroutet werden und
müssen nicht physikalisch auf allen Geräten verfügbar sein. Wird beispielsweise
ein großes Festplattenimage (~8GB) in einem Vorlesungssaal von jedem Teilnehmer
heruntergeladen, so muss bei zentralen Diensten die Datei mehrmals über das
vermutlich bereits ausgelastete Netzwerk der Hochschule gezogen werden. In einem
*CAN*, kann die Datei in Blöcke unterteilt werden, die von jedem Teilnehmer
gleich wieder verteilt werden können, sobald sie heruntergeladen wurden. Der
Nutzer sieht dabei ganz normal die gesamte Datei, ``brig``, beziehungsweise das *CAN* erledigt
dabei das Routing transparent im Hintergrund.

Technisch basiert ``ipfs`` auf der verteilten Hashtabelle
*Kademlia*[@maymounkov2002kademlia], welches mit den Erkenntnissen aus den
Arbeiten *CoralDHST*[@freedman2004democratizing] (Ansatz um das Routing zu
optimieren) und *S/Kademlia*[@baumgart2007s] (Ansatz um das Netzwerk gegen
Angriffe zu schützen) erweitert und abgesichert wurde. *S/Kademlia* verlangt
dabei, dass jeder Knoten im Netzwerk über ein Schlüsselpaar, bestehend aus
einem öffentlichen und privaten Schlüssel verfügt. Die Prüfsumme des
öffentlichen Schlüssels dient dabei als einzigartige Identifikation des Knotens
und der private Schlüssel dient als Geheimnis mit dem ein Knoten seine
Identität nachweisen kann. Diese Kernfunktionalitäten sind bei ``ipfs`` in
einer separaten Bibliothek namens ``libp2p``[^LIBP2P] untergebracht, welche
auch von anderen Programmen genutzt werden können.

[^CAN]: Siehe auch: <https://en.wikipedia.org/wiki/Content_addressable_network> 
[^LIBP2P]: Mehr Informationen in der Dokumentation unter: <https://github.com/ipfs/specs/tree/master/libp2p>

### Eigenschaften des *Interplanetary Filesystems* {#sec:ipfs-attrs}

Im Folgenden werden die Eigenschaften von ``ipfs`` kurz vorgestellt, welche von
``brig`` genutzt werden. Einige interessante Features wie beispielsweise das
*Interplanetary Naming System* (IPNS) werden dabei ausgelassen, da sie für
``brig`` aktuelle keine praktische Bedeutung haben.

**Weltweites Netzwerk:** Standardmäßig bilden alle ``ipfs``--Knoten ein
zusammenhängendes, weltweites Netzwerk.
``ipfs`` verbindet sich beim Start mit
einigen, wohlbekannten *Bootstrap--Nodes*, deren
Adressen mit der Software mitgeliefert werden. Diese können dann wiederum den
neuen Knoten an ihnen bekannte, passendere Knoten vermitteln. Die Menge der so
entstandenen verbundenen Knoten nennt ``ipfs`` den *Swarm* (dt. Schwarm). Ein
Nachbarknoten wird auch *Peer* genannt.

Falls gewünscht, kann allerdings auch ein abgeschottetes Subnetz erstellt
werden. Dazu ist es lediglich nötig, die *Bootstrap*--Nodes durch Knoten
auszutauschen, die man selbst kontrolliert. Unternehmen könnten diesen Ansatz
wählen, falls ihr Netzwerk komplett von der Außenwelt abgeschottet sein soll. Wie in
[@sec:architektur] beleuchtet wird, ist eine Abschottung des Netzwerks
rein aus Sicherheitsgründen nicht zwingend nötig.

**Operation mit Prüfsummen:** ``ipfs`` arbeitet nicht mit herkömmlichen Dateipfaden,
sondern nur mit der Prüfsumme einer Datei. Im folgenden Beispiel
wird eine Fotodatei mittels der ``ipfs``--Kommandozeile in das Netzwerk
gelegt[^IPFS_DAEMON]:

```bash
$ ipfs add my-photo.png
QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG
```

Wird eine Datei modifiziert, so muss sie neu mittels ``ipfs add`` hinzugefügt
werden und wird in dieser Version unter einer anderen Prüfsumme erreichbar
sein. Im Gegensatz zu normalen Dateisystemen kann es keinen allgemeinen
Einstiegspunkt (wie das Wurzelverzeichnis ``/``) geben. Die Prüfsumme eines
Verzeichnisses definiert sich in ``ipfs`` durch die Prüfsummen seiner Inhalte.
Das Wurzelverzeichnis hätte also nach jeder Modifikation eine andere Prüfsumme.

``ipfs`` nutzt dabei ein spezielles Format um Prüfsummen zu
repräsentieren[^IPFS_HASH]. Die ersten zwei Bytes einer Prüfsumme
repräsentieren dabei den verwendeten Algorithmus und die Länge der darauf
folgenden, eigentlichen Prüfsumme. Die entstandene Byte--Sequenz wird dann
mittels ``base58``[^BASE58] enkodiert, um sie menschenlesbar zu machen. Da der momentane
Standardalgorithmus ``sha256`` ist, beginnt eine von ``ipfs`` generierte
Prüfsumme stets mit »``Qm``«. Abbildung [@fig:ipfs-hash-format] zeigt dafür ein
Beispiel.

![Layout der ``ipfs`` Prüfsumme](images/2/ipfs-hash-layout.pdf){#fig:ipfs-hash-format}


[^BASE58]: <https://de.wikipedia.org/wiki/Base58>

[^IPFS_DAEMON]: Voraussetzung hierfür ist allerdings, dass der ``ipfs``--Daemon
vorher gestartet wurde und ein Repository mittels ``ipfs init`` erzeugt wurde.

[^IPFS_HASH]: Mehr Informationen unter: <https://github.com/multiformats/multihash>

Auf einem anderen Computer, mit laufenden ``ipfs``--Daemon, ist das Empfangen
der Datei möglich, indem die Prüfsumme an das Kommando ``ipfs cat`` gegeben wird. Dabei wird für
den Nutzer transparent über die DHT ein Peer ausfindig gemacht, der die Datei
anbieten kann und der Inhalt von diesem bezogen:

```bash
$ ipfs cat QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG > my-photo.png
```

**Public--Key Infrastructure:** Jeder Knoten im ``ipfs``--Netzwerk besitzt ein
RSA--Schlüsselpaar, welches beim Anlegen des Repositories erzeugt wird. Mittels
einer Prüfsumme  wird aus dem öffentlichen Schlüssel eine Identität berechnet
($ID = H_{sha256}(K_{Public})$). Diese kann dann dazu genutzt werden einen Knoten
eindeutig zu identifizieren und andere Nutzer im Netzwerk nachzuschlagen und
deren öffentlichen Schlüssel zu empfangen:

```bash
# Nachschlagen des öffentlichen Schlüssels eines zufälligen Bootstrap-Nodes:
$ ipfs id QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ
{
  "ID": "QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ",
  "PublicKey": "CAASpgIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK[...]",
  ...
}
```

Der öffentliche Schlüssel kann dazu genutzt werden, mit einem Peer mittels
asymmetrischer Verschlüsselung eine verschlüsselte Verbindung aufzubauen (siehe
[@cpiechula], Kapitel TODO). Von ``brig`` wird dieses Konzept weiterhin
genutzt, um eine Liste vertrauenswürdiger Knoten zu verwalten. Jeder Peer muss
bei Verbindungsaufbau nachweisen, dass er den zum öffentlichen Schlüssel passenden
privaten Schlüssel besitzt (für Details siehe [@cpiechula], Kapitel TODO).

**Pinning und Caching:** Das Konzept von ``ipfs`` basiert darauf, dass Knoten nur
das speichern, worin sie auch interessiert sind. Daten, die von außen zum
eigenen Knoten übertragen worden sind werden nur kurzfristig zwischengelagert.
Nach einiger Zeit bereinigt der eingebaute Garbage--Collector die Daten im
*Cache*.[^IPFS_MANUAL_GC]

Werden Daten allerdings über den Knoten selbst hinzugefügt, so bekommen sie
automatisch einen *Pin* (dt. Stecknadel). *Gepinnte* Daten werden automatisch
vom *Garbage-Collector* ignoriert und beliebig lange vorgehalten, bis sie
wieder *unpinned* werden. Möchte ein Nutzer sicher sein, dass die Datei im
lokalen Speicher bleibt, so kann er sie manuell pinnen:

```bash
$ ipfs pin add QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG
```

Wenn die Dateien nicht mehr lokal benötigt werden, können sie *unpinned* werden:

```bash
$ ipfs pin rm QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG
```

[^IPFS_MANUAL_GC]: Der Garbage--Collector kann auch manuell mittels ``ipfs repo gc`` von der Kommandozeile aufgerufen werden.

**Flexibler Netzwerkstack:** Einer der größten Vorteile von ``ipfs`` ist, dass es
auch über NAT--Grenzen hinweg funktioniert. 
XXX: Schauen ob das noch passt.
Um die Garantien, die *TCP*
bezüglich der Paketzustellung gibt, zu erhalten nutzt ``ipfs`` das
Anwendungs--Protokoll *UDT*. Insgesamt implementiert ``ipfs`` also einige
Techniken, um, im Gegensatz zu den meisten theoretischen Ansätzen, eine leichte
Usability zu gewährleisten. Speziell wäre hier zu vermeiden, dass ein
Anwender die Einstellungen seines Routers ändern muss, um ``brig`` zu nutzen.

[^UDT]: http://udt.sourceforge.net/

In Einzelfällen kann es natürlich trotzdem dazu kommen, dass die von ``ipfs``
verwendeten Ports durch eine besonders in Unternehmen übliche Firewall
blockiert werden. Dies kann nötigenfalls aber vom zuständigen Administrator
geändert werden.

**Übermittlung zwischen Internet und ``ipfs``:** Ein Client/Server--Betrieb
lässt sich mithilfe der ``ipfs``--*Gateways* emulieren. Gateways sind
zentrale, wohlbekannte Dienste, die zwischen dem »normalen Internet« und dem
``ipfs`` Netzwerk mittels HTTP vermitteln. Die Datei ``my-photo.png`` aus dem
obigen Beispiel kann von anderen Nutzern bequem über den Browser
heruntergeladen werden:

```bash
$ export PHOTO_HASH=QmPtoEEMMnbTSmzr28UEJFvmsD2dW88nbbCyyTrQgA9JR9
$ curl https://gateway.ipfs.io/ipfs/$PHOTO_HASH > my-photo.png
```

Auf dem Gateway läuft dabei ein Webserver, der intern dasselbe tut wie ``ipfs cat``,
aber statt auf der Kommandozeile die Daten auf eine HTTP--Verbindung ausgibt.
Standardmäßig wird bei jedem Aufruf von ``ipfs daemon`` ein Gateway auf der
Adresse <http://localhost:8080> gestartet.
