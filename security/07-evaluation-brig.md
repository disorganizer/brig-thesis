# Evaluation von Brig

## Einleitung

Parallel zu der Arbeit wird der »brig«--Prototyp entwickelt. Das Ziel dieses
Kapitels ist es die bisherige Arbeit aus Sicht der Sicherheit erneut zu
evaluieren und bisher gemachte Fehler zu identifizieren. Für weitere allgemeine
Details zur Architektur von »brig« siehe die Arbeit vom Herrn Pahl[@cpahl].

## Getestete Version

Für die Evaluation wird die Softwareversion mit dem größten Testumfang verwendet:

~~~sh
freya :: code/brig-thesis/security ‹master*› » brig --version
brig version v0.1.0-alpha+0d4b404 [buildtime: 2016-10-10T10:05:10+0000]
~~~

Zum aktuellen Zeitpunkt gibt es zwar bereits eine weitere Iteration in der
Entwicklung von »brig«, bei welchem das interne »Store«--Handling geändert
wurde.

## Einleitung »brig«

Das Ziel ist es, mit »brig« ein dezentrales Dateisynchronisationswerkzeug zu
entwickeln welches eine gute Balance zwischen Sicherheit und Usability
bietet. Die Entwicklung eines gut funktionierenden dezentralen
Protokolls/Dateisystems ist nicht trivial.

In [@sec:CAP_DEC_SERVICES] wurden bereits verschiedene dezentrale Protokolle
genannt. Diese sind jedoch hauptsächlich für den generellen Dateiaustausch
ausgelegt. Um die in [@sec:CAP_REQUIREMENTS] aufgeführten Anforderungen zu
realisieren, müssen die genannten Protokolle beziehungsweise das Verhalten des
Peer--To--Peer--Netzwerks an die gesetzten Anforderungen angepasst werden. Als
Basis für die Implementierung eines Prototypen standen die beiden Protokolle
*BitTorrent* und *IPFS* in der engeren Auswahl. Aufgrund der unter
[@sec:CAP_SUMMARY] genannten Funktionalitäten wurde *IPFS* als Basis bevorzugt.

![»brig« als Overlay--Netwerk für *IPFS*](images/brigoverlay.png){#fig:img-brig-overlay width=80%}

[@fig:img-brig-overlay] zeigt die Funktionsweise von »brig« als sogenanntes
Overlay--Netzwerk. »brig« wird verwendet um die in [@sec:CAP_SUMMARY] fehlenden
Eigenschaften des *IPFS*--Protokolls zu ergänzen.

## Sicherheit

### Datenverschlüsselung

Standardmäßig werden die Daten bei *IPFS* unverschlüsselt gespeichert.
Weiterhin basiert die aktuelle Transportverschlüsselung der Daten auf einem
nicht standardisiertem Protokoll.

Um die gesetzten Anforderungen (Vertraulichkeit von Daten, [@sec:requirements])
zu erreichen muss »brig« die Funktionalität von *IPFS* so erweitern, dass die
Authentizität und Vertraulichkeit der Daten bei lokaler Speicherung aber auch
bei der Übertragung gewährleistet ist. [@fig:img-aesgcm] zeigt das
Containerformat welches für »brig« entwickelt wurde um diese Anforderungen zu
erreichen.

![»brig«-Containerformat für Datenverschlüsselung mit Authenzität.](images/aesgcm.png){#fig:img-aesgcm width=100%}

Das Container--Format wurde so angelegt um wahlfreier Zugriff auf Daten zu
ermöglichen und den Verschlüsselungsalgorithmus austauschbar zu machen. Falls
Schwächen bei einem bestimmten Algorithmus auftauchen sollten, kann die
Vertraulichkeit der Daten durch den Wechseln auf einen noch sicheren
Algorithmus gewährleistet werden.

### Verwendete Algorithmen

Die aktuelle Softwareversion[^FN_SYMALGO] beherrscht die *AEDA*--Blockchiffren[^AEAD]:

* AES--GCM
*userlookup  ChaCha20/Poly1305 (externe Bibliothek[^FN_CHACHA20])

TODO: encrypt-than-mac vs GCM/Poly1305, key reuse? 
http://security.stackexchange.com/questions/2202/lessons-learned-and-misconceptions-regarding-encryption-and-cryptology

[^FN_SYMALGO]: Aktuell von »brig« unterstützte symmetrische Verschlüsselungsverfahren: <https://github.com/disorganizer/brig/blob/fa9bb634b4b83aaabaa967ac523123ce67aa217d/store/encrypt/format.go>
[^FN_CHACHA20]: ChaCha20/Poly1305--Bibliothek: <https://github.com/codahale/chacha20poly1305>
[^AEAD]: Authenticated encryption: <https://en.wikipedia.org/wiki/Authenticated_encryption>

Der *AEAD*--Betriebsmodi wurde gewählt, weil er den Vorteil hat, dass er neben
der Vertraulichkeit auch Authentizität und Integrität sicherstellt.

Erste Benchmarks [@cpahl] haben gezeigt, dass die Performance bei
Verschlüsselung (chacha20/poly1305) stark einbricht. Es gibt unter von
*cloudflare* einen Go--Fork [^FN_CLOUDFLARE] welcher AES--NI--Erweiterungen
unterstützt.

[^FN_CLOUDFLARE]: CloudFlare Go--Crypto--Fork: <https://blog.cloudflare.com/go-crypto-bridging-the-performance-gap/>

Der *AES--NI*--Befehlserweiterungssatz war lange Zeit aufgrund von
Lizenzproblemen nicht in *Go* implementiert. Nach eingehender Recherche
scheinen die Patches von *Cloudflare* jedoch mittlerweile in *Go*
Einzug[^FN_AESNI_MERGE][^FN_ECDSA_MERGE] gefunden haben.

[^FN_AESNI_MERGE]: Go AES--NI--Patch--Merge: <https://go-review.googlesource.com/#/c/10484/>
[^FN_ECDSA_MERGE]: Go ECDSA--P256--Patch--Merge: <https://go-review.googlesource.com/#/c/8968/>

Benchmark 1 [@fig:img-aesni] zeigt den Geschwindigkeitszugewinn der durch die
Nutzung des *AES--NI*--Befehlserweiterungssatzes zustande kommt.

![Geschwindigkeitszuwachs durch AES--NI](images/aesni-impact.json.svg.pdf){#fig:img-aesni width=100%}

Benchmark 2 [@fig:img-aesni] zeigt den Geschwindigkeitszugewinn der durch die
Nutzung des *AES--NI*--Befehlserweiterungssatzes zustande kommt.

![Keygeneration overhead.](images/keygenoverhead-profile.json.svg.pdf){#fig:img-keyoverhead width=100%}

![Low end systeme.](images/low-end-performance.json.svg.pdf){#fig:img-lowend width=100%}

![Lese--Geschwindigkeit des Kryptographielayers bei der Benutzung verschiedener Blockgrößen.](images/read-performance-blocksize.json.svg.pdf){#fig:img-read-block width=100%}

![Schreib--Geschwindigkeit des Kryptographielayers bei der Benutzung verschiedener Blockgrößen.](images/write-performance-blocksize.json.svg.pdf){#fig:img-write-block width=100%}

Cross compiling note: Raspberry Pi Binary: GOARM=6 GOARCH=arm GOOS=linux  go build main.go

### Schlüsselgenerierung

Aktuell wird für jede Datei ein Schlüssel zufällig generiert. Dieser wird in
den Metadaten abgelegt. Durch das zufällige generieren eines Schlüssels wird
bei zwei unterschiedlichen Kommunikationspartnern für die gleiche Datei ein
unterschiedlicher Schlüssel erstellt. Dies hat den Nachteil, dass die
Deduplizierungsfunktionalität von *IPFS* aktuell nicht funktioniert.

### Metadatenverschlüsselung

Neben dem Nutzdaten, die von *IPFS* verwaltet werden, werden weiterhin die
sogenannten »Stores« verschlüsselt. Diese beinhalten den Metadatenstand der
jeweiligen Synchronisationspartner.

Folgend die Struktur eines neu initialisierten eines »brig«--Repositories (vgl.
auch [@cpahl]):

~~~sh
freya :: tree -al alice
alice
|-- .brig
    |-- index # Stores der Synchronisationspartner
    |   |-- alice@ipfsnetwork.de.locked
    |-- config
    |-- ipfs
    |   |-- config
    |   |...|
    |   |-- version
    |-- master.key.locked
    |-- remotes.yml.locked # Bekannte Synchronisationspartner
    |-- shadow
~~~

Die Dateien mit der Endung `locked` sind durch »brig« verschlüsselt. Als
Einstiegspunkt für den Zugriff auf das Repository fungiert aktuell eine
Passwort--Abfrage. Das Passwort ist samt zufällig generiertem Salt als
*SHA-3*--Repräsentation in der `shadow`--Datei [^FN_BRIG_SHADOW] gespeichert.

[^FN_BRIG_SHADOW]: Quellcode: <https://github.com/disorganizer/brig/blob/fa9bb634b4b83aaabaa967ac523123ce67aa217d/repo/shadow.go>

Die verschlüsselte Remotes--Datei beinhaltet den *Benutzernamen* mit
dazugehörigen *Peer--ID* und einen *Zeitstempel* für die jeweils bekannten
(authentifizierten) Synchronisationspartner.

**Einschätzung:** Das *IPFS*--Repository, sowie das Schlüsselpaar von *IPFS* ist aktuell
unverschlüsselt. Dies würde diverse Modifikationen am erlauben wie
beispielsweise die Manipulation der *Peer--ID* von *IPFS*. Der `master.key` hat
aktuell keine Verwendung.

### »brig«--Identifier

Da *IPFS* an sich keinen Authentifizierungsmechanismus bietet, muss dieser von
»brig« bereitgestellt werden. Im *IPFS*--Netzwerk haben die *Peers* durch die
Prüfsumme über den öffentlichen Schlüssel eine eindeutige Kennung. Diese
Prüfsumme ist aufgrund des Aufbaues und der Länge als Menschen--lesbare Kennung
nicht geeignet. Aus diesem Grund wurde ein »brig«--Identifier (»brig«--*ID*)
eingeführt.

Die »brig«--*ID* repräsentiert den Benutzer mit einem Benutzernamen im
»brig«--Netzwerk nach außen. Der Aufbau dieses Namens ist an die Semantik des
XMPP--Standard[^FN_XMPPID] angelehnt und mit dem Präfix `brig#user:` versehen.
Folgendes Beispiel mit dem *Multihash*--Tool vom *IPFS*--Projekt zeigt die
Generierung einer User--ID aus dem Benutzernamen.

~~~sh
freya :: ~ » echo 'brig#user:alice@university.cc' | multihash -
QmYRofJVzXGsL4njv5BW7HNhCkpLCiCjQvrqesbm7TWUCe
~~~

Diese Definition ermöglicht es Organisationen ihre Mitarbeiter und deren
Ressourcen im »brig«--Netzwerk abzubilden. Weiterhin hat es den Vorteil, dass
eine E-Mail--Adresse auch einen korrekten Benutzernamen darstellen würde.

[^FN_XMPPID]: Jabber--ID: <https://de.wikipedia.org/w/index.php?title=Jabber_Identifier&oldid=147048396>

Um diese Funktionalität bereitzustellen wird ein »Trick« angewendet, bei
welchem die Zeichenkette des Nutzernamen als Block dem *IPFS*--Netzwerk bekannt
gemacht wird (vgl. [@cpahl]). Dieser Block selbst ist nicht eindeutig und
könnte auch von einem Angreifer selbst erstellt worden sein. Um eine
Eindeutigkeit herzustellen, wird der Benutzername direkt an die öffentliche
*ID* (siehe [@sec:CAP_IPFS_ID]) geknüpft.

Folgende Daten werden kombiniert um einen Benutzer eindeutig zu identifizieren:

* **Peer--ID:** Prüfsumme über den öffentlichen *IPFS*--Schlüssel.
* **User--ID:** Prüfsumme über die »brig«--ID, welche einen vom Benutzer gewählten
  Identifier darstellt.

[@fig:img-userlookup] zeigt das Auffinden von einem Benutzer im
*IPFS*--Netzwerk. Für weitere Details zur Softwarearchitektur und
Funktionsweise siehe auch [@cpahl].

![User lookup mittels »brig«-ID (gekürzter Peer--Fingerprint + User--ID). Nur bei Übereinstimmung vom Peer--Fingerprint und Benutzernamen--Fingerprint wird der Benutzer als valide erkannt.](images/userlookup.png){#fig:img-userlookup width=100%}

### Authentifizierung

#### Im Netzwerk

Eine Schwierigkeit die sich im Voraus stellt, ist die »sichere«
Authentifizierung. Mit der »brig«--ID ist es aufgrund des *Multihash* vom
öffentlichen *IPFS*--Schlüssel möglich den Benutzer eindeutig zu
identifizieren. Bei der aktuellen »brig«--Version muss der Fingerabdruck beim
hinzufügen des Synchronisationspartners manuell hinzugefügt werden. Dies setzt
voraus, dass die Synchronisationspartner ihre *IPFS*--Fingerabdrücke
austauschen. Anschließend können beide Synchronisationspartner ihre
Repositories synchronisieren.

~~~sh
# Alice fügt Bob (Bob's brig-ID:bob@jabber.nullcat.de/desktop,
# Bob's IPFS-Fingerabdruck: QmbR6tDXRCgpRwWZhGG3qLfJMKrLcrgk2q)
# als Synchronisationspartner hinzu
brig remote add bob@jabber.nullcat.de/desktop QmbR6tDXRCgpRwWZhGG3qLfJMKrLcrgk2q
~~~

Analog dazu muss auch Alice von Bob als Synchronisationspartner hinzugefügt
werden.

#### Aufbau einer verschlüsselten Verbindung

[@fig:img-keyexchange] zeigt den Ablauf beim Aufbau einer Verschlüsselten
Verbindung zwischen zwei Synchronisationspartnern.

![Vereinfachte Ansicht bei der Aushandlung eines Sitzungsschlüssel beim Verbindungsaufbau.](images/keyexchange.png){#fig:img-keyexchange width=90%}

**Ablauf aus der Sicht von Alice**:

1. *Alice* generiert  eine zufällige Nonce $nA$.
2. *Alice* verschlüsselt $nA$ mit dem öffentlichen Schlüssel von *Bob*.
3. *Alice* schickt verschlüsselte Nonce $nA$ an *Bob* (bob_pub_key($nA$)).
4. *Bob* entschlüsselt die Nonce $nA$ von *Alice* mit seinem privaten Schlüssel.
5. *Bob* generiert eine Prüfsumme der Nonce $nA$ und schickt diese an *Alice*.
6. *Alice* vergleicht die von *Bob* erhaltene Prüfsumme SHA3($nA$) mit ihrer
   eigenen. Stimmt diese überein, so kann der Vorgang fortgesetzt werden,
   ansonsten wird dieser abgebrochen.
7. Analog zu *Alice* hat *Bob* auf die gleiche Art und Weise seine
   Nonce $nB$ mit *Alice* ausgetauscht.
8. *Alice* entschlüsselt die Nonce $nB$ von *Bob* und lässt diese in die
   Schlüsselgenerierung einfließen.
9. Der gemeinsame Schlüssel ist nun eine *XOR*--Verknüpfung der beiden Noncen
   $nA$ und $nB$. Um den Schlüssel zu »verstärken« wird zusätzlich die
   Schlüsselableitungsfunktion *scrypt* angewendet.

**Einschätzung**: Dir Aufbau der Verschlüsselten Verbindung setzt eine
vorherige Authentifizierung des jeweiligen Kommunikationspartners. Wäre dieser
nicht authentifiziert, so wäre in diesem Fall ein
*Man--In--The--Middle*--Angriff denkbar.

Die aktuelle Softwareversion bietet hier keinen Automatismus und auch keinen
Authentifizierungsmechanismus wie er beispielsweise bei *Pidgin*--Messenger mit
*OTR*--Verschlüsselung.

#### Lokal

Um Zugriff auf das »brig«--Repository zu erhalten muss sich der Benutzer »brig«
gegenüber mit einem Passwort authentifizieren. Schlechte Passwörter (TODO: Ref)
sind ein großes Problem im Informationszeitalter, da von ihnen die Sicherheit
eines gesamten Systems abhängen kann. Menschen sind schlecht darin die
*Entropie*[^FN_ENTROPY] von Passwörter richtig einzuschätzen. »brig« verwendet
für die Bestimmung der Passwort--Entropie *zxcvb*--Bibliothek, welche von
*Dropbox* entwickelt wurden. Laut einer Studie [@Carnavalet] wird die
Bibliothek, im Vergleich zu den getesteten Konkurrenten, als akkurater in ihrer
Funktionsweise bezeichnet. Eine Schwäche, welche bei den
Entropie--Schätzungswerkzeugen auftritt ist, dass diese ohne Basis eines
Wörterbuchs arbeiten und somit bei Zeichenketten *Brute--Force* als schnellsten
Ansatz annehmen (TODO: Ref Passwortcracking.).

Ein weiteres Problem dass bei der Definition einer minimalen Entropie besteht
ist, dass Benutzer bei komplexen Passwörtern dazu neigen werden diese
aufzuschreiben.

[^FN_ENTROPY]: Password--Entropy: <https://en.wikipedia.org/wiki/Password_strength#Entropy_as_a_measure_of_password_strength>

**Einschätzung**: Bei der aktuellen Authentifikation gegenüber dem Repository
ist ein schlechtes Passwort oder die erzwungene Komplexität (Benutzer schreiben
Komplexe Passwörter auf) eine Schwachstelle.

Evaluation der Geschwindigkeit der aktuellen »Sicherheitsfeatures«.

https://git.schwanenlied.me/yawning/chacha20

* Keymanagement.
* Key/Identify--Backup.
