# Evaluation {#sec:evaluation}

In diesem Kapitel wird die Implementierung und die dahinter stehende
Architektur auf Schwächen untersucht. Es wird gezeigt, was die Software nicht
zu leisten vermag und welche eingangs definierten Anforderungen sie (noch)
nicht erfüllen kann. Abgeschlossen wird das Kapitel mit verschiedenen
Geschwindigkeitsmessungen, sowie einigen Konzepten zur weiteren Entwicklung.

## Was ``brig`` *nicht* ist

``brig`` kann nicht die beste Alternative in allen Bereichen sein. Keine
Software kann die sprichwörtliche »eierlegende Wollmilchsau«[^WOLLMILCH] sein und sollte
auch nicht als solche benutzt werden. Insgesamt ist es für folgende Bereiche
weniger geeignet:

[^WOLLMILCH]: Siehe auch: <https://de.wikipedia.org/wiki/Eierlegende_Wollmilchsau>

**High Performance:** Besonders im Bereich Effizienz kann es nicht mit hochperformanten
Cluster--Dateisystemen wie Ceph[^CEPH] oder GlusterFS[^GLUSTER] mithalten.  Das
liegt besonders an der sicheren Ausrichtung von ``brig``, welche oft
Rechenleistung zugunsten von Sicherheit eintauscht (siehe [@sec:benchmarks]).

**Echtzeitanwendungen:** Schreibt ein Nutzer etwas in eine Datei, so ist diese
Änderung nicht augenblicklich anderen Nutzern zugänglich. Selbst wenn
Live--Updates (siehe [@sec:transfer-layer]) verfügbar sind, kann ``brig``
selbst entscheiden, wann die Änderungen synchronisiert werden.[^SYNC_NOTE]
Insbesondere macht es beispielsweise kaum Sinn, SQL--Datenbanken von ``brig``
synchronisieren zu lassen. Hierfür gibt es weitaus bessere Alternativen wie
*CockroachDB*[^COCKROACH].

[^COCKROACH]: <https://www.cockroachlabs.com>

[^SYNC_NOTE]: In der momentanen Implementierung bei jedem ``fsync()`` und beim Schließen einer Datei.

**Volle POSIX-Kompabilität notwendig:** Der *POSIX*--Standard definiert (unter
anderem) eine gemeinsame, standardisierte API, die von vielen (zumeist
unixoiden) Betriebssystemen implementiert wird (siehe auch [@1999standard]).
Nicht alle Teile dieses Interfaces können von ``brig`` umgesetzt werden. So
gibt es kaum eine verträgliche Definition von harten und weichen Verlinkungen
(*Hardlinks* und *Symbolic Links*) für dezentrale Netzwerke. Auch spezielle
Dateien wie *FIFOs* können in diesem Kontext nicht ohne Race--Conditions
umgesetzt werden. Entsprechende Operationen werden von *FUSE--Layer* mit
dem *POSIX*--Fehlercode ``ENOSYS`` (»nicht implementiert«) quittiert.

**Glaubhafte Abstreitbarkeit:** Auch wenn ein ``brig``--Repository in der
geschlossenen Form als sicherer »Datensafe« einsetzbar ist, so bietet ``brig``
nicht die Eigenschaft der »glaubhaften Abstreitbarkeit«[^ABSTREIT], die
Werkzeuge wie Veracrypt bieten.

**Zeilenbasierte Differenzen:** Im Gegensatz zu Versionsverwaltungssystemen wie ``git``,
kann ``brig`` keine zeilenbasierten Differenzen zwischen zwei Dateien anzeigen,
da es nur auf den Metadaten von Dateien arbeitet.

**Reiner Speicherdienst auf der Gegenseite:** Auf der Gegenseite muss ein
``brig``--Daemon--Prozess laufen, um mit der Gegenseite zu kommunzieren. Daher
können reine Speicherdienste wie *Amazon S3*[^AMAZON_S3] nicht ohne weiteres
als Datenlager benutzt werden. Das kann allerdings leicht umgangen werden,
indem der entfernte Speicher lokal gemounted[^REMOTE_MOUNT] wird, und der
``brig``--Prozess lokal gestartet wird. Werkzeuge wie ``rsync`` oder ``git-annex``
benötigen lediglich einen ``ssh``--Zugang zum Datenlager und funktionieren
daher auch ohne Gegenüber.

**Keine starke Ausfallsicherheit:** ``brig`` speichert nur ganze Dateien auf
$1$ bis $n$ Knoten. Es wird kein *Erasure--Enconding*[^ERASURE_ENCODING]
angewendet, wie beispielsweise ``Tahoe-LAFS`` das tut. Damit eine Datei im
Falle des Ausfalls eines Knotens wiederherstellbar ist, muss mindestens ein
anderer Knoten, die Datei vollständig gespeichert haben, während andere
Werkzeuge kleine Blöcke der Dateien redundant auf mehreren Rechnern ablegen.
Werden diese beschädigt können diese sich selbst reparieren oder von anderen
Knoten neu übertragen werden. Für die meisten Anwendungszwecke ist
aus Sicht des Autors Redundanz auf dem Dateilevel ausreichend.

**Embedded Devices:** ``brig`` benötigt ein vollständiges Betriebssystem mit
Netzwerkanschluss, Hauptspeicher und einer ausreichend starken CPU. Die
»unterste Grenze« für einen vernünftigen Betrieb wäre vermutlich ein aktueller
Raspberry Pi in Version 3.

[^REMOTE_MOUNT]: Möglich mittels Werkzeugen wie ``sshfs``
(<https://de.wikipedia.org/wiki/SSHFS>) und ``s3fs``
(<https://github.com/s3fs-fuse/s3fs-fuse>)

[^AMAZON_S3]: Mehr Informationen unter:
<https://de.wikipedia.org/wiki/Amazon_Web_Services\#Speicher>

[^REPO]: *Repository:* Hier ein »magischer« Ordner in denen alle Dateien im
Netzwerk angezeigt werden.

[^ERASURE_ENCODING]: Eine Enkodierung, welche die Wiederherstellung der Inhalte
bis zu einen gewissen, konfigurierbaren *Beschädigungsgrad* erlaubt. Siehe auch
[@lin2010secure].

[^CEPH]: Webpräsenz: <http://ceph.com>
[^GLUSTER]: Webpräsenz: <https://www.gluster.org>
[^ABSTREIT]: Siehe auch: <https://de.wikipedia.org/wiki/VeraCrypt>

## Erfüllung der Anforderungen

Im Folgenden wird die Umsetzung der in [@sec:requirements] aufgelisteten
Anforderungen betrachtet. Auf jede Anforderung wird dabei kurz zusammenfassend
eingegangen und die Erfüllung wird mit »\cmark« (*Erfüllt*), »\qmark«
(*Teilweise erfüllt*) und »\xmark« (*Überwiegend nicht erfüllt*) bewertet.

### Anforderungen an die Integrität

**Entkopplung von Metadaten und Daten** (\cmark): Daten und Metadaten sind
vollkommen entkoppelt und werden sowohl getrennt gespeichert (``ipfs`` und
*BoltDB*) als auch getrennt behandelt. Die Daten können irgendwo im
``ipfs``--Netzwerk liegen, die Metadaten werden von allen Teilnehmern vorgehalten.

**Pinning** (\qmark): Es ist möglich einen Pin zu Dateien und Verzeichnissen
hinzuzufügen (``brig pin``) und wieder zu entfernen (``brig pin -u``).
Allerdings wird dieses Konzept von ``brig`` selbst noch sehr simpel behandelt.
Neu hinzugefügte Dateien bekommen automatisch einen Pin, die Pins eines
Synchronisationspartners werden nicht übernommen. Der Pin von gelöschten
Dateien wird entfernt. Es wird allerdings im momentanen Zustand weder eine
Speicherquote eingehalten, noch wird der Pin automatisch ab einer bestimmten
Versionierungstiefe entfernt.

**Langlebigkeit** (\qmark): Redundante Speicherung von Dateien ist manuell möglich,
aber noch ist keine Anzahl minimaler Kopien einstellbar, die von ``brig``
überwacht wird. Eine Veränderung der Datei kann durch Neuberechnung der
Prüfsumme überprüft werden.

**Verfügbarkeit** (\qmark): Lokale Daten sind stets verfügbar. Daten von
Synchronisationspartnern sind verfügbar wenn diese online sind. Ein Knoten der
automatisch alle Metadaten von mehreren Partnern sammelt scheint technisch
machbar (entsprechend dem Nutzer »``rabbithole@wonderland``« in
[@sec:remote-list]), ist aber noch nicht implementiert. Problematisch für den
Nutzer ist der Umgang mit momentan nicht verfügbaren Dateien. ``brig`` selbst
hat keine Informationen darüber ob die Datei tatsächlich verfügbar ist, da
diese Aufgabe von ``ipfs`` übernommen wird. Daher wird dies für den Benutzer
erst ersichtlich wenn er versucht die Datei auszulesen. Sollte die Datei nicht
verfügbar sein, so wird das Öffnen der Datei eine lange Zeit benötigen und
schließlich mit einem Zeitüberschreitungsfehler enden. Hier müsste ``brig``
mehr Aufwand betreiben, um den Nutzer dabei zu helfen nicht zugreifbare Dateien
frühzeitig zu erkennen.

**Integrität** (\cmark): Jede Datei ist in Blöcke aufgeteilt, von denen jeder
eine MAC speichert. Mithilfe dieser können absichtliche und unabsichtliche
Modifikationen erkannt werden. Eine Integritätsprüfung für Metadaten
(beispielsweise eine MAC die den Store--Inhalt vor der Übertragung absichert)
ist allerdings noch nicht implementiert.

### Anforderungen an die Sicherheit

**Verschlüsselte Speicherung:** (\cmark) Jede Datei wird in einem
verschlüsselten Container (siehe [@sec:encryption]) abgelegt.
Der Schlüssel wird momentan zufällig generiert und wird mit den anderen
Metadaten zum Synchronisationspartner übertragen.

**Verschlüsselte Übertragung:** (\cmark) Nicht nur ``ipfs``--Verbindungen an
sich werden verschlüsselt, auch ``brig's`` Transferprotokoll (welches darauf
aufsetzt) verschlüsselt die Daten zusätzlich, um sich gegen eventuelle Lücken in
``ipfs`` abzusichern.

**Authentifizierung:** (\cmark) Bevor eine Synchronisation stattfinden kann,
müssen die Teilnehmer auf beiden Seiten ihr Gegenüber initial authentifizieren.
Das geschieht indem sie den Nutzernamen mit der dazugehörigen
Identitäts--Prüfsumme über einen sicheren Seitenkanal vergleichen. Da die
Prüfsumme fälschungssicher ist, muss es sich um den gewünschten Partner
handeln. Nach erfolgreicher initialer Authentifizierung wird der Partner in die
Remote--Liste unter seinem Nutzernamen aufgenommen. Bei jedem
erneuten Verbindungsaufbau zum Kommunikationspartner wird dieser basierend auf
den Informationen in der Remote--Liste authentifiziert.

**Identität:** (\cmark) Als menschenlesbarer Identifikationsbezeichner wird
eine modifizierte Form der Jabber--ID eingesetzt. Dieses Format ist gut lesbar
und schränkt den Nutzer bei der Namenswahl nicht signifikant ein. Wie in [@sec:user-management]
beschrieben, wird keine zentrale Instanz zur Registrierung benötigt.

**Transparenz:** (\cmark) Die Implementierung steht unter der freien
``APGLv3``--Lizenz. Diese stellt rückwirkend die Freiheit des Quelltextes
sicher. Zukünftige Versionen könnten prinzipiell proprietär werden, falls
die Entwickler sich dazu entscheiden sollten. Auch wenn das nicht die aktuelle
Absicht der Entwickler ist, könnte ``brig`` in diesem Fall von der
Open--Source--Community weiterentwickelnd werden. Eine Einsicht in den Quelltext
oder Beteiligung am Projekt ist durch die Code--Hosting--Plattform *GitHub*
leicht möglich.

### Anforderungen an die Usability

**Automatische Versionierung:** (\cmark) Eine Versionierung von Dateien ist
gegeben, die vergleichbar mit ``git`` ist und umfangreicher als die, der
meisten existierenden Werkzeuge. Momentan wird (hardkodiert) alle 15 Minuten
ein automatisierter Commit gemacht (falls Änderungen vorlagen). Wie bereits
oben beschrieben, wurde allerdings noch keine Quota implementiert, weshalb
viele Änderungen an großen Dateien schnell sehr viel Speicherplatz benötigen
werden.

**Portabilität:** (\qmark) Bei der Entwicklung wurde bei der Auswahl der
Bibliotheken auf leichte Portierbarkeit zu anderen Systemen geachtet. Getestet
und eingesetzt wurde die Software bisher nur auf einem Linux--System.
Prinzipiell sollte sie auf anderen unixoiden Systemen lauffähig sein. Die volle
Portierung auf Windows ist problematischer, da dort FUSE nicht lauffähig ist.
Dabei gäbe es entweder die Möglichkeit eine Implementierung
für das ähnliche, rein Windows--komaptible *Dokany*[^DOKANY] zu liefern oder
einen WebDAV[^WEBDAV] Server zu implementieren. Bei letzterer Option
würde ``brigd`` als WebDAV--Server fungieren, der von Windows und anderen
Betriebssystemen als Dateisystem eingehängt werden kann.
Noch schwieriger wird der Einsatz von ``brig`` auf mobilen Plattformen. Dort
ist *Go* momentan nur bedingt einsetzbar[^MOBILE]. Sollte es einsetzbar werden,
müsste eine eigene grafische Oberfläche implementiert werden, um ``brig``
beispielsweise auf einem Android--Smartphone nutzen zu können.

[^DOKANY]: <https://github.com/dokan-dev/dokany>, eine Go--Bibliothek ist bereits verfügbar: <https://godoc.org/github.com/keybase/kbfs/dokan>
[^WEBDAV]: <https://de.wikipedia.org/wiki/WebDAV>

**Einfache Installation:** (\cmark) Auf unixoiden Betriebssystemen ist die
Installation sehr einfach (siehe auch [@sec:installation]). Die einzige
Abhängigkeit von ``brig`` ist *Go*. Im späteren Projektverlauf können für die
meistgenutzten Plattformen und Architekturen auch fertige Binärdateien angeboten werden.

**Keine künstlichen Limitierungen:** (\cmark) Durch den FUSE--Layer wird ein
ganz normaler Systemordner bereitgestellt. Bis auf den lokalen
Festplattenspeicher hat dieser keine zusätzlichen Limitierungen. Der einzige
Unterschied für den Benutzer ist, dass die darin gespeicherten Daten entweder
gar keinen Speicherplatz brauchen oder (durch das Verschlüsselungsformat)
geringfügig größer ist als die eigentliche Datei. Durch die Versionierung
benötigen zudem alte Kopien zusätzlichen Speicherplatz.

**Generalität:** (\qmark) ``brig`` ist mit denen im Punkt »Portabilität«
genannten Einschränkungen auf allen Rechnern lauffähig und macht keine Annahmen
zum Dateisystem oder zur Hardware auf der es läuft. Momentan sind allerdings
alle Nutzer, mit denen synchronisiert werden soll, gezwungen ``brig`` zu
nutzen. Dies betrifft auch Nutzer, mit denen nur eine einzelne geteilt werden
soll. Ein »HTTPS--Gateway«, mit dem einzelne Dateien veröffentlicht werden
können wurde noch nicht implementiert.

**Stabilität:** (\xmark) Die momentane Implementierung ist vergleichsweise instabil
und bräuchte mehr Testfälle, um ein gewisses Vertrauen in die Stabilität der
Software herzustellen. Welchen Umfang die Testsuite momentan hat, kann in
[@sec:testsuite] nachgelesen werden.

**Effizienz:** (\qmark) ``brig`` ist schnell genug, um auf einem typischen
Arbeitsrechner eine lokale Full--HD Filmdatei vom FUSE--Dateisystem aus abzuspielen.
Details zu der Geschwindigkeit findet sich in [@sec:benchmarks]. Besonders im
FUSE--Dateisystem sind noch einige Optimierungsmöglichkeiten vorhanden, welche
die Gesamteffizienz steigern können.

## Stand der Testsuite {#sec:testsuite}

Obwohl die Testsuite im momentanen Zustand zu klein ist, existieren für die
meisten Pakete bereits Unittests. Insgesamt gibt es derzeit 24 Dateien die Tests
beinhalten, in denen sich 50 einzelne Unittests befinden.
Diese versuchen immer möglichst kleine Teile der Codebasis anzusprechen,
um die Fehlersuche zu erleichtern. So wird für viele Tests ein *Mock*--Store
in einem temporären Verzeichnis angelegt oder es wird ein temporäres ``ipfs``--Repository
angelegt anstatt diese Arbeit den Quelltext hinter »``brig init``« erledigen zu lassen.
Diese Methode hilft zusätzlich, um den Quelltext allgemein und austauschbar zu halten.

Noch existieren keine Zahlen, was die Testabdeckung angeht. Diese machen aus
Sicht des Autors zum jetzigen Zeitpunkt auch noch keinen Sinn, da sich die
Implementierung noch stark verändern wird. In Zukunft sollte die »Coverage«
aber ein wichtiges Instrument werden, um nicht getesteten Quelltext
aufzuspüren.

## Benchmarks {#sec:benchmarks}

Die Umsetzung von sauberen Benchmarks ist schwierig, da ``brig`` genau wie
andere Synchronisationswerkzeuge ein sehr komplexes System ist, dessen
Effizienz von einer Vielzahl von Faktoren abhängt. Grundsätzlich ist es
schwierig die Gesamteffizienz eines Systems sinnvoll zu messen, da folgende
Komponenten sich von System zu System drastisch unterscheiden können:

* Hauptspeicher und Prozessor.
* Speichermedium  und Netzwerklatenz.
* Betriebssystem und verwendeter Scheduler.
* Spezielle Befehlserweiterungssätze[^SSE].

[^SSE]: Beispielsweise SSE4.x: <https://de.wikipedia.org/wiki/Streaming_SIMD_Extensions_4>

### Aufbau

Aus diesem Grund wird im Folgenden rein die lokale Effizienz beim Hinzufügen
einer Datei in Megabyte pro Sekunde untersucht. Alle Benchmarks
werden direkt im Hauptspeicher ausgeführt, es erfolgen keine Festplattenzugriffe.
Möglich wird das durch den Einsatz eines ``ramfs``[^RAMFS], welches ein temporäres
Dateisystem bereitstellt, in dem alle Dateien direkt im Hauptspeicher geschrieben
und gelesen werden. Dadurch ist der Prozessor[^CPU] der ausschlaggebende Faktor
bei der Effizienz in diesem Benchmark, da ausreichend Hauptspeicher vorhanden war.

[^RAMFS]: <https://de.wikipedia.org/wiki/Ramfs>
[^CPU]: In diesem Fall ein *AMD Phenom(tm) II X4 955*.

Als Eingabedateien wurden zwei unterschiedliche Datensätze genommen:

* Eine schlecht komprimierbare Filmdatei[^BBB].
* Ein gut komprimierbarer Textkorpus in deutscher Sprache[^CORPUS].

[^BBB]: Die 1080p Version von *Big Buck Bunny* von <http://bbb3d.renderfarming.net/download.html>
[^CORPUS]: <http://corpora2.informatik.uni-leipzig.de/downloads/deu_news_2015_3M.tar.gz>

Aus beiden Dateien werden jeweils zehn kleinere Dateien durch Abschneiden hergestellt.
Diese sind jeweils 1, 2, 4, 8, 16, 32, 64, 128, 256 und 512 MB groß sind und werden in das
``ramfs`` gelegt. Es entstehen also insgesamt 20 kleinere Dateien. Im
``ramfs`` wird ebenfalls ein ``brig``--Repository und ein ``ipfs``--Repository angelegt.
Zudem wird im ``ramfs`` noch ein FUSE--Dateisystem, basierend auf dem
``brig``--Repository angelegt.

Basierend auf diesen Eingabedateien werden für beide Datensätze folgende Zeitmessungen erhoben:

* Lesen mit/ohne Dekompression und mit/ohne Entschlüsselung.
* Schreiben mit/ohne Kompression und mit/ohne Verschlüsselung.
* Lesen direkt von ``ipfs`` mit/ohne Entschlüsselung plus Dekompression.
* Schreiben direkt zu ``ipfs`` mit/ohne Verschlüsselung plus Kompression.
* Hinzufügen der Datei über ``brig stage``.
* Ausgabe der Datei mit ``brig cat`` und über das FUSE--Dateisystem mit ``cat``.

Als Grunddurchsatz (»Baseline«) wird zusätzlich gemessen wie lange ein
direktes Kopieren der Datei im ``ramfs`` dauert. Zur Kompression wurde immer
der *Snappy*--Algorithmus verwendet. *LZ4* zeigt ähnliche Eigenschaften, ist
aber stets etwas langsamer. Zur Verschlüsselung wird *ChaCha20* eingesetzt. Das
ebenfalls unterstützte *AES256* im GCM--Modus war ebenfalls immer etwas
langsamer.

Die untenstehenden Ergebnisse wurden halbautomisch mit einem Shellskript
erhoben und mit einem Python--Skript, mithilfe der ``pygal``[^PYGAL]--Bibliothek,
in Plots gerendert. Beide Skripte finden sich in
[@sec:appendix-benchmarks].

[^PYGAL]: <http://pygal.org/en/stable>

### Ergebnisse

Die Plots nutzen kubische Interpolation zwischen den einzelnen Messpunkten.
Die Zeitachse ist zudem logarithmisch aufgetragen, um den linearen Zusammenhang
zwischen den Achsen zu verdeutlichen. Insgesamt wurden vier Plots erstellt.
Zwei für jede Eingabedatenmenge (Filmdatei und Textkorpus) und dafür jeweils
ein Plot für das Schreiben und Lesen dieser Eingabedaten.

![Schreiboperationen auf der Datei ``movie.mp4``](images/7/movie_write.pdf){#fig:plot-movie-write width=95%}

![Leseoperationen auf der Datei ``movie.mp4``](images/7/movie_read.pdf){#fig:plot-movie-read width=95%}

![Schreiboperationen auf der Datei ``archive.tar``](images/7/archive_write.pdf){#fig:plot-archive-write width=95%}

![Leseoperationen auf der Datei ``archive.tar``](images/7/archive_read.pdf){#fig:plot-archive-read width=95%}

Insgesamt können folgende Konklusionen aus den Ergebnissen gezogen werden:

- Der Lese/Schreib--Durchsatz bleibt unabhängig von der Dateigröße größtenteils konstant.
* »``brig stage``« hat gegenüber »``ipfs add``« mit Verschlüsselung und Kompression einen
  geringen Overhead durch die interne Programmlogik. Dieser steigt aber bei einer
  größeren Datenmenge nicht weiter an (siehe [@fig:plot-movie-write] und
  [@fig:plot-archive-write]).
* Ähnliches lässt sich zu »``brig cat``« und »``ipfs add``« feststellen (siehe
  [@fig:plot-movie-read] und [@fig:plot-archive-read]).
* Kompression und Dekompression ist stets weniger ressourcenaufwändig als
  Verschlüsselung und Entschlüsselung. Ob an der Implementierung etwas verbessert
  werden kann, muss separat untersucht werden.
* Der Zugriff über das FUSE--Dateisystem ($12.8$ MB/s) ist verglichen mit ``brig cat``
  ($85$ MB/s) deutlich langsamer. Die Gründe hierfür liegen
  vermutlich weniger an FUSE an sich, als an der aktuellen, ineffizienten Implementierung.
* Die Messergebnisse bis 8MB sind noch relativ stark von Messungenauigkeiten beeinträchtigt.
  Erst bei höheren Datenmengen werden die Ergebnisse repräsentativ.

Als Fazit lässt sich sagen, dass viel Optimierungspotenzial vorhanden ist,
auch wenn die momentanen Durchsatzraten für viele Anwendungsfälle ausreichend sind.
In vielen Szenarios werden zudem nicht die lokalen Dateioperationen der Flaschenhals sein,
sondern die Übertragung über das Netzwerk.

## Zukünftige Erweiterungen

Abschließend sollen noch einige mögliche Erweiterungsmöglichkeiten der
momentanen Implementierung besprochen werden. Diese werden erst angegangen, sobald der
momentane Prototyp stabilisiert, dokumentiert und veröffentlicht wurde. Die
folgenden Ideen sind also noch in der Konzeptionsphase. Unterteilt wird die
Auflistung in Verbesserungen an der existierenden Implementierung (welche
vergleichsweise einfach umsetzbar sind), sowie konzeptuelle Erweiterungen
(welche typischerweise weitgehendere Änderungen erfordern).

### Verbesserungen an der Implementierung {#sec:verbesserungen}

**Kompression basierend auf MIME--Type:** Kompression lohnt sich nicht bei allen
Dateiformaten. Gut komprimieren lassen sich Dateien mit Textinhalten (wie XML--Dateien)
oder allgemein Daten mit sich wiederholenden Mustern darin. Schlecht komprimieren
lassen sich hingegen bereits komprimierte Bilder, Videos und Archivdateien.
Es wäre sinnvoll, basierend auf dem MIME--Type[@freed1996multipurpose] einen geeigneten
Kompressionsalgorithmus auszuwählen. Textdateien könnten so beispielsweise mit
dem speicherplatzeffizienteren *LZ4* komprimiert werden, größere Dateien mit dem schnelleren
*Snappy*. Multimediadateien könnten von der Kompression ausgenommen werden.
Der MIME--Type kann dabei in vielen Fällen automatisiert durch das Lesen
der ersten Bytes einer Datei erkannt werden.
Entsprechender Code existiert bereits[^MIME_UTIL], wird aber noch nicht eingesetzt.

[^MIME_UTIL]: <https://github.com/disorganizer/brig/blob/master/store/mime-util/main.go>

**Integritätsprüfung:** Wie in [@sec:requirements] beschrieben, können Daten
auf der Festplatte sich ohne Zutun des Nutzers verändern. Dieser Datenverlust
ist nicht nur aus Sicht der fehlenden Information kritisch, sondern führt auch dazu,
dass die Datei sich möglicherweise nicht mehr synchronisieren lässt, da bei einer Übertragung
festgestellt werden würde, dass die Datei sich unerwartet verändert hat. An
dieser Stelle könnte ein »``brig fsck``«--Kommando ansetzen, welches jede
gespeichert Datei neu von ``ipfs`` liest und die Prüfsumme neu berechnet.
Treten Diskrepanzen auf, so kann versucht werden, den fehlerhaften Block aus
alten Versionsständen oder von einem Synchronisationspartner zu beziehen.
Diese Funktionalität könnte auch direkt in ``ipfs`` eingebaut werden.
Auch könnte eine solche Reparaturfunktion die BoltDB von ``brig`` auf Konsistenz
prüfen und nötigenfalls und falls möglich reparieren. Im Gegensatz zu ``git``
sollten bei ``brig`` keine unerreichbaren Referenzen mehr im MDAG entstehen.
Trotzdem könnte ein Programm wie »``brig gc``« einen *Garbage--Collector*
laufen lassen, der solche Referenzen aufspüren und bereinigen kann. Diese würden
auf Programmfehler hindeuten. Weiterhin könnte dieses Kommando genutzt werden,
um ``ipfs gc`` zu starten.

**Nutzung eines existierenden OpenPGP--Schlüssels:** Momentan wird beim Anlegen
eines Repositories ein neues RSA--Schlüsselpaar generiert. Viele Nutzer haben
aber bereits einen Schlüsselpaar in Form eines OpenPGP--Schlüsselpaars oder
eines SSH--Schlüsselpaars. Diese könnten beim Anlegen des Repositories
importiert werden. Sollte das Repository neu angelegt werden müssen, so kann
der existierende Schlüssel in einem gängigen Format exportiert werden. Es
muss allerdings darauf geachtet werden, dass keine zwei Repositories dasselbe
Schlüsselpaar benutzen, da dies von ``ipfs`` nicht vorgesehen ist. Auch hier
könnte die Funktionalität in ``ipfs`` direkt eingebaut werden.

**Update Mechanismus:** Sicherheitskritische Software wie ``brig`` sollte
möglichst aktuell gehalten werden, um Sicherheitslücken schnell schließen zu
können. Wie ein solcher Mechanismus im Detail aussehen könnte, zeigt
die Arbeit von Herrn Piechula (siehe [@cpiechula]).

**HTTPS--Gateway:** Wie in [@fig:gateway] gezeigt könnte ``brig`` als Webserver
fungieren, der eine Schnittstelle zum »normalen« Internet bildet. Dieser könnte
alle Dateien in einem speziellen Verzeichnis (beispielsweise mit dem Namen
``/Public``) nach außen über einen Link zugreifbar machen. Dies hätte den
Vorteil, dass bestimmte Dateien von anonymen Nutzern direkt zugegriffen werden
können, ohne dass diese zu einem zentralen Dienst im Internet hochgeladen werden
müssen. Voraussetzung dazu ist, dass ein Rechner von »außen« (also vom
Internet) aus zugreifbar ist.
Möglich wäre auch die Implementierung eines Passwortschutzes, um den Zugriff
auf die Dateien zusätzlich abzusichern. Die Verbindung kann dabei durch HTTPS
abgesichert werden. Dies benötigt auf Seite des Webservers ein gültiges
TLS--Zertifikat. Mittlerweile gibt es dafür automatisierte Dienste wie
*LetsEncrypt*[^LETS_ENCRYPT]. Der in *Go* geschriebene Webserver
``caddy``[^CADDY] beherrscht bereits das automatische Besorgen eines
*LetsEncrypt*--Zertifikats.

[^LETS_ENCRYPT]: <https://letsencrypt.org>
[^CADDY]: <https://caddyserver.com>

**Hooking Mechanismus:** Um die Erweiterbarkeit von ``brig`` zu gewährleisten,
könnte ``brigd`` seinen Clients Benachrichtigungen mitgeben, sofern sich diese
dafür registrieren. Dieser würde den jeweiligen Client mitteilen wenn sich eine
Datei geändert hat, gelöscht wurde oder Ähnliches. Auch Statistiken wie die
aktuelle Speicherplatzauslastung könnten über diese Schnittstelle realisiert
werden.

**Packfiles:** Mehrere Dateien könnten zu einem gemeinsamen, komprimierten *Pack*
zusammengeschlossen werden, um Speicherplatz zu sparen. Für eine besonders
effiziente Kompression können einzelne Versionen einer Datei zusammengepackt
werden. Diese unterscheiden sich oft nur in einzelnen Blöcken und es wäre aus
Sicht der Speichereffizienz ungünstig, diese redundant zu speichern. Wie in
[@fig:stride] gezeigt, können immer kleine Blöcke (beispielsweise 16 Kilobyte) von
beispielsweise vier Dateien genommen werden und zu einem größeren Block (hier
64 Kilobyte) zusammengefasst werden. Diese großen Blöcke haben den Vorteil, dass sie
viel redundante Informationen speichern, wenn sich dieser Block in den
einzelnen Versionsständen nicht signifikant geändert hat.
Kompressionsalgorithmen wie *Snappy* arbeiten auf 64 Kilobyte Blöcken[^SNAPPY_FORMAT], daher
kann ein solcher Block relativ platzsparend komprimiert werden. Das Prinzip
lässt sich auch auf mehr als die Versionen einer Datei erweitern. Mittels einer
Heuristik können Dateien ausgewählt werden, die ähnlich groß sind und auch
diese gemeinsam gepackt werden.

[^SNAPPY_FORMAT]: Siehe auch: <https://github.com/google/snappy/blob/master/framing_format.txt#L91>

Bei kleinen Dateien ($< 64$ KB) ist bereits das Packen zu einer gemeinsamen
Datei vorteilhaft, da diese mit weniger Overhead und effizienterer Kompression
gepackt werden können. Die *Packfiles* von ``git`` nutzen einen anderen Ansatz,
indem nur Deltas in den einzelnen Archiven gespeichert werden. Dies wäre bei
Dateien möglicherweise auch für ``brig`` eine valide Herangehensweise und bleibt
zu evaluieren.

Es wäre also möglich Speicherplatz im Tausch gegen Rechenzeit zu sparen, indem
zwischen ``ipfs`` und ``brig`` noch eine Abstraktionsschicht eingebaut wird,
die intelligent Dateien in *Packs* verpackt und zugreifbar macht. Die
Implementierung dieses Konzeptes hätte zu viel Zeit in Anspruch genommen,
weswegen hier weitere Arbeiten ansetzen könnten.

**Atomarität und Transaktionen:** In der momentanen Implementierung ist bei
einem Ausfall von ``brigd`` (beispielsweise durch einen Absturz oder Stromausfall)
nicht sichergestellt, dass eine Aktion (wie ``MakeCommit()``) vollständig, atomar
abgelaufen ist. Auch wenn die jeweilige Aktion von der API aus durch Locks atomar ist,
wird im momentanen Zustand kein Rollback bei Fehlern ausgeführt.
BoltDB an sich unterstützt atomare Transaktionen, aber durch die Abstraktion
von der konkreten Datenbank werden mehrere kleine Transaktionen nicht zu einer
zusammenhängenden, großen Transaktion zusammengefasst. Da aber die Datenbank
austauschbar bleiben soll, muss von der Abstraktionsschicht eine Möglichkeit
implementiert werden, zurückspulbare Transaktionen zu
starten. Dazu dürfen Modifikationen an der Datenbank nicht direkt ausgeführt
werden, sondern müssen in einem »Journal«[^JOURNAL] zusammengefasst werden. Dieses kann
dann in einer einzigen, atomaren Datenbank--Transaktion zusammengefasst werden.

[^JOURNAL]: Siehe auch: <https://de.wikipedia.org/wiki/Journaling-Dateisystem>

![Beispielhaftes Packen von vier einzelnen Versionständen.](images/7/stride.pdf){#fig:stride}

### Konzeptuelle Verbesserungen

**Zugriffsrechte:** ``brig`` unterscheidet im jetzigen Konzept nicht zwischen
lesbaren, schreibbaren oder ausführbaren Dateien. Auch gibt es keinen Besitzer
oder eine Gruppenzugehörigkeit der Datei. Die einzigen Dateiattribute bilden
momentan die Größe und der letzte Änderungszeitpunkt. Aus diesem Grund bewirkt
der Aufruf von »``chmod``« auf eine Datei im FUSE--Dateisystem nichts. Es muss
nicht das System von Unix übernommen werden, allerdings wären die Informationen
über den Eigentümer wichtig, um selektive Synchronisation zu implementieren.
Dabei könnte eine Nutzergruppe angelegt werden. Nur die Nutzer, die dieser
Gruppe angehören, können dann Dateien und Verzeichnisse einsehen, die auch
dieser Gruppe zugeordnet sind.

**Automatische Synchronisation:** Änderungen müssen explizit synchronisiert
werden. Um eine Dropbox--ähnliche Funktionalität zu erreichen sollte eine neue
Option eingeführt werden: »``brig sync --auto bob@wonderland.lit``«. Dabei wird
zuerst regulär mit *Bob* synchronisiert. Im Anschluss wird der Knoten von *Bob*
angewiesen, *Alice* alle Änderungen auf seiner Seite sofort zu schicken.
*Alice* empfängt diese und ändert ihre eigenen Dateien im Staging--Bereich, um
die Änderung nachzuahmen.

**Schlagwortbasiertes Dateisystem:** ``brig`` arbeitet momentan rein als
hierarchisches Dateisystem. Einzelne Knoten des MDAG werden also vom Nutzer
mittels Pfad zugegriffen. Eine Erweiterung dazu könnte die Einführung eines
schlagwortbasierten Ansatzes (ähnlich zu Tagsistant[^TAG]) sein, welcher es
möglich macht die Menge aller Dateien semantisch durchsuchbar zu machen.
Dateien und Verzeichnisse können vom Nutzer mit einem Schlagwort versehen
werden (``brig tag <path> [<tag>...]``). Im FUSE--Dateisystem könnte das
Konzept durch die Einführung eines speziellen Ordners (beispielsweise
``/tags``) eingeführt werden. Dieser würde alle definierten Schlagworte als
Ordner beinhalten. Unter jedem Schlagwortordner werden alle entsprechend
verschlagworteten Dateien angezeigt.

[^TAG]: <https://en.wikipedia.org/wiki/Tagsistant>

**Auto--Discovery anderer Nutzer:** Momentan kann ``brig`` einen anderen Nutzer
nur finden, wenn man seinen Nutzernamen kennt. Eine »unscharfe« Suche nach
Benutzernamen wäre praktisch, ist aber aufgrund der dezentralen Natur von
``brig`` schwer umzusetzen. Machbar erscheint aber die automatische Erkennung
von anderen ``brig``--Nutzer »in der Nähe« (also im selben, lokalen Netzwerk). Für
diesen Anwendungsfall würde sich das *Zeroconf--Protokoll*[^ZEROCONF] eignen. Auch diese
Funktionalität ließe sich eventuell direkt in ``ipfs`` integrieren.

[^ZEROCONF]: <https://de.wikipedia.org/wiki/Zeroconf>

**In--Memory Laden des Repositores:** Beim Starten von ``brigd`` werden einige
sensible Dateien im Repository entschlüsselt. Solange ``brigd`` läuft
bleiben diese auch lesbar und werden erst wieder verschlüsselt, wenn
``brigd`` sich beendet. Dies ist problematisch, wenn ein Angreifer
in Besitz einzelner Dateien des Repositories kommen kann. Auch werden
die Dateien nicht verschlüsselt, wenn ``brigd`` unvermittelt abstürzt und
unsauber beendet wird. Schöner wäre eine reine Entschlüsselung
der Daten im Hauptspeicher. Änderungen würden direkt in verschlüsselter Form
wieder zurückgeschrieben werden.

**Intelligenteres Key--Management:** In der momentanen Implementierung werden
alle Schlüssel in den Metadaten der Dateien gelagert. Die Metadaten werden als Ganzes
zum Synchronisationspartner übertragen. Hier wäre entweder eine Trennung von den
Metadaten (und damit gesonderte Übertragung) sinnvoll oder eine
Schlüsselhierarchie, bei denen der eigentliche Schlüssel beispielsweise noch
mit einem Gruppenschlüssel verschlüsselt werden.
Siehe auch [@cpiechula] für weitere Details.

**Anonymisierung:**  Eine Anonymisierung des Datenverkehrs ist momentan nicht
implementiert. Angreifer können zwar den Datenverkehr nicht mitlesen, doch
können sie durchaus feststellen, welche Partner miteinander kommunizieren.
In manchen Fällen kann dies bereits eine wichtige Information für einen Angreifer
sein. Abhilfe könnte die Nutzung des Tor--Netzwerks[^TOR] schaffen. Die einzelnen Knoten
würden dabei nicht direkt miteinander kommunizieren, sondern schicken ihren Datenverkehr,
verpackt in mehrere verschlüsselte Schichten, über mehre Knoten des Tor--Netzwerks.
Diese Funktionalität muss direkt in ``ipfs`` implementiert werden. Entsprechende
Überlegungen scheinen auf ``ipfs``--Seite bereits zu existieren[^IPFS_TOR].

[^TOR]: Siehe auch: <https://www.torproject.org>
[^IPFS_TOR]: Siehe auch: <https://github.com/ipfs/notes/issues/37>
