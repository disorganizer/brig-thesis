# Evaluation IPFS

*IPFS* (*InterPlanetary File System*) stellt die Netzwerkbasis für »brig« dar.
Da *IPFS* teilweise andere Ziele als »brig« hat, ist es wichtig, dass die
Anforderungen von »brig« durch die *IPFS*--Basis nicht verletzt werden. Im
Folgenden wird *IPFS* bezüglich bestimmter sicherheitstechnischer Anforderungen
genauer beleuchtet, um Diskrepanzen zwischen den Zielen von »brig« zu
identifizieren.

## Projektumfang und getestete Version

Die *IPFS*--Codebasis umfasst aktuell $\approx{900.000}$ *LoC* (siehe
[@sec:APP_IPFS_LOC]). Davon gehören $\approx{100.000}$ *LoC* direkt dem
*IPFS*--Projekt an, $\approx{800.000}$ *LoC* stammen aus Drittanbieter--Bibliotheken.

Im zeitlich begrenzten Umfang der Master--Arbeit können nur selektive
Mechanismen der Software untersucht werden. Eine genaue Analyse der
Quelltext--Basis ist aufgrund der Projektgröße und der begrenzten Zeit nicht
möglich.

Es wurde folgende Version aus den *Arch Linux*--Repository evaluiert:

~~~sh
freya :: ~ » ipfs version
ipfs version 0.4.3
~~~

## Einleitung IPFS

Das *InterPlanetary File System* wird als  »content-addressable, peer-to-peer
hypermedia distribution protocol« definiert. Das besondere an *IPFS* ist, dass
es ein sogenanntes *Content--Addressable--Network (CAN)* darstellt. Ein *CAN*
arbeitet mit einer verteilten Hashtabelle (*Distributed Hash Table (DHT)*),
welche als grundlegende »Datenstruktur« verwendet wird um die Daten innerhalb
eines Peer--to--peer--Netzwerks zu lokalisieren und zu speichern.

Eine *DHT* als Datenstruktur bringt in der Theorie laut Wikipedia[^FN_DHT]
folgende Eigenschaften mit sich:

[^FN_DHT]: Verteilte Hashtabelle: <https://de.wikipedia.org/w/index.php?title=Verteilte_Hashtabelle&oldid=157901191>

* **Fehlertoleranz:** Das System sollte zuverlässig funktionieren, auch wenn Knoten
  ausfallen oder das System verlassen.
* **Lastenverteilung:** Schlüssel werden gleichmäßig auf alle Knoten verteilt.
* **Robustheit:** Das System sollte „korrekt“ funktionieren können, auch wenn ein
  Teil (möglicherweise ein Großteil) der Knoten versucht, das System zu stören.
* **Selbstorganisation:** Es ist keine manuelle Konfiguration nötig.
* **Skalierbarkeit:** Das System sollte in der Lage sein, auch mit einer großen
  Anzahl von Knoten funktionsfähig zu bleiben.

## IPFS--Basis

Das *IPFS*--Dateisystem beziehungsweise Protokoll bringt das
Kommandozeilenwerkzeug `ipfs` mit. Dieses ermöglicht eine rudimentäre Nutzung
von *IPFS*. Beim initialisieren von *IPFS* wird ein *RSA*--Schlüsselpaar
generiert. Ein *IPFS*--Repository kann mit dem Befehl `ipfs init` initialisiert
werden. Dabei wird standardmäßig unter `~/.ipfs` ein Repository angelegt.

~~~sh
freya :: ~ » ipfs init
initializing ipfs node at /home/qitta/.ipfs
generating 2048-bit RSA keypair...done
peer identity: QmbEg4fJd3oaM9PrpcMHcn6QR2HMdhRXz5YyL5fHnqNAET
to get started, enter:

        ipfs cat /ipfs/QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/readme
~~~

Bei der Initialisierung wird eine *Peer ID* erzeugt. Anschließend kann
der Benutzer die `readme`--Datei aus dem *IPFS*--Store betrachten.
[@sec:APP_IPFS_SECWARNING] zeigt weiterhin die aktuelle Sicherheitswarnung der
*IPFS*--Software. Es wird explizit ein paar mal darauf hingewiesen, dass *IPFS*
sich im Alphastadium befindet. Weiterhin gibt es Details zur »Sicherheit« in
der Datei `security-notes`, welche analog zur `readme`--Datei betrachtet werden
kann.

## Speicherung und Datenintegrität

Die Speicherung von Daten mag auf den ersten Blick simpel erscheinen.
Betrachtet man jedoch die »Rahmenbedingungen« die zu beachten sind um Daten
»sicher« zu speichern, wird die Thematik kompilierter. Das Hauptproblem an
dieser Stelle ist der die sogenannten *Silent Data Corruption*, oft auch
»Bitrot« genannt. Der Begriff beschreibt den Umstand, dass Fehler in Daten im
Laufe der Zeit auftreten. Für die Fehlerursache können verschiedene Gründe wie
beispielsweise:

* Hardwarefehler bedingt durch Alterungsprozess der Festplatte
* Fehler in der Festplatten--Firmware
* Fehler in der Controller--Firmware
* Fehler in der Software (Kernel, Dateisystem)
* Schadsoftware

Obwohl die Technologien mit steigenden Kapazitäten verbessert wurden, ist die
Fehlerrate bisher konstant geblieben. Analysen haben ergeben, dass die
Wahrscheinlichkeit von *Silent Data Corruption* höher ist wie bisher angenommen
(vgl TODO:REF).

Gängige Dateisysteme wie beispielsweise *NTFS*[^FN_NTFS] oder *EXT4*[^FN_EXT4]
können Fehler verursacht durch *Silent Data Corruption* nicht erkennen und den
Benutzer von dieser Fehlerart nicht schützen. Um eine Veränderung der Daten
fest zu stellen, müsste der Benutzer beispielsweise die Daten mit einer
kryptographischen Prüfsumme validieren. Entspricht die Prüfsumme beim Lesen der
Daten, der gleichen Prüfsumme, welche bei der Speicherung der Daten ermittelt
wurde, so sind die Daten mit hoher Wahrscheinlichkeit korrekt an den Benutzer
zurückgegeben worden. Diese Art der Validierung der Integrität ist jedoch
aufgrund des hohen Aufwands nicht praxistauglich.

Dateisysteme wie *BTRFS* oder *ZFS* validieren die Daten und Metadaten bei
während der Lese-- und Schreibvorgänge mittels Prüfsummen. Durch dieses
»spezielle« Feature kann die Verarbeitungskette beim Lesen-- und Speichern der
Daten bezüglich ihrer Integrität validiert werden. Bei der Benutzung eines
*RAID*--System können die Daten sogar automatisiert ohne Zutun des Benutzers
korrigiert werden. TODO: ZFS Beispiel?

[^FN_NTFS]: NTFS Dateisystem: <https://en.wikipedia.org/w/index.php?title=NTFS&oldid=743913107>
[^FN_EXT4]: EXT4 Dateisystem: <https://en.wikipedia.org/w/index.php?title=Ext4&oldid=738311553>

Das Speichern der Daten erfolgt bei *IPFS* (blockweise, in sogennanten chunks)
mittels eines Hash--Tree), auch *Merkle--DAG* (directed acyclic graph,
gerichteter azyklischer Graph) genannt. 

*IPFS* verwendet als Prüfsummen--Format den eigens entwickelte
*Multihash*--Format[^FN_MULTIHASH]. [@fig:img-multihash] zeigt das
*Multihash*--Format, es stellt einen selbstbeschreibende Prüfsumme welche den
Algorithmus, die Länge und die eigentliche Prüfsumme kombiniert. Dieser wird in
verschiedenen Varianten encodiert. Beispielsweise `base32` für die interne
Namensvergabe der Datenblocks oder `base58` für die Repräsentation der
*Peer--ID* intern verwendet.

![Das *Multihash*--Format.](images/multihash.png){#fig:img-multihash width=80%} 

Das folgende Listing zeigt den internen Aufbau eines *IPFS*--Repository. Die
Daten sind hierbei als ».data«--Blöcke aufgeteilt und gespeichert. Die
Benennung der Datenblöcke ist basierend auf dem *Multihash*, die Enkodierung
bei Datenblocks ist `Base32`.

[^FN_MULTIHASH]: Github Multihash: <https://github.com/multiformats/multihash>

~~~sh
freya :: ~ » tree .ipfs
.ipfs
|--- blocks
|   |--- CIQBE
|   |   |--- CIQBED3K6YA5I3QQWLJOCHWXDRK5EXZQILBCKAPEDUJENZ5B5HJ5R3A.data
|   |--- CIQCL
|   |   |--- CIQCLECESM3B72OM5DWMSFO6C2EA6KNCIO4SFVFDHO6JVBYRSJ5G3HQ.data
...
|   |--- CIQPP
|       |--- CIQPPQVFU2X6L6RB67SNEYN4MPR236SNPL5OML2TBA4RIQQPM4FY6VY.data
|--- config
|--- datastore
|   |--- 000002.ldb
...
|   |--- 000009.log
|   |--- CURRENT
|   |--- LOCK
|   |--- LOG
|   |--- MANIFEST-000010
|--- version

17 directories, 25 files
~~~

Die Speicherung der Daten in einem Hash--Tree hat den Vorteil, dass die Daten
bei der Speicherung üblicherweise mit einer kryptographischen Prüfsumme
abgelegt werden. Durch diesen Umstand kann *IPFS* eine unerwünschte Veränderung
an den Daten feststellen. Das folgende Beispiel zeigt die unerwünschte
Modifikation der `readme`--Datei und wie die Integritätsprüfung von *IPFS* die
Änderung der Daten erkennt:

~~~sh
# Validierung der Integrität der Daten
freya :: ~ » ipfs repo verify
verify complete, all blocks validated.

# Unerwünschte Modifikation der Daten.
freya :: ~ » echo "Trüffelkauz" >> .ipfs/blocks/CIQBED3K6YA[..]JENZ5B5HJ5R3A.data

# Erneute Validierung der Integrität der Daten
freya :: ~ » ipfs repo verify
block QmPZ9gcCEpqKTo6aq61g2nXGUhM4iCL3ewB6LDXZCtioEB \
was corrupt (block in storage has different hash than requested)
Error: verify complete, some blocks were corrupt.
~~~

## IPFS--ID

Das generierte Schlüsselpaar wird im Klartext auf der Festplatte abgelegt. Der
öffentliche Schlüssel kann mit `ipfs id` angeschaut werden, dies liefert
folgende Ausgabe (gekürzt):

~~~sh
freya :: ~ » ipfs id
{
        "ID": "QmbEg4fJd3oaM9PrpcMHcn6QR2HMdhRXz5YyL5fHnqNAET",
		"PublicKey":
		"CAASpgIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDGDgKtgJ9FW/EL1qY0Ohz
		 nGGh7dPAszDDpC3fhHcF7rI9iyLp5ei0T9gjfvsj+ULhxKqXHU9qoD7LjiUPUHQKPnND1Yv
		 [...]
		 7X5gVmtkEB8eDjLkcMNCmqMarAjjSb9Sg5uYIQj1WHPPCrvTVQioZIIIHJ6Z7ogWIDpDR5T
		 Og55tS4kW7qSJUQebh54v1gyEVd2mSgUf40MBAgMBAAE=",
        "Addresses": null,
        "AgentVersion": "go-libp2p/3.3.4",
        "ProtocolVersion": "ipfs/0.1.0"
}
~~~

Die unter *ID* gelistete Nummer ist stellt die Prüfsumme über den öffentlichen
Schlüssel dar als *Multihash* in `base58`--Enkodierung dar. Mit dieser *ID*
lässt sich ein Benutzer beziehungsweise Peer im *IPFS*--Netzwerk eindeutig
identifizieren.

Der private Schlüssel ist neben weiteren Informationen zum `ipfs`--Repository
in der `~/.ipfs/config`--Datei zu finden, welche beim anlegen des Repositories
automatisch erstellt wird.

~~~sh
freya :: ~ » cat .ipfs/config | grep PrivKey
	"PrivKey":
	"CAASpwkwggSjAgEAAoIBAQDGDgKtgJ9FW/EL1qY0OhznGGh7dPAszDDpC3fhHcF7rI9iyLp
	 5ei0T9gjfvsj+ULhxKqXHU9qoD7LjiUPUHQKPnND1YvWzpBIZNUhaiuo107J5MztPvroQ8/
	 [...]
	 cWTidFNBZdz5IGzj0P0oO5OK6gadI608TqTvxcLWf4iC/hOMvTUA7W9r1l9dea+YXubchvY
	 VQMS8YcXyzXoE+DQXzM5TqbZT/jxUS/UUFcs7UKhuEu+E9etcYBgpncrMoQckQE="
~~~

Für weitere Details zur Erstellung der *Identität* sollte der
Quelltext[^FN_IPFS_CODE_INIT] zu Rate gezogen werden.

[^FN_IPFS_CODE_INIT]: IPFS Schlüsselgenerierung: <https://github.com/ipfs/go-ipfs/blob/master/repo/config/init.go#L95>

Ein Authentifizierungsmechanismus im eigentlichen Sinne existiert bei *IPFS*
nicht. Benutzer lassen sich global über ihre *Peer--ID* ansprechen.

* IPFS Test--Subnetz
* Wie schaut es mit Verschlüsselung aus?
* Welche Authentifizierungsmechanismen gibt es?

TODO: IPFS Subnetz

## Mögliche Probleme

## Angriffsszenarien

## Risikomanagement
