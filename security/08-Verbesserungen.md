# Verbesserungen und Erweiterungen

Auf Basis der Evaluation von »brig« sollen nun mögliche Konzepte vorgestellt
werden um die in der Evaluation identifizierten Schwächen abzumildern
beziehungsweise zu beheben.

## Sicherheitstechnische Anpassungen

### Datenverschlüsselung

* Verschlüsselung des gesamten Repository?
* BSI: Richtlinie für AES-GCM?
* Integrität der Shadow--File?
* Convergent encryption

## Keymanagement

Das asymmetrische Schlüsselpaar von *IPFS* ist standardmäßig in keinster Weise
gesichert und muss daher besonders geschützt werden, da dieses die Identität
eines Individuums oder eine Institution darstellt. Bei Diebstahl des Schlüssels
(Malware, Laptop--Verlust/Diebstahl) kann die jeweilige Identität nicht mehr
als vertrauenswürdig betrachtet werden.

Die *IPFS*--Identität ist eng mit dem *IPFS*--Netzwerk und verwoben. Da das
Softwaredesign und auch die Sicherheitskomponenten sich aktuell in keinem
finalen Stadium befinden, ist für »brig« sinnvoll eine eigene
Schlüsselhierarchie umzusetzen, welche die Komponenten von *IPFS* schützt. So
haben auch zukünftige Änderungen an *IPFS* selbst keinen oder nur wenig
Einfluss auf das Sicherheitskonzept von »brig«.

[@fig:img-externalkey] zeigt ein Konzept, bei welchem ein »externes« und vom
Benutzer kontrolliertes Schlüsselpaar als Master--Schlüsseln für die
Absicherung des *IPFS*--Repository dient.

![Externes asymmetrisches Schlüsselpaar dient als »Master--Key« zur Sicherung der ungesicherten IPFS--Daten. Das Signieren der öffentlichen IPFS--ID ermöglich eine Zusätzliche Schicht der Authentifizierung.](images/external-key.png){#fig:img-externalkey width=70%}

Diese »externe« Identität muss dabei besonders vor Diebstahl geschützt werden
um Missbrauch zu vermeiden. Auf üblichen »Endverbrauchergeräten« ist der
Passwortschutz dieses Schlüsselpaars ein absolutes Minimalkriterium.

Eine weitere Maßnahme und »Best Practise« ist die sogenannte »Key Seperation«.
Obwohl es möglich ist das selbe Schlüsselpaar zum Signieren und Verschlüsseln
zu nehmen ist dies aus sicherheitstechnischen Gründen nicht empfehlenswert. Im
Klartext heißt das, dass für unterschiedliche Einsatzzwecke unterschiedliche
Schlüssel verwendet werden sollen. Um dies zu realisieren bietet *GnuPG* die
Möglichkeit von sogenannten *Subkeys*.

Beim erstellen eines Schlüsselpaars mit *GPG* wird standardmäßig ein
Masterschlüssel (zum Signieren von Daten und Zertifizieren Subkeys) und ein
*Subkey* für das Verschlüsseln von Daten erstellt[^FN_DEBIAN_SUBKEY].

Der Vorteil von *Subkeys* ist, dass diese an einen bestimmten Einsatzzweck
gebunden sind und auch unabhängig vom eigentlich Master--Schlüsselpaar
widerrufen werden können --- was eine sehr wichtige Eigenschaft bei der
Verwaltung von Schlüsseln darstellt.

Eine weitere Empfehlung an dieser Stelle wäre es den *privaten Schlüssel* ()

[^FN_DEBIAN_SUBKEY]: Debian Wiki Subkeys: <https://wiki.debian.org/Subkeys>

## Authentifizierungskonzept

Unter [birg-Auth] wurde die aktuelle Situation evaluiert. Zum aktuellen
Zeitpunkt hat »brig« keine Authentifizierungsmechanismus, der kommunizierenden
Parteien müssen im Grunde ihre »brig«--Fingerabdrücke gegenseitig validieren
und auf dieser Basis manuell Ihrer Liste mit Kommunikationspartnern hinzufügen.
Neben der Möglichkeit den Fingerabdruck über einen Seitenkanal (Telefonat,
E--Mail) auszutauschen, sollen nun benutzerfreundlichere Konzepte vorgestellt
werden.

Da *IPFS* bereits ein *Public/Private*--Schlüsselpaar mitbringt würde sich im
einfachste Falle nach dem ersten Verbindungsaufbau die Möglichkeit bieten den
sein Gegenüber anhand eines *Gemeinsamen Geheimnis* oder anhand eines
*Frage--Antwort--Dialogs* zu verifizieren.

![Frage--Antwort--Authentifizierung. Alice stellt Bob eine Frage auf die nur er die Antwort wissen kann.](images/question-answer.png){#fig:img-qa width=95%}

## Smartcards und RSA--Token als 2F--Authentifizierung

Wie bereits erwähnt, ist die Authentifizierung über ein Passwort oft der
Schwachpunkt eines zu sichernden Systems. Ist das Passwort oder die
Passwort--Richtlinien zu komplex, so neigen Benutzer oft dazu dieses
aufzuschreiben. Ist die Komplexität beziehungsweise Entropie zu niedrig so ist
es mit modernen Methoden vergleichsweise einfach das Passwort »berechnen«.

Ein weiterer Schwachpunkt der oft ausgenutzt wird ist die »unsichere«
Speicherung von kryptographischen Schlüsseln.

Da Passwörter sowie kryptographische Schlüssel können bei handelsüblichen
Endanwendersystemen wie beispielsweise PC, Smartphone relativ einfach
mitgeloggt beziehungswiese entwendet werden können. 

Um hier die Sicherheit zu steigern wird von Sicherheitsexperten oft zur
Zwei--Faktor--Authentifizierung beziehungsweise zur hardwarebasierten
Speicherung kryptographischer Schlüssel (persönliche Identität,
RSA--Schlüsselpaar) geraten (vgl. [@martin2012everyday]).

Für die Speicherung von kryptographischen Schlüsseln eignen sich beispielsweise
Chipkarten, welche die Speicherung kryptographischer Schlüssel ermöglichen. Die
Problematik bei Smartcards ist, dass man zusätzlich ein Lesegerät benötigt.
Dieser Umstand schränkt die Benutzung stark ein und ist deswegen weniger für
den privaten Einsatzzweck geeignet.

Bei der Zwei--Faktor--Authentifizierung gibt es verschiedene Varianten, welche
in der Regel ein Passwort mit einem weiterem Element wie einer Bankkarte oder
einem Hardware--Token wie beispielsweise der RSA SecureID[^FN_SECUREID] verknüpfen.

[^FN_SECUREID]: RSA--SecureID: <https://de.wikipedia.org/wiki/SecurID>

Ein Problem hierbei ist wieder die Umsetzung im privaten Bereich.

Eine relativ »neue« Möglichkeit bieten beispielsweise die Hardware--Token von
*Yubico*[^FN_YUBICO] und *Nitrokey*[^FN_NITROKEY]. Diese Hardware--Token haben
zudem den Vorteil, dass sie die Funktionalität einer Smartcard und eines
Hardware--Token für Zwei--Faktor--Authentifizierung vereinen. 

Der besondere bei diesen Hardware--Komponenten ist, dass sie sich über die
USB--Schnittstelle als HID (Human--Interface--Device) ausgeben und somit keine
weitere Zusatzhardware wie beispielsweise ein Lesegerät benötigt wird.

[^FN_NITROKEY]: Nitrokey: <https://www.nitrokey.com/>
[^FN_YUBICO]: Yubico: <https://www.yubico.com>

Bei beiden Herstellern gibt es die Hardware--Token in verschiedenen
Ausführungen. Für die Entwicklung von »brig« wurden *Yubico
Neo*--Hardware--Token --- aufgrund der Umfangreichen Programmier--API --- des
Herstellers *Yubico* beschafft. Alle weiteren Ausführungen und Demonstrationen
beziehen sich auf dieses Modell.

### Yubikey--NEO Einleitung

[^FN_YUBIKEY_PNG]: Bild--Quelle: <https://hao0uteruy2io8071pzyqz13-wpengine.netdna-ssl.com/wp-content/uploads/2015/04/YubiKey-NEO-1000-2016-444x444.png>

Der *Yubikey Neo* hat folgende Funktionalitäten beziehugnsweise Eigenschaften:

* Yubico OTP, One--Time--Password--Verfahren des Herstellers. Standardmäßig
  kann jeder YubiKey gegen die YubiCloud--Authentifizierungdienst mittels OTP
  authentifiziert werden
* OATH–Kompitabilität (HMAC--Based--OTP-- und Time--Based--OTP--Verfahren[^FN_HOTP][^FN_TOTP])
* Challange--Response--Verfahren (HMAC-SHA1, Yubico OTP)
* FIDO U2F (Universal Second Factor)
* Statische Passwörter

Smartcard--Funktionalität:

* PIV (Personal Identity Verification) Standard[^FN_NISTPIV]
* OpenPGP--Smartcard--Standard

Weitere Eigenschaften sind im Datenblatt[^FN_YUBIKEY_NEO] des YubiKey--Neo zu finden.

[^FN_HOTP]: HOTP: <https://en.wikipedia.org/wiki/HMAC-based_One-time_Password_Algorithm>
[^FN_TOTP]: TOTP: <https://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm>
[^FN_NISTPIV]: PIV--Standard: <http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.201-2.pdf>
[^FN_YUBIKEY_NEO]: YubiKey--Neo: <https://www.yubico.com/wp-content/uploads/2016/02/Yubico_YubiKeyNEO_ProductSheet.pdf>

Der *YubiKey--NEO* bietet mit zwei Konfigurationsslots (siehe GUI--Screenshot
[@fig:img-ykgui]) die Möglichkeit an mehrere Verfahren gleichzeitig nutzen zu
können. Ein beispielhafte Konfiguration wäre den ersten Konfigurationsslot mit
einem statischen Passwort und den zweiten mit einem One--Time--Passwort zu
belegen. 

[^FN_YUBICO_PERSON_TOOL]: Yubico Personalization Tool: <https://www.yubico.com/products/services-software/personalization-tools/use/>

Die grundlegende Konfiguration des *YubiKey* ist mit dem *YubiKey
Personalisation Tool* möglich.  

![GUI des YubiKey Personalisation Tool. Das Konfigurationswerkzeug ist eine QT--Anwendung, diese wird von den gängigen Betriebssystemen (Linux, MacOs, Windows) unterstützt.](images/ykgui2.png){#fig:img-ykgui width=75%}

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
const (
	// Passwort und Yubikeu (zweites Token) welches gegenüber
	// »brig« registriert ist
	RegistredYubikeyID = "ccccccababab"
	UserPassword       = "katzenbaum"
)

func answer(flag bool) string {
	if flag {
		return "Yes"
	}
	return "No"
}

func main() {
	// Passwort und OTP einlesen
	password, otp := os.Args[1], os.Args[2]
	yubiAuth, err := yubigo.NewYubiAuth("00042", "78AJl49l2924j2393jl29dsjlp9=")

	if err != nil {
		log.Fatalln(err)
	}

	// Validierung an der Yubico Cloud
	_, ok, err := yubiAuth.Verify(otp)
	if err != nil {
		log.Fatalln(err)
	}

	// Validierung welche Authentifizierungs-Parameter korrekt sind
	fmt.Printf("Yubico Auth valid? :\t %s\n", answer(ok))
	fmt.Printf("YubiKey known by brig? : %s\n", answer(otp[0:12] == RegistredYubikeyID))
	fmt.Printf("Password valid? :\t %s\n", answer(password == UserPassword))
}
~~~

Beim Ausführen des Code--Snippets wird der *Yubikey*--OTP--Schlüssel als erster
Parameter übergeben. Folgende Ausgabe zeigt den Test mit zwei verschiedenen
*Yubikey*--Token.

~~~sh
# Korrektes Passwort, korrekter Yubikey und OTP
$ ./twofac katzenbaum ccccccabababkdnkekdfvltennnlulrngvujviikcerg
[Yubico Auth valid? : Yes] ++++ [YubiKey known by brig? : Yes] ++++ [Password valid? : Yes]

# Korrektes Passwort, anderer Yubikey und OTP
$ ./twofac katzenbaum cccccccdcdcdfjckvrnckvfufkglckrdrgjlrntbcgbn
[Yubico Auth valid? : Yes] ++++ [YubiKey known by brig? : No] ++++ [Password valid? : Yes]

# Falsches Passwort, korrekter Yubikey und OTP
$ ./twofac elchwald ccccccabababgfbtejutvddbvdrfcrdrtbvlkktrdknl
[Yubico Auth valid? : Yes] ++++ [YubiKey known by brig? : Yes] ++++ [Password valid? : No]

# Korrektes Passwort, korrekter Yubikey und vorheriges OTP (replay)
$ ./twofac elchwald ccccccabababgfbtejutvddbvdrfcrdrtbvlkktrdknl
2016/11/28 12:20:43 The OTP is valid, but has been used before. If you receive
this error, you might be the victim of a man-in-the-middle attack.
[Yubico Auth valid? : No] ++++ [YubiKey known by brig? : Yes] ++++ [Password valid? : No]
~~~

TODO: Lieber Tabelle?

##### Proof of concept 2FA von »brig« mit Eigener Serverinfrastruktur

~~~go

import ...

~~~

### Yubikey als Smartcard


* Speicherung von Schlüsseln auf YubiKey möglich? Wie?

### Authentifizierung von Benutzern auf Basis vom Web--of--trust

* IPFS--ID mit privaten Schlüssel signieren und über
  »Web--of--Trust--Overlay--Network«


## Schlüsselhierarchie-- und Authentifizierungskonzept

* Master--Key auf Yubikey
* Subkeys für Daten, Sitzung, Repo?
* Backup--Keys für Hierarchie?
* Dateiverschlüsselung mittels Ableitung?

Mit einem Ansatz wie »Convergent encryption« würde es die Möglichkeit geben die
kryptographischen Schlüsseln von den zu verschlüsselten Dateien abzuleiten.
Diese Verfahren bringt Vor-- und Nachteile mit sich, welche weiter unter XY
beleuchtet werden.


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

$ gpg --list-sig E9CD5AB4075551F6F1D6AE918219B30B103FB091 | tail -n 4
sig     P    D2BB0D0165D0FD58 2016-11-29  CA Cert Signing Authority (Root CA) <gpg@cacert.org>
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

Ein weiterer Punkt der für eine »benutzerfreundliche« 
* Key/Identify--Backup.
