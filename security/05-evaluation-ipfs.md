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

das *ipfs*--dateisystem bzw. protokoll bringt das kommandozeilenwerkzeug `ipfs` mit. Dieses ermöglicht eine rudimentäre Nutzung des *IPFS*---
beim initialisieren von *ipfs* wird ein *rsa*--schlüsselpaar generiert. ein
*ipfs*--repository kann mit dem befehl `ipfs init` initialisiert werden. dabei
wird standardmäßig unter `~/.ipfs` ein repository angelegt.

~~~sh
freya :: ~ » ipfs init
initializing ipfs node at /home/qitta/.ipfs
generating 2048-bit rsa keypair...done
peer identity: qmbeg4fjd3oam9prpcmhcn6qr2hmdhrxz5yyl5fhnqnaet
to get started, enter:

        ipfs cat /ipfs/qmywapjzv5czsna625s3xf2nemtygpphdwez79ojwnpbdg/readme
~~~

Bei der Initialisierung wird eine *peer identity* erzeugt. Anschließend kann der Benutzer die `readme`--Datei aus dem *IPFS*--Store betrachten. [@sec:APP_IPFS_SECWARNING] zeigt weiterhin die aktuelle Sicherheitswarnung der *IPFS*--Software. Es wird explizit ein paar mal darauf hingewiesen, dass *IPFS* sich im Alphastadium befindet. Weiterhin gibt es Details zur »Sicherheit« in der Datei `security-notes`, welche analog zur `readme`--Datei betrachtet werden kann.

### IPFS--ID

das generierte schlüsselpaar wird in der getesteten version (ipfs version
0.4.3) im klartext auf der festplatte abgelegt. der öffentliche schlüssel kann
mit `ipfs id` angeschaut werden, dies liefert folgende Ausgabe:

~~~sh
freya :: ~ » ipfs id
{
        "id": "qmbeg4fjd3oam9prpcmhcn6qr2hmdhrxz5yyl5fhnqnaet",
		"publickey":
		"caaspgiwggeima0gcsqgsib3dqebaquaa4ibdwawggekaoibaqdgdgktgj9fw/el1qy0ohz
		 nggh7dpaszddpc3fhhcf7ri9iylp5ei0t9gjfvsj+ulhxkqxhu9qod7ljiupuhqkpnnd1yv
		 wzpbiznuhaiuo107j5mztpvroq8/rpsac3vparqiq9u9aytlyfpmpirkwia7f1fx7tb//lj
		 3wktfeums/vincgboasxbkwktf3sypsc5sklsevflrafq0ro9/x1kqnt321/1salgm74bi8
		 7x5gvmtkeb8edjlkcmncmqmarajjsb9sg5uyiqj1whppcrvtvqioziiihj6z7ogwidpdr5t
		 og55ts4kw7qsjuqebh54v1gyevd2msguf40mbagmbaae=",
        "addresses": null,
        "agentversion": "go-libp2p/3.3.4",
        "protocolversion": "ipfs/0.1.0"
}
~~~

der private schlüssel ist neben weiteren informationen zum `ipfs`--repository
in der `~/.ipfs/config`--datei zu finden, welche beim anlegen des repositories
automatisch erstellt wird.

~~~sh
freya :: ~ » cat .ipfs/config | grep privkey
	"privkey":
	"caaspwkwggsjageaaoibaqdgdgktgj9fw/el1qy0ohznggh7dpaszddpc3fhhcf7ri9iylp
	 5ei0t9gjfvsj+ulhxkqxhu9qod7ljiupuhqkpnnd1yvwzpbiznuhaiuo107j5mztpvroq8/
	 [...]
	 cwtidfnbzdz5igzj0p0oo5ok6gadi608tqtvxclwf4ic/homvtua7w9r1l9dea+yxubchvy
	 vqms8ycxyzxoe+dqxzm5tqbzt/jxus/uufcs7ukhueu+e9etcybgpncrmoqckqe="
~~~

todo: warum sind die keys unterschiedlich lang?

* <https://github.com/ipfs/go-ipfs/blob/master/repo/config/init.go#l112>

hashstuff: <https://github.com/ipfs/go-ipfs/blob/73cd8b3e98aba252f0eadcc625472103a2dd1d53/importer/importer.go>

* wie schaut es mit verschlüsselung aus?
* wie schaut es mit datenintegrität aus?
* welche authentifizierungsmechanismen gibt es?

## mögliche probleme

## angriffsszenarien

## risikomanagement
