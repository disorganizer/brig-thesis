# Verbesserungen und Erweiterungen

Auf Basis der Evaluation von »brig« sollen nun mögliche Konzepte vorgestellt
werden um die in der Evaluation identifizierten Schwächen abzumildern
beziehungsweise zu beheben.

## Sicherheitstechnische Anpassungen

### Datenverschlüsselung

Aktuell verwendet der Datenverschlüsselungsschicht bei der Generierung der
*MAC* xy bit. Laut *BSI* werden hierfür zz bit empfohlen. BSI--Richtlinie für GCM.

Wie unter yy zu sehen sind aktuell die *IPFS*--Schlüssel in der `config`--Datei
von *IPFS* im Klartext hinterlegt. »brig« verschlüsselt diese Datei zum
aktuellen Zeitpunkt nicht. Hier wäre eine Verschlüsselung mit einem
*Repository*--Key möglich, welcher wiederrum durch einen Masterschlüssel
geschützt werden sollte (siehe [@sec:keymanagement]). Eine weitere Überlegung
wäre das gesamte *Repository* mittels eines externen Masterschlüssel zu
verschlüsseln.

Wie unter [@sec:schluesselgenerierung] erläutert, wird aktuell für jede Datei
ein zufälliger Schlüssel generiert. Mit diesem Ansatz wird die
Deduplizierungsfunktinalität von *IPFS* weitgehend nutzlos gemacht.

Ein Ansatz dieses »Problem« zum Umgehen ist die sogenannte »Convergent
Encryption«. Diese Technik wird beispielsweise von *Cloud--Storage*--Anbietern
verwendet um verschlüsselte Daten deduplizieren zu können, ohne dabei auf den
eigentlichen Inhalt zugreifen zu müssen (vgl. [@convergent-encryption]). 

![Bei Convergent Encryption resultiert aus gleichem Klartext der gleiche Geheimtext da der Schlüssel zur Verschlüsselung vom Klartext selbst abgeleitet wird.](images/convergent-encryption.png){#fig:img-convergent-encryption width=80%}

Wie in [@fig:img-convergent-encryption] zu sehen, wird hierbei beispielsweise
der Schlüssel zum verschlüsseln einer Datei von dieser selbst mittels einer
kryptographischen Hashfunktion abgeleitet.

Diese Verfahren lässt sich jedoch bei der aktuellen Architektur (separate
Verschlüsselungsschicht) nur eingeschränkt realisieren, da die Prüfsumme der
Daten erst nach dem Hinzufügen zum *IPFS* bekannt ist. Um die Daten zu
verschlüsseln müssten diese vor dem Hinzufügen komplett *gehasht* werden. Dies
würde bedeuten dass man die Daten insgesamt zwei mal einlesen müsste (1.
Prüfsumme generieren, 2. `brig stage`), was bei vielen und/oder großen Dateien
sehr ineffizient wäre.

Ein Kompromiss beispielsweise wäre anstatt der kompletten Prüfsumme über die
ganze Datei, nur die Prüfsumme über einen Teil (beispielsweise 1024Bytes vom
Anfang der Datei) der Datei zu machen und zusätzlich die Dateigröße mit in die
Berechnung des »Schlüssels« einfließen zu lassen. Dies hätte den Nachteil, dass
man auch viele Unterschiedliche Dateien mit dem gleichen Schlüssel
verschlüsseln würde, da mehrere unterschiedliche Dateien mit einer gewissen
Wahrscheinlichkeit fälschlicherweise die gleiche »Prüfsumme« generieren würden.

Ein weiteres Problem der *Convergent Encryption* ist, dass dieses Verfahren für
den »confirmation of a file«--Angriff anfällig ist. Das heißt, dass es einem
Angreifer möglich ist durch das Verschlüsseln eigener Dateien darauf zu
schließen was beispielsweise ein anderer Benutzer in seinem Repository
gespeichert hat.

## Keymanagement {#sec:keymanagement}

### Sicherung und Bindung der kryptographischen Schlüssel an eine Identität 

Das asymmetrische Schlüsselpaar von *IPFS* ist standardmäßig in keinster Weise
gesichert und muss daher besonders geschützt werden, da diese die Identität
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
Passwortschutz dieses Schlüsselpaars ein absolutes Minimalkriterium. Weiterhin
könnte »brig« den Ansatz fahren und die kryptographischen Schlüssel
(`config`--Datei von *IPFS*) selbst nur »on demand« im Speicher beispielsweise
über ein *VFS* (Virtual Filesystem) *IPFS* bereitstellen. [@fig:img-vfs] zeigt
ein Konzept bei welchem »brig« über einen *VFS*--Adapter die
Konfigurationsdateien und somit auch die kryptographischen Schlüssel *IPFS*
bereit stellt. 

![»brig« stellt mittels VFS eine Zugriffsschnittstelle für *IPFS* dar.](images/vfs.png){#fig:img-vfs width=60%}

Dabei wird beim Starten des »brig«--Daemon die verschlüsselte
Datei im Arbeitsspeicher entschlüsselt und anschließen *IPFS* über einen
Zugriffsadapter bereitgestellt. Dabei wird der komplette Zugriff über das *VFS*
von »brig« verwaltet. 

### GNUPG als Basis für »externe Identität«

*GnuPG* ist eine freie Implementierung vom OpenPGP--Standard
(RFC4880[^FN_RFC4880]). Die Implementierung ist heutzutage auf den gängigen
Plattformen (Windows, MacOS, Linux, *BSD) vorhanden. Die Implementierung für
Windows (*Gpg4win*[^FN_GPG4WIN]) wurde vom Bundesamt für Sicherheit in der
Informationstechnik in Auftrag gegeben. Neben den Einsatz der sicheren
E--Mail--Kommunikation, wird *GnuPG* heute unter vielen unixoiden
Betriebssystemen zur vertrauenswürdigen Paketverwaltung verwendet.
Distributionen wie beispielsweise *Debian*[^FN_DEBIAN_GPG],
*OpenSuse*[^FN_OPENSUSE_GPG], *Arch Linux*[^FN_ARCH_GPG] und weitere verwenden
*GnuPG* zum signieren von Paketen.

[^FN_GPG4WIN]: Gpg4win: <https://de.wikipedia.org/wiki/Gpg4win>
[^FN_ARCH_GPG]: Pacman/Package Signing: <https://wiki.archlinux.org/index.php/Pacman/Package_signing>
[^FN_DEBIAN_GPG]: Archive Signing Keys: <https://ftp-master.debian.org/keys.html>
[^FN_OPENSUSE_GPG]: RPM -- der Paket--Manager: <http://www.mpipks-dresden.mpg.de/~mueller/docs/suse10.3/opensuse-manual_de/manual/cha.rpm.html>
[^FN_GNUPG]: Internetpräsentation GnuPG: <www.gnupg.org>
[^FN_RFC4880]: RFC4880: <https://www.ietf.org/rfc/rfc4880.txt>

Eine weitere Maßnahme und »Best Practise« ist die sogenannte »Key Seperation«.
Obwohl es mit *GnuPG* möglich ist das selbe Schlüsselpaar zum Signieren und
Verschlüsseln zu nehmen ist dies aus sicherheitstechnischen Gründen nicht
empfehlenswert. Im Klartext heißt das, dass für unterschiedliche Einsatzzwecke
unterschiedliche Schlüssel verwendet werden sollen. Um dies zu realisieren
bietet *GnuPG* die Möglichkeit von sogenannten *Subkeys*.

*GnuPG* hat einen `gpg-agent`, welcher für das Management der vom Benutzer
eingegebenen Passphrase zuständig ist (gewisse Zeit Speichern, bei Bedarf
Abfragen). Weiterhin bietet der Agent seit Version 2.0.x die Möglichkeit auf
Smartcards zuzugreifen. Zusätzlich ist es seit Version 2 möglich GPG--Schlüssel
für die SSH--Authentifizierung zu verwenden.

Beim erstellen eines Schlüsselpaars mit *GPG* wird standardmäßig ein
Masterschlüssel (zum Signieren von Daten und Zertifizieren Subkeys) und ein
*Subkey* für das Verschlüsseln von Daten erstellt[^FN_DEBIAN_SUBKEY].

Der Vorteil von *Subkeys* ist, dass diese an einen bestimmten Einsatzzweck
gebunden sind und auch unabhängig vom eigentlich Master--Schlüsselpaar
widerrufen werden können --- was eine sehr wichtige Eigenschaft bei der
Verwaltung von Schlüsseln darstellt.

*GnuPG* bietet neben dem RFC4880--Standard die Möglichkeit den privaten
Master--Schlüssel »offline« zu speichern. Dieser sollte in der Regel so
konfiguriert sein, dass er lediglich zum Signieren/Zertifizieren und Anlegen
neuer Subkeys verwendet wird.

Eine weitere Empfehlung an dieser Stelle wäre es die *Subkeys* zusätzlich auf
eine *Smartcard* auszulagern (siehe [@sec:smartcard]).

[^FN_DEBIAN_SUBKEY]: Debian Wiki Subkeys: <https://wiki.debian.org/Subkeys>

## Authentifizierungskonzept

### Authentifizierungkonzept mit IPFS--Bordmitteln

Unter [birg-Auth] wurde die aktuelle Situation evaluiert. Zum aktuellen
Zeitpunkt hat »brig« keine Authentifizierungsmechanismus, der kommunizierenden
Parteien müssen im Grunde ihre »brig«--Fingerabdrücke gegenseitig validieren
und auf dieser Basis manuell Ihrer Liste mit Kommunikationspartnern hinzufügen.
Neben der Möglichkeit den Fingerabdruck über einen Seitenkanal (Telefonat,
E--Mail) auszutauschen, sollen nun benutzerfreundlichere Konzepte vorgestellt
werden.

Eine sinnvolle Erweiterung an dieser Stelle wäre die Einführung eines QR--Codes
welcher die Identität eines Kommunikationspartners eindeutig klassifiziert.
Beispielsweise auf Visitenkaten gedurckte QR--Codes lassen den Benutzer seinen
Synchronisationspartner mit wenig Aufwand über ein Smartphone--App
verifizieren. Bei Anwendung eines »Masterschlüssels«, welcher für das Signieren
der »brig«--ID verwendet werden kann --- wie unter [@sec:keymanagement]
vorgeschlagen --- würde der Datensatz zur Verifikation wie folgt aussehen:

* IPFS--ID: `QmbR6tDXRCgpRwWZhGG3qLfJMKrLcrgk2qv5BW7HNhCkpL`
* GPG--Key--ID (16Byte[^FN_EVIL32]): `D3B2 790F BAC0 7EAC`, wenn keine GPG--Key--ID
  existiert: `0000 0000 0000 0000`

und könnte beispielsweise in folgender Form auf untergebracht werden:

* `QmbR6tDXRCgpRwWZhGG3qLfJMKrLcrgk2qv5BW7HNhCkpL | D3B2790FBAC07EAC`

[@fig:img-qrcode] zeigt den definieren Datensatz als QR--Code.

![»brig« QR--Code um einen Synchronisationspatner auf einfache Art und Weise zu authentifizieren.](images/qrcode.png){#fig:img-qrcode width=30%}

[^FN_EVIL32]: Evil32. Check Your GPG Fingerprints: <https://evil32.com/>

Da *IPFS* bereits ein *Public/Private*--Schlüsselpaar mitbringt würde sich im
einfachste Falle nach dem ersten Verbindungsaufbau die Möglichkeit bieten den
sein Gegenüber anhand eines *Gemeinsamen Geheimnis* oder anhand eines
*Frage--Antwort--Dialogs* zu verifizieren. [@fig:img-question-answer] zeigt den
Ablauf einer Authentifizierung des Synchronisationspartners, welcher in Folgenden Schritten abläuft:

![Frage--Antwort--Authentifizierung. Alice stellt Bob eine Frage auf die nur er die Antwort wissen kann.](images/question-answer.png){#fig:img-question-answer width=95%}

1. Alice generiert eine zufällige Nonce, Frage und Antwort
2. Alice verschlüsselt Nonce + Antwort, signiert mit ihrem privaten Schlüssel
   und schickt sie an Bob
3. Bob prüft die Signatur, ist diese ungültig, wird abgebrochen, bei
   Gültigkeit entschlüsselt Bob die Nachricht
4. Bob inkrementiert die Nonce von Alice um eins und erstellt ein Antwortpaket
   bestehend aus Nonce, Frage und Antwort und schickt dieses an Alice
5. Alice prüft die Signatur, ist diese ungültig wird abgebrochen, bei
   Gültigkeit entschlüsselt Alice die Nachricht
6. Alice prüft ob Nonce um eins inkrementiert wurde, ob die Frage zur
   gestellten Frage passt und ob die Antwort die erwartete Antwort ist
7. Stimmen alle drei Parameter überein, dann wird Bob von Alice als
   vertrauenswürdig eingestuft und kann somit Bobs ID als vertrauenswürdig
   hinterlegen
8. Um Alice gegenüber Bob zu verifizieren, muss das Protokoll von Bob aus
   initialisiert werden

Eine weitere Möglichkeit wäre auch wie beim OTR--Plugin des
*Pidgin*--Messengers das Teilen eines gemeinsamen Geheimnisses.
[@fig:img-shared-secret] zeigt den Ablauf der Authentifizierungsphase bei der
Nutzung eines gemeinsamen Geheimnisses.

![Authentifizierung über ein gemeinsames Geheimnis.](images/shared-secret.png){#fig:img-shared-secret width=95%}

1. Alice und Bob generieren jeweils eine zufälligen Nonce (NA und NB)
2. NA und NB werden mit dem Public Key des Gegenübers verschlüsselt,
   signiert und an den Kommunikationspartner versendet
3. Die Kommunikationspartner validieren die Signatur und entschlüsseln jeweils die erhaltene Nonce N(A|B)
4. Die Kommunikationspartner inkrementieren die erhaltene Nonce fügen eine
   Prüfsumme ihres gemeinsamen geglaubten Geheimnisses hinzu, verschlüsseln,
   signieren und versenden diese an den Kommunikationspartner
5. Alice und Bob erhalten die inkrementierte Nonce und Prüfsumme (in
   verschlüsselter Form) des gemeinsam geglaubten Geheimnisses des Gegenübers
   Beide prüfen wieder die Signatur, entschlüsseln das Paket und Prüfen ob die
   Nonce inkrementiert wurde und ob die Prüfsumme ihres Geheimnisses mit dem des
   Gegenübers übereinstimmt
6. Bei gültiger Nonce und Prüfsumme sind beide Kommunikationspartner
   Gegenseitig authentifiziert und können Ihren Kommunikationspartner jeweils als
   vertrauenswürdig einstufen

Bei beiden Abläufen wurde jeweils ein zufällige Nonce verschlüsselt und
signiert versendet. Dies soll in beiden Fällen das Abgreifen der Nonce
verhindern und die bisherige Quelle Authentifizieren. Würde man an dieser
stelle die Nonce weglassen, so wäre ein *Replay*--Angriff möglich.

TODO: Anforderungen an Authentifizierung validieren. 

### Authentifizierungkonzept auf Basis des Web--of--Trust

![Authentifizierung auf Basis des Web--Of--Trust.](images/web-of-trust.png){#fig:img-web-of-trust width=100%}

Eine weitere Möglichkeit einer Authentifizierung ist auf Basis des
*Web--of--trust*.  Dieses beschreibt einen typischen dezentralen PKI--Ansatz,
welcher mittels der aktuell mittels der GnuPG--Software umgesetzt wird.
*IPFS--ID* kann hierbei mit dem privaten Schlüssel signiert werden und über
»Web--of--trust--Overlay--Network« von den jeweiligen Benutzer validiert
werden. [@fig:img-web-of-trust] stellt das Konzept grafisch dar. 

Die Authentifizierung von Kommunikationspartnern ist für den Benutzer keine
triviale Aufgabe. Die in [@fig:img-web-of-trust] dargestellte Situation stellt
jedoch eine ideale Sichtweise des *Web--of--trust*--Vertrauensmodells dar. Das
Vertrauen zwischen den verschiedenen Parteien des *Web--of--trust* ist nicht
generell übertragbar, da es lediglich auf Empfehlungen einzelner Individuen
basiert (vgl. [@pgp-trust-model]). »A Probabilistic Trust Model for GnuPG«
stellt eine interessante wahrscheinlichkeitstheoretische Erweiterung des
klassischen Vertrauensmodells dar (vgl. [@gpg-probabilistic]).

**Kurze Erläuterung:**

1. Alice und Bob sie Teilnehmer des *Web--of--trust*, ihre öffentlichen Schlüssel
   sind von weiteren Personen (Freunden) signiert.
2. Alice und Bob signieren ihre *IPFS--ID* vor dem Austausch mit dem jeweiligen
   Synchronisationspartner
3. Alice und Bob beschaffen sich den öffentlichen Schlüssel des
   Synchronisationspartners aus dem *Web--of--trust* um die Signatur der *IPFS--ID* damit zu prüfen
4. Da die öffentlichen Schlüssel der jeweiligen Parteien von bereits anderen
   vertrauenswürdigen Parteien unterschrieben sind, akzeptieren beide
   Synchronisationspartner die Signatur und somit die *IPFS--ID*

Dieses Konzept ist um so vertrauenswürdiger, je mehr vertrauenswürdige Parteien
einen öffentlichen Schlüssel unterschreiben. Durch zusätzlichen Instanzen wie
beispielsweise die Zertifizierungsstelle CAcert[^FN_CACERT] und die *c't*
Krypto--Kampagne[^FN_CTCRYPTO], kann das Vertrauen in die Identität einer Partei
weiter erhöht werden.

Wissenschaftliche Untersuchen haben weiterhin ergeben das ein großteil der
Web--of--trust Teilnehmer zum sogenanntem *Strong Set* gehören. Diese Teilmenge
repräsentiert Benutzer/Schlüssel welche durch gegenseitige Bestätigung
vollständig mit einander verbunden sind. Projekte wie die c't Krypto--Kampagne
oder auch das *Debian*--Projekt sollen hierzu einen deutlichen Beitrag
geleistet haben (vgl. [@wot1], [@wot2]).

[^FN_CACERT]: CAcert: <https://de.wikipedia.org/wiki/CAcert>
[^FN_CTCRYPTO]: Krypto-Kampagne: <https://www.heise.de/security/dienste/Krypto-Kampagne-2111.html>

## Smartcards und RSA--Token als 2F--Authentifizierung {#sec:smartcard}

Wie bereits erwähnt, ist die Authentifizierung über ein Passwort oft der
Schwachpunkt eines zu sichernden Systems. Ist das Passwort oder die
Passwort--Richtlinien zu komplex, so neigen Benutzer oft dazu dieses
aufzuschreiben. Ist die Komplexität beziehungsweise Entropie zu niedrig so ist
es mit modernen Methoden vergleichsweise einfach das Passwort »berechnen«.

Ein weiterer Schwachpunkt der oft ausgenutzt wird ist die »unsichere«
Speicherung von kryptographischen Schlüsseln. Passwörter sowie kryptographische
Schlüssel können bei handelsüblichen Endanwendersystemen wie beispielsweise PC
oder Smartphone relativ einfach mitgeloggt beziehungswiese entwendet werden
können. Neben dem *FreeBSD*--Projekt welches dem Diebstahl von
kryptographischen Schlüsseln zum Opfer fiel[^FN_FREEBSD_SSH_MALWARE] gibt es
laut Berichten[^FN_SSH_MALWARE][^FN_PRIV_KEY_MALWARE] zunehmend Schadsoftware
welcher explizit für diesen Einsatzzweck konzipiert wurde.

[^FN_FREEBSD_SSH_MALWARE]:Hackers break into FreeBSD with stolen SSH key: <http://www.theregister.co.uk/2012/11/20/freebsd_breach/>
[^FN_SSH_MALWARE]:Malware & Hackers Collect SSH Keys to Spread Attacks: <https://www.ssh.com/malware/>
[^FN_PRIV_KEY_MALWARE]:Are Your Private Keys and Digital Certificates a Risk to You?: <https://www.venafi.com/blog/are-your-private-keys-and-digital-certificates-a-risk-to-you>

Um hier die Sicherheit zu steigern wird von Sicherheitsexperten oft zur
zwei--Faktor--Authentifizierung beziehungsweise zur hardwarebasierten
Speicherung kryptographischer Schlüssel (persönliche Identität beziehungswiese
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
*Yubico*[^FN_YUBICO] (siehe [@fig:img-yubikey]) und *Nitrokey*[^FN_NITROKEY]. Diese Hardware--Token haben
zudem den Vorteil, dass sie die Funktionalität einer Smartcard und eines
Hardware--Token für Zwei--Faktor--Authentifizierung vereinen.

![YubKey Neo mit USB--Kontaktschnittstelle und »Push--Button«, welcher auf Berühung reagiert.](images/yubikeyneo.png){#fig:img-yubikey width=35%}

Der besondere bei diesen Hardware--Komponenten ist, dass sie sich über die
USB--Schnittstelle als HID (Human--Interface--Device) ausgeben und somit keine
weitere Zusatzhardware wie beispielsweise ein Lesegerät benötigt wird.

[^FN_NITROKEY]: Nitrokey: <https://www.nitrokey.com/>
[^FN_YUBICO]: Yubico: <https://www.yubico.com>

Bei beiden Herstellern gibt es die Hardware--Token in verschiedenen
Ausführungen. Bekannte Institutionen welche den *YubiKey* verwenden ist
beispielsweise die Universität von Auckland[^FN_YK_UNIVERSITY_AUCKLAND], das
*CERN*[^FN_YK_CERN] oder auch das [^FN_YK_MIT].

[^FN_YK_UNIVERSITY_AUCKLAND]: Auckland University YubiKey--Benutzeranweisung: <https://www.auckland.ac.nz/en/about/the-university/how-university-works/policy-and-administration/computing/use/twostepverification.html>
[^FN_YK_MIT]: Massachusetts Institute of Technology YubiKey--Benutzeranweisung: <https://security.web.cern.ch/security/recommendations/en/2FA.shtml>
[^FN_YK_CERN]: CERN YubiKey--Benutzeranweisung: <http://kb.mit.edu/confluence/pages/viewpage.action?pageId=151109106>

Für die Entwicklung von »brig« wurden *Yubico Neo*--Hardware--Token ---
aufgrund der Umfangreichen Programmier--API --- des Herstellers *Yubico*
beschafft. Alle weiteren Ausführungen und Demonstrationen beziehen sich auf
dieses Modell.

### Yubikey--NEO Einleitung

[^FN_YUBIKEY_PNG]: Bild--Quelle: <https://hao0uteruy2io8071pzyqz13-wpengine.netdna-ssl.com/wp-content/uploads/2015/04/YubiKey-NEO-1000-2016-444x444.png>

Der *Yubikey Neo* hat folgende Funktionalitäten beziehugnsweise Eigenschaften:

* Yubico OTP, One--Time--Password--Verfahren des Herstellers. Standardmäßig
  kann jeder YubiKey gegen die YubiCloud--Authentifizierungdienst mittels OTP
  authentifiziert werden
* OATH–Kompitabilität (HMAC--Based--OTP-- und Time--Based--OTP--Verfahren, für weitere Details vgl. [@oath])
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

### Yubico OTP Zwei--Faktor--Authentifizierung

Der YubiKey ist im Auslieferungszustand so konfiguriert dass er sich gegenüber
der YubiCloud mittels Yubico OTP authentifizieren kann. [@fig:img-otp-details]
zeigt den Ablauf des Authentifizierungsprozesses. Das One--Time--Passwort ist
insgesamt 44 Zeichen lang und besteht dabei aus zwei Teilkomponenten. Die
ersten 12 Zeichen repräsentieren eine statische öffentliche *ID* mit welcher
sich die YubiKey Hardware identifizieren lässt. Die verbleibenden Zeichen
repräsentieren das dynamisch generierten Teil des One--Time--Passwort. Der
dynamische Teil besteht aus mehreren verschiedenen Einzelkomponenten die
beispielsweise eine zufällige Nonce, Sitzungsschlüssel und Zähler beinhalten.
Weiterhin fließt ein AES--Schlüssel in die Generierung des One--Time--Password
ein, es ist für einen Angreifer somit nicht möglich die eigentlichen Daten
auszuwerten.

![Yubico OTP[^FN_YUBICO_OTP]](images/otp-details.png){#fig:img-otp-details width=65%}

Das One--Time--Password ist nur ein Mal gültig. Zur Validierung werden am
Server Sitzung und Zähler jeweils mit den zuvor gespeicherten Daten überprüft.
Stimmen diese nicht --- da beispielsweise der aktuelle Zähler kleiner ist als
der zuletzt gespeicherte --- so wird das One--Time--Password nicht akzeptiert.

[^FN_YUBICO_OTP]: OTPs Explained: <https://developers.yubico.com/OTP/OTPs_Explained.html>

Für das Testen der korrekten Funktionalität stellt *Yubico* eine Demoseite für
*OTP*[^FN_YUBICO_DEMO_OTP] und *U2F*[^FN_YUBICO_DEMO_U2F] bereit. Über diese
lässt sich ein One--Time--Password an die YubiCloud schicken und somit die
korrekte Funktionsweise eines *YubiKey* validieren. [@fig:img-otp-response]
zeigt die Authentifizierungsantwort der *YubiCloud*.

![YubiCloud Response bei Zwei--Faktor--Authentifizierung. Seriennummer des YubiKeys wurde retuschiert.](images/response-noserial.png){#fig:img-otp-response width=65%}

Die Demoseite bietet hier neben dem einfachen Authentifizierungstest, bei
welchem nur das One--Time--Passwort validiert wird, auch noch die Möglichkeit
einen Zwei--Faktor--Authentifizierungstest und einen
Zwei--Faktor--Authentifizierungstest mit Passwort durchführen.

[^FN_YUBICO_DEMO_OTP]: Yubico OTP--Demopage: <https://demo.yubico.com>
[^FN_YUBICO_DEMO_U2F]: Yubico U2F--Demopage: <https://demo.yubico.com/u2f>

### Konzept Zwei--Faktor--Authentifizierung von »brig« mit YubiCloud

Für die Proof--of--concept Implementierung der Zwei--Faktor--Authentifizierung
wird die *yubigo*--Bibliothek[^FN_YUBIGO] verwendet.

[^FN_YUBIGO]: Yubigo Dokumentation: <https://godoc.org/github.com/GeertJohan/yubigo>

besteht aus einer *Client--ID*, welche beispielsweise die Applikation repräsentieren
Für den Einsatz unter »brig« wird ein *API*--Key von *Yubico* benötigt. Diese
kann und einem *Secret--Key* über welchen der Anwendung genehmigt wird den
Dienst zu verwenden. Die Beantragung erfolgt online[^FN_APIKEY] und erfordert
einen YubiKey.

[^FN_APIKEY]: Yubico API--Key beantragen: <https://upgrade.yubico.com/getapikey/>

Das folgende minimale Implementierung zeigt eine voll funktionsfähigen
Authentifizierung eine *Yubikey* am *YubiCloud*--Service.

![Schematische Darstellung der Zwei--Faktor--Authentifizierung gegenüber einem »brig«--Repository.](images/poc-2fa-auth.png){#fig:img-poc-brig-2fa width=85%}

[@fig:img-poc-brig-2fa] zeigt schematisch den Zwei--Faktor--Authentifizierung
mit einem *YubiKey* über die *YubiCloud*. Um auf das »brig«--Repository Zugriff
zu erhalten müssen folgende Informationen validiert werden:

1. »brig« prüft das Passwort von Alice
2. »brig« prüft anhand der *Public--ID* ob der *YubiKey* von Alice dem Repository bekannt ist
3. »brig« lässt das One--Time--Passwort des *YubiKey* von der *YubiCloud* validieren

Eine essentiell wichtige Komponente an dieser Stelle ist der Zusammenhang
zwischen dem Repository und dem *YubiKey*. Der *YubiKey* muss beim
Initialisieren dem System genauso wie das Passwort bekannt gemacht werden.

Dies kann bei der Initialisierung durch ein One--Time--Password gegenüber
»brig« gemacht werden.

Bei der Implementierung des Hardwaretokens als zweiten Faktor, ist es wichtig
darauf zu achten, dass die *Public--ID* des *YubiKey* »brig« bekannt ist. Passiert dies
nicht, so könnte sich jeder Benutzer mit einem gültigen *YubiKey* gegenüber
»brig« authentifizieren. 

~~~go
const (
	// Passwort und Yubikey (zweites Token) welches gegenüber
	// »brig« registriert ist
	YubiKeyPublicID = "ccccccababab"
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
	fmt.Printf("YubiKey known by brig? : %s\n", answer(otp[0:12] == YubiKeyPublicID))
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

##### Konzept mit eigener Serverinfrastruktur

Neben der Möglichkeit das *YubiKey* One--Time--Password gegen die *YubiCloud*
validieren zu lassen gibt es auch die Möglichkeit eine eigene Infrastruktur für
die Validierung bereit zu stellen[^FN_YUBICO_VAL_SERVER].

[^FN_YUBICO_VAL_SERVER]:YubiCloud Validation Servers: <https://developers.yubico.com/Software_Projects/Yubico_OTP/YubiCloud_Validation_Servers/>

Dies ist in erster Linie für Unternehmen interessant, das keine Abhängigkeit zu
einem externen Dienst besteht. Weiterhin bekommt das Unternehmen dadurch mehr
Kontrolle und kann den *YubiKey* feingranularer als Sicherheitstoken nicht nur
für »brig« sondern die gesamte Infrastruktur nutzen.

Als Vorbereitung hierfür muss der *YubiKey* mit einer neuen »Identität«
programmiert werden. Für die Programmierung wird das
Yubikey--Personalisation--Tool verwendet. Hier kann unter *Yubico OTP->Quick*
eine neue Identität »autogeneriert werden. Die hier erstellte *Public--ID*
sowie der *AES*--Schlüssel müssen anschließend dem Validierungsserver bekannt
gemacht werden. Für die Registrierung einer neuen »Identität« an der
*YubiCloud* stellt *Yubico* eine Seite[^FN_AESKEY_UPLOAD] bereit über welche
der *AES*--Schlüssel an die *Yubico* Validierungsserver geschickt werden kann.

[^FN_AESKEY_UPLOAD]: Yubico AES--Key--Upload: <https://upload.yubico.com/>

~~~sh
$ ./yubikey-server -app "brig"
app created, id: 1 key: Q0w7RkvWxL/lvCynBh+TYiuhZKg=

$ ./yubikey-server -name "Christoph" -pub "vvrfglutrrgk" -secret "619d71e138697797f7af68924e8ecd68"
creation of the key: OK

$ ./yubikey-server -s
2016/12/08 19:28:20 Listening on: 127.0.0.1:4242...

~~~

Der folgende Konsolenauszug zeigt die Validierung am lokalen
Validierungsserver. Für den Zugriff wird das Kommandozielen--Tool
*cURL*[^FN_CURL] verwendet.

[^FN_CURL]: cURL Homepage: <https://curl.haxx.se/>

~~~sh
# Validierung des YubiKey OTP
$ curl "http://localhost:4242/wsapi/2.0/verify \ 
  ?otp=vvrfglutrrgkkddjfnkjlitiuvfglnbkfghlnjvnkflj&id=1&nonce=test42"
nonce=test42 otp=vvrfglutrrgkkddjfnkjlitiuvfglnbkfghlnjvnkflj
name=Christoph
status=OK
t=2016-12-08T19:29:20+01:00
h=7DJyK6NZOIeCcs9lHcH+K8RFaYY=
~~~

Beim wiederholten einspielen des gleichen OTP verhält sich der eigene
Validierungsserver genauso wie die Yubicloud und meldet die erwartete 
Fehlermeldung `REPLAYED_OTP`. Weitere Response--Tests sind im Anhang X zu
finden.

~~~sh
# Widerholtes OTP
$ curl "http://localhost:4242/wsapi/2.0/verify \ 
  ?otp=vvrfglutrrgkkddjfnkjlitiuvfglnbkfghlnjvnkflj&id=1&nonce=test42"
nonce=test42
otp=vvrfglutrrgkkddjfnkjlitiuvfglnbkfghlnjvnkflj
name=
status=REPLAYED_OTP
t=2016-12-08T19:35:18+01:00
h=JqO407mZWS4Us/J/n2jCtbSnRFk=
~~~

Beim Betreiben eines eigenen Validierungsserver muss besonderen Wert auf die
Sicherheit dieses geachtet werden, da dieser die *AES*--Schlüssel der
registrierten *YubiKeys* enthält.

Es ist für Unternehmen empfehlenswert den Validierungsserver nicht direkt am
Netz, sondern über einen Reverse--Proxy zu betreiben.
[@fig:img-reverseproxy-auth] zeigt den Ansatz. Alle an One--Time--Passwöter
werden über einen »normalen« Webserver entgegengenommen und an den
*YubiKey*--Validierungsserver weitergeleitet. Der Vorteil an dieser stellte

* HTTPS
* Besseres Patchmanagement.
* Debian--Validierungsserver Buggy.

Letsencrypt für gemeinnützige Organisationen. Zertifikate für Unternehmen.

### Yubikey als Smartcard
* Speicherung von Schlüsseln auf YubiKey möglich? Wie?

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
