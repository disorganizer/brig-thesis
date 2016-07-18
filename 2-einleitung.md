# Einleitung

In diesem Kapitel wird... TODO

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
Effizienz (wie beispielsweise die meisten verteilten Dateisysteme es tun)
sondern versucht möglichst generell anwendbar über Netzwerkgrenzen hinweg zu
sein. 

## Eigenschaften und Anforderungen

TODO: Infinit thesis anschauen wegen Anforderungen.

Basis:

    Durability:  Keep what was inserted once agreed.
        Problem: Hardware ist nicht ausfallsicher, kann gestohlen werden.
        -> Redundanz.

    Availability: Daten müssen erreichbar sein und bleiben.
        -> Ausfallsicherheit
        
    Integrity: Inserted == Output (MACs etc.)
        Daten sollen nicht absichtlich oder unabsichtlich verändert werden können.

    Effizienz: 

Sicherheit:

    Privacy: Verschlüsselte Speicherung.
    Anonymität:  Verschlüsselte übertragung.
    Sharing: Easy sharing with other users being users of brig or not. 
    Offenheit und Transparenz: 

Benutzbarkeit:

    Versionierung: 
        Verhinderung mehrerer Nutzerkopien.

    Usability:
        Vertrautheit: Organisation als Datei.
        Einfache Installation
        Einfache Nutzung

    Capacity: No size/file limits

    Generalität: Keine Nutzung von techniken die den Nutzerstamm
    auf bestimmte Plattformen einschränken würde oder den Kauf zusätzlicherHardware
    bedingt. Der Einsatz von btrfs oder zfs zur Speicherung oder die Annahme
    eines bestimmten RAID--Verbundes entfällt daher.
    Portabilität: Auch mobile Plattform, zunehmende Fragmentierung

## Zielgruppen

Auch wenn ``brig`` extrem flexibel einsetzbar ist, sind die primären Zielgruppen
Unternehmen und Heimanwender. Aufgrund der starken Ende-zu-Ende Verschlüsselung
ist ``brig`` auch für Berufsgruppen, bei denen eine hohe Diskretion bezüglich
Datenschutz gewahrt werden muss, attraktiv. Hier wären in erster Linie
Journalisten, Anwälte, Ärzte mit Schweigepflicht auch Aktivisten und politisch
verfolgte Minderheiten, zu nennen.

### Unternehmen

Unternehmen können ``brig`` nutzen, um ihre Daten und Dokumente intern zu
verwalten. Besonders sicherheitskritische Dateien entgehen so der Lagerung in
Cloud--Services oder der Gefahr von Kopien auf unsicheren
Mitarbeiter--Endgeräten. Größere Unternehmen verwalten dabei meist ein
Rechenzentrum in dem firmeninterne Dokumente gespeichert werden. Von den
Nutzern werden diese dann meist mittels Diensten wie *ownCloud* oder *Samba*
»händisch« heruntergeladen.

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

## Problemstellung

Hürden bei entwicklung

## Annahmen
