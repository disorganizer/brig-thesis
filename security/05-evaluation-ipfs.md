# Evaluation IPFS

*IPFS* (*InterPlanetary File System*) stellt die Netzwerkbasis für »brig« dar.
Da *IPFS* teilweise andere Ziele als »brig« hat, ist es wichtig, dass die
Anforderungen von »brig« durch die *IPFS*--Basis nicht verletzt werden. Im
Folgenden wird *IPFS* bezüglich bestimmter sicherheitstechnischer Anforderungen
genauer beleuchtet, um Diskrepanzen zwischen den Zielen von »brig« zu
identifizieren.

## Einleitung

Das *InterPlanetary File System* wird als  »content-addressable, peer-to-peer
hypermedia distribution protocol« definiert. Das besondere an *IPFS* ist, dass
es ein sogenanntes *Content--Addressable--Network (CAN)* darstellt. Ein *CAN*
arbeitet mit einer verteilten Hashtabelle (*Distributed Hash Table (DHT)*),
welche als grundlegende »Datenstruktur« verwendet wird um die Daten innerhalb
eines Peer--to--peer--Netzwerks zu lokalisieren und zu speichern. Eine *DHT*
als Datenstruktur bringt in der Theorie laut Wikipedia[^FN_DHT] folgende
Eigenschaften mit sich:

[^FN_DHT]: Verteilte Hashtabelle: <https://de.wikipedia.org/wiki/Verteilte_Hashtabelle>

* **Fehlertoleranz:** Das System sollte zuverlässig funktionieren, auch wenn Knoten
  ausfallen oder das System verlassen.
* **Lastenverteilung:** Schlüssel werden gleichmäßig auf alle Knoten verteilt.
* **Robustheit:** Das System sollte „korrekt“ funktionieren können, auch wenn ein
  Teil (möglicherweise ein Großteil) der Knoten versucht, das System zu stören.
* **Selbstorganisation:** Es ist keine manuelle Konfiguration nötig.
* **Skalierbarkeit:** Das System sollte in der Lage sein, auch mit einer großen
  Anzahl von Knoten funktionsfähig zu bleiben.

## Projektumfang und Version

TODO: Abkürzungsverzeichnis LoC

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

## Sicherheit

### IPFS--Basis 

Das *IPFS*--Dateisystem bzw. Protokoll bringt das Kommandozeilenwerkzeug `ipfs`
mit. Dieses ermöglicht eine rudimentäre Nutzung von *IPFS*. Beim initialisieren
von *IPFS* wird ein *RSA*--Schlüsselpaar generiert. Ein *IPFS*--Repository kann
mit dem Befehl `ipfs init` initialisiert werden. Dabei wird standardmäßig unter
`~/.ipfs` ein Repository angelegt.

~~~sh
freya :: ~ » ipfs init
initializing ipfs node at /home/qitta/.ipfs
generating 2048-bit RSA keypair...done
peer identity: QmbEg4fJd3oaM9PrpcMHcn6QR2HMdhRXz5YyL5fHnqNAET
to get started, enter:

        ipfs cat /ipfs/QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/readme
~~~

Bei der Initialisierung wird eine *peer identity* erzeugt. Anschließend kann
der Benutzer die `readme`--Datei aus dem *IPFS*--Store betrachten.
[@sec:APP_IPFS_SECWARNING] zeigt weiterhin die aktuelle Sicherheitswarnung der
*IPFS*--Software. Es wird explizit ein paar mal darauf hingewiesen, dass *IPFS*
sich im Alphastadium befindet. Weiterhin gibt es Details zur »Sicherheit« in
der Datei `security-notes`, welche analog zur `readme`--Datei betrachtet werden
kann.

### IPFS--ID

Das generierte Schlüsselpaar wird in der getesteten Version (*IPFS*--Version
0.4.3) im Klartext auf der Festplatte abgelegt. Der öffentliche Schlüssel kann
mit `ipfs id` angeschaut werden, dies liefert folgende Ausgabe:

~~~sh
freya :: ~ » ipfs id
{
        "ID": "QmbEg4fJd3oaM9PrpcMHcn6QR2HMdhRXz5YyL5fHnqNAET",
		"PublicKey":
		"CAASpgIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDGDgKtgJ9FW/EL1qY0Ohz
		 nGGh7dPAszDDpC3fhHcF7rI9iyLp5ei0T9gjfvsj+ULhxKqXHU9qoD7LjiUPUHQKPnND1Yv
		 WzpBIZNUhaiuo107J5MztPvroQ8/RpSAC3VpARQiQ9U9AYtlyFPmpiRKwIA7f1FX7tb//Lj
		 3WkTFeUmS/vINCgBOasXbkwKtf3sYpsC5SKlSevFLrAFQ0Ro9/x1kQNt321/1sALgM74bI8
		 7X5gVmtkEB8eDjLkcMNCmqMarAjjSb9Sg5uYIQj1WHPPCrvTVQioZIIIHJ6Z7ogWIDpDR5T
		 Og55tS4kW7qSJUQebh54v1gyEVd2mSgUf40MBAgMBAAE=",
        "Addresses": null,
        "AgentVersion": "go-libp2p/3.3.4",
        "ProtocolVersion": "ipfs/0.1.0"
}
~~~

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

TODO: Warum sind die Keys unterschiedlich lang?

* <https://github.com/ipfs/go-ipfs/blob/master/repo/config/init.go#L112>

Hashstuff: <https://github.com/ipfs/go-ipfs/blob/73cd8b3e98aba252f0eadcc625472103a2dd1d53/importer/importer.go>

* Wie schaut es mit Verschlüsselung aus?
* Wie schaut es mit Datenintegrität aus?
* Welche Authentifizierungsmechanismen gibt es?

## Mögliche Probleme

## Angriffsszenarien

## Risikomanagement
