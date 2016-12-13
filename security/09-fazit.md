# Fazit {#sec:SEC09_FAZIT}

## Zusammenfassung {#sec:SEC09_ZUSAMMENFASSUNG}

Wie bereits unter [@cpahl] erwähnt ist mit dem aktuellen »brig«--Stand eine
solide Basis für ein Synchronisationswerkzeug entstanden. 

Die übergreifende Anforderung an das Projekt, eine gute Balance zwischen
Sicherheit und Usability zu finden, kann noch nicht endgültig bewertet werden.
Auch wenn man bei der aktuellen Version weniger von einem Prototypen aus Anwendersicht sprechen kann, so wurden 



* Ungelöst: Convergent Encryption
* Benutzerfreundlichkeit?

## Selbstkritik {#sec:SEC09_SELBSTKRITIK}

* Ist *IPFS* gute Wahl?
* Keymanagement in IPFS besser aufgehoben?
* Validierung der aktuellen Konzepte durch weitere Experten
* Performance auf kleinen Systemen Untragbar  aes-128 bit algorithmen?  alternativen zu chacha.
* Aktuell auf RSA/DSA basierend auf ECC umsteigen?
https://www.nccgroup.trust/globalassets/newsroom/us/news/documents/2013/ritter_samuel_stamos_bh_2013_cryptopocalypse.pdf


## Offene Fragen {#sec:SEC09_OFFENE_FRAGEN}

* Yubikey mit PIV sinnvoll? <https://developers.yubico.com/PIV/Introduction/YubiKey_and_PIV.html>
* Protokolle wie https://github.com/stealth/opmsg sinnvoll?

* Weitere Algorithmen überdenken? * Verbesserungen vllt mit Assembler
optimierter Variante: <https://git.schwanenlied.me/yawning/chacha20>? 

RSA empfohlen dass DSA kompromitiert werden kann wenn schlechte
zufallszahlengenerator:
<https://www.heise.de/security/artikel/Digitale-Signaturen-und-Zertifikate-270982.html>

## Auffälligkeiten 

* GPG: Passphrase 1234567890 sicher?
* yubikey private gpg schlüssel werden gecached?
* Dropbox-Library--Passwort--Problem?

