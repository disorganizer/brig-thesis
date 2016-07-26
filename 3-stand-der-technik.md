# Stand der Technik

## Wissenschaftliche Ansätze

### Theorie zu P2p Netzwerken

- Distributed Hashtable
- Bittorrent vergleich
- Chunking (miller rabin)
- Begriffe allgemein einführen und referenzieren

## Markt und Wettbewerber

Bereits ein Blick auf Wikipedia[@wiki_filesync] zeigt, dass der momentane Markt
an Dateisynchronisationssoftware (im weitesten Sinne) sehr unübersichtlich ist.
Ein näherer Blick zeigt, dass die Softwareprojekte dort oft nur in Teilaspekten
gut funktionieren oder mit anderen unlösbaren Problemen behaftet sind. Manch
andere Software wie ``bazil``[^BAZIL] oder ``infinit``[^INFINIT] ist
vielversprechender, allerdings ebenfalls noch im Entstehen und im Falle von
``infinit`` auch nur teilweise quelloffen.

[^BAZIL]: Webpräsenz: \url{https://bazil.org}
[^INFINIT]: Webpräsenz: \url{http://infinit.sh}

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

[^ENCFS]: Mehr Informationen unter \url{https://de.wikipedia.org/wiki/EncFS}

Die Server von Dropbox stehen in den Vereinigten Staaten, was spätestens seit
den Snowden--Enthüllungen für ein mulmiges Gefühl sorgen sollte. Wie oben
erwähnt, kann diese Problematik durch die Verschlüsselungssoftware *Boxcryptor*
abgemildert werden. Diese kostet aber zusätzlich und benötigt noch einen
zusätzlichen zentralen Keyserver[^KEYSERVER]. Ein weiterer Nachteil ist hier die
Abhängigkeit von der Verfügbarkeit des Dienstes.

[^KEYSERVER]: Mehr Informationen zum Keyserver unter \url{https://www.boxcryptor.com/de/technischer-\%C3\%BCberblick\#anc09}

Technisch nachteilhaft ist vor allem, dass jede Datei »über den Pazifik« hinweg
synchronisiert werden muss, nur um schließlich auf dem Arbeitsrechner 
»nebenan« anzukommen.

#### ownCloud

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

[^ANNEX]: Webpräsenz: \url{https://git-annex.branchable.com/}

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

\newpage

Zusammengefasst findet sich hier noch eine tabellarische Übersicht mit den aus
unserer Sicht wichtigsten Eigenschaften: 

**Technische Aspekte:**

|                      | **Dezentral**       | **Verschlüsselung (Client)**     | **Versionierung**                      |  **Quotas**       | **N-Kopien**    |  
| -------------------- | ------------------- | -------------------------------- | -------------------------------------- | ------------------|------------------|
| *Dropbox/Boxcryptor* | \xmark              | \xmark                           | \textcolor{YellowOrange}{Rudimentär}   |  \xmark           | \xmark          |
| *ownCloud*           | \xmark              | \xmark                           | \textcolor{YellowOrange}{Rudimentär}   |  \xmark           | \xmark          |
| *Syncthing*          | \cmark              | \cmark                           | \textcolor{YellowOrange}{Archivordner} |  \xmark           | \xmark          |
| *BitTorrent Sync*    | \cmark              | \cmark                           | \textcolor{YellowOrange}{Archivordner} |  \xmark           | \xmark          |
| ``git-annex``        | \cmark              | \cmark                           | \cmark                                 |  \xmark           |  \cmark         |
| ``brig`` (Prototyp)  | \cmark              | \cmark                           | \cmark                                 |  \xmark           |  \xmark         |
| ``brig`` (Ziel)      | \cmark              | \cmark                           | \cmark                                 |  \xmark           |  \cmark         |


**Praktische Aspekte:**

|                      | **FOSS**            | **Einfach nutzbar** | **Einfache Installation**  | **Intell. Routing** | **Kompression** |
| -------------------- | ------------------- | ------------------- |--------------------------  | ------------------------- |-----------------|
| *Dropbox/Boxcryptor* | \xmark              | \cmark              | \cmark                     |  \xmark             | \xmark          |
| *ownCloud*           | \cmark              | \cmark              | \xmark                     |  \xmark             | \xmark          |
| *Syncthing*          | \cmark              | \cmark              | \cmark                     |  \cmark             | \xmark          |
| *BitTorrent Sync*    | \xmark              | \cmark              | \cmark                     |  \cmark             | \xmark          |
| ``git-annex``        | \cmark              | \xmark              | \xmark                     |  \xmark             | \xmark          |
| ``brig`` (Prototyp)  | \cmark              | \xmark              | \textcolor{YellowOrange}{Auf Linux} |  \cmark             | \cmark          |
| ``brig`` (Ziel)      | \cmark              | \cmark              | \cmark                     |  \cmark             | \cmark          | 

## Interplanetary Filesystem

Anstatt das Rad neu zu erfinden, setzt ``brig`` auf das relativ neue
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
dient als Geheimnis mit dem ein Knoten seine Identität nachweisen kann.

[^CAN]: Siehe auch: \url{https://en.wikipedia.org/wiki/Content_addressable_network} (TODO: eigenes buch referenzieren)

Im Folgenden werden die Verhaltensweisen, Features und Limitationen von ``IPFS`` kurz vorgestellt, welche aus
Sicht  von ``brig`` wichtig sind.

### Pinning

### Dezentrales Routing

### Public Key Infrastructure

### Merkle Tree

### Service Discovery
