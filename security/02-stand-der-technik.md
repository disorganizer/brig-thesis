# Stand der Technik

## Wissenschaftlicher Stand

### Sicherheit und Usability von Dateiverteilungssystemen

Zentrale und dezentrale Systeme sind die Basis für den Austausch von
Informationen. Ob ein System zentral oder dezentral fungiert ist nicht immer
klar abgrenzbar. Oft kommen auch hybride Systeme zum Einsatz, welche zwar
dezentral funktionieren, jedoch eine Zentrale Instanz benötigen, hier wäre
beispielsweise das *Torrent*--Konzept zu nennen, weitere Informationen hierzu
sind unter [@cpahl] zu finden. Bei den Cloud--Storage--Service Anbietern wird
Dropbox als Vertreter der Klasse zentraler Systeme hergenommen.

#### Datenaustausch über zentrale Cloud--Dienste

Zentrale Dienste klassifizieren sich durch die Eigenschaft, dass es eine
zentrale Instanz gibt, welche zum Austausch der Daten benötigt wird. Dies sind
in den meisten Fällen die Storage--Server der Cloud--Service Anbieter, welche
für die Kommunikation und Speicherung der Daten zuständig sind.

**Allgemeine Sicherheit:** Beim Einsatz zentraler Dienste hängt die Sicherheit
der Daten in erster Linie vom Dienstanbieter ab. Den meisten Anbietern kann man
allerhöchstens Vertrauen, dass diese mit den Daten sorgsam Umgehen. Auch wenn
sich viele Anbieter wie beispielsweise Dropbox bemühen aus den Fehlern der
Vergangenheit zu lernen und verbesserte Sicherheitsmechanismen wie
beispielsweise Zwei--Faktor--Authentifizierung in Ihre Software zu integrieren,
bleibt jedoch die Krux der proprietären Software. Laut Meinung der Autoren von
brig, sowie auch vieler Sicherheitsexperten, wird den Einsatz proprietärer
Software die Sicherheit untergraben, da bei proprietärer Software explizit
eingebaute Hintertüren nicht ausgeschlossen werden können und es auch keine
Möglichkeit der Prüfung auf solche durch den Endbenutzer gibt.

**Datenverschlüsselung:** Ein weiteres Problem ist die Umsetzung der
Daten--Verschlüsselung der gängigen Cloud--Storage--Anbieter. Anbieter wie
Dropbox verschlüsseln laut eigener Aussage die Daten in der Cloud nach
aktuellen Sicherheitsstandards. Das Problem hierbei ist jedoch, dass Dropbox
und nicht der Endbenutzer der alleinige Schlüsselinhaber ist. Es ist also, auch
wenn es laut Dropbox verboten ist, möglich dass Mitarbeiter beziehungsweise
dritte Parteien die Daten des Nutzers einsehen können (vgl. [@ko2015cloud] S.
103 ff.). Abhilfe würde in diesem Fall eine zusätzliche Verschlüsselung auf
Seiten des Nutzers helfen, jedoch ist die Software hier für den Endverbraucher
oft zu kompliziert, aufgrund Fehlern in der Implementierung nicht optimal
geeignet (EncFS Audit[^encfsaudit]) oder proprietär (Boxcryptor[^boxcryptor]).

[^encfsaudit]:  EncFS Audit: <https://defuse.ca/audits/encfs.htm>
[^boxcryptor]: Boxcryptor: <https://de.wikipedia.org/wiki/Boxcryptor>

Die Sicherheit der Software beziehungsweise der verwendeten Algorithmen hängt
in diesem Fall nicht alleine vom Schlüssel ab, wie es nach Kerckhoffs' Prinzip
gefordert wird. Die Vergangenheit hat beispielsweise beim GSM--Standard
gezeigt, dass durch die Geheimhaltung eines Verschlüsselungsverfahrens
erfolgreiche Angriffe nicht unterbunden werden konnten (vgl.
[@spitz2011kryptographie]).

Weiterhin gibt es bei den Cloud--Storage--Lösung auch die Möglichkeit einen
eigenen Cloud--Storage--Dienst aufzusetzen. Hierfür wird oft die
Open--Source--Lösung *Owncloud* genommen. Der Nachteil hierbei ist, dass der
Benutzer selbst für die Bereitstellung der Infrastruktur verantwortlich ist.
Eine weitere Hürde stellt für den Verbraucher das fehlende Know--How dar,
welches essentiell für das Betreiben eines Cloud--Dienstes ist.

Ein weiterer Bereich sind sogenannte One--Click--Hoster, welche es dem Benutzer

#### Dezentraler Datenaustausch

Der dezentrale Bereich klassifiziert sich durch den Dateiaustausch, welcher
in der Regel ohne eine zentrale Instanz auskommt. In der Regel handelt es sich
hierbei um Systeme aus dem Bereich des Peer-to-Peer--Models. Eins der
bekanntesten Vertreter der P2P--Protkolle ist BitTorrent[^bittorrent]. Das
Protokoll kommt beispielsweise bei der Verbreitung von Linux--Distributionen
oder der Verteilung von Updates bei diversen Spieleherstellern zum Einsatz. 

Die dezentralen Systeme unterliegen in der Regel keiner Regulierung durch eine
zentrale Instanz. Unter den Vertretern der dezentralen Systeme gibt es
vergleichsweise zu den Cloud--Diensten nur wenige Produkte, welche für die
Synchronisation von Daten beziehungsweise den Austausch von Dokumenten
eingesetzt werden für den Endbenutzer konzipiert sind. Zu den bekannten
Lösungen gehören:

* Resilio (ehem. BitTorrent-Sync, proprietär)
* Infinit (Open--Source) 
* Syncthing (Open--Source) 

Bei den bekannten Vertretern wie dem BitTorrent--Client werden die Daten in der
Regel unverschlüsselt übertragen und gespeichert. Eine Authentifizierung finden
in der Regel nicht statt. Alternativen wie Syncthing, Resilio oder Infinit
ermöglichen Benutzern auf Basis von dezentralen Netzwerken Dateien zu tauschen.
Ob die Daten verschlüsselt gespeichert und übertragen werden ist je nach
Projekt unterschiedlich und unterliegt Änderungen in der aktuellen
Entwicklungshase.

Einen bisher nicht genannter, relativ neuen dezentraler Ansatz bietet das
InterPlanetary--File--System, als Teil seiner Funktionalität. Dieses ist in der
aktuellen Implementierung jedoch eher als ein fortgeschrittener Prototyp
anzusehen. Der Ansatz des IPFS--Protokolls ist vielversprechend. IPFS
kombiniert dabei viele bereits bekannte Technologien zu einem einzigen Projekt.
Hierdurch lassen sich schwächen aktuell genutzter Systeme abmildern oder gar
vermeiden. 

### Ähnliche Arbeiten

Von den genannten Projekten haben die folgenden Gemeinsamkeiten mit brig,
verfolgen jedoch unterschiedliche Ziele:

* Infinit
* Resilio
* Syncthing
* Bazil[^bazil] 

[^bazil]: Projektseite: <https://bazil.org/>

* Schöler Mail--Link

## Markt und Wettbewerber

* Google Drive/Dropbox mit encfs
* Syncthing
* git--annex
* Btsync
...

## Problemstellung

* Datensicherheit
* Ausfallsicherheit

## Gesellschaftliche und Politische Aspekte

Seit den Snowden--Enthüllungen ist offiziell bekannt, dass Unternehmen im
Notfall rechtlich gezwungen werden können personenbezogene Daten rauszugeben.

* Snowden--Affäre
* Gesellschaftliche Aspekte: Ich habe nichts zu verbergen
* politische Lage und Probleme

## Verschiedene Alternativen

Es gibt Alternativen, diese haben jedoch Probleme:

* kompliziert
* unsicher
* propritär
* ...
