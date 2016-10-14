# Stand der Technik {#sec:stand-der-technik}

In diesem Kapitel wird ein kurze Einführung zum Thema Peer--to--Peer--Netzwerke
gegeben. Danach wird eine Einordnung der Arbeit zu den bisher existierenden
Arbeiten zum Thema Dateisynchronisation gegeben. Im Anschluss wird ``brig``
zudem in Relation zu einigen auf dem Markt verfügbaren Produkten gesetzt.
Darauf aufbauend wird von verschiedenen Perspektiven aus überlegt, welche
Eigenschaften ``brig`` übernehmen kann und von wem und in welchem Rahmen die
Software eingesetzt werden kann.

## Peer--to--Peer Netzwerke

Bilden viele Rechner ein dezentrales Netzwerk, bei dem jeder Rechner (ein
»Peer«) die gleichen Rechte besitzt und Aktionen ausführt wie jeder andere, so
wird dieses Netz ein *Peer--to--Peer--Netzwerk* genannt (kurz *P2P--Netzwerk*,
vgl. auch [@peer2peer], S. 4 ff.). Statt Verbindungen über einen Mittelsmann
aufzubauen, kommunizieren die einzelnen Peers für gewöhnlich direkt
miteinander. Jeder Knoten des Netzwerks kann Anfragen an andere Knoten richten,
trägt aber selbst etwas bei indem er selbst Anfragen beantwortet. Im
Client--Server--Modell entspricht ein Peer also sowohl Server als auch Client
(siehe auch [@fig:central-distributed]).

![Anschaulicher Unterschied zwischen zentralen und verteilten Systemen.](images/2/central-distributed.pdf){#fig:central-distributed}

Im alltäglichen Gebrauch der meisten »Otto--Normal--Nutzer« scheinen
P2P--Netzwerke derzeit eine eher untergeordnete Rolle zu spielen. Die
bekanntesten und populärsten P2P--Netzwerke sind vermutlich das BitTorrent- und
Skype--Protokoll (vgl. [@peer2peer], S. 232 ff. und S. 2). Darüber hinaus gibt
es auch viele sehr große Filesharing--Netzwerke, wie Gnutella (vgl. auch
[@peer2peer], S. 57 ff.). Gemeinsam ist allen, dass sie als sogenanntes
*Overlay--Netzwerk*[^OVERLAY_NETWORK] über das Internet gelegt werden und
dessen existierende Infrastruktur wiederverwenden.

[^OVERLAY_NETWORK]: Siehe auch: <https://de.wikipedia.org/wiki/Overlay-Netz>

### Zugrundeliegende Technik

Die meisten Dienste im Internet hingegen basieren auf dem Client--Server--Modell, bei
dem viele anonyme Clients eine Anfrage an einen zentralen Server stellen.
Dieser muss mit der steigenden Anzahl an Clients skalieren, indem er
typischerweise mehr Prozessorleistung und Bandbreite zur Verfügung hat. Dieses
Modell passt auf viele heterogene Anwendungsfälle, wo Client und Server
grundverschiedene Rollen zugeordnet sind (Beispiel: Dienstleiter und Kunde).
Ein weitere Eigenschaft, ist dass das Client--Server--Modell kein Problem mit
dem sogenannten *NAT--Traversal* hat.

NAT steht dabei für *Network Address Translation* (dt.
Netzwerkadressübersetzung, siehe auch [@peer2peer], S. 47 ff.) und
ist eine Technik, um zwischen einer öffentlichen und mehreren lokalen
IP--Adressen zu vermitteln. Es wird aufgrund der Knappheit von IPv4 sehr häufig
eingesetzt, um einem Heim- oder Unternehmensnetzwerk eine einzige IP-Adresse
nach außen zu geben, die über bestimmte Ports dann den Verkehr auf die
jeweiligen lokalen Adressen übersetzt. Der Nachteil in Bezug auf P2P--Netzwerke
ist dabei, dass die Rechner hinter einem *NAT* nicht direkt erreichbar sind.
Client--Server--Anwendungen haben damit kein Problem, da der »anonyme« Client
die Verbindung zum »wohlbekannten« Server selbstständig aufbaut. Bei einer
P2P--Kommunikation hingegen, muss eine Verbindung in beide Richtungen möglich
sein --- und das möglicherweise sogar über mehrere *NATs* hinweg. Die Umgehung
dieser Grenzen ist in der Literatur als *NAT Traversal* bekannt. Eine populäre
Technik ist dabei das UDP--Hole--Punching[^HOLE_PUNCH]. Dabei wird,
grob erklärt, ein beiden Parteien bekannter Mittelsmann herangezogen, über den
die eigentliche, direkte Verbindung aufgebaut wird. Eine technische
Notwendigkeit dabei ist die Verwendung von *UDP* anstatt *TCP*.

[^HOLE_PUNCH]: Siehe auch: <https://en.wikipedia.org/wiki/UDP_hole_punching>

Typischerweise ist dieser Mittelsmann ein sogenannter *Bootstrap--Knoten*. Dieser
ist innerhalb eines P2P--Netzwerks ein wohlbekannter Knoten unter mehreren, zu dem sich neue
Netzwerkteilnehmer verbinden, um von ihm an weitere Teilnehmer vermittelt zu
werden. Der Boostrap--Knoten führt aber normalerweise das selbe Programm aus,
wie jeder andere, ist aber vertrauenswürdiger.
Bemerkenswert ist, dass sich keine zentrale Instanz um die Koordination
des Datenflusses im Netzwerk kümmern muss. Die Grundlage für die Koordination
bildet dabei die *Distributed Hashtable (DHT, vgl. [@peer2peer], S. 63 ff.)*
Diese Datenstruktur bildet sich durch den Zusammenschluss vieler
Rechner und nutzt eine *Hashfunktion*[^HASH_FUNCTION], um für
einen bestimmten Datensatz zu entscheiden, welche Knoten (mindestens aber
einer) im Netzwerk für diesen Datensatz zuständig ist. Ist ein Teilnehmer an
einem Datensatz interessiert, so muss er nur die Prüfsumme desselben kennen, um
zu wissen von welchem Teilnehmer er den Datensatz beziehen kann. Jeder Knoten
verwaltet dabei einen bestimmten Wertebereich der Prüfsummenfunktion und ist
für diese Prüfsummen zuständig. Werden neue Knoten hinzugefügt oder andere
verlassen das Netz, werden die Wertebereiche neu verteilt.

[^HASH_FUNCTION]: Bildet einen Datensatz beliebiger auf eine kurze Prüfsumme mit fixer Länge ab. Eine Rückrechnung von der Prüfsumme zum ursprünglichen Datensatz ist theoretisch möglich, aber extrem rechenaufwendig. Kleine Änderungen der Eingabe, erzeugen eine gänzlich andere Prüfsumme.
Siehe auch: <https://de.wikipedia.org/wiki/Hashfunktion>

### Dateisynchronisation in P2P--Netzwerken

In diesem Kontext meint der Begriff »Synchronisation« das Zusammenführen der Dateistände
mehrerer Netzwerkteilnehmer. Typischerweise nutzen viele Nutzer heutzutage
dafür einen zentralen Dienst. Dieser hält einen Dateistand vor, der von allen
Teilnehmern als Referenz angesehen wird. Ändert ein Teilnehmer seinen Stand, so
wird die Änderung zum zentralen Server übertragen und erreicht so auch alle
anderen Teilnehmer.

In vielen Fällen skalieren aber solche Client--Server Anwendungen bei weitem
schlechter als verteilte Anwendungen. Man stelle sich einen Vorlesungssaal mit
50 Studenten vor, die ein Festplattenimage (Größe: 5 Gigabyte) aus dem Internet
herunterladen sollen. Bei einer Client--Server Anwendung werden hier 50
Verbindungen zu einem zentralen Server (beispielsweise Dropbox) geöffnet. Der
Server muss nun 50 Verbindungen gleichzeitig bearbeiten und muss eine
entsprechende Bandbreite zur Verfügung stellen. Bei kleineren Diensten kann
dies bereits der Flaschenhals sein, teilweise kann aber auch die Bandbreite auf
Seiten des Empfängers limitiert sein. Fällt der zentrale Server aus (»Single--Point--of--Failure«),
so kann kein neuer Nutzer mehr das Festplattenimage empfangen.

![Veranschaulichung der Netzwerklast bei zentralen und dezentralen Systemen.](images/2/zentral-dezentral-speedup.pdf){#fig:speedup}

Bilden die Rechner der Studenten ein verteiltes Netzwerk, so
genügt es wenn nur ein Rechner einen Teil der Datei hat. Diesen
Teil kann er im lokalen Netz anderen Teilnehmern wieder anbieten und sich Teile
der Datei besorgen, die er selbst noch nicht hat. So muss in der Theorie die
Datei nur maximal einmal vom zentralen Server übertragen werden. In
diesem etwas konstruierten[^CACHING_PROXY] Beispiel würde im dezentralen
Netzwerk die Datei also bis zu 50-mal schneller verteilt werden, als im
zentralen Anwendungsfall. Fällt der zentrale Server aus nachdem die Datei
bereits einmal komplett heruntergeladen wurde, so werden die bereits
existierenden Teile von den jeweiligen Teilnehmern weiter angeboten.
[@fig:speedup] veranschaulicht diesen Zusammenhang noch einmal.

Dezentrale Netzwerke eignen sich sehr gut um Dateien auszutauschen,
da ganze Dateien in kleine Blöcke unterteilt werden können. Diese können dann von
interessierten Knoten vorgehalten und weitergegeben werden. Protokolle wie *BitTorrent*
haben das Problem, dass ein Block nur solange verfügbar ist, solange es Teilnehmer
gibt, die diesen Block anbieten. Prinzipiell hat auch ``brig`` dieses Problem,
doch besteht ein ``brig``--Netzwerk nur aus den Teilnehmern, die einen gemeinsamen
Dateistand synchronisieren wollen. Daher kann angenommen werden, dass alle darin enthaltenen
Dateien von mindestens einem Teilnehmer angeboten werden können.

[^CACHING_PROXY]: Typischerweise sorgen auch vorgeschaltete *Caching Proxies* wie Squid (<https://de.wikipedia.org/wiki/Squid>) dafür, dass Dateien nicht zigmal heruntergeladen werden.

## Ähnliche Arbeiten

Es gibt viele unterschiedliche wissenschaftliche Arbeiten rund um das Thema der
Dateiverteilung in P2P--Netzwerken. Die meisten Arbeiten scheinen sich mehr auf
das Thema des Dateiaustausches an sich zu konzentrieren und weniger auf das
Thema der Dateisynchronisation, wo eine Menge von Dateien auf dem selben Stand
gehalten werden muss. Die dazu vorhandenen Arbeiten legen ihren Fokus dabei
meist auf die Untersuchung und Implementierung verteilter Dateisysteme, die
sehr ähnliche Probleme lösen müssen, aber mehr auf Effizienz als auf
Einfachheit Wert legen.

Stellvertretend für eine solche Arbeit soll hier die Dissertation von Julien
Quintard *»Towards a worldwide storage infrastructure«*[@quintard2012towards]
genannt werden. In dieser wird die Implementierung und die Konzepte hinter dem
verteilten Dateisystem *Infinit* vorgestellt. Obwohl der Fokus hier auf
Effizienz liegt, hat *Infinit* einige auffällige Ähnlichkeiten mit den Zielen
von ``brig``:

* Weltumspannendes P2P-Netzwerk als Grundlage.
- Nutzung von FUSE[^FUSE_EXPL]  als Frontend zum Nutzer.
- Verschlüsselte Speicherung der Daten.
* Eingebaute Deduplizierung.
* Eine Versionierung der Dateien ist geplant.

[^FUSE_EXPL]: Eine Technik, um ein Dateisystem im Userspace zu implementieren. Dem Nutzer kann dadurch ein normaler Ordner mit beliebigen Daten als Dateien präsentiert werden.

Der Hauptunterschied ist allerdings die Zielgruppe. Während das bei ``brig``
der »Otto--Normal--Nutzer« als kleinster Nenner ist, so ist *Infinit* auf
Entwickler und Administratoren ausgelegt und leider nur teilweise quelloffen
[^INFINIT_SOURCE], also keine »Free Open Source Software« *(FOSS)*.

[^INFINIT_SOURCE]: Siehe auch: <https://infinit.sh/open-source>

Eine sehr detaillierte Gegenüberstellung vieler Produkte rund um das Thema
Dateisynchronisation findet sich in der Dokumentation von ``inifinit``[^INF_COMP]

[^INF_COMP]: Beispielsweise mit Dropbox: <https://infinit.sh/documentation/comparison/dropbox>

[^INFINIT]: Mehr Informationen unter: <https://infinit.sh>  --- *Anmerkung:* Neben dem verteilten Dateisystem bietet das Unternehmen
auch noch eine reine Datei--Transfer--Lösung namens *Infinit Transfer*. Dazu gibt es hier mehr Informationen: <https://infinit.io>

Es gibt eine Reihe nicht--kommerzieller Projekte, die teilweise eine ähnliche
Ausrichtung wie ``brig`` haben und daher mindestens eine Erwähnung verdienen.
Im Folgenden werden die Ähnlichkeiten zu ``brig`` genannt:

**bazil:**[^BAZIL_ORG]  Ein Werkzeug um Dateien verschlüsselt und dezentral zu
verteilen. In seinen Zielen ist es sehr ähnlich zu ``brig``, besonders da
es ebenfalls ein FUSE--Dateisystem implementiert.[^FUSE_NOTE] Es ist eher an
technisch versierte Nutzer gerichtet und momentan noch nicht
für den Produktivbetrieb geeignet. Zu diesem Zeitpunkt funktioniert es
nur lokal auf einem System ohne mit anderen Knoten kommunizieren zu können.

**Tahoe-LAFS:**[^TAHOE_LAFS] Ein verteiltes Dateisystem, welches Dateien auf
eine Menge an Rechnern möglichst ausfallsicher verteilen kann, selbst wenn
einzelne Rechner ausfallen. Es richtet sich tendenziell an Administratoren und
technisch versierte Nutzer, die eine große Menge an Daten sicher lagern wollen.
Ähnliche Produkte in diesem Bereich gibt es mit *XtreemFs*[^XTREEMFS],
*LizardFs*[^LIZARDFS] und *MooseFs*[^MOOSEFS] mit jeweils unterschiedlichen
Schwerpunkten.

**restic:**[^RESTIC] Ein in *Go* geschriebenes Backup--Programm. Es
synchronisiert zwar keine Dateien über das Netzwerk, setzt aber eine
Versionsverwaltung mittels *Snapshots* um. Zudem verschlüsselt es alle ihm
bekannten Dateien in einem *Repository* und gewährleistet mittels eines
speziellen Dateiformats deren Integrität. ``brig`` verwendet analog zu
``restic`` (und ``git``) den Begriff *Repository* für den Ordner, in dem es
seine Daten ablegt.

[^BAZIL_ORG]: Siehe auch: <https://bazil.org>
[^FUSE_NOTE]: Der Entwickler von ``bazil``  Tommi Virtanen betreut auch dankenswerterweise die FUSE--Bindings für *Go*, die auch ``brig`` nutzt.
[^TAHOE_LAFS]: Siehe auch: <https://tahoe-lafs.org/trac/tahoe-lafs>
[^RESTIC]: Siehe auch: <https://restic.github.io>
[^LIZARDFS]: Siehe auch: <https://lizardfs.com/>
[^XTREEMFS]: Siehe auch:  <http://www.xtreemfs.org>
[^MOOSEFS]: Siehe auch: <http://moosefs.org/>

## Wissenschaftliche Lücke

![Die Neuerung von ``brig`` liegt in der Zusammenführung vieler Teildisziplinen.](images/2/science-hole.pdf){#fig:science-hole width=66%}

Die wissenschaftliche Neuerung der vorliegenden Arbeit ist die Zusammenführung
vieler wissenschaftlicher Teildisziplinen, die es nach Wissen des Autors vorher
noch nicht in dieser Kombination gab. Dabei werden viele bestehende Ideen und
Konzepte genommen, um sie in einer Software zu vereinen, die ein versioniertes
und verteiltes Dateisystem implementiert. Dieses soll nicht nur »sicher« (im
weitesten Sinne, siehe [@cpiechula]) sein, sondern auch
für ein Großteil der Anwender benutzbar sein.

Im Konkreten besteht die Neuerung hauptsächlich aus der Kombination folgender Punkte:

* Eine Erweiterung des Datenmodells von ``git``, welches Metadaten von den
  eigentlichen Daten trennt, leere Verzeichnisse sowie umbenannte Pfade nativ
  unterstützt und eine eigene Historie pro Datei mit sich bringt.
* Die Möglichkeit nur die Metadaten zu synchronisieren und die eigentlichen Daten dynamisch
  nachzuladen und nach Anwendungsfall zu »pinnen«. Dateien mit einem *Pin* werden dabei auf dem lokalen Rechner
  gespeichert, Dateien ohne Pin dürfen falls nötig wieder gelöscht werden.
- Ein Containerformat für Verschlüsselung (ähnlich dem Secretbox der freien NaCl[^NACL]
  Bibliothek), welches effizienten wahlfreien Zugriff erlaubt und eine Austauschbarkeit
  des Algorithmus gewährleistet.
- Ein Containerformat zur Kompression, welches blockbasierten, wahlfreien Zugriff und den
  Einsatz verschiedener Algorithmen erlaubt.
- Ein Konzept und Implementierung zur dezentralen Benutzerverwaltung, ohne dass
  ein Nutzer dabei registriert werden muss.
- Verschiedene Ansätze um die Usability zu verbessern ohne an Sicherheit zu
  verlieren (siehe [@sec:usability]).

[^NACL]: Mehr Informationen unter <https://nacl.cr.yp.to/secretbox.html>

## Markt und Wettbewerber

Bereits ein Blick auf Wikipedia[^wiki_filesync] zeigt, dass der momentane Markt
an Dateisynchronisationssoftware sehr unübersichtlich ist. Ein näherer Blick
zeigt, dass die dortigen Softwareprojekte oft nur in Teilaspekten gut
funktionieren und manchmal mit architektonischen Problemen behaftet sind.

[^wiki_filesync]: Siehe <https://en.wikipedia.org/wiki/Comparison_of_file_synchronization_software>

Im Folgenden wird eine unvollständige Übersicht über bekannte
Dateisynchronisationsprogramme gegeben. Davon stehen nicht alle in Konkurrenz zu
``brig``, sind aber zumindest aus Anwendersicht ähnlich.

### Dropbox + Boxcryptor

![Screenshot eines Dropbox--Accounts](images/2/dropbox.png){#fig:scrn-dropbox}

Dropbox (siehe [@fig:scrn-dropbox]) ist der vermutlich bekannteste und am
weitesten verbreitete zentrale Dienst zur Dateisynchronisation. Verschlüsselung
kann man mit Tools wie ``encfs`` (Open--Source, siehe auch [^ENCFS]) oder dem
etwas umfangreicheren, proprietären ``boxcryptor`` nachrüsten. Was das Backend
genau tut ist leider das Geheimnis von Dropbox --- es ist nicht Open--Source.
Mehr Details liefert die Arbeit von Herrn Piechula [@cpiechula].

[^ENCFS]: Mehr Informationen unter <https://de.wikipedia.org/wiki/EncFS>

Die Server von Dropbox stehen in den Vereinigten Staaten von Amerika, was spätestens seit
den Snowden--Enthüllungen Besorgnis um die Sicherheit der Daten weckt. Wie oben
erwähnt, kann diese Problematik durch die Verschlüsselungssoftware ``boxcryptor``
abgemildert werden. Diese kostet aber zusätzlich und benötigt noch einen
zusätzlichen zentralen Keyserver[^KEYSERVER]. Ein weiterer Nachteil ist hier die
Abhängigkeit von der Verfügbarkeit des Dienstes.

[^KEYSERVER]: Mehr Informationen zum Keyserver unter <https://www.boxcryptor.com/de/technischer-\%C3\%BCberblick\#anc09>

Technisch nachteilhaft bei vielen zentralen Diensten ist, dass die Datei »über
den Pazifik« hinweg synchronisiert werden muss, nur um möglicherweise auf dem
Arbeitsrechner »nebenan« anzukommen. Dropbox hat hier nachgerüstet, indem es
nach Möglichkeit direkt über LAN synchronisiert[^DROPBOX_LAN_SYNC].
Nichtsdestotrotz können Kunden nicht mehr synchronisieren, wenn der zentrale
Dienst ausgefallen ist oder den Dienst eingestellt hat.

[^DROPBOX_LAN_SYNC]: <https://www.dropbox.com/de/help/137>

#### ``ownCloud`` / ``nextCloud``

![Screenshot der ownCloud--Weboberfläche](images/2/owncloud.png){#fig:scrn-owncloud}

Eine Alternative zu einem von einem Unternehmen bereitgestellten zentralen
Dienst, ist die Nutzung einer eigenen »Private Cloud« mithilfe der Open--Source
Lösung ``ownCloud`` (siehe [@fig:scrn-owncloud], beziehungsweise dessen Fork
``nextCloud``).
Nutzer installieren auf ihren Servern selbst eine ``ownCloud``--Instanz und stellen
ausreichend Speicherplatz bereit. Vorteilhaft ist also, dass die Daten auf den
eigenen Servern liegen. Nachteilig hingegen, dass das zentrale Modell von Dropbox
lediglich auf eigene Server übertragen wird. Einerseits ist ``ownCloud`` nicht so
stark wie ``brig`` auf Sicherheit fokussiert, andererseits ist die Installation
eines Serversystems für viele Nutzer eine große Hürde und somit zumindest für
den Heimanwender nicht praktikabel.

### ``syncthing``

![Screenshot der Syncthing--Weboberfläche](images/2/syncthing.png){#fig:scrn-syncthing}

Das 2013 veröffentlichte quelloffene ``syncthing`` (siehe
[@fig:scrn-syncthing]) versucht diese zentrale Instanz zu vermeiden, indem die
Daten jeweils von Teilnehmer zu Teilnehmer übertragen werden. Die Dateien
werden in einem speziellen Ordner gelegt, der von ``syncthing`` überwacht wird.
Nach der Installation wird eine einzigartige Client--ID generiert. Über eine
Weboberfläche oder eine native Desktopanwendung kann konfiguriert werden, mit
wem dieser Ordner geteilt werden soll, indem die Client--ID eines anderen
Teilnehmers eingegeben wird.

Es ist allerdings kein vollständiges Peer--to--peer--Netzwerk: Geteilte Dateien
liegen immer als vollständige Kopie bei allen Teilnehmern, welche die Datei
haben. Alternativ ist nur die selektive Synchronisation bestimmter Dateien
möglich. Zwischen den Teilnehmern wird ein Protokoll mit dem Namen *Block
Exchange Protocol*[@borg2015syncthing] etabliert. Dieses sorgt für eine
sichere, differentielle und blockweise Übertragung. 

Praktisch ist auch, dass ``syncthing``--Instanzen mittels eines zentralen
Discovery--Servers entdeckt werden. Nachteilig ist aber die fehlende
Benutzerverwaltung: Man kann nicht festlegen von welchen Nutzern man Änderungen
empfangen will und von welchen nicht. Eingesetzt wird ``syncthing`` zwar auch
gerne von technisch versierten Nutzern, doch existiert auch für Neulinge
ausreichend Dokumentation.

### ``resilio``

![Screenshot der ``resilio``--Weboberfläche](images/2/resilio.png){#fig:scrn-resilio}

Das kommerzielle und proprietäre ``resilio`` (früher *Bittorrent Sync*) nutzt
eine Modifikation[^PROTO_REF] des bekannten und freien BitTorrent Protokoll zur
Übertragung. Vom Feature--Umfang ist es in etwa vergleichbar mit *Syncthing*.
Das Anlegen von verschlüsselten Repositories ist möglich.

[^PROTO_REF]: Siehe auch: <http://blog.bittorrent.com/2016/03/17/%CE%BCtp2-the-evolution-of-an-enterprise-grade-protocol>

Genauere Aussagen über die verwendete Technik kann man aufgrund der
geschlossenen Natur des Programms und der eher vagen Werbeprosa nicht treffen.
Ähnlich zu ``syncthing`` ist allerdings, dass eine Versionsverwaltung nur mittels
eines »Archivordners« vorhanden ist. Gelöschte Dateien werden in diesen
Ordner verschoben und können von dort wiederhergestellt werden.
Etwas mehr Details liefert der Vergleich des *Infinit*--Projekts.[^RESILIO_INFINIT]

[^RESILIO_INFINIT]: <https://infinit.sh/documentation/comparison/bsync>

#### ``git-annex``

![Screenshot des ``git-annex``--Assistenten[^ANNEX_SRC]](images/2/git-annex-assistant.png){#fig:scrn-git-annex}

[^ANNEX_SRC]: Bildquelle: <http://code.178.is/git-annex-is-magic/git-annex-assistant2.png>

Das 2010 erstmals von Joey Hess veröffentlichte ``git-annex``[^ANNEX] geht in
vielerlei Hinsicht einen anderen Weg als die oben genannten Werkzeuge.
Einerseits ist es in der funktionalen Programmiersprache Haskell geschrieben,
andererseits nutzt es intern das Versionsverwaltungssystem ``git``[@git], um
die Metadaten zu den Dateien abzuspeichern, die es verwaltet. Auch werden
Dateien standardmäßig nicht automatisch synchronisiert, hier ist die Grundidee
die Dateien selbst zu »pushen«, beziehungsweise zu »pullen«.

[^ANNEX]: Webpräsenz: <https://git-annex.branchable.com/>

Dieser »Do-it-yourself« Ansatz ist sehr nützlich, um ``git-annex`` als Teil der
eigenen Anwendung einzusetzen. Für den alltäglichen Gebrauch scheint es aber selbst
für erfahrene Anwender zu kompliziert, um es praktikabel einzusetzen.

Trotzdem sollen zwei interessante Features genannt werden, welche auch
für ``brig`` interessant sind:

* *Special Remotes:* »Datenablagen« bei denen ``git-annex`` nicht installiert
  sein muss. Damit können beliebige Cloud--Dienste als Speicher genutzt werden.
+ *N-Copies:* Von wichtigen Dateien kann ``git-annex`` bis zu ``N`` Kopien
  speichern. Versucht man eine Kopie zu löschen, so verweigert ``git-annex``
  dies.

### Weitere Alternativen

Obwohl ``brig`` eine gewisse Ähnlichkeit mit verteilten
Dateisystemen, wie *GlusterFS* hat, wurden diese in der Übersicht weggelassen
--- einerseits aus Gründen der Übersicht, andererseits weil diese andere Ziele
verfolgen und von Heimanwendern kaum genutzt werden. Zudem ist der
Vollständigkeit halber auch OpenPGP zu nennen, was viele Nutzer zum
Verschlüsseln von E-Mails benutzen. Aber auch hier ist der größte Nachteil die
für den Otto Normalbenutzer schwierige Einrichtung und Benutzung.
Auch das freie Projekt ``librevault``[^LIBREVAULT] wurde im Vergleich
ausgelassen, da es sich noch im Alpha--Stadium befindet und bei einem Test
reproduzierbar abstürzte.

[^LIBREVAULT]: Mehr Informationen hier: <https://librevault.com>

### Zusammenfassung

In [@tbl:table-technical-overview] und [@tbl:table-practical-overview] findet
sich zusammenfassend eine Übersicht, mit den wichtigsten
Unterscheidungsmerkmalen. Die Bewertung ist in Punkten wie *»Einfach nutzbar«*
subjektiver Natur.

|                      | **Dezentral**       | **Verschlüsselung im Client**     | **Versionierung**                      |
| -------------------- | ------------------- | -------------------------------- | -------------------------------------- |
| *Dropbox/Boxcryptor* | \xmark              | \xmark                           | \textcolor{YellowOrange}{Rudimentär}   |
| ``ownCloud``         | \xmark              | \xmark                           | \textcolor{YellowOrange}{Rudimentär}   |
| ``syncthing``        | \cmark              | \cmark                           | \textcolor{YellowOrange}{Archivordner} |
| ``resilio``          | \cmark              | \cmark                           | \textcolor{YellowOrange}{Archivordner} |
| ``git-annex``        | \cmark              | \xmark                           | \cmark                                 |
| ``infinit``          | \cmark              | \xmark                           | \xmark                                 |
| ``brig`` *(Prototyp)*  | \cmark            | \cmark                           | \cmark                               |
| ``brig`` *(Ziel)*      | \cmark            | \cmark                           | \cmark                               |


: Vergleich der Software aus technischer Sicht {#tbl:table-technical-overview}


|                      | **FOSS**            | **Einfach nutzbar** | **Einfache Installation**  |
| -------------------- | ------------------- | ------------------- |--------------------------  |
| *Dropbox/Boxcryptor* | \xmark              | \cmark              | \cmark                     |
| ``ownCloud``         | \cmark              | \cmark              | \xmark                     |
| ``syncthing``        | \cmark              | \cmark              | \cmark                     |
| ``resilio``          | \xmark              | \cmark              | \cmark                     |
| ``infinit``          | \xmark              | \xmark              | \cmark                     |
| ``git-annex``        | \cmark              | \xmark              | \xmark                     |
| ``brig`` *(Prototyp)*  | \cmark            | \xmark              | \textcolor{YellowOrange}{Auf Linux} |
| ``brig`` *(Ziel)*      | \cmark            | \cmark              | \cmark                     |


: Vergleich der Software aus Nutzersicht {#tbl:table-practical-overview}

Abschießend kann man sagen, dass ``syncthing`` dem Gedanken hinter ``brig`` am
nächsten kommt. Der Hauptunterschied ist, dass die Basis hinter ``brig`` ein
volles P2P--Netzwerk ist namens ``ipfs`` (dazu später mehr). Wie in den
nächsten Kapiteln ersichtlich ist, eröffnet dieser Unterbau eine Reihe von
Möglichkeiten, die ``syncthing`` nicht bieten kann[^BEISPIELE].

[^BEISPIELE]: Beispielsweise ``git``--ähnliche Versionierung und die Möglichkeit auf alle Daten zuzugreifen, aber nur wenige physikalisch zu speichern. Hierzu später mehr.

## Zielgruppen

Die primären Zielgruppen von ``brig`` sind Unternehmen und Heimanwender.
Aufgrund der starken Ende-zu-Ende Verschlüsselung ist ``brig`` allerdings auch
insbesondere für Berufsgruppen attraktiv, bei denen eine hohe Diskretion
bezüglich Datenschutz gewahrt werden muss. Hier wären in erster Linie
Journalisten, Anwälte, Ärzte mit Schweigepflicht und auch Aktivisten und
politisch verfolgte Minderheiten, zu nennen.

**Unternehmen:** Unternehmen können ``brig`` nutzen, um ihre Daten und
Dokumente intern zu verwalten und zwischen Mitarbeitern zu teilen. Besonders
sicherheitskritische Dateien entgehen so der Lagerung in Cloud--Services oder
der Gefahr von Kopien auf unsicheren Mitarbeiter--Endgeräten. Größere
Unternehmen verwalten dabei oft ein Rechenzentrum in dem firmeninterne
Dokumente gespeichert werden. Von den Nutzern werden diese dann meist mittels
Diensten wie *ownCloud*[^NEXTCLOUD] »händisch« heruntergeladen.

In diesem Fall könnte man ``brig`` im Rechenzentrum und auf allen Endgeräten
installieren. Das Rechenzentrum würde die Datei mit tiefer Versionierung
vorhalten. Endanwender würden alle Daten sehen, aber auf ihrem Gerät nur die
Daten tatsächlich speichern, die sie auch benötigen. Hat beispielsweise ein
Kollege im selben Büro die Datei bereits vorliegen, kann ``brig`` diese dann
direkt transparent vom Endgerät des Kollegen holen. Das »intelligente Routing«
erlaubt den Einsatz von ``brig`` auf Smartphones, Tablets und anderen
speicherplatzlimitierten Geräten. Nutzer, die eine physikalische Kopie der Datei
auf ihrem Gerät haben wollen, können das entsprechende Dokument »pinnen«. Ist
ein Außendienstmitarbeiter beispielsweise im Zug unterwegs, kann er vorher ein
benötigtes Dokument pinnen, damit ``brig`` die Datei persistent verfügbar macht.

[^NEXTCLOUD]: Siehe auch <https://owncloud.org>, bzw. dessen Fork *Nextcloud* <https://nextcloud.com>

**Privatanwender:** Privatanwender können ``brig`` für ihren Datenbestand aus
Fotos, Filmen, Musik und sonstigen Dokumenten nutzen. Ein typischer
Anwendungsfall wäre dabei ein Network--Attached-Storage--Server (NAS), der alle
Dateien mit niedriger Versionierung speichert. Endgeräte, wie Laptops und
Smartphones, würden dann ebenfalls ``brig`` nutzen, aber mit deutlich
geringeren Speicherquotas (maximales Speicherlimit), so dass nur die aktuell
benötigten Dateien physikalisch auf dem Gerät vorhanden sind. Die anderen
Dateien lagern im Netz und können transparent von ``brig`` von anderen
verfügbaren Knoten geholt werden.

**Plattform:** Da ``brig`` auch komplett automatisiert und ohne Interaktion
nutzbar ist, kann es auch als Plattform für andere Anwendungen genutzt
werden, die Dateien sicher austauschen und synchronisieren müssen. Eine
Anwendung in der Industrie 4.0 wäre beispielsweise die Synchronisierung von
Konfigurationsdateien im gesamten Netzwerk.

**Einsatz im öffentlichen Bereich:** Aufgrund der Ende-zu-Ende Verschlüsselung
und einfachen Usability ist eine Nutzung an Schulen, Universitäten sowie auch
in Behörden zum Dokumentenaustausch denkbar. Vorteilhaft wäre für die
jeweiligen Institutionen hierbei vor allem, dass man sich aufgrund des
Open--Source--Modells an keinen Hersteller bindet (Stichwort: *Vendor
Lock--In*) und keine behördlichen Daten in der Cloud landen. Eine praktische
Anwendung im universitärem Bereich wäre die Verteilung von Studienunterlagen an
die Studenten. Mangels einer Standardlösung ist es heutzutage schwierig
Dokumente sicher mit Behörden auszutauschen. ``brig`` könnte hier einen
Standard etablieren und in Zukunft als eine Plattform dienen, um beispielsweise
medizinische Unterlagen mit einem Krankenhaus auszutauschen.

## Einsatszenarien

Basierend auf den vorgestellten Nutzergruppen lassen sich einige konkrete
Einsatszenarien ableiten:

**Synchronisationslösung:** Spiegelung von zwei oder mehr Ordnern und das
Teilen desselben zwischen ein oder mehreren Nutzern. Ein häufiger
Anwendungsfall ist dabei die Synchronisation zwischen mehreren Geräten eines
einzigen Nutzers. Eine selektive Synchronisation bestimmter Ordner ist vorerst
nicht vorgesehen.

**Transferlösung:** Veröffentlichen von Dateien nach Außen mittels eines
*Gateway* über den Browser. Eine beliebige Anzahl an anonymen Teilnehmern
können die Datei herunterladen.

**Versionsverwaltung:** Alle Modifikationen an den bekannten Dateien werden
aufgezeichnet. Bis zu einer bestimmten Tiefe können Dateien
wiederhergestellt werden.

**Backup- und Archivierungslösung:** Es ist möglich Knoten so zu konfigurieren, dass
alle Dateien gepinned werden. Ein solcher Knoten kann dann
anderen Teilnehmern automatisch als Archiv für alte Dateien dienen.

**Verschlüsselter Safe:** Da alle Dateien verschlüsselt sind, müssen sie beim Zugriff
der Software erst entschlüsselt werden. Da die entschlüsselten Daten nur
im Hauptspeicher vorgehalten werden, ist nach Beenden der Software kein
Zugriff mehr möglich.

Es gibt natürlich auch einige Einsatzzwecke, für die ``brig`` weniger geeignet
ist. Diese werden im [@sec:evaluation] beleuchtet, da die dortige Argumentation
teilweise ein Verständnis von der internen Architektur benötigt.

## Annahmen während der Konzeption {#sec:assumptions}

Das Design von ``brig`` basiert auf einigen Annahmen, die im Voraus getroffen
werden mussten:

**Durchschnittliche Netzwerkkonfiguration:** Für den Prototypen wird ein
normales Heimnetzwerk mit mehren Computern angenommen, welche typischerweise
hinter einem NAT liegen. Diese sollen sich mit anderen
Computern in anderen Heimnetzwerken über das Internet austauschen können.

**Durchschnittlicher Arbeitsrechner:** Das Design wurde nicht auf
leistungsschwache Hardware ausgerichtet. Ausgegangen wird von einem »normalen«
Arbeitsrechner. Normal wird hier definiert durch Vorhandensein eines typischen
Mehrkernprozessors aus dem Jahr 2008 oder später und mindestens 2 Gigabyte
Arbeitsspeicher. Der Internetanschluss sollte ein Download von mindestens
4 Mbit/s[^ANSCHLUSS_DURCHSCHNITT] besitzen und ein Upload von 1 Mbit/s.

[^ANSCHLUSS_DURCHSCHNITT]: Der Durchschnitt im Jahr 2016 beträgt bereits etwa
14 Mbit/s. Quelle: Statista, [@statistaDownload].

**Stabilität von ``ipfs:``** Es wird angenommen, dass ``ipfs`` stetig
weiterentwickelt wird und im momentanen Zustand keine gravierenden
Sicherheitsmängel enthält. Zudem wird angenommen, dass es für die Zwecke von ``brig``
ausreichend hohe Performanz bietet.

**Keine Kollision der Prüfsummen:** ``brig`` kann (genau wie ``ipfs``) Dateien
nicht auseinander halten, die einen unterschiedlichen Inhalt besitzen, aber die
selbe Prüfsumme erzeugen. Auch wenn dieser Fall in der Theorie eintreten kann,
so ist dieser extrem schwer zu erreichen. Der von
``ipfs`` standardmäßig verwendete Algorithmus ist *sha256*[^SHA256], welcher eine Prüfsumme
von 256 Bit Länge liefert. Wie in [@eq:hash-collision] gezeigt, müssten trotz des
Geburtstagsparadoxons[@wiki:geburtstagsparadoxon] unpraktikabel viele
Prüfsummen erzeugt werden, um eine Kollisionswahrscheinlichkeit von $0.1\%$ zu
erreichen, selbst wenn man sehr optimistisch annimmt, dass die Berechnung einer
einzigen Prüfsumme nur eine Pikosekunde dauert.

[^SHA256]: Ein Prüfsummenalgorithmus der SHA-2 Familie. Siehe auch: <https://de.wikipedia.org/wiki/SHA-2>

$$(\frac{1}{1000} \times 2^{\frac{256}{2}}) \times 10^{-12}s \simeq 10^{35.5} \times 10^{-12}s \simeq 10^{15} \text{Jahre}$$ {#eq:hash-collision}
