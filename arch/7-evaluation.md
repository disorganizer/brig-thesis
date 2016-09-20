# Evaluation {#sec:evaluation}

## Was ``brig`` *nicht* ist

TODO: Siehe auch: https://bazil.org/doc/antigoals/?

``brig`` kann nicht die beste Alternative in allen Bereichen sein. Keine
Software kann die sprichwörtliche »eierlegende Wollmilchsau« sein und sollte
auch nicht als solche benutzt werden. Insgesamt ist es für folgende Bereiche
weniger geeignet:

TODO: Schöler: Sauberer Vergleich der Implementierung/Lösung anhang von Anforderungen.

**High Performance:** Besonders im Bereich Effizienz kann es nicht mit hochperformanten
Cluster--Dateisystemen wie Ceph[^CEPH] oder GlusterFS[^GLUSTER] mithalten.  Das
liegt besonders an der sicheren Ausrichtung von ``brig``, welche oft
Rechenleistung zugunsten von Sicherheit eintauscht. 

**Echtzeitanwendungen:** Schreibt ein Nutzer etwas in eine Datei, so ist diese
Änderung nicht augenblicklich anderen Nutzern zugänglich. Stattdessen kann
``brig`` selbst entscheiden, wann die Änderungen synchronisiert
werden.[^SYNC_NOTE] Insbesondere macht es beispielsweise kaum Sinn,
SQL--Datenbanken von ``brig`` synchronisieren zu lassen. Hierfür gibt es
weitaus bessere Alternativen. (TODO: wie was? CockroachDB)

[^SYNC_NOTE]: In der momentanen Implementierung bei jedem ``fsync()`` und beim Schließen einer Datei.

**Volle POSIX-Kompabilität notwendig:** Der *POSIX*--Standard definiert (unter
anderem) eine gemeinsame, standardisierte API, die von vielen (zumeist
unixoiden) Betriebssystemen implementiert wird (siehe auch [@1999standard]).
Nicht alle Teile dieses Interfaces können von ``brig`` umgesetzt werden. So
gibt es kaum eine verträgliche Definition von harten und weichen Verlinkungen
(*Hardlinks* und *Symbolic Links*) für dezentrale Netzwerke. Auch spezielle
Dateien wie *FIFOs* können in diesem Kontext nicht ohne Race--Conditions
umgesetzt werden. Entsprechende Operationen werdem von *FUSE--Layer* mit
dem *POSIX*--Fehlercode ``ENOSYS`` (Nicht implementiert) quittiert.

**Glaubhafte Abstreitbarkeit:** Auch wenn ein ``brig``--Repository in der
geschlossenen Form als sicherer »Datensafe« einsetzbar ist, so bietet ``brig``
nicht die Eigenschaft der »glaubhaften Abstreitbarkeit«[^ABSTREIT], die
Werkzeuge wie Veracrypt (TODO: ref) bieten.

**Zeilenbasierte Differenzen:** Im Gegensatz zu Versionsverwaltungssystemen wie ``git``,
kann ``brig`` keine zeilenbasierten Differenzen zwischen zwei Dateien anzeigen,
da es nur auf den Metadaten von Dateien arbeitet. 

**Reiner Speicherdienst auf der Gegenseite:** Auf der Gegenseite muss ein
``brig``--Daemon--Prozess laufen, um mit der Gegenseite zu kommunzieren. Daher
können reine Speicherdienste wie *Amazon S3*[^AMAZON_S3] nicht ohne weiteres
als Datenlager benutzt werden. Das kann allerdings leicht umgangen werden,
indem der entfernte Speicher lokal gemounted[^REMOTE_MOUNT] wird, und der
``brig``--Prozess lokal gestartet wird. Werkzeuge wie ``rsync`` oder ``git--annex``
benötigen lediglich einen ``ssh``--Zugang zur Maschine.

**Keine starke Ausfallsicherheit:** ``brig`` speichert nur ganze Dateien auf
$1$ bis $n$ Knoten. Es wird kein *Erasure--Enconding*[^ERASURE_ENCODING]
angewendet, wie beispielsweise ``Tahoe-LAFS`` das tut. Damit eine Datei im
Falle des Ausfalls eines Knotens wiederherstellbar ist, muss mindestens ein
anderer Knoten, die Datei vollständig gespeichert haben, während andere
Werkzeuge kleine Blöcke der Dateien redundant auf mehreren Rechnern ablegen.
Werden diese beschädigt können diese sich selbst reparieren oder von anderen
Knoten neu übertragen werden. Für die meisten Anwendungszwecke halten wir
Redundanz auf dem Dateilevel allerdings für ausreichend.

**Embedded Devices:** ``brig`` benötigt ein vollständiges Betriebssystem mit
Netzwerkanschluss, Hauptspeicher und einer ausreichend starken CPU. Die
»unterste Grenze« für einen vernünftigen Betrieb wäre vermutlich ein aktueller
Raspberry Pi (Revision 3).

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
[^ABSTREIT]: Siehe auch: <https://de.wikipedia.org/wiki/VeraCrypt\#Glaubhafte_Abstreitbarkeit>

## Defizite der aktuellen Implementierung

### Beschränkte Synchronisationsfähgikeiten

### Testsuite zu klein

### Zu geringe Ausfallsicherheit

### Atomizität

Filesystem anforderunge (transactions?)
Journal-log für atomic operations


## Fehlende Anforderungen

Durch Anforderungen in Kapite 2 gehen und nachschauen ob alles jut ist. (Hint: Nö.)

Storage Quotas

Simpler Sync algorithmus

kein checkpoint squashing


## Zukünftige Erweiterungen

Permissions: momentan gar keine.

*Semantisch durchsuchbares* Tag-basiertes Dateisystem[^TAG].

Integritätsprüfung (git fsck ähnlich)

Auto-Discovery anderer Nutzer / Gruppenbildung.

Docker erwähnen, weil's so hipp ist?

Update Mechanismus?

Hooking Mechanismus (i.e. API nach außen, notify on file change)

Virtual file system interface für repositories
(macht möglich, das gesamte repo im speicher zu halten, oder per ssh zu streamen)

https://github.com/attic-labs/noms

* Möglich machen, dass man einen existierenden OpenPGP nehmen kann.

* Garbagecollector um alte Referenzen zu entfernen.

Repair-Funktionalität und saubere Transaktionen um Verlässlichkeit zu erhöhen (wenn metadata index kaputt -> daten nur schwer besorgbar)

[^TAG]: Mit einem ähnlichen Ansatz wie <https://en.wikipedia.org/wiki/Tagsistant>

## Portierbarkeit

Android, Windows.

WebDav als Alternative zu FUSE.
