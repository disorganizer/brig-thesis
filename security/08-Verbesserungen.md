# Verbesserungen und Erweiterungen

Auf Basis der Evaluation von »brig« sollen nun mögliche Konzepte vorgestellt
werden um die in der Evaluation identifizierten Schwächen abzumildern
beziehungsweise zu beheben.

## Sicherheitstechnische Anpassungen

* Verschlüsselung des gesamten Repository?
* BSI: Richtlinie für AES-GCM?
* Integrität der Shadow--File?
* Sicherung der Identität?
* Convergent encryption

### Schlüsselhierarchie-- und Authentifizierungskonzept

* Master--Key auf Yubikey
* Subkeys für Daten, Sitzung, Repo?
* Backup--Keys für Hierarchie?
* Dateiverschlüsselung mittels Ableitung?

Mit einem Ansatz wie »Convergent encryption« würde es die Möglichkeit geben die
kryptographischen Schlüsseln von den zu verschlüsselten Dateien abzuleiten.
Diese Verfahren bringt Vor-- und Nachteile mit sich, welche weiter unter XY
beleuchtet werden.


#### Hardwaretoken als 2F--Authentifizierung

Wie bereits erwähnt, ist die Authentifizierung über ein Passwort oft der
Schwachpunkt eines zu sichernden Systems. Ist das Passwort oder die
Passwort--Richtlinien zu komplex, so neigen Benutzer oft dazu dieses
aufzuschreiben. Ist die Komplexität beziehungsweise Entropie zu niedrig so ist
es mit modernen Methoden vergleichsweise einfach das Passwort »berechnen«.

Ein weiterer Schwachpunkt der oft ausgenutzt wird ist die »unsichere«
Speicherung von kryptographischen Schlüsseln.

##### Yubikey Einleitung

Der *Yubikey* ist ein Hardwaretoken, welcher dem Benutzer eine
One--Time--Password--Authentifizierung ermöglicht.

##### Proof of concept 2FA von »brig« mit Yubico--Cloud

Für die Proof--of--concept Implementierung der Zwei--Faktor--Authentifizierung
wird die *yubigo*--Bibliothek[^FN_YUBIGO] verwendet.

[^FN_YUBIGO]: Yubigo Dokumentation: <https://godoc.org/github.com/GeertJohan/yubigo>

Das folgende minimale Implementierung zeigt eine voll funktionsfähigen
Authentifizierung eine *Yubikey* am *Yubico*--Cloud--Service. Bei der
Implementierung des Hardwaretokens als zweiten Faktor, ist es wichtig darauf zu
achten, dass die *Yubikey ID* gesichert wird. Passiert dies nicht, so könnte
sich jeder Benutzer mit einem gültigen *Yubikey* gegenüber »brig«
authentifizieren.

~~~go
package main

import (
	"fmt"
	"log"
	"os"
	"github.com/GeertJohan/yubigo"
)

// Yubikey ID, diese stellt die eigetnliche Identität des Benutzers dar.
const RegistredYubikeyID = "ababab"

func main() {
	OneTimePassword := os.Args[1]
	curTokenID := OTP[6:12]

	// Neues Authentifizierungstoken
	yubiAuth, err := yubigo.NewYubiAuth("XXXXX", "XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	if err != nil {
		log.Fatalln(err)
	}

	// Validierung des OTP durch die Yubico-Cloud
	_, ok, err := yubiAuth.Verify(OneTimePassword)
	if err != nil {
		log.Fatalln(err)
	}

	if ok {
		if curTokenID == RegistredYubikeyID {
			fmt.Printf("%s %s\n", "Authentification successful.", curTokenID)
		} else {
			fmt.Printf("%s %s\n", "Authentification failed. Wrong ID: ", curTokenID)
		}
	}
}
~~~

Beim Ausführen des Code--Snippets wird der *Yubikey*--OTP--Schlüssel als erster
Parameter übergeben. Folgende Ausgabe zeigt den Test mit zwei verschiedenen
*Yubikey*--Token.

~~~sh
# Test mit einem am System bekannten/registrierten Token
$ ./simple2fa cccccckjrbajrhridrbfudkvijfglighvjhnkfliciij                                                                                                   1 ↵
Authentification successful. ababab

# Test mit einem am System unbekannten/nicht registrierten Token
$./simple2fa ccccccjwnahgnfvgfbhikgrdgjnekdltlnbbrhiebuhi                                                                                                 127 ↵
Authentification failed. Wrong ID:  ejjegn

~~~

##### Proof of concept 2FA von »brig« mit Eigener Serverinfrastruktur

~~~go

import ...

~~~

##### Yubikey als Smartcard


* Speicherung von Schlüsseln auf YubiKey möglich? Wie?

#### Authentifizierung von Benutzern auf Basis vom Web--of--trust

* IPFS--ID mit privaten Schlüssel signieren und über
  »Web--of--Trust--Overlay--Network«

## Signieren von Quellcode

Um die Verantwortlichkeit sowie den Urheber bestimmter Quellcodeteile besser
identifizieren zu können und dadurch die Entwickler auch vor Manipulationen am
Quelltext--Repository besser zu schützen bietet sich das Signieren von
Quellcode (auch *code signing* genannt) an. Zwar bietet beispielsweise `git`
bereits mit kryptographischen Prüfsummen (*SHA--1*) eine gewissen
Manipulationssicherheit, jedoch ermöglicht *SHA--1* keine Authentifizierung der
Quelle.

Eine Quelle zu Authentifizieren ist keine einfache Aufgabe. Gerade bei
Open--Source--Projekten, bei welchen im Grunde jeder (auch Angreifer) Quellcode
zum Projekt beitragen können, ist eine Authentifizierung um so wichtiger. 

Eine weit verbreitete Möglichkeit zur Authentifizierung, ist hierbei die
*Digitale Signatur*. Quelltext beziehungsweise *Commits* (Beitrag u. Änderungen
an einem Projekt) können auf eine ähnliche Art signiert werden. 

`git` bietet im Fall von »brig«, welches über *GitHub* entwickelt wird, das
Signieren und Verifizieren von *Commits* und *Tags*. Hierzu kann beispielsweise
mit `git config` global die *Schlüssel--ID* des Schlüssels hinzugefügt werden, mit welchem
der Quelltext in Zukunft signiert werden soll:
Anschließend kann mit dem zusätzlichen Parameter (`-S[<keyid>],
--gpg-sign[=<keyid>]`) ein digital unterschriebener *Commit* abgesetzt werden:

~~~sh
# Schlüssel-ID des Entwicklers über Fingerprint ausfindig machen
$ gpg --list-keys christoph@nullcat.de
	pub   rsa2048 2013-02-09 [SC] [expires: 2017-01-31]
		  E9CD5AB4075551F6F1D6AE918219B30B103FB091
	uid           [ultimate] Christoph Piechula <christoph@nullcat.de>
	sub   rsa2048 2013-02-09 [E] [expires: 2017-01-31]

$ gpg --list-sig E9CD5AB4075551F6F1D6AE918219B30B103FB091 | tail -n 3
sub   rsa2048 2013-02-09 [E] [expires: 2017-01-31]
sig          8219B30B103FB091 2016-02-01  Christoph Piechula <christoph@nullcat.de>

# Signier-Schlüssel git mitteilen
$ git config --global user.signingkey  8219B30B103FB091

# Signierten Commit absetzen
$ git commit -S -m 'Brig evaluation update. Signed.'
~~~

Durch das signieren von *Commits* wird auf *GitHub* über ein Label ein
erweiterter Status zum jeweiligen *Commit* beziehungsweise *Tag* angezeigt,
siehe [@fig:img-signunveri].

![Nach dem Absetzen eines signierten Commits/Tags erscheint auf der *GitHub*--Plattform ein zusätzliches Label verifiziert, wenn der öffentliche Schlüssel des Entwicklers bei Github nicht hinterlegt ist.](images/signed-unverified2.png){#fig:img-signunveri width=65%}

Pflegen die Entwickler zusätzlich ihren privaten Schlüssel im *GitHub*--Account
ein, so signalisiert das Label eine verifizierte Signatur des jeweiligen
*Commits* beziehungsweise *Tags*, siehe [@fig:img-signed].

![Verifiziertes *GitHub*--Signatur--Label eines Commit/Tag welches aufgeklappt wurde.](images/signed2.png){#fig:img-signed width=70%}

## Signatur und Update der Binaries

1.) Signieren wie das Tor Projekt?
2.) Update Proof of concept mit Public-Key aufbauend?

## Repository--Backup--Konzept

* Key/Identify--Backup.

## Crypto--Layer Performance

* Verbesserungen vllt mit Assembler optimierter Variante: https://git.schwanenlied.me/yawning/chacha20?
* Benchmark mit https://git.schwanenlied.me/yawning/chacha20
* https://calomel.org/aesni_ssl_performance.html

# Weiter?

Piv sinnvoll? https://developers.yubico.com/PIV/Introduction/YubiKey_and_PIV.html
