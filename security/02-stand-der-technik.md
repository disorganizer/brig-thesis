# Stand von Wissenschaft und Technik {#sec:SEC02_STAND_DER_WISSENSCHAFT_UND_TECHNIK}

## Sicherheit und Usability von Dateiverteilungssystemen {#sec:SEC02_SICHERHEIT_UND_USABILITY_VON_DATEIVERTEILUNGSSYSTEMEN}

### Allgemeines {#sec:SEC02_ALGEMEINES}

Zentrale und dezentrale Systeme sind die Basis für den Austausch von
Informationen. Ob ein System zentral oder dezentral fungiert ist nicht immer
klar abgrenzbar. Oft kommen auch hybride Systeme zum Einsatz, welche zwar
dezentral funktionieren, jedoch teilweise zentrale Instanzen benötigen. Hier
wäre beispielsweise das Torrent--Konzept zu nennen. Weitere Informationen
hierzu, vgl. [@peer2peer], S. 232 ff.

### Der »Sicherheitsbegriff« {#sec:SEC02_DER_SICHERHEITSBEGRIFF}

Betrachten man die »Sicherheit« von Dateiverteilungssystemen, so müssen
verschiedene Teilaspekte betrachten werden. Leider ist das Umfeld der
Sicherheit sehr groß und die Begrifflichkeiten nicht immer eindeutig definiert.
In der Fachliteratur (vgl. [@pauly2004netzwerk], S. 21 f.) spricht man bei »Sicherheit«
oft von den folgenden fünf Sicherheitsaspekten:

* Vertraulichkeit: Schutz der Daten vor Zugriff durch Dritte.
* Integrität: Schutz der Daten vor Manipulation.
* Authentifizierung: Eindeutige Identifikation von Benutzern.
* Autorisierung: Definiert die Zugangs-- und Zugriffssteuerung auf Dienste.
* Verfügbarkeit: Dienste stehen legitimen Benutzern tatsächlich zur Verfügung.

Dies sind auch die Sicherheitsaspekte, die bei der Verwendung von
Cloud--Speicher--Anbietern zu tragen kommen. Zur Umsetzung der genannten
Sicherheitsaspekte reicht in der Regel die alleinige Implementierung
technischer Komponenten nicht aus. Es muss viel mehr ein Prozess entwickelt
werden, der Sicherheit permanent sicherstellt und evaluiert. Hierzu gehört auch
im großen Maße eine gewisse Sensibilität, für welche der Anwender geschult
werden muss.

### Angriffe und Bedrohungen {#sec:SEC02_ANGRIFFE_UND_BEDROHUNGEN}

Die Sicherheit eines System lässt sich nicht mit einem einfachen »ja« oder
»nein« beantworten. Betrachtet man ein System bezüglich seiner Sicherheit, so
muss auch genau definiert werden, gegen welches »Angriffsszenario« ein System
sicher ist. Auch ein System das aus kryptographischer Sicht als »sicher« zu
betrachten wäre, kann im einfachsten Fall, durch die Weitergabe von
Zugangsdaten an Dritte, kompromittiert werden.

![Scherzhafte Darstellung eines möglichen Angriffs auf eine Festplattenverschlüsselung mit optimalem Kosten--Nutzen--Verhältnis.[^FN_XKCD_ENC_COMIC]](images/security.png){#fig:img-security width=66%}

[^FN_XKCD_ENC_COMIC]:Bildquelle: <http://imgs.xkcd.com/comics/security.png>

Neben dem technischen Ansatz beim Angriff auf ein System, gibt es auch die
psychologische Komponente, beim Menschen, welche wahrscheinlich die größte
Schwachstelle in den meisten Systemen darstellt.

Beim technischen Ansatz werden in der Regel Fehler in der Software oder
Infrastruktur ausgenutzt, um sich unbefugten Zugriff auf Informationen zu
verschaffen.

Beim nicht technischen Angriff wird der Benutzer auf »psychologischer Ebene«
manipuliert und mit sogenannten »Social Hacking«--, auch »Social
Engineering«--Methoden dazu verleitet beispielsweise sein Passwort
weiterzugeben. Auch der Einsatz von »Phishing«, ist eine Variante
von »Social Engineering«. [@fig:img-security] zeigt scherzhaft eine weitere
Variante für welche Menschen anfällig sind.

Um Sicherheit zu gewährleisten, ist es wichtig ein System »im Ganzen« zu
betrachten. Die Implementierung bestimmter Sicherheitsfeatures ist nur die
technische Maßnahme. Der Benutzer eines Systems erwartet in erster Linie
Funktionalität und möchte sich in den wenigsten Fällen mit dem System oder der
Sicherheit des Systems auseinandersetzen. Benutzer sind oft nicht genug
sensibilisiert was den Datenschutz oder auch die Gefahren und Konsequenzen bei
einem Sicherheitsproblem angeht.

Weiterhin sollte bedacht werden, dass die Definition eines »sicheren Systems«, in
der Regel ein Kompromiss aus den folgenden Punkten ist:

* Finanzieller Aufwand
* Sicherheit
* Usability

### Datenaustausch über zentrale Lösungen {#sec:SEC02_DATENAUSTAUSCH_UEBER_ZENTRALE_LOESUNGEN}

#### Funktionsweise zentraler Dienste {#sec:SEC02_FUNKTIONSWEISE_ZENTRALER_DIENSTE}

Zentrale Dienste klassifizieren sich im Kontext dieser Arbeit durch die
Eigenschaft, dass es eine zentrale Instanz gibt, welche zum Austausch der Daten
benötigt wird. Dies sind in den meisten Fällen die Server des
Cloud--Speicher--Anbieters, welche für die Synchronisation und Speicherung der
Daten verantwortlich sind.

![Datensynchronisation über zentrale Cloud--Speicher--Dienste, wie beispielsweise Dropbox. *Alice* und *Bob* teilen gemeinsam Dateien über das »shared storage« aus. *Mallory* stellt einen potentiellen Angreifer dar. *Mallory* kann ein externer Angreifer oder auch ein interner Mitarbeiter sein, der Zugriff auf die Daten hat.](images/cloud.png){#fig:img-cloud width=80%}

[@fig:img-cloud] zeigt schematisch das Konzept beim Austausch von Daten über
einen Cloud--Speicher--Dienst. Die Daten des Benutzers werden hierbei mit
einer »zentralen Stelle« synchronisiert. In der Regel legt der Benutzer einen
Account beim Cloud--Speicher--Anbieter an, installiert dessen Client--Software,
legt einen Ordner zur Synchronisation fest und registriert sich abschließend
online beim Cloud--Speicher--Anbieter.

Dieser Ordner lässt sich dann beispielsweise auf weitere Geräte des Benutzer
synchronisieren. Weiterhin gibt es in der Regel, die Möglichkeit Dateien mit
anderen Benutzern zu teilen (siehe @fig:img-cloud). Welche genauen
Einstellungen sich vornehmen lassen und wie feingranular die
Benutzerverwaltung und die Möglichkeiten beim Synchronisieren sind, ist von dem
jeweiligen Cloud--Speicher--Anbieter abhängig.

Mittlerweile werben die Anbieter mit »starker Verschlüsselung« und dass die
Daten in der »Cloud« »sicher« sind. Spätestens seit den Snowden--Enthüllungen
ist es jedoch klar, dass die Anbieter dazu gezwungen werden können die Daten
eines Benutzers herauszugeben (vgl. [@bibgreenwald2013nsa]).

#### Synchronisations--Software {#sec:SEC02_SYNCHRONISATIONS_SOFTWARE}

Die verwendete Software zur Synchronisation ist ebenfalls vom jeweiligen
Anbieter abhängig. Das Problem hierbei ist, dass die Software in der Regel
proprietär ist und der Benutzer weder die genaue Funktionalität kennt, noch das
Vorhandensein von Hintertüren ausschließen kann. Die Software wird in den
meisten Fällen für verschiedene Plattformen bereitgestellt. Weiterhin
ermöglichen die Anbieter auch den Zugriff auf die Daten mittels eines
Webbrowser--Interface.

#### Sicherheit von Cloud--Speicher--Anbietern {#sec:SEC02_SICHERHEIT_VON_CLOUDSPEICHER_ANBIETERN}

Es ist sehr schwierig, die Sicherheit der Cloud--Speicher--Anbieter
realistisch zu bewerten, da sowohl die Infrastruktur als auch die verwendete
Software intransparent und proprietär sind.

Die Daten werden laut Aussagen der
Hersteller[^FN_APPLE_SECURITY][^FN_DROPBOX_SECURITY] verschlüsselt übertragen
und mittlerweile auch verschlüsselt gespeichert.

[^FN_APPLE_SECURITY]:Apple iCloud Security: <https://support.apple.com/en-us/HT202303>
[^FN_DROPBOX_SECURITY]:Dropbox Security: <https://www.dropbox.com/security>

Beim Einsatz der Cloud--Speicher--Dienste hängt die Sicherheit der Daten somit
in erster Linie vom Dienstanbieter ab. Beim iCloud--Dienst von Apple
beispielsweise werden die Daten verschlüsselt bei Drittanbietern wie der
Amazon--S3- oder Windows--Azure--Cloud gespeichert[^FN_IOS_SECGUIDE]. Die
Metadaten und kryptographischen Schlüssel verwaltet Apple auf seinen eigenen
Servern. Dropbox hat laut Medienberichten mittlerweile von der Amazon--Cloud
auf eine eigene Infrastruktur migriert[^FN_DROPBOX_S3_OWN].

[^FN_DROPBOX_S3_OWN]:Dropbox Exodus Amazon Cloud Empire:

	<http://www.wired.com/2016/03/epic-story-dropboxs-exodus-amazon-cloud-empire/>

[^FN_IOS_SECGUIDE]: Apple iOS Security: <http://www.apple.com/business/docs/iOS_Security_Guide.pdf>

Das Problem hierbei ist die Umsetzung der Datenverschlüsselung der gängigen
Cloud--Speicher--Anbieter. Anbieter wie Dropbox verschlüsseln laut eigener
Aussage die Daten in der Cloud nach aktuellen Sicherheitsstandards. Das Problem
im Fall von Dropbox ist jedoch, dass Dropbox und nicht der Endbenutzer der
Schlüsselinhaber ist. Es ist also, auch wenn es laut internen
Dropbox--Richtlinien verboten ist, möglich, dass Mitarbeiter beziehungsweise
dritte Parteien die Daten des Nutzers einsehen können (vgl. [@ko2015cloud] S. 103).

Ein weiteres Problem ist, dass ein Cloud--Speicher--Anbieter aufgrund seiner
zentralen Rolle ein gutes Angriffsziel bildet. Erst kürzlich wurde bekannt,
dass Angreifer im Jahr 2012 ungefähr 70 Millionen
Zugangsdaten[^FN_DROPBOX_DATALEAK] bei Dropbox entwendet haben. Hat ein
Angreifer also die Zugangsdaten erbeutet, bringt die Verschlüsselung die der
Cloud--Dienst betreibt in diesem Fall nichts. Die gestohlenen Passwörter waren
nicht im Klartext einsehbar, moderne Angriffsmöglichkeiten auf Passwörter
zeigen jedoch, dass das nichtsdestotrotz ein großes Problem ist (siehe auch
@sec:SEC05_SICHERHEIT_UND_ANGRIFFSSZENARIEN).

[^FN_DROPBOX_DATALEAK]: Dropbox hackers stole 68 million passwords:

	<http://www.telegraph.co.uk/technology/2016/08/31/dropbox-hackers-stole-70-million-passwords-and-email-addresses/>

Abhilfe könnte in diesem Fall eine zusätzliche Verschlüsselung auf Seiten des
Nutzers schaffen. Diese ist jedoch für den Endverbraucher oft zu kompliziert,
aufgrund von Fehlern in der Implementierung nicht optimal geeignet (EncFS
Audit[^FN_ENCFS_AUDIT]) oder proprietär (Boxcryptor[^FN_BOXCRYPTOR]).

[^FN_ENCFS_AUDIT]:  EncFS Audit: <https://defuse.ca/audits/encfs.htm>
[^FN_BOXCRYPTOR]: Boxcryptor: <https://de.wikipedia.org/w/index.php?title=Boxcryptor&oldid=161953026>

Den meisten Anbietern muss man vertrauen, dass diese mit den Daten und
Schlüsseln sorgsam umgehen. Auch wenn sich viele Anbieter wie beispielsweise
Dropbox bemühen, aus den Fehlern der Vergangenheit zu lernen und verbesserte
Sicherheitsmechanismen wie beispielsweise
Zwei--Faktor--Authentifizierung[^FN_TWO_FACTOR_AUTH] in ihre Software
integrieren, bleibt jedoch die Krux der Intransparenz und der proprietären
Software. Es ist für den Benutzer nicht ohne weiteres möglich, die Sicherheit der
Client--Software zu validieren.

[^FN_TWO_FACTOR_AUTH]: Zwei--Faktor--Authentifizierung:

	<https://de.wikipedia.org/w/index.php?title=Zwei-Faktor-Authentifizierung&oldid=160891860>

2011 hat der Sicherheitsforscher *Derek Newton* den
Authentifizierungsmechanismus von Dropbox kritisiert. Nach einmaligem
Registrieren und Einrichten des Dropbox--Client, werden für die
Synchronisation keine weiteren Zugangsdaten mehr benötigt. Der
Authentifizierungsmechanismus benötigt nur ein sogenanntes
»Authentifizierungs--Token« (diese wird dem Client nach der Registrierung vom
Server zugewiesen), die sogenannte `HOST_ID`. Mit dieser authentifiziert sich
der Dropbox--Client bei zukünftigen Synchronisationsvorgängen gegenüber dem
Dropbox--Dienst.

Ein großes Problem war hierbei auch, dass die `HOST_ID` unverschlüsselt in
einer Konfigurationsdatei (sqlite3--Datenkbank) abgelegt war. Diese ID bleibt
anscheinend auch nach Änderung der Zugangsdaten weiterhin bestehen.

[^FN_DROPBOX_INSECURE_BY_DESIGN]: Dropbox authentication: »insecure by design«: <http://dereknewton.com/2011/04/dropbox-authentication-static-host-ids/>

Eine weitere Arbeit aus dem Jahr 2011 beschreibt verschiedene Angriffsszenarien
und Probleme welche die Datensicherheit und Privatsphäre von
Cloud--Speicher--Benutzern in Frage stellt (vgl. [@mulazzani2011dark]).

2013 haben weitere Sicherheitsforscher den Dropbox--Client mittels *Reverse
Engineering* analysiert. Ab der Version 1.2.48 wird die `HOST_ID` in einer
verschlüsselten sqlite3--Datenbank abgespeichert. Diese Nachbesserung
seitens Dropbox war nicht besonders effektiv, da sich die Schlüssel zum
Entschlüsseln weiterhin auf dem Client--PC befinden. Zusätzlich wird für die
Authentifizierung in neueren Dropbox--Versionen ein `HOST_INT`--Wert
benötigt, welcher ebenfalls vom Client--PC extrahiert werden kann.

Mittels dieser beiden Werte kann die Zwei--Faktor--Authentifizierung (2FA), wie
sie von Dropbox implementiert ist, umgangen werden. Die Client--API verwendet
anscheinend keine Zwei--Faktor--Authentifizierung. Darüber hinaus lassen sich auf Basis
der beiden  Parameter sogenannte »Autologin--URLs« generieren. Den Forschern ist
es auch gelungen, einen Open--Source--Prototypen zu entwickeln. Für weitere
Details vgl. [@kholia2013looking], beziehungsweise siehe Vortag *USENIX Open
Access Content*[^FN_USENIX].

[^FN_USENIX]: USENIX Vortrag »Looking Inside the (Drop) Box«:

	<https://www.usenix.org/conference/woot13/workshop-program/presentation/kholia>

2015 wurde bekannt, dass die vorherrschenden Cloud--Speicher--Anbieter für
sogenannte »Man--in--the--Cloud«--Angriffe anfällig sind. Die bereits im Jahr
2011 entdeckten Schwächen bei der Authentifizierung von Dropbox sind
weiterhin präsent und auch auf andere Cloud--Speicher--Anbieter übertragbar. Um
die Client--Software gegenüber dem Cloud--Speicher--Dienst zu authentifizieren,
werden wie auch bei Dropbox, Authentifizierungs--Token verwendet. Für den
Angriff haben die Forscher ein sogenanntes »Switcher«--Programm entwickelt,
welches in der Lage ist, ein Authentifizierungs--Token auf dem Computer des
potentiellen Opfers auszutauschen. [@fig:img-mitc] zeigt den Ablauf eines
möglichen »Man--in--the--Cloud«--Angriffs.

![»Quick Double Switch Attack Flow«--Man--in--the--Cloud--Angriff. Die Buchstaben a, b, c und d repräsentieren dabei jeweils die Synchronisationsvorgänge.](images/mitc.png){#fig:img-mitc width=80%}

1. Der Angreifer platziert den »Switcher« auf dem Rechner des Opfers
   (beispielsweise mittels Social Engineering oder Phishing--Methoden)
2. Der »Switcher« ändert den Token des Benutzers. Hierbei wird der
   Synchronisationssoftware der Token vom Angreifer »injiziert« (first switch)
   und anschließend der Orignal--Token vom Opfer in den nun vom Angreifer
   kontrollierten Synchronisationsordner kopiert.  (a) wird inaktiv, (b) wird
   aktiv.
3. Die Synchronisationssoftware synchronisiert nun den Token des Opfers zum
   Angreifer (b).
4. Der Angreifer kann sich nun mittels des »gestohlenen« Token mit dem Account
   des Opfers synchronisieren (c).
5. Anschließend wird der »Switcher« noch einmal ausgeführt, um beim Opfer
   wieder den ursprünglichen Synchronisationszustand herzustellen (second switch).

Der Ablauf in [@fig:img-mitc] zeigt den »Quick Double Switch Attack Flow«. Im
Bericht der *IMPERVA -- Hacker Intelligence Initiative* werden noch weitere
Angriffe auf Basis dieses Verfahrens aufgezeigt (vgl. [@mitcref]).

Neben dem Dropbox--Client wurden auch die Synchronisationsapplikationen
Microsoft OneDrive, Box und Google Drive untersucht. Diese verwenden zum
Authentifizieren den offenen *OAuth 2.0* Authentifizierungsstandard. Dropbox
hingegen verwendet ein proprietäres Verfahren. Problematisch bei Dropbox
ist, dass die gesamte Sicherheit von der `HOST_ID` (und `HOST_INT`) abhängt.
Hat ein Angreifer diese erbeutet, so kann er auch über den
Dropbox--Webzugang sämtliche administrativen Aufgaben durchführen.

Laut Meinung der Autoren von »brig«, sowie auch vieler Sicherheitsexperten, wird
beim Einsatz proprietärer Software die Sicherheit untergraben, da bei
proprietärer Software explizit eingebaute Hintertüren nicht ausgeschlossen
werden können und es auch keine einfache Möglichkeit der Prüfung auf solche
durch den Endbenutzer gibt.

Insbesondere hat die Freilegung der Snowden--Dokumente weiterhin zu der
Schlussfolgerung geführt, dass der Einsatz von Freier Software empfehlenswerter
ist. Bekannte Sicherheitsexperten wie *Bruce
Schneier*[^FN_SCHNEIER_1][^FN_SCHNEIER_2] oder auch *Rüdiger Weis* sehen Freie
Software als eine der wenigen Möglichkeiten, der Überwachung durch
Geheimdienste (oder auch anderen Institutionen) entgegen zu wirken. Weiterhin
kann Kryptographie dank Freier Software von unabhängigen Sicherheitsforschern
bewertet werden.

Auch wenn für viele Benutzer die Geheimhaltung der Software und Infrastruktur
auf den ersten Blick als »sicherer« erscheinen mag, widerspricht Sie dem
Kerckhoffs’schen Prinzip, bei welchem die Sicherheit eines System nur von der
Geheimhaltung des Schlüssels, jedoch nicht von der Geheimhaltung weiterer
Systemelemente abhängen sollte. Die Vergangenheit hat beispielsweise beim
GSM--Standard oder beim DVD--Kopierschutz »CSS«[^FN_CSS] gezeigt, dass durch die
Geheimhaltung von Systemkomponenten erfolgreiche Angriffe, höchstens erschwert,
jedoch nicht unterbunden werden können (vgl. [@2009understanding], S. 11 und
[@ertel2012angewandte], S. 23).

[^FN_CSS]: Cryptanalysis of Contents Scrambling System: <http://www.cs.cmu.edu/~dst/DeCSS/FrankStevenson/analysis.html>
[^FN_SCHNEIER_1]: Defending Against Crypto Backdoors: <https://www.schneier.com/blog/archives/2013/10/defending_again_1.html>
[^FN_SCHNEIER_2]: How to Remain Secure Against the NSA: <https://www.schneier.com/blog/archives/2013/09/how_to_remain_s.html>
[^FN_WEIS]: Krypto nach Snowden | 19. Netzpolitischer Abend: <https://www.youtube.com/watch?v=T_ojwHReMkM>

Abgesehen von den Snowden--Enthüllungen, gibt es für den Endverbraucher viel
näherliegendere Gefahren, welche die Daten und Privatsphäre gefährden. Neben dem
soeben genannten Dropbox Datenleck, welches rund 70 Millionen Benutzerdaten
betraf und über fast vier Jahre unentdeckt war, gibt es immer wieder Probleme
mit zentralen Diensten. Ein Ausschnitt von bekannt gewordenen Vorfällen in
letzter Zeit:

**Datenlecks:**

* Datenleck bei Dropbox[^FN_DROPBOX_DATALEAK_4]
* Google Drive Datenleck[^FN_GDRIVE_DATALEAK]
* Microsoft OneDrive Datenleck[^FN_MS_DATALEAK]
* 7 Millionen Zugangsdaten von Dropbox im Umlauf (unbestätigt)[^FN_DROPBOX_DATALEAK_3]
* iCloud--Hack auf private Fotos von Prominenten[^FN_FAPPENING]

**Weitere Probleme:**

* Dropbox--Client greift auf Daten außerhalb des Sync--Ordners zu[^FN_DROPBOX_SPY].
* Microsoft synchronisiert Bitlocker--Schlüssel (Festplattenverschlüsselung)
  standardmäßig in die Cloud[^FN_BITLOCKER_CLOUD]
* Dropbox akzeptiert beliebige Passwörter über mehrere Stunden[^FN_DROPBOX_ACCESS]
* Ausfallzeit über zwei Stunden[^FN_DROPBOX_DOS]

[^FN_FAPPENING]: iCloud--Hack:

	<https://de.wikipedia.org/w/index.php?title=Hackerangriff_auf_private_Fotos_von_Prominenten_2014&oldid=159942418>

[^FN_BITLOCKER_CLOUD]: Bitlocker--Schlüssel werden standardmäßig in die Cloud synchronisiert:

	<https://theintercept.com/2015/12/28/recently-bought-a-windows-computer-microsoft-probably-has-your-encryption-key/>

[^FN_DROPBOX_ACCESS]: Dropbox--Authentifizierungs--Bug:

	<https://techcrunch.com/2011/06/20/dropbox-security-bug-made-passwords-optional-for-four-hours/>

[^FN_MS_DATALEAK]: OneDrive Datenleck: <https://www.heise.de/security/meldung/Microsoft-dichtet-OneDrive-Links-ab-2227485.html>
[^FN_GDRIVE_DATALEAK]: Google Drive Datenleck:

	<https://www.heise.de/security/meldung/Auch-Google-schliesst-Datenleck-im-Cloud-Speicher-2243366.html>

[^FN_DROPBOX_DATALEAK_4]: Dropbox Datenleck: <https://www.heise.de/security/meldung/Dropbox-bestaetigt-Datenleck-1656798.html>
[^FN_DROPBOX_DATALEAK_3]: 7 Mio. Zugangsdaten im Umlauf:

	<https://www.heise.de/security/meldung/Angeblich-7-Millionen-Dropbox-Passwoerter-im-Umlauf-2423684.html>

[^FN_DROPBOX_SPY]: Dropbox--Schnüffelverdacht:

	<http://www.heise.de/security/meldung/Dropbox-unter-Schnueffelverdacht-2565990.html>

[^FN_DROPBOX_DOS]: Dropbox--Ausfall: <https://www.heise.de/security/meldung/Dropbox-Ausfall-war-kein-Angriff-2083688.html>

Auch wenn viele Unternehmen ihre Priorität nicht in der Sicherung ihrer Daten
sehen mögen, sollten die Folgekosten von Datenlecks nicht unterschätzt werden.
Laut einer jährlich durchgeführten Studie vom *Ponemon Institute* belaufen sich
die Kosten im Zusammenhang mit Datenlecks auf mehrere Millionen Dollar (vgl.
[@ponemon]). Die Tendenz ist von Jahr zu Jahr steigend wenn man die Berichte
aus dem jeweiligem Vorjahr zuzieht.

Abgesehen von den Datenlecks verschiedener Cloud--Speicher--Anbieter, haben
zentrale Dienste immer wieder Probleme mit größeren Datenlecks. Welcher Dienst
und welche Daten betroffen sind, sammelt der Sicherheitsforscher *Troy Hunt* auf
seiner Webseite[^FN_HAVEIBEENBWNED].

[^FN_HAVEIBEENBWNED]: Gesammelte Informationen zu Datenlecks: <https://haveibeenpwned.com/>

### Private Cloud {#sec:SEC02_PRIVATE_CLOUD}

Weiterhin gibt es bei der Cloud--Speicher--Lösung auch die Möglichkeit, einen
eigenen »Cloud--Speicher« aufzusetzen. Hierfür wird oft die
Open--Source--Lösung Owncloud genommen. Der Nachteil hierbei ist, dass der
Benutzer selbst für die Bereitstellung der Infrastruktur verantwortlich ist.
Für Unternehmen mag die Owncloud durchaus interessant sein, für die meisten
Privatanwender ist der Aufwand höchstwahrscheinlich zu hoch. Weiterhin haben
Endanwender in der Regel nicht das nötige Know--How, welches für das Betreiben
eines Cloud--Speicher--Dienstes essentiell ist.

### Datenaustausch über dezentrale Lösungen {#sec:SEC02_DATENAUSTAUSCH_UEBER_DEZENTRALE_LOESUNGEN}

#### Funktionsweise dezentraler Dienste {#sec:SEC02_FUNKTIONSWEISE_DEZENTRALER_DIENSTE}

Der dezentrale Bereich klassifiziert sich durch den Dateiaustausch, welcher in
der Regel *ohne* eine zentrale Instanz auskommt. Es handelt sich hierbei um
Systeme aus dem Bereich des Peer-to-peer--Modells. Eines der frühen
Peer--to--Peer--Protokolle ist das Napster--Protokoll der gleichnamigen
Anwendung Napster, welche Ende der 90' Jahre für den Tausch von Musik
verwendet wurde. Später sind weitere Peer--to--Peer--Protokolle wie das
Multisource--File--Transfer--Protocol oder das BitTorrent--Protokoll hinzugekommen.

[@fig:img-p2p] zeigt schematisch den Austausch von Daten in einem dezentralen
Netzwerk. Bei einem dezentralem System liegen die Daten in der Regel nur auf
den Rechnern der Benutzer. Die Speicherung auf zentralen Speicher--Servern wie
bei den zentralen Diensten ist nicht vorgesehen, jedoch aufgrund der
Architektur realisierbar.

Bei der Nutzung eines dezentralen Netzwerks zum Austausch beziehungsweise zur
Synchronisation von Daten muss der Benutzer in der Regel eine spezielle
Software installieren und einen »Synchronisationsordner«, wie bei den zentralen
Diensten definieren. Dieser Ordner wird dem Netzwerk »bekannt« gemacht. Je
nach eingesetztem Protokoll, variiert die Funktionsweise und Sicherheit.

![Dezentraler Datenaustausch über Peer--to-Peer--Kommunikation. Es existiert keine zentrale Instanz, jeder Peer im Netzwerk ist »gleichberechtigt«.](images/p2p.png){#fig:img-p2p width=80%}

Die dezentralen Systeme unterliegen in der Regel keiner Regulierung durch eine
zentrale Instanz. Je nach verwendeter Technologie zum Datenaustausch,
existieren sogenannte »rendezvous hosts«[^FN_RENDEZVOUS_HOST], welche für die
initiale Konfiguration und als »Einstiegspunkt« benötigt werden. Hier
unterscheiden sich die verschiedenen Protokolle und Netzwerke voneinander.

[^FN_RENDEZVOUS_HOST]: Rendezvous Host/Bootstrapping node:

	<https://en.wikipedia.org/w/index.php?title=Bootstrapping_node&oldid=693889298>

Ein bekannter Vertreter der P2P--Protokolle ist BitTorrent[^FN_BITTORRENT].
Das Protokoll kommt beispielsweise bei der Verbreitung von Software,
Computerspielen (HumblieIndieBundle.com), dem Blender Movie--Projekten,
Linux--Distributionen, der Verteilung von Updates (Windows 10), bei diversen
Spieleherstellern und auch anderen Anwendungen zum Einsatz[^FN_BTUSAGE].

[^FN_BITTORRENT]: BitTorrent: <https://de.wikipedia.org/w/index.php?title=BitTorrent&oldid=160095352>
[^FN_BTUSAGE]: BitTorrent Einsatzgebiete: <https://en.wikipedia.org/w/index.php?title=BitTorrent&oldid=761280798#Adoption>

Ein Vorteil bei den dezentralen Systemen ist, dass es im Vergleich zu zentralen
Architekturen keinen »Single Point Of Failure«[^FN_SPOF] gibt. Ein weiterer
Unterschied zur zentralen Lösung ist bei dezentralen Netzwerken der
»Datenfluss«. Die Daten werden nicht von einer zentralen Instanz »besorgt«,
sondern liegen im jeweiligen Netzwerk, verteilt auf die Netzwerkteilnehmer
(peers). Jeder Teilnehmer des Netzwerks fungiert in der Regel als Client und
als Server. Daten werden beim Austausch nicht zwangsläufig von einem
einzelnem Teilnehmer geladen, sondern von einer Gruppe aus Teilnehmern, welche
die gleiche Datei besitzen, siehe [@fig:img-swarm].

[^FN_SPOF]: Single Point of Failure: <https://de.wikipedia.org/w/index.php?title=Single_Point_of_Failure&oldid=156306981>

![Zeigt einen »Swarm«. *Alice* lädt die Datei »image.iso« von mehreren Teilnehmern gleichzeitig, die Datei »mydog.png« jedoch nur von *Dan*.](images/distsync.png){#fig:img-swarm width=70%}

Aktuell verbreitete Peer--to--Peer--Protokolle:

* Bittorrent (Filesharing allgemein)
* Skype Protokoll (VOIP--Telephonie)

Früher eingesetzte Peer--to--Peer--Filesharing--Protokolle:

* Direct Connect
* Multisource File Transfer Protocol (Einsatz: eDonkey2000, Overnet)
* Fasttrack (Einsatz: Kazaa, Grokster, IMesh, Morpheus file sharing)
* Gnutella Protokoll (Einsatz: Gnutella Client)
* Napster--Protokoll

#### Synchronisations--Software {#sec:SEC02_SYNCHRONISATIONSSOFTWARE}

Zu den Vertretern der etablierten dezentralen Systeme gibt es vergleichsweise
zu den Cloud--Speicher--Anbietern nur wenige Produkte, welche für die
Synchronisation von Daten beziehungsweise den Austausch von Dokumenten
eingesetzt werden können. Bekannten Lösungen sind:

* Resilio (ehem. BitTorrent--Sync, proprietär)
* Infinit (proprietär, [@quintard2012towards])
* git--annex (Open--Source)
* Syncthing (Open--Source)
* Librevault (Open--Source)

#### Sicherheit von Peer--to--Peer--Synchronisationsanwendungen {#sec:SEC02_SICHERHEIT_VON_PEERTOPEER_SYNCHRONISATIONSANWENDUNGEN}

Bei den bekannten Vertretern des BitTorrent--Netzwerks wie dem
BitTorrent--Client werden die Daten in der Regel unverschlüsselt übertragen und
gespeichert. Auch eine Authentifizierung findet in der Regel nicht statt. Die
Benutzer geben die Daten mit ihrem Synchronisationsordner automatisch für
alle Teilnehmer des Netzwerks zum Teilen frei.

Wie bei zentralen Diensten, ist es auch bei dezentralen Netzwerken schwierig
die Sicherheit zu beurteilen. Diese hängt in diesem Fall nicht zwangsläufig von
einem Dienst--Anbieter ab, sondern vielmehr von der Umsetzung der Software, der
Infrastruktur des Netzwerks, der Sicherung der Daten (verschlüsselte
Speicherung, verschlüsselte Übertragung) und der Möglichkeit, einen
Kommunikationspartner zu authentifizieren.

**Resilio--Sync** (ehemals Bittorrent--Sync), verwendet eine modifizierte
Variante des BitTorrent--Protokolls[^FN_RESILIO_PROTOCOL]. Alle Daten werden
laut Hersteller zusätzlich symmetrisch mit AES--128 (siehe
@sec:SEC04_SYMMETRISCHE_VERSCHLUESSELUNGSVERFAHREN) verschlüsselt übertragen.
Die getestete Version entspricht der Standardversion welche kostenfrei
benutzbar ist, jedoch nur einen eingeschränkten Funktionsumfang bietet.
Weiterhin gibt es eine »Pro«--Version welche »selektive und kollaborative
Synchronisation« ermöglicht.

[^FN_RESILIO_PROTOCOL]:Inoffizielle Protokoll--Spezifikation <https://forum.resilio.com/topic/21338-inofficial-protocol-specification/>

Bei Resilio (Webbasierte GUI[^FN_GUI]) werden Daten mittels verschiedener »Schlüssel«
synchronisiert. Beim Anlegen eines Synchronisationsordners erscheinen dem
Benutzer folgende »Schlüssel«, über welche er den Synchronisationsordner mit
anderen Synchronisationspartnern teilen kann. Anhand des gewählten Schlüssels,
wird folgende Funktionalität beim Synchronisieren realisiert:

[^FN_GUI]: Grafische Benutzeroberfläche:

	<https://de.wikipedia.org/w/index.php?title=Grafische_Benutzeroberfl%C3%A4che&oldid=155859783>

* Nur Leserechte
* Lese-- und Schreibrechte
* Verschlüsselte Speicherung

Mittels dieser Schlüssel lässt sich die Synchronisation mit anderen
Peers/Synchronisationsordnern steuern. Neue Peers können über das Teilen eines
Schlüssels hinzugefügt werden. Die Anwendung macht einen undurchsichtigen
Eindruck. Eine 2014 durchgeführte Analyse von BitTorrent--Sync auf der
*Hackito* kommt aufgrund mehrerer Sicherheits-- und Designprobleme zur
Einschätzung[^FN_HACKITO], dass BitTorrent--Sync nicht für sensitive Daten
verwendet werden sollte.

[^FN_HACKITO]: Security analysis of BTsync:

	<http://2014.hackitoergosum.org/bittorrentsync-security-privacy-analysis-hackito-session-results/>

**Infinit** ist eine weitere proprietäre Lösung, welche es ermöglicht, Dateien
zwischen verschiedenen Benutzern, ohne Server--Instanz, auszutauschen. Die
Basis für Infinit stellt [@quintard2012towards] dar. Bei Infinit findet bei der
Installation der Anwendung eine Registrierung statt. Diese Daten
(Benutzername/E--Mail--Addresse) können anschließend verwendet werden, um mit der
Anwendung andere Infinit--Partner zu finden oder von diesen gefunden zu werden.
Anschließend kann eine Datei über eine *Drag & Drop*--Fläche an den gefundenen
Partner gesendet werden. Es ist unklar, ob Daten/Metadaten an die
Infinit--Plattform übertragen werden. Infinit wirbt mit »point--to--point
encryption« und »bank-level encryption algorithms such as AES-256 and RSA
2048«. Eine Authentifizierung des Kommunikationspartners findet rudimentär
anhand von Benutzernamen/E--Mail statt. Daten werden lokal nicht verschlüsselt.

**Syncthing** basiert auf einem eigens entwickeltem Protokoll, dem *Block
Exchange Protocol*[^FN_BEP]. Der Syncthing--Client (Web--GUI Variante)
ermöglicht das Hinzufügen von Synchronisationsordner und »Remote Devices«.
Diese GUI ist standardmäßig von außen nicht zugreifbar, da sie auf »localhost
only« läuft.

[^FN_BEP]: Block exchange protocol: <https://docs.syncthing.net/specs/bep-v1.html>

Die Peers werden durch eine eindeutige Device--ID identifiziert. Diese leitet
sich aus einen asymmetrischen Schlüsselpaar (3072 Bit RSA[^FN_SYNCTHING_KEYS])
ab, welches beim ersten Start der Anwendung erstellt wird. Abgelegt wird ein
privater Schlüssel und ein selbst signiertes Zertifikat. Der private Schlüssel
scheint nicht geschützt zu sein:

[^FN_SYNCTHING_KEYS]: Syncthing--Keys: <https://docs.syncthing.net/dev/device-ids.html#keys>

~~~bash
$ ~/.config/syncthing » cat key.pem
	-----BEGIN EC PRIVATE KEY-----
	MIGkAgEBBDCQIMwVr730vKzoyHCbIqDoxNxAjKvdFYL+XnKk65GurCc9q2qiZJEU
	zMNWSD+N/eCgBwYFK4EEACKhZANiAASJ0YZUMQVAuW8tT7DvuLFkanCw2gpgD1DE
	P69XHqMS0MFg6ZwMqzvlV65WXQMOHfsNw/xKMagSGlyTh17W/Up0y2PPygUlj6H1
	d0vMI1OguPD9heeqYjU67R4GxlHMj54=
	-----END EC PRIVATE KEY-----
~~~

Das selbst signierte Zertifikat bringt keine zusätzliche Sicherheit, ermöglicht
jedoch die Nutzung von Transport Layer Security (TLS)[^FN_TLS]. Diese ID ist
für jeden Teilnehmer eindeutig (aufgrund der asymmetrischen Kryptographie). Sie
besteht aus einer kryptographischen Prüfsumme (SHA--256, siehe
@sec:SEC04_HASHFUNKTIONEN) eines eindeutigen kryptographischen Zertifikates,
welches für die verschlüsselte Kommunikation und Authentifizierung zwischen den
einzelnen Peers verwendet wird.

[^FN_TLS]: Transport Layer Security: <https://de.wikipedia.org/w/index.php?title=Transport_Layer_Security&oldid=160767422>

Weiterhin ist das aktuelle Design für *Discovery
Spoofing*[^FN_SYNCTHING_SPOOFING] anfällig. Das heißt, dass ein Angreifer der
im Netzwerk mitliest, Device--IDs mitlesen kann und sich somit als ein
bestimmter Peer ausgeben kann. Das würde einem Angreifer die Information
liefern, mit welchen Peers sich eine bestimmte Device--ID synchronisiert. Mehr
zu Device--IDs sowie möglichen damit in Verbindung stehenden Problemen findet
sich in der offiziellen Syncthing--Dokumentation[^FN_SYNCTHING_DEVID].

[^FN_SYNCTHING_SPOOFING]: Problems and Vulnerabilities: <https://docs.syncthing.net/dev/device-ids.html#problems-and-vulnerabilities>
[^FN_SYNCTHING_DEVID]: Understanding Device--IDs: <https://docs.syncthing.net/dev/device-ids.html>

Eine lokale Verschlüsselung der Daten finden nicht statt. Schlüssel, welche die
Device--ID eindeutig identifizieren sind nicht weiter gesichert.

**Librevault** ist ein sich noch im Frühstadium befindlicher Prototyp. Die
aktuell getestete Alphaversion ist beim Hinzufügen eines
Synchronisationsordners reproduzierbar abgestürzt. Laut Projekt--Beschreibung
scheint sich Librevault an Resilio/Syncthing zu orientieren. Weitere Details
zur Spezifikation und Projektzielen sind auf dem Blog des
Entwicklers[^FN_LIBREVAULT_BLOG] zu finden.

[^FN_LIBREVAULT_BLOG]: Librevault Entwicklerblog: <https://librevault.com/blog/>

**git--annex** ist ein sehr stark am git--Versionsverwaltungssystem
orientiertes Synchronisationswerkzeug. Prinzipiell ist es für die Kommandozeile
entwickelt worden, es existiert mittlerweile jedoch ein Webfrontend (Webapp).

git--annex verwaltet nur die Metadaten in git. Es funktioniert als
git--Aufsatz, welcher es dem Benutzer ermöglicht, auch große binäre Dateien
mittels git zu verwalten, beziehungsweise zu synchronisieren. Zum
Synchronisieren der Metadaten wird git verwendet, zum Synchronisieren der
eigentlichen Daten wird git--annex genutzt. Es überträgt die Daten
verschlüsselt mit *rsync über ssh*. Mittels der git--Erweiterung
gcrypt[^FN_GCRYPT] ist es möglich, vollständig verschlüsselte »git--remotes«
anzulegen.

[^FN_GCRYPT]: gcrypt git addon: <https://spwhitton.name/tech/code/git-remote-gcrypt/>

Neben normalen git--Repositories werden sogenannte »Special
Remotes«[^FN_GIT_ANNEX_SPECIALREMOTES] unterstützt. Diese werden verwendet, um
Daten auf ein System, auf welchem git nicht installiert ist, zu synchronisieren.

Neben der Verschlüsselung von git--remotes mit gcrypt gibt es auch die
Möglichkeit, die Daten auf special remotes zu verschlüsseln. Hierfür gibt es
die vier Verfahren:

* **hybrid encryption:** Gemeinsamer »shared key« wird im mit einem »public
  key«  verschlüsselt im Repository gespeichert.
* **shared encryption:** Gemeinsamer »shared key« wird im Klartext im
  Repository gespeichert.
* **public key encryption:** Hierbei wird der »Public--Key« verwendet, zum
  Entschlüsseln benötigt man den »private key«.
* **shared public key encryption:** Wie beim »Public--Key«--Verfahren, jedoch
  nur Besitzer des geheimen Schlüssel dürfen die Daten von einem »special remote« beziehen.

[^FN_GIT_ANNEX_SPECIALREMOTES]: git--annex special remotes: <https://git-annex.branchable.com/special_remotes/>
[^FN_GIT_ANNEX_ENCRYPTION]: git--annex encryption: <http://git-annex.branchable.com/design/encryption/>

### Ähnliche Arbeiten {#sec:SEC02_AEHNLICHE_ARBEITEN}

Neben den genannten dezentralen Projekten existieren weitere Ansätze im Bereich
des dezentralen Datenaustausches:

**Infinit**: Neben dem Datei--Austauschwerkzeug existiert ein dezentrales
Dateisystem. Die Arbeit (vgl. [@quintard2012towards]) von *Julien Quintard*
setzt eine Ebene tiefer als »brig« an und befasst sich mit den Eigenschaften
und dem Entwurf eines dezentralen Dateisystems.

**Bazil**[^FN_BAZIL]ist ein weiteres Projekt, welches als dezentrales
Dateisystem entwickelt wird. Bazil hat ähnliche Ziele wie »brig«. Es
verschlüsselt die Daten, arbeitet dezentral und hat auch Features wie
Deduplizierung von Daten oder Snapshots. Weiterhin ist die
Go--FUSE--Bibliothek[^FN_GOFUSE] aus dem Projekt entstanden, welche auch von
»brig« verwendet wird.

[^FN_BAZIL]: Projektseite: <https://bazil.org/>
[^FN_GOFUSE]: Projektseite GO--FUSE: <https://bazil.org/fuse/>

**IPFS** (InterPlanetary--File--System[^FN_IPFS]) ist ein relativ neuer
dezentraler Ansatz, welcher verschiedene bekannte Technologien kombiniert.
Dadurch lassen sich Schwächen aktuell genutzter Systeme und Protokolle
abmildern oder gar vermeiden. In der aktuellen Implementierung ist das
Projekt jedoch eher als fortgeschrittener Prototyp anzusehen. Aufgrund des
vielversprechenden Ansatzes, ist IPFS die Grundlage von »brig«.

[^FN_IPFS]: InterPlanetary--File System: <https://en.wikipedia.org/w/index.php?title=InterPlanetary_File_System&oldid=757419434>

## Markt und Wettbewerber {#sec:SEC02_MARKT_UND_WETTBEWERBER}

Da der Cloud--Speicher--Markt sehr dynamisch und fragmentiert ist, ist es
schwierig hier zuverlässige Daten zu finden. Laut einem Online--Beitrag der
»Wirtschafts Woche«[^FN_CLOUDSTORAGE] gehören folgende Anbieter zu »den
größten« Cloud--Speicher--Anbietern:

* Dropbox
* Apples iCloud
* Microsoft OneDrive
* Google Drive

[^FN_CLOUDSTORAGE]: Größte Cloud--Speicher--Anbieter:

	<http://www.wiwo.de/unternehmen/it/cloud-wer-sind-die-groessten-cloud-anbieter-und-was-kosten-sie/11975400-7.html>

In Deutschland gehört Dropbox zu den bekannteren Anbietern, Apples iCloud ist
in erster Linie für Mac--Benutzer interessant.

Im Open--Source--Bereich können die Projekte

* OwnCloud
* NextCloud (OwnCloud fork)

als zentrale Konkurrenz--Produkte angesehen werden.

Diese zentralen Systeme stellen in gewisser Weise ein indirektes
Konkurrenz--Produkt dar. Als weitere Wettbewerber können auch die bereits
genannten dezentralen Synchronisationswerkzeuge angesehen werden.

## Closed--Source vs. Open--Source {#sec:SEC02_CLOSEDSOURCE_VS_OPENSOURCE}

Es ist schwierig zu beantworten, ob Open--Source--Software als sicherer
anzusehen ist. Es spielen hierbei sehr viele Faktoren eine Rolle, weswegen eine
eindeutige Aussage nicht möglich ist. Oft wird mit »Linus's Law« --- *Given
enough eyeballs, all bugs are shallow.*[^FN_LINUS_LAW] --- für die Sicherheit *Freier
Software* argumentiert. Software--Bugs wie

[^FN_LINUS_LAW]:Linus's Law: <https://en.wikipedia.org/w/index.php?title=Linus%27s_Law&oldid=761677049>

* Debian--Random--Number--Generator--Bug[^FN_DEBIAN_RNG_BUG]
* Open--SSL--Heartbleed--Bug[^FN_HEARTBLEED]

[^FN_DEBIAN_RNG_BUG]: Random Number Bug in Debian Linux: <https://www.schneier.com/blog/archives/2008/05/random_number_b.html>
[^FN_HEARTBLEED]: Heartbleed: <https://www.schneier.com/blog/archives/2014/04/heartbleed.html>

haben jedoch gezeigt, dass auch Freie Software vor »Sicherheitskatastrophen«
nicht sicher ist. Die besagten Bugs wurden erst nach mehreren Jahren entdeckt
und es ist unbekannt, ob und in welchem Ausmaß diese ausgenutzt werden konnten.
Diese Beispiele zeigen, dass man sich auf das »More eyeballs principle« allein
nicht verlassen darf. Weiterhin kann das Open--Source--Modell auch dazu
verwendet werden, um automatisiert nach Sicherheitslücken im Quelltext auf
GitHub bei jedem Commit zu suchen. Der Google Softwareentwickler *Kees
Cook* verweist auf diese Problematik auf dem aktuellsten *Linux Security Summit
2016*[^FN_LINUX_SEC_SUMMIT].

[^FN_LINUX_SEC_SUMMIT]: Status of the Kernel Self Protection Project:

	<http://events.linuxfoundation.org/sites/events/files/slides/KernelSelfProtectionProject-2016.pdf>

Untersuchungen von Closed-- und Open--Source--Projekten haben gezeigt, dass es
keine signifikanten Unterschiede bezüglich der Sicherheit zwischen den beiden
Entwicklungsmodellen gibt. Open--Source scheint jedoch ein extrem schlechtes
Patch--Management seitens des Herstellers zu verhindern (vgl. [@Schryen]).

Wenn man davon ausgeht, dass schlechte Quellcode--Qualität zu mehr Bugs und
somit zu mehr Sicherheitslücken führt, kann man auch einen Teil der
Sicherheit über die Quellcode--Qualität definieren. Eine Studie, welche die
Quellcode--Qualität von vier großen Betriebssystemkerneln (Linux (open source),
FreeBSD (open source), Solaris (closed source), Windows (closed source)) mit
Hilfe verschiedener Metriken vergleicht, kommt zum Ergebnis, dass es keine
signifikanten Unterschiede zwischen dem Closed--Source-- und
Open--Source--Softwareentwicklungmodell bezüglich Quellcode--Qualität gibt (vgl.
[@Spi08b]). Neuere Studien widersprechen hier und attestieren
Open--Source--Software--Projekten eine tendenziell bessere Quellcode--Qualität
als Closed--Source--Projekten (vgl. [@csr2013] und [@csr2014]).

Durch Freie Software hat der Verbraucher jedoch immer die Möglichkeit, den
Quelltext zu validieren und auch an die eigenen Sicherheitsbedürfnisse
anzupassen. Wenn man beispielsweise wissen möchte, ob und wie die
Festplattenverschlüsselungssoftware (in diesem Fall *Cryptsetup/LUKS*)  den
Volume--Schlüssel aus dem Speicher entfernt, kann man sich den Quelltext auf
GitHub anschauen. Im Fall von LUKS wir der Speicherbereich mit Nullen
überschrieben[^FN_LUKS_VK_MEMSET].

[^FN_LUKS_VK_MEMSET]: LUKS Volume--Key Free--Funktion:

	<https://github.com/mhfan/cryptsetup/blob/ae9c9cf369cb24ac5267376401c80c2c40ada6a2/lib/volumekey.c#L46>

## Gesellschaftliche und politische Aspekte {#sec:SEC02_GESELLSCHAFTLICHE_UND_POLITISCHE_ASPEKTE}

Seit den Snowden--Enthüllungen[^FN_SNOWDEN_LEAK] ist offiziell bekannt, dass
Unternehmen rechtlich gezwungen werden können, personenbezogene Daten an
Behörden weiter zu geben. Betrachtet man die großflächige Verbreitung von
Facebook und Whatsapp, macht es den Anschein, dass viele Menschen für die
Thematik der Privatsphäre nicht genug sensibilisiert sind. Diskutiert man über
sichere Alternativen oder macht Personen auf den problematischen Datenschutz
von zentralen Diensten wie Facebook, Dropbox und Co. aufmerksam, bekommt
man oft das Argument »Ich habe nichts zu verbergen!« zu hören.

[^FN_SNOWDEN_LEAK]: Globale Überwachungs-- und Spionageaffäre:

	<https://de.wikipedia.org/w/index.php?title=Globale_%C3%9Cberwachungs-_und_Spionageaff%C3%A4re&oldid=161594120> \_

Edward Snowden sagte, dass dies der falsche Ansatz ist, weil dadurch das
Grundprinzip der Demokratie »umgedreht« wird. Alle Macht geht vom Volke aus, aber
wenn das Volk überwacht wird --- kann dann noch Demokratie gewährleistet
werden? Ist das Recht auf Privatsphäre mit dem Recht auf freie Meinungsäußerung
vergleichbar?

>> *Arguing that you don’t care about the right to privacy because you have
   nothing to hide is no different than saying you don’t care about free speech
   because you have nothing to say.* -- Edward Snowden

Die eigene Privatsphäre aus der »Ich habe nichts zu verbergen«--Perspektive zu
betrachten, ist ein diskussionswürdiger Ansatz. Es geht bei der Privatsphäre nicht
darum, irgend etwas »Illegales« zu verbergen, es geht um den Schutz der eigenen
Persönlichkeit und um die Wahrung der eigenen Persönlichkeitsrechte. Die
Privatsphäre stellt ein Grundrecht dar und ist in allen modernen Demokratien
verankert[^FN_WP_PRIVACY].

[^FN_WP_PRIVACY]: Privatsphäre: <https://de.wikipedia.org/w/index.php?title=Privatsph%C3%A4re&oldid=161564657>

Ob man etwas zu verbergen hat, wird weiterhin durch den »Beobachter«
entschieden. In unserem heutigen gesellschaftlichen Kontext heißt das, dass
sich die politische Lage auch jederzeit ändern kann. Durch eine Änderung auf
politischer Ebene kann eine vorher als »unschuldig« geglaubte Person plötzlich
aufgrund ihrer politischen Einstellung, ihrem Glauben oder der sexuellen
Orientierung zu einer politisch verfolgten Minderheit gehören.

Dass ein Datensatz über Leben und Tod entscheiden kann, zeigt die Geschichte.
Anfang des 19ten Jahrhunderts wurden in Amsterdam alle Bürger bereitwillig in
einem »Bevölkerungsregister« erfasst. Die dort gespeicherten Informationen
enthielten Beziehungsstatus, Beruf und Religionszugehörigkeit. Die Bürger der
Stadt glaubten sicherlich an ihre »Unschuld« und hatten nichts zu verbergen.
Als im Mai 1940 die deutschen Besatzer einmarschierten, konnten sie anhand des
Registers alle jüdischen Bürger in kürzester Zeit identifizieren. Diese
wurden in Konzentrationslager deportiert. In diesem Fall hat ein einfacher
Datensatz über Leben und Tod entschieden (vgl. [@ct-juden], S. 3).

Nicht nur Daten, die von öffentlichen Einrichtungen erhoben werden sind als
problematisch anzusehen. Auch Daten, die wir jeden Tag unfreiwillig in der
»digitalen Welt« zurücklassen, werden täglich missbraucht --- Personen die sich
als »unschuldig« glaubten, geraten plötzlich ins Visier von Ermittlern.
Ermittlungsfehler, welche unschuldige Menschen hinter Gittern bringen oder zu
Selbstmord treiben, sind hier leider an der Tagesordnung[^FN_DATENMISSBRAUCH].

[^FN_DATENMISSBRAUCH]: Datenmissbrauch und Irrtümer: <http://www.daten-speicherung.de/index.php/faelle-von-datenmissbrauch-und-irrtuemern/>

Laut Meinung des Autors ist es allgemein sinnvoll und wichtig, Daten heutzutage
vorwiegend verschlüsselt zu speichern. Der Wert der Daten wird vom Benutzer oft
nicht »korrekt« eingestuft. Das Paradebeispiel hierfür ist die oben
genannte geschichtliche Entwicklung.

Auch wenn bei mobilen Geräten noch Einsicht herrscht (Diebstahl, Verlust des
Smartphone), wird in anderen Fällen oft argumentiert, dass sensible Daten bei
Bedarf sicher gelöscht werden können. Auch wenn dies für die meisten Fälle
korrekt sein mag, sind folgende Fälle weiterhin als problematisch anzusehen:

* Diebstahl auch bei nicht--mobilen Geräten möglich
* Garantiefall (»defekte« Festplatte kann vielleicht nicht mehr gelöscht werden)
* Software Wipe--Tools bei *SSDs*[^FN_SSD] sind problematisch (vgl. [@BIB_SSD_ERASE])

[^FN_SSD]: Solid--Sate--Drive: <https://de.wikipedia.org/w/index.php?title=Solid-State-Drive&oldid=160808976>
