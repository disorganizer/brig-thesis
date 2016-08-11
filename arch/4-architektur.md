# Architektur {#sec:architektur}

In diesem Kapitel wird die Architektur des Prototypen von ``brig`` erklärt.
Dabei wird weniger auf die genaue Funktionsweise der Komponenten eingegangen
(das passiert im [@sec:implementierung], *Implementierung*), sondern das
Zusammenspiel der einzelnen Komponenten wird spezifiziert und welche Eingaben
sie entgegennehmen und welche Ausgaben sie produzieren. Die Berührungspunkte
mit dem Nutzer werden ebenfalls diskutiert.

## Architektur von IPFS

Da ``brig`` eine Art »Frontend« für das »Backend« ``IPFS`` ist, wird dessen
Architektur hier kurz schematisch erklärt.

- Bitswap
- For the swarm!

TODO: Komponentendiagramm

-----

Aufbau der Software aus funktionaler Sicht.
Eher blackbox, was kommt rein was kommt raus.

- Berührungspunkte mit Nutzer.

## Architekturübersicht

TODO: Komponentendiagramm

### Aufbau von ``brigctl``

Protobuf einführen

Handling von mehreren Repositories

### Aufbau von ``brigd``

## Einzelkomponenten

### Metadatenindex

Virtueller Wurzelknoten.

(/home/sahib/x.png -> /x.png)

TODO: Datenentkopplung.

Alle Metadaten werden in einer einzigen Key--Value basierten Datenbank gespeichert.
Die Basis eines Key--Value--Stores sind sogenannte *Buckets* (dt. Eimer).
In diesem können wie bei einer Hashtabelle einzelne Werte einzigartigen
Schlüsseln zugeordnet werden. Die Werte können wieder *Buckets* sein,
wodurch die Bildung einer verschachtelten Hierarchie möglich ist.
Die verwendete Hierarchie ist dabei schematisch in [@fig:brig-store-layout] abgebildet.

![Hierarchie innerhalb der Key--Value--Datenbank](images/tree-store-layout.pdf){#fig:brig-store-layout width=100%}

Anmerkung: Die Struktur ist momentan auf Einfachheit und nicht auf Speichereffizienz ausgelegt.
Es wäre beispielsweise leicht möglich im ``index``--Bucket einen Präfixbaum (TODO: ref) zu speichern.
Dieser würde verhindern, dass Pfade teilweise doppelt abgespeichert werden.

(TODO: In Grafik umwandeln)

### Serialisierung

### Dateiströme

https://en.wikipedia.org/wiki/Convergent_encryption

Schaubild mit den relevanten io.Reader/io.Writer

#### Verschlüsselung

#### Kompression

### Dateisystemordner

FUSE

### Deduplizierung

### Gateway

### Sonstiges

### Logging

### Konfiguration
