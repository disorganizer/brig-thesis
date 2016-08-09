# Stand der Technik {#sec:stand-der-technik}

In diesem Kapiteln wird ein kurzer Überblick über die wissenschaftlichen
Arbeiten und Begrifflichkeiten zum Thema Peer--to--Peer--Dateisysteme und
Dateisynchronisation gegeben. Im Anschluss werden einige der derzeit
verfügbaren und populären Softwarelösungen zur Dateisynchronisation untersucht.
Schließlich wird *IPFS* als Grundlage von ``brig`` vorgestellt und beleuchtet
warum es unserer Ansicht nach eine geeignete technische Basis bildet.

## Begrifflichkeiten

An dieser Stelle wird eine kurze Zusammenfassung der Begrifflichkeiten gegeben,
welche zum Verständnis der folgenden Kapitel notwendig sind.

(TODO: https://github.com/ipfs/specs/blob/master/libp2p/2-state-of-the-art.md irgendwo verlinken?)

### Einführung

Peer-to-Peer (kurz *P2P*) Netzwerke sind gut erforscht, aber bei weitem nicht
so weit verbreitet wie typische *Client/Server Architekturen*. Protokolle wie
Bittorrent (TODO: ref) fristen trotz ihrer Flexibilität eher ein Nischen-Dasein
beim Dateiaustausch. Das mag vor allem praktische Gründe haben: Die Teilnehmer
eines P2P--Netzwerks müssen etwas zum Netzwerk beitragen. Je nach Einsatzzweck
kann diese beizutragende Ressource Bandbreite, CPU--Zeit oder Ähnliches sein.
Außerdem passt das Client/Server Modell auf viele Anwendungszwecke, wie ein
Unternehmen das seinen Kunden einen Dienst oder eine Webseite anbietet. Zudem
haben solche 'wohl-bekannten' Dienste kein Problem mit NAT Traversal (TODO:
erklären).

Dabei skalieren Client/Server Anwendungen bei weitem schlechter als verteilte
Anwendungen. Man stelle sich einen Vorlesungssaal mit 50 Studenten vor, die ein
Festplattenimage (Größe 5 Gigabyte) aus dem Internet laden sollen. Bei einer
Client/Server Anwendung werden hier 50 Verbindungen zu einem Filehoster
geöffnet. Der Flaschenhals dabei ist in diesem Fall vermutlich das WLAN im
Saal, welches stark zusammenbrechen würde. Anders ist es wenn die Rechner der
Studenten ein verteiltes Netzwerk bilden. Hier genügt es wenn nur ein Rechner
einen Teil der Datei hat. Diesen Teil kann er im lokalen Netz anderen
Teilnehmern wieder anbieten und sich Teile der Datei besorgen, die er selbst
noch nicht hat. So muss in der Theorie die Datei nur maximal einmal über das
WLAN übertragen werden. In diesem etwas konstruierten Beispiel hätte man also
ein Speedupfaktor von ca. 50.

(TODO: veranschaulichungsgrafik)

### Aufbau eines P2P Netzwerks

Eine P2P--Netzwerk wird aus den Rechnern seiner Teilnehmer aufgebaut (oft
*Knoten* genannt). Bemerkenswert ist dabei, dass keine zentrale Instanz sich um
die Koordination des Datenflusses im Netzwerk kümmern muss. Die Grundlage für
die Koordination bildet dabei die *Distributed Hashtable* (dt. verteilte
Hashtabelle). Diese nutzt eine *Hashfunktion*, um für einen bestimmten
Datensatz zu entscheiden, welche Knoten (mindestens aber einer) im Netzwerk für
diesen Datensatz zuständig ist. Jeder Knoten verwaltet dabei einen bestimmten
Wertebereich der Hashfunktion und ist für diese Hashwerte zuständig. Werden
neue Knoten hinzugefügt oder andere verlassen das Netz, werden die Wertebereich
neu verteilt.

Werden ganze Dateien in das Netzwerk »gelegt«, so können diese je nach
Anwendung in kleine Teilblöcke aufgeteilt werden, für die jeweils unterschiedliche
Knoten zuständig sind. Wie die einzelnen Blöcke zusammenhängen, kann beispielsweise
in einer *Torrent*--Datei definiert sein.[^BITTORRENT]

[^BITTORRENT]: Anmerkung: Bei Bittorrent kümmert sich ein *Tracker* um das Auffinden von zuständigen Knoten.

### Dateisynchronisation in P2P-Netzwerken

Ein häufiges Problem bei Filesharing--Netzwerken wie *Bittorrent* ist, dass
viele Dateien nach einiger Zeit nicht mehr erreichbar sind, da es keine Knoten
mehr gibt, welche die Blöcke der Datei *seeden* (dt. sähen, also verteilen).
Auch ist es nur problematisch, wenn nur wenige Teilnehmer eine Block *seeden*,
während viele andere Teilnehmer den Block herunterladen wollen.[^LEECHER] Für
einen globale und dauerhafte Dateisynchronisation ist das
*Bittorrent*--Protokoll also nur bedingt geeignet.

Diese Problemen mildern sich deutlich ab wenn man nur eine vergleichsweise kleine
Anzahl von Knoten verwalten muss, bei dem jeder Knoten den anderen kennt ---
eine Vorbedingung, die bei sicherer Dateisynchronisation durchaus anzunehmen ist.

[^LEECHER]: Die einseitig herunterladenden Teilnehmern werden dabei häufig als *Leecher* bezeichnet.

## Wissenschaftliche Ansätze

Es gibt viele unterschiedliche Arbeiten rund um das Thema der Dateiverteilung
in P2P--Netzwerken. Relativ wenige (TODO: refs?) konzentrieren sich dabei aber
auf das Thema der Dateisynchronisation, wo nicht nur eine Datei ausgetauscht
wird, sondern ein Menge von Dateien auf dem selben Stand gehalten wird. Die
vorhandenen Arbeiten legen ihren Fokus dabei meist auf verteilte Dateisysteme,
die sehr ähnliche Probleme lösen müssen, aber mehr auf Effizienz als auf
Einfachheit ihren Wert legen.

Stellvertretend für eine solche Arbeit soll hier die Disseration von Julien
Quintard »Towards a worldwide storage infrastructure«[@quintard2012towards]
genannt werden. In dieser wird die Implementierung und die Konzepte hinter dem
verteilten Dateisystem *Infinit* vorgestellt. Obwohl der Fokus hier auf
Effizienz liegt, hat *Infinit* einige auffällige Ähnlichkeiten mit ``brig``:

* Weltumspannendes P2P-Netzwerk als Grundlage.
- Nutzung von FUSE (TODO: ref) als Frontend zum Nutzer.
- Verschlüsselte und komprimierte Speicherung der Daten.
* Eingebaute Deduplizierung.
* Versionierung ist vorhanden.

Der Hauptunterschied ist allerdings die Zielgruppe. Während das bei ``brig``
der »Otto--Normal--Nutzer« als kleinster Nenner ist, so ist *Infinit* auf
Entwickler und Adminstratoren ausgelegt und leider nur teilweise quelloffen ist (TODO: ref).

[^INFINIT]: Mehr Informationen unter: <https://infinit.sh>

TODO: [@cox2004optimistic] beschreiben.

### Projekte mit ähnlichen Ansätzen

Es gibt eine Reihe nicht--kommerzieller Projekte, die teilweise eine ähnliche
Ausrichtung wie ``brig`` haben und daher mindestens eine Erwähnung verdient
haben. Im Folgenden werden die Ähnlichkeiten zu ``brig`` genannt:

**bazil:**[^BAZIL_ORG]  Ein Werkzeug um Dateien verschlüsselt und dezentral zu
verteilen. In seinem Zielen ist es also sehr ähnlich zu ``brig``, besonders da
es ebenfalls ein FUSE--Dateisystem implementiert.[^FUSE_NOTE] Es ist eher an
fortgeschrittene Heimanwender und Poweruser gerichtet und momentan noch nicht
für den Produktivbetrieb geeignet. Zu diesem Zeitpunkt funktioniert es zudem
nur lokal auf einem System ohne mit anderen Knoten kommunizieren zu können.

**Tahoe-LAFS:**[^TAHOE_LAFS] Ein verteiltes Dateisystem, welches Dateien über
eine Menge an Rechnern möglichst ausfallsicher verteilen kann, selbst wenn
einzelne Rechner ausfallen. Es richtet sich tendenziell an Administratoren und
Poweruser, die eine große Menge an Daten sicher lagern wollen.

**restic:**{^RESTIC} Ein in *Go* geschriebenes Backup--Programm. Es
synchronisiert zwar keine Dateien über das Netzwerk, setzt aber eine
Versionsverwaltung mittels *Snapshots* um. Zudem verschlüsselt es alle ihm
bekannten Dateien in einem *Repository* und gewährleistet mittels eines
speziellen Formats deren Integrität.

TODO: noch mehr nennen?

[^BAZIL_ORG]: Mehr Informationen unter: <https://bazil.org>
[^FUSE_NOTE]: Der Entwickler von ``bazil``  Tommi Virtanen betreut auch dankenswerterweise die FUSE--Bindings für *Go*, die auch ``brig`` nutzt.
[^TAHOE_LAFS]: Mehr Informationen unter: <https://tahoe-lafs.org/trac/tahoe-lafs>
[^RESTIC]: Mehr Informationen unter: <https://restic.github.io>

## Markt und Wettbewerber

TODO: Diesen Teil überarbeiten, wurde aus Expose übernommen.

Bereits ein Blick auf Wikipedia[@wiki_filesync] zeigt, dass der momentane Markt
an Dateisynchronisationssoftware (im weitesten Sinne) sehr unübersichtlich ist.
Ein näherer Blick zeigt, dass die Softwareprojekte dort oft nur in Teilaspekten
gut funktionieren oder mit anderen unlösbaren Problemen behaftet sind.

## Verschiedene Alternativen

Im Folgenden geben wir eine unvollständige Übersicht über bekannte
Dateisynchronisations--Programme. Davon stehen nicht alle in Konkurrenz zu
``brig``, sind aber zumindest aus Anwendersicht ähnlich. ``brig`` hat sich zum
Ziel gesetzt, die Vorteile der unterschiedlichen Werkzeuge in puncto Sicherheit
und Benutzerfreundlichkeit zu vereinen, mit dem Versuch die Probleme der
einzelnen Alternative zu minimieren.

#### Dropbox + Boxcryptor

Der vermutlich bekannteste und am weitesten verbreitete zentrale Dienst zur
Dateisynchronisation. Verschlüsselung kann man mit Tools wie ``encfs``
(Open--Source, siehe auch [^ENCFS]) oder dem etwas umfangreicheren, proprietären
*Boxcryptor* nachrüsten. Was das Backend genau tut ist leider das Geheimnis von
Dropbox --- es ist nicht Open--Source. 

[^ENCFS]: Mehr Informationen unter <https://de.wikipedia.org/wiki/EncFS>

Die Server von Dropbox stehen in den Vereinigten Staaten, was spätestens seit
den Snowden--Enthüllungen für ein mulmiges Gefühl sorgen sollte. Wie oben
erwähnt, kann diese Problematik durch die Verschlüsselungssoftware *Boxcryptor*
abgemildert werden. Diese kostet aber zusätzlich und benötigt noch einen
zusätzlichen zentralen Keyserver[^KEYSERVER]. Ein weiterer Nachteil ist hier die
Abhängigkeit von der Verfügbarkeit des Dienstes.

[^KEYSERVER]: Mehr Informationen zum Keyserver unter <https://www.boxcryptor.com/de/technischer-\%C3\%BCberblick\#anc09>

Technisch nachteilhaft ist vor allem, dass jede Datei »über den Pazifik« hinweg
synchronisiert werden muss, nur um schließlich auf dem Arbeitsrechner 
»nebenan« anzukommen.

#### ownCloud / nextCloud

Aus dieser Problemstellung heraus entstand die Open--Source Lösung *ownCloud*.
Nutzer hosten auf ihren Servern selbst eine ownCloud--Instanz und stellen
ausreichend Speicherplatz bereit. Vorteilhaft ist also, dass die Daten auf den
eigenen Servern liegen. Nachteilig hingegen, dass das zentrale Modell von Dropbox
lediglich auf eigene Server übertragen wird. Einerseits ist ownCloud nicht so
stark wie ``brig`` auf Sicherheit fokussiert, andererseits ist die Installation
eines Serversystems für viele Nutzer eine »große« Hürde und somit zumindest für
den Heimanwender nicht praktikabel.

#### Syncthing

Das 2013 veröffentliche quelloffene *Syncthing* versucht diese zentrale Instanz
zu vermeiden, indem die Daten jeweils von Peer zu Peer übertragen werden. Es ist
allerdings kein vollständiges Peer--to--peer--Netzwerk: Geteilte Dateien liegen
immer als vollständige Kopie bei allen Teilnehmern, welche die Datei haben.
Alternativ ist selektives Synchronisieren von Dateien möglich.

*Syncthing* besitzt bereits eine Art »intelligentes Routing«, d.h. Dateien werden
vom nächstgelegenen Peer mit der höchsten Bandbreite übertragen. Praktisch ist
auch, dass *Syncthing* Instanzen mittels eines zentralen Discovery--Servers
entdeckt werden können. Nachteilig hingegen ist die fehlende
Benutzerverwaltung: Man kann nicht festlegen von welchen Nutzern man Änderungen
empfangen will und von welchen nicht. 

#### BitTorrent Sync

In bestimmten Kreisen scheint auch das kommerzielle und proprietäre *BitTorrent
Sync* beliebt zu sein. Hier wird das bekannte und freie BitTorrent Protokoll zur
Übertragung genutzt. Vom Feature--Umfang ist es in etwa vergleichbar mit
*Syncthing*. Die Dateien werden allerdings noch zusätzlich AES--verschlüsselt
abgespeichert.

Genauere Aussagen kann man leider aufgrund der geschlossenen Natur des Programms
und der eher vagen Werbeprosa nicht treffen. Ähnlich zu *Syncthing* ist
allerdings, dass eine Versionsverwaltung nur mittels eines »Archivordners«
vorhanden ist. Gelöschte Dateien werden schlicht in diesen Ordner verschoben und
können von dort wiederhergestellt werden.

#### ``git-annex``

Das 2010 erstmals veröffentlichte ``git-annex``[^ANNEX] geht in vielerlei Hinsicht
einen anderen Weg. Einerseits ist es in der funktionalen Programmiersprache
Haskell geschrieben, andererseits nutzt es das Versionsverwaltungssystem ``git``[@git],
um die Metadaten zu den Dateien abzuspeichern, die es verwaltet. Auch werden
Dateien standardmäßig nicht automatisch synchronisiert, hier ist die Grundidee
die Dateien selbst zu »pushen«, beziehungsweise zu »pullen«.

[^ANNEX]: Webpräsenz: <https://git-annex.branchable.com/>

Dieser »Do-it-yourself« Ansatz ist sehr nützlich, um ``git-annex`` als Teil der
eigenen Anwendung einzusetzen. Für den alltäglichen Gebrauch ist es aber selbst
für erfahrene Anwender zu kompliziert, um es praktikabel einzusetzen.

Trotzdem sollen zwei interessante Features nicht verschwiegen werden, welche wir
langfristig gesehen auch in ``brig`` realisieren wollen:

* *Special Remotes:* »Datenablagen« bei denen ``git-annex`` nicht installiert sein muss.
                      Damit können beliebige Cloud--Dienste als Speicher genutzt werden.
+ *N-Copies:* Von wichtigen Dateien kann ``git-annex`` bis zu ``N`` Kopien speichern.
              Versucht man eine Kopie zu löschen, so verweigert ``git-annex`` dies.

*Zusammenfassung:* Obwohl ``brig`` eine gewisse Ähnlichkeit mit verteilten
Dateisystemen, wie *GlusterFS* hat, wurden diese in der Übersicht weggelassen
--- einerseits aus Gründen der Übersicht, andererseits weil diese andere Ziele
verfolgen und von Heimanwendern kaum genutzt werden. Zudem ist der
Vollständigkeit halber auch OpenPGP zu nennen, was viele Nutzer zum
Verschlüsseln von E-Mails benutzen. Aber auch hier ist der größte Nachteil die
für den Ottonormalbenutzer schwierige Einrichtung und Benutzung.

In [@tbl:table-technical-overview] und [@tbl:table-practical-overview] findet
sich zusammenfassend eine Übersicht, mit den aus unserer Sicht wichtigsten
Eigenschaften.

|                      | **Dezentral**       | **Verschlüsselung (Client)**     | **Versionierung**                      |  **Quotas**       | **N-Kopien**    |
| -------------------- | ------------------- | -------------------------------- | -------------------------------------- | ------------------|------------------|
| *Dropbox/Boxcryptor* | \xmark              | \xmark                           | \textcolor{YellowOrange}{Rudimentär}   |  \xmark           | \xmark          |
| *ownCloud*           | \xmark              | \xmark                           | \textcolor{YellowOrange}{Rudimentär}   |  \xmark           | \xmark          |
| *Syncthing*          | \cmark              | \cmark                           | \textcolor{YellowOrange}{Archivordner} |  \xmark           | \xmark          |
| *BitTorrent Sync*    | \cmark              | \cmark                           | \textcolor{YellowOrange}{Archivordner} |  \xmark           | \xmark          |
| ``git-annex``        | \cmark              | \cmark                           | \cmark                                 |  \xmark           |  \cmark         |
| ``brig`` (Prototyp)  | \cmark              | \cmark                           | \cmark                                 |  \xmark           |  \xmark         |
| ``brig`` (Ziel)      | \cmark              | \cmark                           | \cmark                                 |  \xmark           |  \cmark         |


: Übersicht über technische Aspekte {#tbl:table-technical-overview}

|                      | **FOSS**            | **Einfach nutzbar** | **Einfache Installation**  | **Intell. Routing** | **Kompression** |
| -------------------- | ------------------- | ------------------- |--------------------------  | ------------------------- |-----------------|
| *Dropbox/Boxcryptor* | \xmark              | \cmark              | \cmark                     |  \xmark             | \xmark          |
| *ownCloud*           | \cmark              | \cmark              | \xmark                     |  \xmark             | \xmark          |
| *Syncthing*          | \cmark              | \cmark              | \cmark                     |  \cmark             | \xmark          |
| *BitTorrent Sync*    | \xmark              | \cmark              | \cmark                     |  \cmark             | \xmark          |
| ``git-annex``        | \cmark              | \xmark              | \xmark                     |  \xmark             | \xmark          |
| ``brig`` (Prototyp)  | \cmark              | \xmark              | \textcolor{YellowOrange}{Auf Linux} |  \cmark             | \cmark          |
| ``brig`` (Ziel)      | \cmark              | \cmark              | \cmark                     |  \cmark             | \cmark          | 

: Übersicht über praktische Aspekte {#tbl:table-practical-overview}

## IPFS: Das Interplanetary Filesystem

Anstatt das Rad neu zu erfinden, setzt ``brig`` auf das relativ junge
*Interplanetary Filesystem* (kurz ``IPFS``), welches von Juan Benet und seinen
Mitentwicklern unter der MIT--Lizenz in der Programmiersprache Go entwickelt
wird (siehe auch das Original--Paper[@benet2014ipfs]). Im Gegensatz zu den
meisten anderen verfügbaren Peer--to-Peer Netzwerken kann ``IPFS`` als  
Software--Bibliothek genutzt werden. Dies ermöglicht es ``brig`` als,
vergleichsweise dünne Schicht, zwischen Benutzer und ``IPFS`` zu fungieren.

``IPFS`` stellt dabei ein *Content Addressed Network* (kurz *CAN*, [^CAN]) dar.
Dabei wird eine Datei, die in das Netzwerk gelegt wird nicht mittels eines
Dateinamen angesprochen, sondern mittels einer Prüfsumme, die durch eine vorher
festgelegte Hashfunktion berechnet wird. Andere Teilnehmer im Netzwerk können
mittels dieser Prüfsumme die Datei lokalisieren und empfangen.
Vereinfacht gesagt ist es nun die Hauptaufgabe von ``brig`` dem Nutzer die gewohnte
Abstraktionsschicht eines Dateisystem zu geben, während im Hintergrund jede
Datei zu einer Prüfsumme aufgelöst wird.

Im Vergleich zu zentralen Ansätzen (bei dem der zentrale Server einen *Single
Point of Failure* darstellt) können Dateien intelligent geroutet werden und
müssen nicht physikalisch auf allen Geräten verfügbar sein. Wird beispielsweise
ein großes Festplattenimage (~8GB) in einem Vorlesungssaal von jedem Teilnehmer
heruntergeladen, so muss bei zentralen Diensten die Datei vielmals über das
vermutlich bereits ausgelastete Netzwerk der Hochschule gezogen werden. In einem
*CAN*, kann die Datei in Blöcke unterteilt werden, die von jedem Teilnehmer
gleich wieder verteilt werden können, sobald sie heruntergeladen wurden. Der
Nutzer sieht dabei ganz normal die gesamte Datei, ``brig``, bzw. das *CAN* erledigt
dabei das Routing transparent im Hintergrund.

Technisch basiert ``IPFS`` auf der verteilten Hashtabelle
*Kademlia*[@maymounkov2002kademlia], welches mit den Erkenntnissen auf den
Arbeiten *CoralDHST*[@freedman2004democratizing] (Ansatz um das Routing zu
optimieren) und *S/Kademlia*[@baumgart2007s] (Ansatz um das Netzwerk gegen
Angriffe zu schützen) erweitert und abgesichert wurde. *S/Kademlia* verlangt
dabei, dass jeder Knoten im Netzwerk über ein Paar von öffentlichen und
privaten Schlüssel verfügt. Die Prüfsumme des öffentlichen Schlüssels dient
dabei als einzigartige Identifikation des Knotens und der private Schlüssel
dient als Geheimnis mit dem ein Knoten seine Identität nachweisen kann. Diese
Kernfunktionalitäten sind bei ``IPFS`` in einer separaten Bibliothek namens
``libp2p``[^LIBP2P] untergebracht, welche auch von anderen Programmen genutzt
werden kann.

[^CAN]: Siehe auch: <https://en.wikipedia.org/wiki/Content_addressable_network> (TODO: eigenes buch referenzieren)
[^LIBP2P]: Mehr Informationen in der Dokumentation unter: <https://github.com/ipfs/specs/tree/master/libp2p>

### Eigenschaften von *IPFS*

Im Folgenden werden die Eigenschaften von ``IPFS`` kurz vorgestellt, welche von
``brig`` genutzt werden. Einige interessante Features wie das *Naming System* (IPNS),
und der *Record Store* (IPLD) werden dabei ausgelassen, da sie für ``brig`` (noch)
keine praktische Bedeutung haben:

**Weltweites Netzwerk:** Standardmäßig nehmen alle *IPFS* Knoten an einem
zusammenhängenden, weltweiten Netzwerk teil. (TODO: Screenshot von Weltkugel
machen?)

Um sich zum Netzwerk zu verbinden, müssen erst einmal passende Knoten »in der
Nähe« des neuen Knotens gefunden werden. Dazu verbindet sich *IPFS* beim Start
des ``ipfs daemon`` mit einigen, wohlbekannten *Bootstrap--Nodes*, dessen
Adressen bei der Software mitgeliefert werden. Diese können dann wiederum den
neuen Knoten an ihnen bekannte, passendere Knoten vermitteln. Die Menge der so
entstandenen verbundenen Knoten nennt *IPFS* den *Swarm* (dt. Schwarm). Ein
Nachbarknoten wird auch *Peer* genannt.

Falls gewünscht, kann allerdings auch ein abgeschottetes Subnetz erstellt
werden. Dazu ist es lediglich nötig, die *Bootstrap*--Nodes durch Knoten
auszutauschen, die man selbst kontrolliert. Unternehmen könnten diesen Ansatz
wählen, falls ihr Netzwerk komplett von der Außenwelt abgeschottet ist. Wie in
[@sec:architektur] beleuchtet wird, ist dieses Vorgehen nicht direkt aus
Sicherheitsgründen notwendig.

**Operation auf Hashes:** *IPFS* arbeitet nicht mit herkömmlichen Dateipfaden,
sondern nur mit der Prüfsumme[^IPFS_HASH] einer Datei. Im folgenden Beispiel
wird eine Photo--Datei mittels der ``ipfs``--Kommandozeile in das Netzwerk
gelegt:[^IPFS_DAEMON]

```bash
$ ipfs add my-photo.png
QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG
```

[^IPFS_DAEMON]: Voraussetzung hierfür ist allerdings, dass der ``ipfs``--Daemon
vorher gestartet wurde und ein Repository mittels ``ipfs init`` erzeugt wurde.

[^IPFS_HASH]: *Anmerkung:* *IPFS* nutzt ein spezielles Format um Hashes zu
repräsentieren. Die ersten zwei Bytes einer Prüfsumme repräsentieren dabei den
verwendeten Algorithmus und die Länge der darauf folgenden, eigentlichen
Prüfsumme. Die entstandene Byte--Sequenz wird dann mittels ``base58``
enkodiert, um sie menschenlesbar zu machen. Da der momentane
Standardalgorithmus ``sha256`` ist, beginnt eine von *IPFS* generierte
Prüfsumme stets mit ``Qm``. Mehr Informationen unter:
<github.com/multiformats/multihash>

Auf einem anderen Computer, mit laufenden ``ipfs``--Daemon, ist das Empfangen
der Datei möglich, indem der Hash an ``ipfs cat`` gegeben wird. Dabei wird für
den Nutzer transparent über die DHT ein Peer ausfindig gemacht, der die Datei
anbieten kann:

```bash
$ ipfs cat QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG > my-photo.png
```

Im Hintergrund wird die Datei dabei in kleinere Blöcke zerlegt. Von jedem Block
wird ein Hashwert erstellt und alle Hashwerte in einem sogenannten *Merkle-DAG*
(*Directed Acyclic Graph*). Diese Struktur ist ähnlich zu einem Merkle--Tree
(TODO: ref), erlaubt aber zusätzlich beliebige Verlinkungen zwischen den
Kindknoten. Der Einsatz dieser Datenstruktur hat mehrere Vorteile:

* Der Wurzelknoten hat eine Prüfsumme, die aus den Unterprüfsummen erstellt wird.
* *Authentifizierung:* Eine Änderung der Blöcke unten resultiert zwangsweise
  in eine Änderung der Prüfsumme oben.
* *Deduplizierung:* Doppelte Blöcke müssen nur einmal gespeichert werden und
  können durch Verlinkung repräsentiert werden. Das reduziert sowohl
  Speicherkosten, als auch Übertragungsaufwand. Wie wir später sehen werden (TODO: ref) ist 
  dieses Konzept aber nur bedingt bei ``brig`` übertragbar.

Auch ganze Verzeichnisse können in einem *Merkle--DAG* gespeichert werden,
intern werden diese ähnlich wie bei ``tar`` in eine große Datei zusammengeführt.

(TODO: Grafik)

### Public--Key Infrastructure

Jeder Knoten im *IPFS*--Netzwerk besitzt ein RSA--Schlüsselpaar, welches beim
Anlegen des Repositories erzeugt wird. Basierend auf den öffentlichen Schlüssel
wird eine Prüfsumme errechnet, die dazu genutzt wird einen Knoten eindeutig zu
identifizieren. Mithilfe dieser Identität ist es möglich, andere Nutzer im
Netzwerk nachzuschlagen und deren öffentlichen Schlüssel zu empfangen:

```bash
# Nachschlagen des öffentlichen Schlüssels eines zufälligen Bootstrap-Nodes:
$ ipfs id QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ
{
  "ID": "Qmdx8h9589Gk3ApQr35S4K8P8Q6cGmsioGBvHRGVzB3b7G",
  "PublicKey": "CAASpgIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK[...]",
  ...
}
```

Der öffentliche Schlüssel kann dazu genutzt werden, mit seinem Peer
mittels asymmetrischer Verschlüsselung eine verschlüsselte Verbindung
aufzubauen. Von ``brig`` wird dieses Konzept weiterhin genutzt, um eine Liste
vertrauenswürdiger Knoten zu verwalten. Jeder Peer muss bei Verbindungsaufbau
nachweisen, dass er den zum öffentlichen passenden privaten Schlüssel besitzt.
Der genaue Ablauf dieser Authentifikation kann in [TODO ref kitteh] nachgelesen werden.

**Pinning und Caching:** Das Konzept von *IPFS* basiert darauf, dass Knoten nur
das speichern, worin sie auch interessiert sind. Daten, die von außen zum
eigenen Knoten übertragen worden sind werden nur kurzzeitig zwischengelagert.
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

**Service Discovery:** In den Anforderungen in [@sec:einleitung] wird eine menschenlesbare Identität
gefordert, mit der *Peers* einfach erkennbar sind. Der von *IPFS* verwendete Identitätsbezeichner ist
allerdings eine tendenziell schwer zu merkende Prüfsumme. Um dieses Dilemma zu lösen, wendet 
``brig`` einen »Trick« an. Jeder ``brig``--Knoten legt eine Datensatz in das *IPFS* Netzwerk mit dem Inhalt
``brig:<username>``. Ein Nutzer der nun einen solchen menschenlesbaren  Namen zu einem Netzwerkadresse  auflösen
möchte, kann den Inhalt des obigen Datensatzes generieren und daraus eine Prüfsumme bilden.
Mit der entstandenen Prüfsumme kann mittels folgenden Befehls herausgefunden werden, welche Knoten
diesen Datensatz anbieten:

```bash
$ ipfs dht findprovs <HASH_OF_BOBS_ID>
<PEER_ID_BOB_1>
<PEER_ID_BOB_2>
...
```

Da prinzipiell jeder Knoten sich als *Bob* ausgeben kann, wird aus den
möglichen Peers, derjenige ausgewählt, dessen *IPFS*--Identitätsbezeichner (bei
``brig`` wird dieser als *Fingerprint* bezeichnet) als vertrauenswürdig
eingestuft wurde. Dies setzt im Umkehrschluss voraus, dass eine erstmalige
Authentifikation stattgefunden haben muss.

TODO: Grafik?

**Flexibles Networking:** Einer der größten Vorteile von *IPFS* ist, dass es
auch NAT--Grenzen hinweg funktioniert. NAT steht dabei für *Network Adress
Resolution* (dt. Netzwerkadressübersetzung) und ist eine Technik, um zwischen
einer öffentlichen und mehreren lokalen IP--Adressen zu vermitteln. Es wird
aufgrund der Knappheit von IPv4 sehr häufig eingesetzt, um einen Heim- oder
Unternehmensnetzwerk eine einzige IP-Adresse nach außen zu geben, die über
bestimmte Ports dann den Verkehr auf die jeweiligen lokalen Adressen übersetzt.
Der Nachteil in Bezug auf P2P--Netzwerken ist dabei, dass die Rechner hinter
einem *NAT* nicht direkt erreichbar sind. Client/Server Anwendungen haben damit
kein Problem, da der Client die Verbindung zum Server selbstständig aufbaut.
Bei einer P2P--Kommunikation hingegen, muss eine Verbindung in beide Richtungen
möglich sein --- und das möglicherweise sogar über mehrere *NATs*.

Die Umgehung dieser Grenzen ist in der Literatur als *NAT Traversal* bekannt
(TODO: ref). Eine populäre Technik ist dabei das UDP--Hole--Punching (TODO:
ref). Dabei wird grob erklärt ein beiden Parteien bekannter Mittelmann (oft ein
*Bootstrap*--Knoten) herangezogen, über den die eigentliche, direkte Verbindung
aufgebaut wird. Mehr Details finden sich in TODO: ref. Eine Notwendigkeit dabei
ist die Verwendung von *UDP* anstatt *TCP*. Um die Garantien, die *TCP*
bezüglich der Paketzustellung gibt, zu erhalten nutzt *IPFS* die
Anwendungs--Protokolle *UDT*. Insgesamt implementiert *IPFS* also einige
Techniken, um, im Gegensatz zu den meisten theoretischen Ansätzen, eine leichte
Benutzbarkeit zu gewährleisten. Speziell wäre hier zu vermeiden, dass ein
Anwender die Einstellungen seines Routers ändern muss, um ``brig`` zu nutzen.

[^UDT]: http://udt.sourceforge.net/

In Einzelfällen kann es natürlich trotzdem dazu kommen, dass die von *IPFS* verwendeten Ports
durch eine (besonders in Unternehmen übliche) Firewall blockiert werden. Dies kann nötigenfalls
aber vom zuständigen Administrator geändert werden. Allerdings werden Unternehmen eh dazu
tendieren nur ein abgeschottetes ``brig``--Netzwerk in der Firma einzusetzen.

**Übermittlung zwischen Internet und IPFS:** Ein Client/Server--Betrieb lässt sich mithilfe der *IPFS Gateways*
bewerkstelligen. *Gateways* sind zentrale, wohlbekannte Dienste, die zwischen dem »normalen Internet« und
dem *IPFS* Netzwerk mittels HTTP vermitteln. Die Datei ``my-photo.png`` aus dem obigen Beispiel kann
von von anderen Nutzern bequem über den Browser heruntergeladen werden:

```bash
$ export PHOTO_HASH=QmPtoEEMMnbTSmzr28UEJFvmsD2dW88nbbCyyTrQgA9JR9 
$ curl https://gateway.ipfs.io/ipfs/$PHOTO_HASH > my-photo.png
```

Auf dem *Gateway* läuft dabei ein Webserver, der dasselbe tut wie ``ipfs cat``, aber statt auf der Kommandozeile
die Daten auf eine HTTP--Verbindung ausgibt. Standardmäßig wird mit jedem Aufruf von ``ipfs daemon``
ein Gateway auf der Adresse ``http://localhost:8080`` gestartet.
