# Motivation

TODO: Erwähnen dass es sich um eine Zusammenarbe it mit Chris P. handelt.

Einfache und sichere Dateisynchronisation ist trotz vieler Lösungsansätze 
noch immer ein unvollständig gelöstes Problem. Versucht man beispielsweise
eine Datei zwischen zwei Personen zu teilen, so kann man unter anderen zwischen
den folgenden Möglichkeiten wählen: Übertragung mittels USB--Stick,
Speicherkarte oder ähnlichem, Übertragung über einen zentralen Dienst, entweder
im lokalen Netz (ownCloud) oder entfernt im Internet (z.B. Dropbox), direkte
Übertragung im Netzwerk mittels Protokollen wie ``ssh`` oder sehr häufig auch
einfach via E--Mail. Jede dieser Ansätze funktioniert auf seine Weise, doch
ergeben sich in der Praxis meist sehr unterschiedliche Probleme. Bei E--Mails
kann oft nur eine maximale Dateigröße übermittelt werden, die Übertragung von
Dateien mittels ``ssh`` ist für die meisten Nutzer zu kompliziert und zentrale
Dienste rufen einerseits Sicherheitsbedenken hervor, andererseits sind sie meist
nur bedingt kostenlos und können ausfallen.

Zahlreiche Ansätze haben versucht diese Probleme in der Praxis abzumildern oder
zu lösen. Ein Gegenentwurf zu den zentralen Ansätzen bilden die dezentralen
Ansätze. Dabei werden nicht alle Dateien an einem zentralen Punkt gespeichert,
sondern können verteilt (ganz oder nur einzelne Blöcke einer Datei) im Netzwerk
vorhanden sein. Dass dabei Dokumente auch durchaus doppelt gespeichert werden
dürfen, erhöht die Ausfallsicherheit und vermeidet den Flaschenhals zentraler
Dienste.

In der Praxis kranken leider auch diese Dienste entweder an der Benutzbarkeit
oder an den Sicherheitsanforderungen, die insbesondere Unternehmen an eine
solche Lösung stellen. Diese Arbeit versucht einen dezentralen Ansatz zur
Dateisynchronisation vorzustellen, der eine Balance zwischen Sicherheit und
Benutzbarkeit herstellt. Die hier vorgestellte und quelloffene Lösung trägt
den Namen »``brig``«.

## Der Name

Eine »Brigg« (englisch »brig«) ist ein kleines und wendiges
Zweimaster--Segelschiff aus dem 18-ten Jahrhundert. Passend erschien uns der
Name einerseits, weil wir flexibel »Güter« (in Form von Dateien) in der ganzen
Welt verteilen, andererseits weil ``brig`` auf (Datei-)Strömen operiert.

Dass der Name ähnlich klingt und kurz ist wie ``git`` (TODO: ref), ist kein Zufall. Das
Versionsverwaltungssystem (version control system, kurz VCS) hat durch seine
sehr flexible und dezentrale Arbeitsweise bestehende zentrale Alternativen wie
``svn`` oder ``cvs`` fast vollständig abgelöst. Zusätzlich ist der Gesamteinsatz
von Versionsverwaltungssystemen durch die verhältnismäßige einfache Anwendung
gestiegen. Wir hoffen mit ``brig`` eine ähnlich flexible Lösung für große
Dateien etablieren zu können. 

# Lizenz

Eine sicherheitskritische Lösung sollte den Nutzern die
Möglichkeit geben nachzuschauen, wie die Sicherheitskonzepte implementieren sind.
Aus diesem Grund und um eine freie Weiterentwicklung zu gewährleisten wird die
entwickelte Software unter die ``AGPLv3`` (Affero General Public License,
Version 3 TODO: ref) gestellt.
