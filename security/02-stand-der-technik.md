# Stand von Wissenschaft und Technik

## Sicherheit und Usability von Dateiverteilungssystemen

### Allgemeines

Zentrale und dezentrale Systeme sind die Basis für den Austausch von
Informationen. Ob ein System zentral oder dezentral fungiert ist nicht immer
klar abgrenzbar. Oft kommen auch hybride Systeme zum Einsatz, welche zwar
dezentral funktionieren, jedoch eine zentrale Instanz benötigen, hier wäre
beispielsweise das *Torrent*--Konzept zu nennen. Weitere Informationen hierzu
sind unter [@cpahl] zu finden. 

### Der »Sicherheitsbegriff« {#sec:sicherheit}

Betrachten man die »Sicherheit« von Dateiverteilungssystemen, so müssen
verschiedene Teilaspekte betrachten werden. Leider ist das Umfeld der
Sicherheit sehr groß und die Begrifflichkeiten nicht immer eindeutig definiert.
In der Fachliteratur (vgl. [@pauly2004netzwerk]) spricht man bei »Sicherheit«
oft von den folgenden fünf Sicherheitsaspekten:

* Vertraulichkeit: Schutz der Daten vor Zugriff durch Dritte.
* Integrität: Schutz der Daten vor Manipulation.
* Authentifizierung: Eindeutige Identifikation von Benutzern.
* Autorisierung: Definiert die Zugangs-- und Zugriffssteuerung auf Dienste.
* Verfügbarkeit: Dienste stehen legitimen Benutzern tatsächlich zur Verfügung.

Dies sind auch die Sicherheitsaspekte die bei der Verwendung von
Cloud--Speicher--Anbietern zu tragen kommen. Um diese zu auf technischer Ebene
realisieren, müssen neben unterschiedliche Kryptographische Komponenten
verwendet werden.

### Angriffe und Bedrohungen

Die Sicherheit eines System lässt sich nicht mit einem einfachen »ja« oder
»nein« beantworten. Betrachtet man ein System bezüglich seiner Sicherheit, so
muss auch genau definiert werden, gegen welches »Angriffsszenario« ein System
»sicher« ist. Auch ein System das aus kryptographischer Sicht als »sicher« zu
betrachten wäre, kann im einfachsten Fall, durch die Weitergabe von Zugangsdaten
an Dritte, kompromittiert werden.

![Scherzhafte Darstellung eines möglichen Angriff auf eine Festplattenverschlüsselung mit optimalem Kosten/Nutzen--Verhältnis.[^src-xkcd]](images/security.png){#fig:img-security width=70%}

[^src-xkcd]:Quelle: <http://imgs.xkcd.com/comics/security.png>

Neben dem technischen Ansatz beim »Angriff« auf ein System, gib es auch die
psychologische Komponente, den Menschen, welcher wahrscheinlich die größte
Schwachstelle in den meisten Systemen darstellt.

Beim technischen Ansatz werden in der Regel Fehler in der Software oder
Infrastruktur ausgenutzt um sich unbefugten Zugriff auf Informationen zu
verschaffen.

Beim nicht--technischen »Angriff« wird der Benutzer auf »psychologischer Ebene«
manipuliert und mit sogenannten »Social Hacking«--, auch »Social
Engineering«--Methoden dazu verleitet beispielsweise sein Passwort
weiterzugeben. Auch der Einsatz von »Phishing« (TODO: Ref), ist eine Variante
von »Social Engineering«. [@fig:img-security] zeigt scherzhaft eine weitere
Variante für welche Menschen anfällig sind.

Um »Sicherheit« zu gewährleisten, ist es wichtig ein System im »Ganzen« zu
betrachten. Die Implementierung bestimmter Sicherheitsfeatures ist nur die
technische Maßnahme. Der Benutzer eines System erwartet in erster Linie
Funktionalität und möchte sich in den wenigsten Fällen mit dem System oder der
Sicherheit des Systems auseinander Setzen. Benutzer sind oft nicht genug
sensibilisiert was den Datenschutz oder auch die Gefahren und Konsequenzen bei
einem Sicherheitsproblem sind.

Weiterhin sollte bedacht werden, dass die Definition eins »sicheren« System in
der Regel ein Kompromiss aus den folgenden Punkten ist:

* Finanzieller Aufwand 
* Sicherheit
* Benutzbarkeit/Benutzerfreundlichkeit


### Datenaustausch über zentrale Lösungen

#### Funktionsweise zentraler Dienste

Zentrale Dienste klassifizieren sich im Kontext dieser Arbeit durch die
Eigenschaft, dass es eine zentrale Instanz gibt, welche zum Austausch der Daten
benötigt wird. Dies sind in den meisten Fällen die Server des
Cloud--Speicher--Anbieter, welche für die Kommunikation und Speicherung der
Daten verantwortlich sind.

![Datensynchronisation über zentrale Cloud--Speicher--Dienste, wie beispielsweise
*Dropbox*.](images/cloud.png){#fig:img-cloud width=80%}

[@fig:img-cloud] zeigt schematisch das Konzept beim Austausch von Daten über
einen Cloud--Speicher--Dienst. Die Daten,des Benutzers, werden hierbei mit einer
»zentrale« Stelle synchronisiert. In der Regel legt der Benutzer »Ordner« fest,
welcher nach Installation einer Client--Software (des jeweiligen Anbieters) und
der Erstellung eines Accounts mit dem Cloud--Speicher des Anbieters
synchronisiert wird.

Dieser »Ordner« lässt sich dann beispielsweise auf weitere Geräte des Benutzer
synchronisieren. Weiterhin gibt es in der Regel die Möglichkeit Dateien mit
anderen Benutzern zu teilen. Welche genauen Einstellungen sich vornehmen lassen
und wie feingranular die die Benutzerverwaltung und Möglichkeiten beim
Synchronisieren sind, ist von dem jeweiligen Cloud--Speicher--Anbieter abhängig.

Mittlerweile werben die Anbieter damit, dass sie »starke Verschlüsselung«
verwenden und die Daten »sicher« in der »Cloud« sind. Spätestens seit den
Snowden--Enthüllungen ist es jedoch klar, dass die Anbieter dazu gezwungen
werden können die Daten eines Benutzers herauszugeben.

#### Synchronisations--Software

Die verwendete Software zum Synchronisation ist wieder vom jeweiligen Anbieter
abhängig. Das Problem hierbei ist, dass die Software in der Regel proprietär ist
und der Benutzer weder die genaue Funktionalität noch das Vorhandensein von
Hintertüren ausschließen kann. Die Software liegt in dem meisten Fälle für
verschiedene Plattformen bereit. Weiterhin ermöglichen Anbieter auch Zugriff auf
die Daten mittels Webbrowser--Interface.

#### Sicherheit von Cloud--Speicher--Anbietern

Es ist sehr schwierig die »Sicherheit« der Cloud--Speicher--Anbieter realistisch
zu bewerten, da sowohl die Infrastruktur als auch die verwendete Software
intransparent und proprietär ist.

Die Daten werden laut Aussagen der Hersteller[^applesec][^dropboxsec]
verschlüsselt übertragen und mittlerweile auch verschlüsselt gespeichert.

[^applesec]:Apple iCloud Security: <https://support.apple.com/en-us/HT202303>
[^dropboxsec]:Dropbox Security: <https://www.dropbox.com/security>

Beim Einsatz der Cloud--Speicher--Dienste hängt die Sicherheit der Daten somit
in erster Linie vom Dienstanbieter ab. Beim *iCloud*--Dienst von Apple
beispielsweise werden die Daten verschlüsselt bei Drittanbietern wie der *Amazon
S3*-- oder *Windows Azure*--Cloud gespeichert[^ios-secguide]. Die Metadaten und
kryptographische Schlüssel verwaltet Apple auf seinen eigenen Servern. Dropbox
hat laut Medienberichten mittlerweile von der *Amazon*--Cloud auf eine eigene
Infrastruktur migriert[^dropbox-s3-own].

[^dropbox-s3-own]:Dropbox Exodus Amazon Cloud Empire: <http://www.wired.com/2016/03/epic-story-dropboxs-exodus-amazon-cloud-empire/>
[^ios-secguide]: Apple iOS Security: <http://www.apple.com/business/docs/iOS_Security_Guide.pdf>

Das Problem hierbei ist die Umsetzung der Daten--Verschlüsselung der gängigen
Cloud--Speicher--Anbieter. Anbieter wie *Dropbox* verschlüsseln laut eigener
Aussage die Daten in der Cloud nach aktuellen Sicherheitsstandards. Das Problem
im Fall von *Dropbox* ist jedoch, dass *Dropbox* und nicht der Endbenutzer der
Schlüsselinhaber ist. Es ist also, auch wenn es laut internen
Dropbox--Richtlinien verboten ist, möglich dass Mitarbeiter beziehungsweise
dritte Parteien die Daten des Nutzers einsehen können (vgl. [@ko2015cloud] S.
103 ff.).

Ein weiteres Problem ist, dass ein Cloud--Speicher--Anbieter aufgrund seiner
»zentralen Lage« ein gutes Angriffsziel bildet. Erst kürzlich wurde bekannt,
dass Angreifer im Jahr 2012 ungefähr 70 Millionen Zugangsdaten[^db-dataleak]
entwendet haben. Hat ein Angreifer also die Zugangsdaten erbeutet, bringt die
Verschlüsselung die der Cloud--Dienst betreibt in diesem Fall nichts. Die
gestohlenen Passwörter waren nicht im Klartext einsehbar, moderne
Angriffsmöglichkeiten auf Passwörter zeigen jedoch, dass das nichtsdestotrotz
ein großes Problem ist. (siehe hierzu TODO: Sicherheit von Passwörtern)

[^db-dataleak]: Dropbox <http://www.telegraph.co.uk/technology/2016/08/31/dropbox-hackers-stole-70-million-passwords-and-email-addresses/>

Abhilfe könnte in diesem Fall eine zusätzliche Verschlüsselung auf Seiten des
Nutzers helfen, jedoch ist die Software hier für den Endverbraucher oft zu
kompliziert, aufgrund Fehlern in der Implementierung nicht optimal geeignet
(EncFS Audit[^encfsaudit]) oder proprietär (Boxcryptor[^boxcryptor]).

[^encfsaudit]:  EncFS Audit: <https://defuse.ca/audits/encfs.htm>
[^boxcryptor]: Boxcryptor: <https://de.wikipedia.org/wiki/Boxcryptor>

Den meisten Anbietern muss man Vertrauen, dass diese mit den Daten und
Schlüsseln sorgsam umgehen. Auch wenn sich viele Anbieter wie beispielsweise
*Dropbox* bemühen, aus den Fehlern der Vergangenheit zu lernen und verbesserte
Sicherheitsmechanismen wie beispielsweise Zwei--Faktor--Authentifizierung[^2fa] in
ihre Software zu integrieren, bleibt jedoch die Krux der Intransparenz und der
proprietären Software. Es ist nicht ohne weiteres Möglich die »Sicherheit« der
Client--Software zu validieren.

[^2fa]: Zwei--Faktor--Authentifizierung: <https://de.wikipedia.org/wiki/Zwei-Faktor-Authentifizierung>

2011 hat der Sicherheitsforscher *Derek Newton* den
Authentifizierungsmechanismus von *Dropbox* kritisiert. Nach einmaligem
»Registrieren« und Einrichten des *Dropbox*--Client, werden für die
Synchronisation keine weiteren Zugangsdaten mehr benötigt. Der
Authentifizierungsmechanismus benötigt nur ein sogenanntes
»Authentifizierungs--Token« (diese wird dem Client nach der Registrierung vom
Server zugewiesen), die sogenannte *HOST_ID*. Mit dieser authentifiziert sich
der *Dropbox*--Client bei zukünftigen Synchronisationsvorgängen gegenüber dem
Dropbox--Service.

Ein großes Problem war hierbei auch, dass die *HOST_ID* unverschlüsselt in
einer Konfigurationsdatei (sqlite3--Datenkbank) abgelegt war. Diese *ID* bleibt
anscheinend auch nach Änderung der Zugangsdaten weiterhin bestehen.

[^dereknewton]: Dropbox authentication: »insecure by design«: <http://dereknewton.com/2011/04/dropbox-authentication-static-host-ids/>

Ein weitere Arbeit aus dem Jahr 2011 beschreibt verschiedene Angriffsszenarien und Probleme welche die Datensicherheit und Privatsphäre von Cloud--Speicher--Benutzern in Frage stellen (vgl. [@mulazzani2011dark]). 

2013 haben weitere Sicherheitsforscher den Dropbox--Client mittels *Reverse
Engineering* analysiert. Ab der Version 1.2.48 wird die *HOST_ID* in einer
verschlüsselten *sqlite3*--Datenbank abgespeichert. Diese »Nachbesserung«
seitens *Dropbox* war nicht besonders effektiv, da sich die Schlüssel zum
entschlüsseln weiterhin auf dem Client--PC befinden. Zusätzlich wird für die
Authentifizierung in »neueren« *Dropbox*--Versionen ein *HOST_INT*--Wert
benötigt, welcher ebenfalls vom Client--PC »extrahiert« werden kann.

Mittels dieser beiden Werte kann die die 2F--Authentifizierung, wie sie von
*Dropbox* implementiert ist, umgangen werden. Die Client--API verwendet
anscheinend keine 2F--Authentifizierung. Darüber hinaus lassen sich auf Basis
der beiden  Parameter sogenannte »Autologin--URLs« generieren. Den Forschen ist
es auch gelungen einen Open--Source--Prototypen zu entwickeln, für weitere
Details vgl. [@kholia2013looking] beziehungsweise siehe Vortag *USENIX Open
Access Content*[^usenix].

[^usenix]: USENIX Vortrag »Looking Inside the (Drop) Box«:<https://www.usenix.org/conference/woot13/workshop-program/presentation/kholia>

2015 wurde bekannt, dass die vorherrschenden Cloud--Speicher--Anbieter für
sogenannte »Man--In--The--Cloud«--Angriffe anfällig sind. Die bereits im Jahr
2011 entdeckten »Schwächen« bei der Authentifizierung von *Dropbox* sind
weiterhin present und auch auf andere Cloud--Speicher--Anbieter übertragbar. Um
die Client--Software gegenüber dem Cloud--Speicher--Dienst zu authentifizieren,
werden wie auch bei *Dropbox*, Authentifizierungs--Token verwendet. Für den
Angriff haben die Forscher ein sogenanntes »Switcher«--Programm entwickelt,
welches in der Lage ist ein Authentifizierungs--Token auf dem Computer des
potentiellen Opfers auszutauschen. [@fig:img-mitc] zeigt den Ablauf eines
möglichen »Man--In--The--Cloud«--Angriffs.

![»Quick Double Switch Attack Flow«--Man in the Cloud--Angriff.](images/mitc.png){#fig:img-mitc width=90%}

1. Der Angreifer platziert den »Switcher« auf dem Rechner des Opfers
   (beispielsweise mittels Social Engeneering oder Phishing--Methoden)
2. Der ,,Switcher'' ändert den Token vom Benutzers. Hierbei wird der
   Synchronisationssoftware der Token vom Angreifer »injiziert« (first switch)
   und anschließend das Orignal--Token vom Opfer in den nun vom Angreifer
   kontrollierten Synchronisationsordner kopiert.  (a) wird inaktiv, (b) wird
   aktiv.
3. Die Synchronisationssoftware synchronisiert nun den Token des Opfers zum
   Angreifer (b).
4. Der Angreifer kann sich nun mittels des »gestohlenen« Tokens mit dem Account
   des Opfers synchronisieren (c).
5. Anschließend wird der ,,Switcher'' noch einmal ausgeführt um beim Opfer
   wieder den ursprünglichen Synchronisationszustand herzustellen (second switch).

Der Ablauf in [@fig:img-mitc] zeigt den »Quick Double Switch Attack Flow«. Im
Bericht der *IMPERVA -- Hacker Intelligence Initiative* werden noch weitere
Angriffe auf Basis dieses Verfahrens aufgezeigt (vgl. [@mitcref]). 

Neben dem *Dropbox*--Client auch die Synchronisationsapplikationen Microsoft
OneDrive, Box und Google Drive untersucht. Diese verwenden zum authentifizieren
den offenen *OAuth 2.0* Authentifizierung--Standard, *Dropbox* hingegen ein
proprietäres Verfahren. Das problematisch bei *Dropbox* ist, dass die »gesamte
Sicherheit« von der *HOST_ID* (und *HOST_INT*) abhängt. Hat ein Angreifer
dieser erbeutet, so kann er auch über den *Dropbox*--Webzugang sämtliche
administrativen Aufgaben durchführen.

Laut Meinung der Autoren von »brig«, sowie auch vieler Sicherheitsexperten, wird
beim Einsatz proprietärer Software die Sicherheit untergraben, da bei
proprietärer Software explizit eingebaute Hintertüren nicht ausgeschlossen
werden können und es auch keine einfache Möglichkeit der Prüfung auf solche
durch den Endbenutzer gibt.

Insbesondere hat die Freilegung der Snowden--Dokumente weiterhin zu der
Schlussfolgerung geführt, dass der Einsatz von »Freier Software«
empfehlenswerter ist. Bekannte Sicherheitsexperten wie *Bruce
Schneier*[^bruce1][^bruce2] oder auch *Rüdiger Weis* sehen »Freie Software« als
eine der wenigen Möglichkeiten dem Überwachungswahn von Geheimdiensten (oder
auch anderen Institutionen) entgegen zu wirken. Weiterhin kann Kryptographie
dank »Freier Software« von unabhängigen Sicherheitsforschern bewertet werden.

Auch wenn für viele Benutzer die Geheimhaltung der Software und Infrastruktur
auf den ersten Blick als »sicherer« erscheinen mag, widerspricht Sie
dem Kerckhoffs’schen Prinzip, bei welchem die Sicherheit eines System nur von der
Geheimhaltung des Schlüssels, jedoch nicht von der Geheimhaltung weiterer
Systemelementen abhängen sollte. Die Vergangenheit hat beispielsweise beim
GSM--Standard oder DVD--Kopierschutz »CSS«[^css] gezeigt, dass durch die
Geheimhaltung von Systemkomponenten erfolgreiche Angriffe, höchstens erschwert,
jedoch nicht unterbunden werden können (vgl. [@spitz2011kryptographie],
[@ertel2012angewandte, S. 23]).

[^css]: Cryptanalysis of Contents Scrambling System: <http://www.cs.cmu.edu/~dst/DeCSS/FrankStevenson/analysis.html>

[^bruce1]: Defending Against Crypto Backdoors: <https://www.schneier.com/blog/archives/2013/09/how_to_remain_s.html>
[^bruce2]: How to Remain Secure Against the NSA: <https://www.schneier.com/blog/archives/2013/10/defending_again_1.html>
[^weis]: Krypto nach Snowden | 19. Netzpolitischer Abend: <https://www.youtube.com/watch?v=T_ojwHReMkM>

Abgesehen von den Snowden--Enthüllungen, gibt es für den Endverbraucher viel
näherliegender Gefahren, welche die Daten und Privatsphäre gefährden. Neben den
soeben genannten *Dropbox* Datenleck, welches rund 70 Millionen Benutzerdaten
betraf und über fast vier Jahre unentdeckt war, gibt es immer wieder Probleme
mit zentralen Diensten. Ein Ausschnitt von bekannt gewordenen Vorfällen in
letzter Zeit:

**Datenlecks:**

* Datenleck bei Dropbox[^dropboxdatenleck]
* Google Drive Datenleck[^gdrive]
* Microsoft OneDrive Datenleck[^msleck]
* 7 Millionen Zugangsdaten im Umlauf (unbestätigt)[^zugangsdaten]
* *iCloud*--Hack auf private Fotos von Prominenten[^fappening]

**Weitere Probleme:**

* Dropbox Client greift auf Daten außerhalb des Sync--Ordners zu[^dropboxschnueffel].
* Microsoft synchronisiert Bitlocker--Schlüssel (Festplattenverschlüsselung) standardmäßig in die Cloud[^bitlockercloud]
* Dropbox akzeptiert beliebige Passwörter über mehrere Stunden[^droppass]
* Ausfallzeit über zwei Stunden[^dropboxausfall]


[^fappening]: iCloud--Hack: <https://de.wikipedia.org/wiki/Hackerangriff_auf_private_Fotos_von_Prominenten_2014> 
[^bitlockercloud]: Bitlocker Cloud--Sync:  <http://arstechnica.com/information-technology/2015/12/microsoft-may-have-your-encryption-key-heres-how-to-take-it-back/>
[^droppass]: Dropbox--Auth--Bug: <https://www.heise.de/security/meldung/Dropbox-akzeptierte-vier-Stunden-lang-beliebige-Passwoerter-1264100.html>
[^msleck]: OneDrive Datenleck: <https://www.heise.de/security/meldung/Microsoft-dichtet-OneDrive-Links-ab-2227485.html>
[^gdrive]: Google Drive Datenleck: <https://www.heise.de/security/meldung/Auch-Google-schliesst-Datenleck-im-Cloud-Speicher-2243366.html>
[^dropboxdatenleck]: Dropbox Datenleck: <https://www.heise.de/security/meldung/Dropbox-bestaetigt-Datenleck-1656798.html>
[^zugangsdaten]: 7 Mio. Zugangsdaten im Umlauf: <https://www.heise.de/security/meldung/Angeblich-7-Millionen-Dropbox-Passwoerter-im-Umlauf-2423684.html>
[^dropboxschnueffel]: Dropbox--Schnüffelverdacht: <http://www.heise.de/security/meldung/Dropbox-unter-Schnueffelverdacht-2565990.html>
[^dropboxausfall]: Dropbox--Ausfall: <https://www.heise.de/security/meldung/Dropbox-Ausfall-war-kein-Angriff-2083688.html>

Auch wenn viele Unternehmen ihre Priorität nicht in der Sicherung ihrer Daten
sehen mögen, sollten die Folgekosten von Datenlecks nicht unterschätzt werden.
Laut einer jährlich durchgeführten Studie vom *Ponemon Institute* belaufen sich
die Kosten im Zusammenhang mit Datenlecks auf mehrere Millionen Dollar (vgl.
[@ponemon]), die Tendenz ist von Jahr zu Jahr steigend wenn man die Berichte aus
dem jeweiligem Vorjahr zuzieht.

Abgesehen von den Datenlecks verschiedener Cloud--Speicher--Anbieter, haben
zentrale Dienste immer wieder Probleme mit größeren Datenlecks. Welcher Dienst
und Daten betroffen sind, sammelt der der Sicherheitsforscher *Troy Hunt* auf
seiner Webseite[^haveibeenpwned].

[^haveibeenpwned]: Gesammelte Informationen zu Datenlecks: <https://haveibeenpwned.com/>

### Private Cloud

Weiterhin gibt es bei der Cloud--Speicher--Lösung auch die Möglichkeit einen
eigenen »Cloud--Speicher« aufzusetzen. Hierfür wird oft die Open--Source--Lösung
*Owncloud* genommen. Der Nachteil hierbei ist, dass der Benutzer selbst für die
Bereitstellung der Infrastruktur verantwortlich ist. Für Unternehmen mag die
*Owncloud* durchaus interessant sein, für die meisten Privatanwender ist der
Aufwand höchstwahrscheinlich zu hoch. Weiterhin haben Endanwender in der Regel
nicht das nötige Know--How, welches für das Betreiben eines
Cloud--Speicher--Dienstes essentiell ist.

\newpage

### Datenaustausch über dezentrale Lösungen

#### Funktionsweise dezentraler Dienste

Der dezentrale Bereich klassifiziert sich durch den Dateiaustausch, welcher in
der Regel *ohne* eine zentrale Instanz auskommt. Es handelt es sich hierbei um
Systeme aus dem Bereich des Peer-to-Peer--Models. Eins der frühen Peer--to--peer
Protokolle ist das *Napster*--Protokoll der gleichnamigen Anwendung *Napster*,
welche Ende der 90' Jahre für den Tausch von Musik verwendet wurde. Später sind
weitere Peer--to--peer--Protokolle wie das Multisource File Transfer Protocol
oderdas BitTorrent--Protokoll .

[@fig:img-p2p] zeigt schematisch den Austausch von Daten in einem dezentralen
Netzwerk. Bei einem dezentralem System liegen die Daten in der Regel nur auf den
Rechnern der Benutzer. Die Speicherung auf zentralen Speicher--Servern wie bei
den zentralen Diensten ist nicht vorgesehen, jedoch aufgrund der Architektur
realisierbar.

Bei der Nutzung eines dezentralen Netzwerks zum Austausch beziehungswiese zur
Synchronisation von Daten musst der Benutzer in der Regel eine spezielle
Software installieren und einen »Synchronisationsordner«, wie bei den zentralen
Diensten, definieren welcher dem Netzwerk »bekannt« gemacht werden soll. Je nach
eingesetztem Protokoll, variiert die Funktionsweise und Sicherheit.

![Dezentraler Datenaustausch über Peer--to-Peer--Kommunikation. Es existiert
keine zetrale Instanz, jeder Peer im Netzwerk ist
»gleichberechtigt«.](images/p2p.png){#fig:img-p2p width=80%}

Die dezentralen Systeme unterliegen in der Regel keiner Regulierung durch eine
zentrale Instanz. Je nach verwendeter Technologie zum Datenaustausch, existieren
sogenannte »rendezvous hosts« in einem dezentralen Netzwerk, welche für die
initiale Konfiguration und als »Einstiegspunkt« benötigt werden. Hier
unterscheiden sich die verschiedenen Protokolle und Netzwerke voneinander. 

Ein der bekannter Vertreter der P2P--Protkolle ist BitTorrent[^bittorrent]. Das
Protokoll kommt beispielsweise bei der Verbreitung von Software, Computerspielen
(HumblieIndieBundle.com), dem Blender Movie--Projekten, Linux--Distributionen
,der Verteilung von Updates (Windows 10), bei diversen
Spieleherstellern und auch anderen Anwendungen zum Einsatz[^btusage]. 

[^btusage]: BitTorrent Einsatzgebiete: <https://en.wikipedia.org/wiki/BitTorrent#Adoption>

Ein Vorteil bei den dezentralen System ist, dass es im Vergleich zu zentralen
Architekturen keinen »Single--Point--Of--Failure« gibt. Ein weiterer Unterschied
zu zentralen Lösung ist ist bei dezentralen Netzwerken der »Datenfluss«. Die
Daten werden nicht von einer zentralen Instanz »besorgt«, sondern liegen im
jeweiligen Netzwerk, verteilt auf die Netzwerkteilnehmer (peers). Jeder
Teilnehmer des Netzwerks fungiert in der Regel als Client und als Server. Daten
werden beim Austausch nicht zwangsläufig von einem »einzelnen« Teilnehmer
geladen, sondern von einer Gruppe aus Teilnehmern welche die gleiche Datei
besitzen, siehe [@fig:img-swarm]

![Zeigt einen »Swarm«. *Alice* lädt die Datei »image.iso« von mehreren
Teilnehmern gleichzeitig, die Datei »mydog.png« jedoch nur von
*Dan*.](images/distsync.png){#fig:img-swarm width=80%}


Aktuell verbreitete Peer--to--peer Protokolle:

* Bittorrent (Filesharing allgemein)
* Skype Protokol (VOIP--Telephonie)

Früher eingesetzte Peer--to--peer Filesharing--Protokolle:

* Direct Connect
* Multisource File Transfer Protocol (Einsatz: eDonkey2000, Overnet)
* Fasttrack (Einsatz: Kazaa, Grokster, IMesh, Morpheus file sharing)
* Gnutella Protokoll (Einsatz: Gnutella Client)
* Napster--Protokoll


#### Synchronisations--Software

Zu den Vertretern der etablierten dezentralen Systeme gibt es vergleichsweise zu
den Cloud--Speicher--Anbietern nur wenige Produkte, welche für die
Synchronisation von Daten beziehungsweise den Austausch von Dokumenten
eingesetzt werden können. Bekannten Lösungen sind:

* Resilio (ehem. BitTorrent-Sync, proprietär)
* Infinit (proprietär, [@quintard2012towards])
* git--annex (Open--Source)
* Syncthing (Open--Source)
* Librevault (Open--Source)

#### Sicherheit von Peer--to--peer Synchronisationsanwendungen

Bei den bekannten Vertretern des BitTorrent--Netzwerks wie dem
BitTorrent--Client werden die Daten in der Regel unverschlüsselt übertragen und
gespeichert. Auch eine Authentifizierung finden in der Regel nicht statt. Die
Benutzer geben die Daten mit ihrem »Synchronisationsordner« automatisch für alle
Teilnehmer des Netzwerks frei zum teilen.

Wie bei zentralen Diensten, ist es auch bei dezentralen Netzwerken schwierig die
»Sicherheit« zu beurteilen. Diesen hängt in diesem Fall nicht zwangsläufig von
einem Dienst--Anbieter ab, sondern vielmehr von der Umsetzung der Software, der
Infrastruktur des Netzwerks, der »Sicherung der Daten« (verschlüsselte
Speicherung, verschlüsselte Übertragung) und den Möglichkeiten, welche es
ermöglichen einen Kommunikationspartner zu authentifizieren. 

**Resilio--Sync** (ehemals Bittorrent--Sync), verwendete eine modifizierte
Variante des BitTorrent--Protokolls[^btsyncprotocol]. Alle Daten werden laut
Hersteller zusätzlich symmetrisch mit AES--128 verschlüsselt übertragen. Die
getestete Version entspricht der Standardversion welche kostenfrei benutzbar
ist, jedoch nur einen eingeschränkten Funktionsumfang bietet. Weiterhin gibt es
eine »Pro«--Version welche »selektive und kollaborative Synchronisation«
ermöglicht. 

[^btsyncprotocol]:Inoffizielle Protokoll Spezifikation <https://forum.resilio.com/topic/21338-inofficial-protocol-specification/>

Bei Resilio (Webbasierte GUI) werden Daten werden hier mittels verschiedenen
»Schlüsseln« synchronisiert. Beim Anlegen eines Synchronisationsordners werden
dem Benutzer erscheinen dem Benutzer folgende »Schlüssel«, über welche er den
Synchronisationsordner mit anderen Synchronisationsordnern teilen kann: 

Schlüssel für: 

* Nur Leserechte
* Lese-- und Schreibrechte
* Verschlüsselte Speicherung

Mittels dieser »Schlüssel« lässt sich die »Synchronisation« mit anderen
Peers/Synchronisationsordnern steuern. Neue Peers können über das Teilen eines
Schlüssels hinzugefügt werden. Die Anwendung macht einen undurchsichtigen
Eindruck. Eine 2014 durchgeführte Analyse von *BitTorrent*--Sync auf der
*Hackito* kommt aufgrund mehrere Sicherheits-- und Designprobleme zum
Einschätzung[^hackito] das *BitTorrent*--Sync nicht für sensitive Daten
verwendet werden sollte.

[^hackito]: Security analysis of BTsync: <http://2014.hackitoergosum.org/bittorrentsync-security-privacy-analysis-hackito-session-results/>

**Infinit** ist eine weitere proprietäre Lösung welche es ermöglicht Dateien
zwischen verschiedenen Benutzern, ohne Server--Instanz, auszutauschen. Die Basis
für Infinit stellt [@quintard2012towards] dar. Bei Infinit findet bei der
Installation der Anwendung eine »Registrierung« statt. Diese Daten
(Benutzername/E--Mail--Addresse) können anschließen verwendet werden um mit der
Anwendung andere Infinit--Partner zu finden oder von diesen gefunden zu werden.
Anschließend kann eine Datei über ein *Drag & Drop*--Menü an den gefundenen
Partner gesendet werden. Es ist unklar ob Daten/Metadaten ans die
Infinit--Plattform übertragen werden. Infinit wirbt mit »point--to--point
encryption« und »bank-level encryption algorithms such as AES-256 and RSA 2048«.
Eine Authentifizierung des Kommunikationspartners findet rudimentär anhand vom
Benutzernamen/E--Mail statt. Daten werden lokal nicht verschlüsselt.


**Syncthing** basiert auf einem eigens entwickeltem Protokol, dem *Block Exchange
Protocol*[^bep]. Der Syncthing--Client (Web--GUI Variante) ermöglicht das
Hinzufügen von »Synchronisationsordner« und »Remote Device«. Diese GUI ist
Standardmäßig von außen nicht zugreifbar, da sie auf »localhost only« läuft. 

[^bep]: Block exchange protocol: <https://docs.syncthing.net/specs/bep-v1.html>

Die Peers werden durch eine eindeutige *Device ID* identifiziert. Diese leitet
sich aus einen asymmetrischen Schlüsselpaar (3072 bit RSA) ab, welches beim
ersten Start der Anwendung erstellt wird. Abgelegt wird ein privater Schlüssel
und ein selbst signiertes Zertifikat. Der private Schlüssel scheint nicht weiter
geschützt zu sein:

~~~bash
freya :: ~/.config/syncthing » cat key.pem 
	-----BEGIN EC PRIVATE KEY-----
	MIGkAgEBBDCQIMwVr730vKzoyHCbIqDoxNxAjKvdFYL+XnKk65GurCc9q2qiZJEU
	zMNWSD+N/eCgBwYFK4EEACKhZANiAASJ0YZUMQVAuW8tT7DvuLFkanCw2gpgD1DE
	P69XHqMS0MFg6ZwMqzvlV65WXQMOHfsNw/xKMagSGlyTh17W/Up0y2PPygUlj6H1
	d0vMI1OguPD9heeqYjU67R4GxlHMj54=
	-----END EC PRIVATE KEY-----
~~~

Das selbst signierte Zertifikat bringt keine zusätzliche Sicherheit, ermöglicht
jedoch die Nutzung von Transport Layer Security (TLS). Diese *ID* ist für jeden
Teilnehmer eindeutig (aufgrund der asymmetrischen Kryptographie). Sie besteht
aus einer kryptographischen Prüfsumme (SHA--256) eines eindeutigen
kryptographischen Zertifikates, welches für die verschlüsselte Kommunikation und
Authentifizierung zwischen den einzelnen Peers verwendet wird.

Weiterhin ist das aktuell Design für *Discovery Spoofing* anfällig. Das heißt,
dass ein Angreifer der im Netzwerk mitliest, *Device IDs* mitlesen kann und sich
somit als eine bestimmter Peer ausgeben kann. Das würde einem Angreifer die
Information liefern, mit welchem Peers sich eine bestimmte *Device ID*
synchronisiert. Mehr zu *Device IDs* sowie möglichen damit in Verbindung
stehenden Problemen findet sich in der offiziellen
Syncthing--Dokumentation[^stsec].

[^stsec]: Understanding Device--IDs:  <https://docs.syncthing.net/dev/device-ids.html>

Eine lokale Verschlüsselung der Daten finden nicht statt. Schlüssel, welche die
*Device ID* eindeutig identifizieren sind nicht weiter gesichert.

*Librevault* ist ein sich noch im Frühstadion befindlicher Prototyp. Die aktuell
getestete alpha Version ist beim hinzufügen eines »Synchronisationsordners«
reproduzierbar abgestürzt. Laut Projekt--Beschreibung scheint sich Librevault
an Resilio/Syncthing zu orientieren. Weitere Details zur Spezifikation und
Projektzielen sind auf dem Blog des Entwicklers[^librevault] zu finden.

[^librevault]: Librevault Entwicklerblog: <https://librevault.com/blog/>

**git--annex** ist ein sehr stark am *git* Versionsverwaltungssystem orientiertes
Synchronisationswerkzeug. Prinzipiell ist es für die Kommandozeile entwickelt
worden, es existiert mittlerweile jedoch ein *Webfrontend* (Webapp).

*git--annex* verwaltet nur die Metadaten in *git*. Es funktioniert als
*git*--Aufsatz, welcher es dem Benutzer ermöglicht auch große Binäre Dateien
mittels *git* zu verwalten beziehungsweise zu synchronisieren. Zum
synchronisieren der Metadaten wird *git* verwendet, zum synchronisieren der
eigentlichen Daten wird *git--annex* genutzt. Es überträgt die Daten
verschlüsselt mit *rsync über ssh*. Mittels der *git*--Erweiterung
*gcrypt*[^FN_GCRYPT] ist es möglich vollständig verschlüsselte *git* »remotes«
anzulegen.

[^FN_GCRYPT]: *gcrypt* git addon: <https://spwhitton.name/tech/code/git-remote-gcrypt/>

Neben »normalen« *git*--Repositories werden sogenannten »Special
Remotes«[^FN_GIT_ANNEX_SPECIALREMOTES] unterstützt. Diese werden verwendet um
Daten auf ein System, auf welchem *git* nicht vorliegt, zu synchronisieren. 

Neben der Verschlüsselung von *git remotes* mit *gcrypt* gibt es auch die
Möglichkeit die Daten auf *special remotes* zu verschlüsseln. Hierfür gibt es
die drei Verfahren:

* **hybrid encryption:** Gemeinsamer »shared key« wird im mit einen »public key« verschlüsselt im Repository gespeichert
* **shared encryption:** Gemeinsamer »shared key« wird im Klartext im Repository gespeichert
* **public key encryption:** Hierbei wird der »public key« verwendet, zum entschlüsseln benötigt man den »private key«
* **shared public key encryption:** Wie beim »public key«--Verfahren, jedoch mit einem gemeinsam genutztem Schlüsselpaar

[^FN_GIT_ANNEX_SPECIALREMOTES]: *git--annex* special remotes: <https://git-annex.branchable.com/special_remotes/>
[^FN_GIT_ANNEX_ENCRYPTION]: *git--annex* encryption: <http://git-annex.branchable.com/design/encryption/>

#### Weiteres

Einen bisher nicht genannten, relativ neuen dezentraler Ansatz bietet das
InterPlanetary--File--System[^FN_IPFS], als Teil seiner Funktionalität. Dieses ist in der
aktuellen Implementierung jedoch eher als ein fortgeschrittener Prototyp
anzusehen. Der Ansatz des *IPFS*--Protokolls ist vielversprechend. IPFS
kombiniert dabei viele bereits bekannte Technologien zu einem einzigen Projekt.
Hierdurch lassen sich schwächen aktuell genutzter Systeme abmildern oder gar
vermeiden.

[^FN_IPFS]: InterPlanetary--File System: <https://en.wikipedia.org/wiki/InterPlanetary_File_System>

### Ähnliche Arbeiten

Von den genannten Projekten haben die folgenden Gemeinsamkeiten mit »brig«,
verfolgen jedoch unterschiedliche Ziele:

* Infinit
* Resilio
* Syncthing
* Bazil[^bazil]

[^bazil]: Projektseite: <https://bazil.org/>

## Markt und Wettbewerber

Da der Cloud--Speicher--Mark sehr dynamisch und fragmentiert ist, ist es
schwierig hier zuverlässige Daten zu finden. Laut einem Online--Beitrag der
»Wirtschafts Woche«[^cloudstorage] gehören folgende Anbieter zu »den größten«
Cloud--Speicher--Anbietern:

* Dropbox
* Apples iCloud
* Microsoft OneDrive
* Google Drive

[^cloudstorage]: Größten Cloud--Speicher Anbieter: <http://www.wiwo.de/unternehmen/it/cloud-wer-sind-die-groessten-cloud-anbieter-und-was-kosten-sie/11975400-7.html>

In Deutschland gehört *Dropbox* zu den bekannten Anbietern, Apples *iCloud* ist
in erster Linie für Mac--Benutzer interessant.

* Google Drive/Dropbox mit »EncFS« oder »Boxcryptor«
* Syncthing
* git--annex
* Btsync 

Verschiedene Alternativen

Es gibt Alternativen, diese haben jedoch Probleme:

* kompliziert
* unsicher
* propritär
* ...

Tabelle: ...

## Gesellschaftliche und Politische Aspekte 

Seit den Snowden--Enthüllungen[^nsa-leak] ist offiziell bekannt, dass Unternehmen im
Notfall rechtlich gezwungen werden können personenbezogene Daten rauszugeben.

[^nsa-leak]: Globale Überwachungs-- und Spionageaffäre: <https://de.wikipedia.org/wiki/Globale_%C3%9Cberwachungs-_und_Spionageaff%C3%A4re>

* Snowden--Affäre
* Gesellschaftliche Aspekte: Ich habe nichts zu verbergen
* politische Lage und Probleme

>> *Arguing that you don’t care about the right to privacy because you have
>> nothing to hide is no different than saying you don’t care about free speech
>> because you have nothing to say.* -- Edward Snowden
