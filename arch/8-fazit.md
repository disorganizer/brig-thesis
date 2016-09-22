# Fazit {#sec:fazit}

## Zusammenfassung

Kurze Zusammenfassung ähnlich abstract. "Es wurde..."
Sowie Resultate

Ambitioniertes Projekt,
trotzdem neutrale bis positive Resultate trotz Zeitmangels.

Zusammengefasst größte (Usability) Probleme:

- Initiale Authentifizierung (QR--Code)
- Partner muss online sein.
* Noch keine automatische Synchronisation.

Aber: Hoffentlich leichter verständlich als viele andere Tools,
da es nach außen nur wenige primitiven gibt.

* Mächtiger syncthing
* Leichter bedienbar als git-annex
* Freier und verständlicher als resilio
* Fortgeschrittener als bazil

Relativ interdisplizinär:

- Sicherheit
- P2P
- Softwarearchitektur
- Usability

Mix aus vielen bestehenden Technologien, Ansätzen und Ideen. (git und co.)

Zeitaufteilung, was hat wie lang gedauert, was waren die größten Zeitfresser

Situation erklären in dem der Prototyp sich befindet.

Noch Fraglich wie gut das System in der Praxis funktioniert.

### Selbstkritik

Was würde man anders machen wenn man jung wäre?

Was würde man anders machen: Prototypischere Entwicklung, vlt. sogar einfach in bash oder python.

Aufteilung von brig in kleinere Teilprogramme, wie die plumbing commands bei git,
um Robustheit und Fehlertoleranz zu erhöhen.

![Ist »brig« letztlich nur ein weiterer Standard?](images/8/xkcd-standards.png){#fig:xkcd-standards width=66%}

## Offene Fragen

Neben den konkreten Fragen aus evaluation, allgemeine fragen das projekt betreffend

Key Management?

### Beziehung zum ``ipfs``--Projekt

Momentan wird ``brig`` vollkommen separat von ``ipfs`` entwickelt. Bleibt das so?

https://github.com/ipfs/ipfs/issues/120

Viele Teile von ``brig`` könnten ipfs helfen (encrpytion format/compression)
sowie anregungen/ideen bei VCS.

### Zukunft der Autoren

Weiterentwicklung gewährleistet?

Finanzierung

Aufgrund privater Probleme von Herrn Piechula, konnte dieser nicht mit voller Kapazität
mitarbeiten.

### Veröffentlichung der Software

Wie man das angeht. reddit?
Website und Dokumentation zur Veröffentlichung nötig.

Veröffentlichung als beta -> Problem: Internas können sich noch ändern,
Inkompatiblitäten können entstehen.
Testing mit verschiedenen Prüfsummen.

Hier noch ein monumentaler Schlussatz.

Auch wenn die Arbeit an ``brig`` sehr kräftezehrend war hab ich viel gelernt! Toll!
