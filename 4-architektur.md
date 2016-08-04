# Architektur

In diesem Kapitel wird die Architektur des Prototypen von ``brig`` erklärt.
Dabei wird weniger auf die genaue Funktionsweise der Komponenten eingegangen
(das passiert im Implementierungskapitel 5 TODO: ref), sondern das
Zusammenspiel der einzelnen Komponenten wird spezifiziert und welche Ein- und
Ausgaben sie nehmen. Die Berührungspunkte mit dem Nutzer werden ebenfalls
diskutiert.

# Architektur von IPFS

Da ``brig`` eine Art »Frontend« für ``IPFS`` ist, wird dessen Architektur
hier kurz schematisch erklärt.

- Bitswap
- For the swarm!

TODO: Komponentendiagramm

-----

Aufbau der Software aus funktionaler Sicht.
Eher blackbox, was kommt rein was kommt raus.

- Berührungspunkte mit Nutzer.

$ Architektur von ``brig``

TODO: Komponentendiagramm

## Daemon und Client Aufteilung

## Metadatenindex

Alle Metadaten werden in einer einzigen Key--Value basierten Datenbank gespeichert.
Die Basis eines Key--Value--Stores sind sogenannte *Buckets* (dt. Eimer).
In diesem können wie bei einer Hashtabelle einzelne Werte einzigartigen
Schlüsseln zugeordnet werden. Die Werte können wieder *Buckets* sein,
wodurch die Bildung einer verschachtelten Hierarchie möglich ist.

Die Hierarchie ist dabei wie folgt:


```html
.
|-- checkpoints                  # Jede Datei hat eine History (Liste von Checkpoints)
|   `-- PATH -> HISTORY          # Jedem PATH ist also eine HISTORY zugeordnet.
|-- commits                      # 1 bis N Checkpoints werden zu einem Commit gepackt.
|   `-- HASH -> COMMIT_METADATA  # Jeder Commit hat einen HASH unter dem Metadaten sind.
|-- id                           # Jeder Nutzer hat einen eigenen 'Store'.
|   `-- USER                     # Der aktuelle Nutzer ist in USER gespeichert.
|-- index                        # Der 'index' speichert die eigentlichen Datei-Metadaten.
|   `-- PATH -> FILE_METADATA    # Jeder Metadateneintrag wird dabei per Pfad referenziert.
|-- refs                         # 'refs' sind besondere Namen für bestimmte COMMITS.
|   `-- head                     # 'head' bezeichnet dabei den obersten/aktuellsten Commit.
|       `-- COMMIT_HASH          # Der COMMIT_HASH
`-- stage                        # Wie bei 'git' gibt es einen Stagingbereich mit Checkpoints.
    `-- PATH -> CHECKPOINT       # Diese können dann in einen Checkpoint zusammengefasst werden.
```

Anmerkung: Die Struktur ist momentan auf Einfachheit und nicht auf Speichereffizienz ausgelegt.
Es wäre beispielsweise leicht möglich im ``index``--Bucket einen Präfixbaum (TODO: ref) zu speichern.
Dieser würde verhindern, dass Pfade teilweise doppelt abgespeichert werden.

(TODO: In Grafik umwandeln)

## Serialisierung

## File Streaming

### Verschlüsselung

### Kompression

## Dateisystemordner

FUSE

### Deduplizierung

## Gateway

## Sonstiges

### Logging

### Konfiguration
