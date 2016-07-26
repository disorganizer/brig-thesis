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

Die Anforderungen an ``brig`` lassen sich in drei Kategorien unterteilen:

- Anforderungen an die Integrität: ``brig`` muss die Daten die es speichert 
  versionieren, auf Integrität prüfen können und korrekt wiedergeben können.
- Anforderungen an die Sicherheit: Alle Daten die ``brig`` anvertraut werden,
  sollten sowohl bei der Speicherung "auf der Festplatte" als auch bei der
  Übertragung zwischen Partnern verschlüsselt werden. Die Implementierung
  der Sicherheitstechniken sollte transparent von Nutzern und Experten
  nachvollzogen werden können.
- Anforderungen an die Benutzbarkeit: Die Software soll möglichst einfach zu
  nutzen und zu installieren sein. Der Nutzer soll ``brig`` auf den populärsten
  Betriebssystemen nutzen können und auch Daten mit Nutzern anderer
  Betriebssysteme austauschen können. 

Die Kategorien beinhalten einzelne, konkretere Anforderungen, die im Folgenden 
aufgelistet und erklärt werden. Dabei wird jeweils im ersten Paragraphen die
eigentliche Anforderung formuliert und danach beispielhaft erklärt.
Nicht jede Anforderung kann dabei voll umgesetzt werden. Teils überschneiden
oder widersprechen sich Anforderungen an die Sicherheit und an die Effizienz,
da beispielsweise verschlüsselte Speicherung mit effizienter Dekodierung
kollidiert. Auch ist hohe Benutzbarkeit bei gleichzeitig hohen
Sicherheitsanforderungen schwierig umzusetzen (das Neueingeben eines Passworts
bei jedem Zugriff mag sicherer sein, aber kaum benutzerfreundlich). 
Die Anforderungen werden daher nach dieser Faustregel priorisiert:

$$Benutzbarkeit \ge Sicherheit \geq Effizienz$$

Im Zweifel wurde sich also beim Entwurf also für die Benutzbarkeit entschieden,
da ein sehr sicheres System zwar den Nutzer beschützen kann, er wird es aber
ungern nutzen wollen und eventuell dazu tendieren um ``brig`` herum zu arbeiten.
Das heißt allerdings keineswegs dass ``brig`` »per Entwurf« unsicher ist. 
Es wurden lediglich auf zu invasive Sicherheitstechniken verzichtet, welche den
Nutzer stören könnten.

Gleichzeitig wird allerdings bei Fragen zwischen Effizienz und Sicherheit
zugunsten der Sicherheit entschieden. (TODO: Begründung?)

(TODO: Referenz zu Infinit Thesis hierhin:)

Die Anforderungen sind an die Eigenschaften des verteilten Dateisystems
*Infinit* (beschrieben in [@quintard2012towards], siehe S.39) angelehnt.

### Anforderungen die Integrität

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

**Verfügbarkeit:** Alle Daten die ``brig`` verwaltet sollen stets erreichbar sein und
bleiben. TODO: Problem: Netzwerkpartner nicht erreichbar.

**Integrität:** Es muss sichergestellt werden, dass absichtliche oder
unabsichtliche Veränderungen an den Daten festgestellt werden können.

Unabsichtliche Änderungen können wie oben beschrieben beispielsweise durch
fehlerhafte Hardware geschehen. Absichtliche Änderungen können durch
Angriffe von außen passieren, bei denen gezielt Dateien gezielt von einem
Angreifer manipuliert werden. Als Beispiel könnte man an einen Schüler denken,
welcher unbemerkt seine Noten in der Datenbank seiner Schule manipulieren will.
    
Aus diesem Grund sollte das Dateiformat von ``brig`` mittels Message Authentication
Codes (MACs) sicherstellen können, dass die gespeicherten Daten denen
entsprechen, welche ursprünglich hinzugefügt worden sind.

**Dezentralität:** TODO

**Pinning:** TODO

### Sicherheit

**Verschlüsselte Speicherung:** Die Daten sollten verschlüsselt auf der
Festplatte abgelegt werden und nur bei Bedarf wieder entschlüsselt werden.
Kryptografische Schlüssel sollten aus denselben Gründen nicht unverschlüsselt
auf der Platte abgelegt werden und sonst nur im Hauptspeicher abgelegt werden.

**Verschlüsselte Übertragung:** Bei der Synchronisation zwischen Teilnehmern
sollte der gesamte Verkehr ebenfalls verschlüsselt erfolgen. Nicht nur die
Dateien selbst, sondern auch die dazugehörigen Metadaten sollen verschlüsselt
werden. 

**Authentifizierung:** ``brig`` sollte die Möglichkeit bieten zu überprüfen, ob
Synchronisationspartner wirklich diejenigen sind die sie vorgeben zu sein.
Dabei muss zwischen der initialen Authentifizierung und der fortlaufenden
Authentifizierung unterschieden werden. Bei der initialen Authentifizierung 
wird neben einigen Sicherheitsfragen ein Fingerprint des Kommunikationspartners
übertragen, welcher bei der fortlaufenden Authentifizierung auf Änderung
überprüft wird.

Mit welchen Partnern synchronisiert werden soll und wie vertrauenswürdig diese
sind kann ``brig`` nicht selbstständig ermessen. 
TODO: weitere erläuterung und ersten paragraphen verkleinern

**Identität:** Jeder Benutzer des Netzwerks muss eine öffentliche Identität besitzen welche ihn eindeutig
kennzeichnet. Gekoppelt mit der öffentlichen Identität soll jeder Nutzer ein Geheimnis kennen, mithilfe 
dessen er sich gegenüber anderen authentifizieren kann. Die öffentliche Identität soll menschenlesbar sein
und keine Registrierung an einer zentralen Stelle benötigen. 

Eine mögliches Format für eine menschenlesbare Identität wäre eine abgeschwächte Form der Jabber--ID[^JID] (*JID*).
Diese hat, ähnlich wie eine E--Mail Adresse, die Form ``Nutzer@Domäne.tld/Ressource``. 
Beim Jabber/XMPP Protokoll ist der Teil hinter dem ``/`` optional, der Rest ist zwingend erforderlich.
Als Abschwächung wird vorgeschlagen, auch den Teil hinter dem ``@`` optional zu machen. 
Valide Identitätsbezeichner wären also:

- ``alice``
- ``alice@company``
- ``alice@company.de``
- ``alice@company.de/laptop``
- ``böb@subdomain.company.de/desktop``

TODO: genaue regeln 

Dies hat aus unserer Sich folgende wesentlichen Vorteile:

- Eine E--Mail Adresse  oder eine JID ist gleichzeitig ein valider Identitätsbezeichner.
- Der Nutzer kann eine fast beliebige Unicode Sequenz als Name verwenden, was beispielsweise
  für Nutzer des kyrillischen Alphabetes nützlich ist.
- Unternehmen können die Identifikationsbezeichner hierarchisch gliedern. So kann *Alice* der
  Bezeichner ``alice@security.google.com`` zugewiesen werden, wenn sie im Sicherheitsteam arbeitet.
- Der *Ressourcen*--Teil hinter dem ``/`` ermöglicht die Nutzung desselben Nutzernamens auf verschiedenen Geräten,
  wie ``desktop`` oder ``laptop``. 

[^JID]: \url{https://de.wikipedia.org/wiki/Jabber_Identifier}

**Sicheres Teilen:** 

**Transparenz:** 

### Benutzbarkeit

**Automatische Versionierung:** Die Dateien die ``brig`` verwaltet, sollen automatisch versioniert
werden. Die Versionierung soll dabei in Form von Checkpoints bei jeder Dateiänderung
erfolgen. Größere Mengen von Checkpoints können manuell oder per Timer in einem
zusammenhängenden Commit zusammengefasst werden. Die Menge an Dateien die in alter Version
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
alle Nutzer ``brig`` verwenden (Lock--in, TODO). Aus diesem Grund 

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


## Annahmen

- Sicherheit der verwendeten Algorithmen gewährleistet -> Quantencomputer.
- IPFS Annahmen:
