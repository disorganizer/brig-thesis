# Evaluation von Brig

## Einleitung

Parallel zu der Arbeit wird der »brig«--Prototyp entwickelt. Das Ziel dieses
Kapitels ist es die bisherige Arbeit aus Sicht der Sicherheit erneut zu
evaluieren und bisher gemachte Fehler zu identifizieren. 

## Getestete Version

Für die Evaluation wird die Softwareversion mit dem größten Testumfang verwendet:

~~~sh
freya :: code/brig-thesis/security ‹master*› » brig --version
brig version v0.1.0-alpha+0d4b404 [buildtime: 2016-10-10T10:05:10+0000]
~~~

Zum aktuellen Zeitpunkt gibt es zwar bereits eine weitere Iteration in der Entwicklung von »brig«, bei welchem das interne »Store«--Handling geändert wurde. Da die »neue« Stor

## Einleitung »brig«

Das Ziel ist es mit, »brig« ein dezentrales Dateisynchronisationswerkzeug zu
entwickeln welches eine Balance zwischen Sicherheit uns Usability. Die
Entwicklung eines gut funktionierenden dezentralen Protokolls/Dateisystems ist
nicht trivial.

In [@sec:CAP_DEC_SERVICES] wurden bereits verschiedene dezentrale Protokolle
genannt. Diese sind jedoch hauptsächlich für den generellen Dateiaustausch
ausgelegt. Um die in [@sec:CAP_REQUIREMENTS] aufgeführten Anforderungen zu
realisieren, müssen die genannten Protokolle beziehungsweise das Verhalten der
Peer--To--Peer--Netzwerks an die eigenen Anforderungen angepasst werden. Als
Basis für die Implementierung eines Prototypen standen die beiden Protokolle
*BitTorrent* und *IPFS* in der engeren Auswahl, aufgrund der unter
[@sec:CAP_SUMMARY] genannten Funktionalitäten wurde *IPFS* als Basis bevorzugt.

![»brig« als Overlay--Netwerk für *IPFS*](images/brigoverlay.png){#fig:img-brig-overlay width=80%}

[@fig:img-brig-overlay] zeigt die Funktionsweise von »brig« als sogenanntes
Overlay--Netzwerk. »brig« wird verwendet um die in [@sec:CAP_SUMMARY] fehlenden
Eigenschaften des *IPFS*--Protokolls zu ergänzen.

## Sicherheit

Welche »Sicherheitsfeatures« sind in brig eingebaut?
Evaluation der Geschwindigkeit der aktuellen »Sicherheitsfeatures«.
https://git.schwanenlied.me/yawning/chacha20

* Keymanagement.
* Key/Identify--Backup.

## Mögliche Probleme

## Angriffsszenarien

## Risikomanagement
