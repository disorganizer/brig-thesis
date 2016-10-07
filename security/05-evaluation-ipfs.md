# Evaluation IPFS

*IPFS* (*InterPlanetary File System*) stellt die Netzwerkbasis für »brig« dar.
Da *IPFS* teilweise zu andere Ziele als »brig« hat, ist es wichtig, dass die
Anforderungen von »brig« durch die *IPFS*--Basis nicht verletzt werden. Im
Folgenden wird *IPFS* bezüglich bestimmter sicherheitstechnischer Anforderungen
genauer beleuchtet um Diskrepanzen zwischen den Zielen von »brig« zu
identifizieren.

## Einleitung

Das *InterPlanetary File System* definiert als als  »content-addressable,
peer-to-peer hypermedia distribution protocol«. Das besondere an *IPFS* ist,
dass es ein sogenanntes *Content--Addressable--Network (CAN)* darstellt. Ein
*CAN* arbeitet mit einer verteilten Hashtabelle (*Distributed Hash Table
(DHT)*), welche als grundlegende »Datenstruktur« verwendet wird um die Daten
innerhalb eines Peer--to--peer--Netzwerks zu lokalisieren und zu speichern.
Eine *DHT* als Datenstruktur bringt laut Wikipedia[^FN_DHT] folgende Eigenschaften mit
sich:

[^FN_DHT]: Verteilte Hashtabelle: <https://de.wikipedia.org/wiki/Verteilte_Hashtabelle>

* Fehlertoleranz: Das System sollte zuverlässig funktionieren, auch wenn Knoten
  ausfallen oder das System verlassen.
* Lastenverteilung: Schlüssel werden gleichmäßig auf alle Knoten verteilt.
* Robustheit: Das System sollte „korrekt“ funktionieren können, auch wenn ein
  Teil (möglicherweise ein Großteil) der Knoten versucht, das System zu stören.
* Selbstorganisation: Es ist keine manuelle Konfiguration nötig.
* Skalierbarkeit: Das System sollte in der Lage sein, auch mit einer großen
  Anzahl von Knoten funktionsfähig zu bleiben.


## Sicherheit

* Wie schaut es mit Verschlüsselung aus?
* Wie schaut es mit Datenintegrität aus?
* Welche Authentifizierungsmechanismen gibt es?

## Mögliche Probleme

## Angriffsszenarien

## Risikomanagement
