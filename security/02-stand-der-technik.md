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

![Datenaustausch über zentrale Cloud--Dienste](images/cloud.png){#fig:img-cloud width=80%}

[@fig:img-cloud] zeigt schematisch das Konzept beim Austausch von Daten über
einen Cloud--Speicher--Dienst. Die Daten, des Benutzers , werden hierbei mit
einer »zentrale« Stelle synchronisiert. In der Regel hat der Benutzer bei
bekannten Anbietern einen »Ordner«, welcher nach Installation und Erstellung
eines Accounts bei dem jeweiligen Anbieter, welcher sich dann mit dem
Cloud--Speicher synchronisiert. Dieser »Ordner« lässt sich dann beispielsweise
auf weitere Geräte des Benutzer synchronisieren. Weiterhin gibt es in der Regel
die Möglichkeit Dateien mit anderen Benutzern zu teilen. Welche genauen
Einstellungen sich vornehmen lassen und wie feingranular die die
Benutzerverwaltung und Möglichkeiten beim Synchronisieren sind, ist von dem
jeweiligen Cloud--Speicher--Anbieter abhängig. 

Mittlerweile werben auch die meisten Anbieter damit, dass sich Verschlüsselung
verwenden und die Daten »sicher« in der »Cloud« sind. Spätestens seit den
Snowden--Enthüllungen ist es jedoch klar, dass die Anbieter dazu gezwungen
werden können die Daten herauszugeben.

#### Synchronisations--Software

Die verwendete Software zum Synchronisation ist wieder vom jeweiligen Anbieter
abhängig. Das Problem hierbei ist, dass die Software in der Regel proprietär und
der Benutzer weder die genau Funktionalität noch das Vorhandensein von
Hintertüren ausschließen kann. Die Software liegt in dem meisten Fälle für
verschiedene Plattformen bereit. Weiterhin ermöglichen Anbieter auch die Daten
mittels Webbrowser--Interface zu synchronisieren.

### Sicherheit von Cloud--Speicher--Anbietern

Es ist sehr schwierig die »Sicherheit« der Cloud--Speicher--Anbieter realistisch
zu bewerten, da sowohl die Infrastruktur als auch die verwendete Software
intransparent und proprietär ist.

Die Daten werden laut Aussagen der Hersteller[^applesec][^dropboxsec]
verschlüsselt übertragen und mittlerweile auch verschlüsselt gespeichert.

[^applesec]: Apple iCloud Security: <https://support.apple.com/en-us/HT202303>
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

Ein weiteres Problem ist, dass der Cloud--Anbieter an sich ein zentrales
Angriffsziel bildet. Erst kürzlich wurde bekannt, dass Angreifer im Jahr 2012
ungefähr 70 Millionen Zugangsdaten[^db-dataleak] entwendet haben. Hat ein
Angreifer also die Zugangsdaten erbeutet, bringt die Verschlüsselung die der
Cloud--Dienst betreibt in diesem Fall nichts. Die gestohlenen Passwörter waren
nicht im Klartext einsehbar, moderne Angriffsmöglichkeiten auf Passwörter
zeigen jedoch, dass das nichtsdestotrotz ein großes Problem ist. (siehe hierzu
TODO: Sicherheit von Passwörtern)

[^db-dataleak]: Dropbox <http://www.telegraph.co.uk/technology/2016/08/31/dropbox-hackers-stole-70-million-passwords-and-email-addresses/>

Abhilfe würde in diesem Fall eine zusätzliche Verschlüsselung auf Seiten des
Nutzers helfen, jedoch ist die Software hier für den Endverbraucher oft zu
kompliziert, aufgrund Fehlern in der Implementierung nicht optimal geeignet
(EncFS Audit[^encfsaudit]) oder proprietär (Boxcryptor[^boxcryptor]).

[^encfsaudit]:  EncFS Audit: <https://defuse.ca/audits/encfs.htm>
[^boxcryptor]: Boxcryptor: <https://de.wikipedia.org/wiki/Boxcryptor>

Den meisten Anbietern kann man allerhöchstens Vertrauen, dass diese mit den
Daten und Schlüsseln sorgsam umgehen. Auch wenn sich viele Anbieter wie
beispielsweise *Dropbox* bemühen, aus den Fehlern der Vergangenheit zu lernen
und verbesserte Sicherheitsmechanismen wie beispielsweise
Zwei--Faktor--Authentifizierung in ihre Software zu integrieren, bleibt jedoch
die Krux der Intransparenz und der proprietären Software. Laut Meinung der
Autoren von »brig«, sowie auch vieler Sicherheitsexperten, wird beim Einsatz
proprietärer Software die Sicherheit untergraben, da bei proprietärer Software
explizit eingebaute Hintertüren nicht ausgeschlossen werden können und es auch
keine Möglichkeit der Prüfung auf solche durch den Endbenutzer gibt. 

Insbesondere hat die Freilegung der Snowden--Dokumente weiterhin zu der
Schlussfolgerung geführt, dass der Einsatz von »Freier Software«
empfehlenswerter ist. Bekannte Sicherheitsexperten wie *Bruce
Schneier*[^bruce1][^bruce2] oder auch *Rüdiger Weis* sehen »Freie Software« als
eine der wenigen Möglichkeiten dem Überwachungswahn von Geheimdiensten (oder
auch anderen Institutionen) entgegen zu wirken. Weiterhin kann Kryptographie
dank »Freier Software« von unabhängigen Sicherheitsforschern bewertet werden.

Auch wenn für viele Benutzer die Geheimhaltung der Software und Infrastruktur
auf den ersten Blick als »sicherer« erscheinen mag, widerspricht Sie
dem Kerckhoffs’sche Prinzip, bei welchem die Sicherheit eines System nur von der
Geheimhaltung des Schlüssels, jedoch nicht von der Geheimhaltung weiterer
Systemelemente abhängen sollte. Die Vergangenheit hat beispielsweise beim
GSM--Standard oder DVD--Kopierschutz »CSS«[^css] gezeigt, dass durch die
Geheimhaltung von Systemkomponenten erfolgreiche Angriffe nicht unterbunden
werden können (vgl. [@spitz2011kryptographie], [@ertel2012angewandte, S. 23]). 

[^css]: Cryptanalysis of Contents Scrambling System: <http://www.cs.cmu.edu/~dst/DeCSS/FrankStevenson/analysis.html>

[^bruce1]: Defending Against Crypto Backdoors: <https://www.schneier.com/blog/archives/2013/09/how_to_remain_s.html>
[^bruce2]: How to Remain Secure Against the NSA: <https://www.schneier.com/blog/archives/2013/10/defending_again_1.html>
[^weis]: Krypto nach Snowden | 19. Netzpolitischer Abend: <https://www.youtube.com/watch?v=T_ojwHReMkM>

Abgesehen von den Snowden--Enthüllungen, gibt es für den Endverbraucher viel
näherliegender Gefahren, welche die Daten und Privatsphäre gefährden. Neben den
soeben genannten *Dropbox* Datenleck, das über fast vier Jahre unentdeckt war,
gibt es immer wieder Probleme mit zentralen Diensten:

* Dropbox Client greift auf Daten außerhalb des Sync--Ordners zu[^dropboxschnueffel].
* 7 Millionen Zugangsdaten im Umlauf (unbestätigt)[^zugangsdaten]
* Ausfallzeit über zwei Stunden[^dropboxausfall]
* Datenleck bei Dropbox[^dropboxdatenleck]
* Google Drive Datenleck[^gdrive]
* Microsoft OneDrive Datenleck[^msleck]

[^msleck]: Microsoft OneDrive Datenleck:
<https://www.heise.de/security/meldung/Microsoft-dichtet-OneDrive-Links-ab-2227485.html>
[^gdrive]: Google Drive Datenleck: <https://www.heise.de/security/meldung/Auch-Google-schliesst-Datenleck-im-Cloud-Speicher-2243366.html>
[^dropboxdatenleck]: Datenleck bei Dropbox: <https://www.heise.de/security/meldung/Dropbox-bestaetigt-Datenleck-1656798.html>
[^zugangsdaten]: 7 Mio. Zugangsdaten im Umlauf: <https://www.heise.de/security/meldung/Angeblich-7-Millionen-Dropbox-Passwoerter-im-Umlauf-2423684.html>
[^dropboxschnueffel]: Dropbox unter Schnüffelverdacht: <http://www.heise.de/security/meldung/Dropbox-unter-Schnueffelverdacht-2565990.html>
[^dropboxausfall]: Dropbox Ausfall: <https://www.heise.de/security/meldung/Dropbox-Ausfall-war-kein-Angriff-2083688.html>

### Private Cloud

Weiterhin gibt es bei der Cloud--Speicher--Lösung auch die Möglichkeit einen
eigenen Cloud--Speicher--Dienst aufzusetzen. Hierfür wird oft die
Open--Source--Lösung *Owncloud* genommen. Der Nachteil hierbei ist, dass der
Benutzer selbst für die Bereitstellung der Infrastruktur verantwortlich ist. Für
Unternehmen mag die *Owncloud* durchaus interessant sein. Für die meisten
Privatanwender ist der Aufwand höchstwahrscheinlich zu hoch, weiterhin  haben
diese in der Regel nicht das nötige Know--How, welches essentiell für das
Betreiben eines Cloud--Speicher--Dienstes ist.


### Datenaustausch über dezentrale Lösungen

Der dezentrale Bereich klassifiziert sich durch den Dateiaustausch, welcher in
der Regel *ohne* eine zentrale Instanz auskommt. Es handelt es sich hierbei um
Systeme aus dem Bereich des Peer-to-Peer--Models. Ein der bekannter Vertreter
der P2P--Protkolle ist beispielsweise BitTorrent[^bittorrent]. Das Protokoll
kommt beispielsweise bei der Verbreitung von Linux--Distributionen oder der
Verteilung von Updates bei diversen Spieleherstellern zum Einsatz.

#### Funktionsweise dezentraler Dienste

[@fig:img-p2p] zeigt schematisch den Austausch von Daten in einem dezentralen
Netzwerk. Die dezentralen Systeme unterliegen in der Regel keiner Regulierung
durch eine zentrale Instanz. Je nach verwendeter Technologie zum
Datenaustausch, existieren beispielsweise bei »IPFS« sogenannten
»Bootstrap--Nodes«, welche einen Einstiegspunkt für die jeweiligen Teilnehmer
darstellen. Für weitere Details zu dezentralen Architekturen siehe TODO: Ref Elch?

![Dezentraler Datenaustausch über Peer--to-Peer--Kommunikation](images/p2p.png){#fig:img-p2p width=80%}

Zu den Vertretern der etablierten dezentralen Systeme gibt es vergleichsweise
zu den Cloud--Diensten nur wenige Produkte, welche für die Synchronisation von
Daten beziehungsweise den Austausch von Dokumenten eingesetzt werden können. Zu
den bekannten Lösungen gehören:


* Resilio (ehem. BitTorrent-Sync, proprietär)
* Infinit (proprietär, [@quintard2012towards])
* git--annex (Open--Source)
* Syncthing (Open--Source)
* Librevault (Open--Source)

Bei den bekannten Vertretern wie dem BitTorrent--Client werden die Daten in der
Regel unverschlüsselt übertragen und gespeichert. Eine Authentifizierung finden
in der Regel nicht statt. Alternativen wie Syncthing, Resilio, Librevault oder
Infinit ermöglichen Benutzern auf Basis von dezentralen Netzwerken Dateien zu
tauschen. Ob die Daten verschlüsselt gespeichert und übertragen werden ist je
nach Projekt unterschiedlich und unterliegt Änderungen in der aktuellen
Entwicklungshase. @tbl:1 zeigt den aktuellen Stand bestimmter Features.


<!--
|                      | **Dezentral**       | **Verschlüsselung (Client)**     | **Versionierung**                      |  **Quotas**       | **N-Kopien**    |
| -------------------- | ------------------- | -------------------------------- | -------------------------------------- | ------------------|------------------|
| *Dropbox/Boxcryptor* | \xmark              | \xmark                           | \textcolor{YellowOrange}{Rudimentär}   |  \xmark           | \xmark          |
| *ownCloud*           | \xmark              | \xmark                           | \textcolor{YellowOrange}{Rudimentär}   |  \xmark           | \xmark          |
| *Syncthing*          | \cmark              | \cmark                           | \textcolor{YellowOrange}{Archivordner} |  \xmark           | \xmark          |
| *BitTorrent Sync*    | \cmark              | \cmark                           | \textcolor{YellowOrange}{Archivordner} |  \xmark           | \xmark          |
| ``git-annex``        | \cmark              | \cmark                           | \cmark                                 |  \xmark           |  \cmark         |
| ``brig``             | \cmark              | \cmark                           | \cmark                                 |  \cmark           |  \cmark         |


**Praktische Aspekte:**

|                      | **FOSS**            | **Einfach nutzbar** | **Einfache Installation**  | **Intelligentes Routing** | **Kompression** |
| -------------------- | ------------------- | ------------------- |--------------------------  | ------------------------- |-----------------|
| *Dropbox/Boxcryptor* | \xmark              | \cmark              | \cmark                     |  \xmark                   | \xmark          |
| *ownCloud*           | \cmark              | \cmark              | \xmark                     |  \xmark                   | \xmark          |
| *Syncthing*          | \cmark              | \cmark              | \cmark                     |  \cmark                   | \xmark          |
| *BitTorrent Sync*    | \xmark              | \cmark              | \cmark                     |  \cmark                   | \xmark          |
| ``git-annex``        | \cmark              | \xmark              | \xmark                     |  \xmark                   | \xmark          |
| ``brig``             | \cmark              | \cmark              | \cmark                     |  \cmark                   | \cmark          |

Table: Demonstration of a simple table. {#tbl:1}

-->




Einen bisher nicht genannter, relativ neuen dezentraler Ansatz bietet das
InterPlanetary--File--System, als Teil seiner Funktionalität. Dieses ist in der
aktuellen Implementierung jedoch eher als ein fortgeschrittener Prototyp
anzusehen. Der Ansatz des IPFS--Protokolls ist vielversprechend. IPFS
kombiniert dabei viele bereits bekannte Technologien zu einem einzigen Projekt.
Hierdurch lassen sich schwächen aktuell genutzter Systeme abmildern oder gar
vermeiden. 




Datenintegrität behandeln.

* Datensicherheit
* Ausfallsicherheit


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
in erster Linie für M

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
