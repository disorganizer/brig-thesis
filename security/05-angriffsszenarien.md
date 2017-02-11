# Sicherheit und Angriffsszenarien {#sec:SEC05_SICHERHEIT_UND_ANGRIFFSSZENARIEN}

>> *Security is a process, not a product.*
                         --- Bruce Schneier

## Beurteilung von Sicherheit {#sec:SEC05_BEURTEILUNG_VON_SICHERHEIT}

Wie bereits in der Einleitung von [@sec:SEC04_EINLEITUNG] erwähnt, ist das
Entwickeln von sicherer Software kein trivialer Prozess. Auch Systeme, die von
Experten entwickelt wurden, können gravierende Sicherheitsmängel aufweisen.

Ein wichtiger Punkt, welcher von Experten oft geraten wird, ist die Verwendung
bekannter und bewährter Algorithmen und Protokolle wie beispielsweise AES,
RSA/DSA, TLS et cetera. Die Entwicklung neuer kryptographischer Algorithmen und
Protokolle sollte nach Möglichkeit vermieden werden. Weiterhin werden Details von
kryptographischen Elementen oftmals missverstanden oder es werden für den
Einsatz von Sicherheit die falschen Techniken eingesetzt. Beispiele hierfür
wären (vgl. [@evertythin1hour]):

* Google Keyczar (timing side channel)[^FN_KEYCZAR_BUG]
* SSL (session renegotiation)[^FN_SSL_BUG]
* Amazon AWS signature method (non-collision-free signing)[^FN_AMAZON_AWS_BUG]
* Flickr API signatures (hash length-extension)[^FN_FLICKR_VUL]
* Intel HyperThreading (architectural side channel)[^FN_INTEL_VUL]


[^FN_KEYCZAR_BUG]: Keyczar Vulnerability: <https://rdist.root.org/2009/05/28/timing-attack-in-google-keyczar-library/>

[^FN_SSL_BUG]: SSL Vulnerability: <https://blog.ivanristic.com/2009/11/ssl-and-tls-authentication-gap-vulnerability-discovered.html>

[^FN_AMAZON_AWS_BUG]: AWS Signature Vulnerability: <https://rdist.root.org/2009/05/20/amazon-web-services-signature-vulnerability/>

[^FN_FLICKR_VUL]: Flickr Signature Vulnerability: <http://netifera.com/research/flickr_api_signature_forgery.pdf>

[^FN_INTEL_VUL]:Intel HyperThreading Vulnerability: <http://www.daemonology.net/hyperthreading-considered-harmful/>

Erschwert kommt bei der Auswahl kryptographischer Algorithmen/Protokolle hinzu,
dass sich Experten nicht immer einig sind oder es kommt erschwerend hinzu, dass
es nicht für jeden Anwendungsfall eine konkrete Empfehlung geben kann. Manchmal
muss auch zwischen Sicherheit und Geschwindigkeit abgewogen werden. Ein
Beispiel hierfür wäre die Abwägung ob man Betriebsmodi verwendet, die
Authentifikation und Verschlüsselung unterstützen, wie beispielsweise GCM, oder
doch besser eine »Encrypt--than--MAC«--Komposition (vgl. auch [@encryptthanmac]). Weiterhin macht die Kryptoanalyse Fortschritte und kommt beispielsweise zu neuen Erkenntnissen[^FN_PRIME_BACKDOOR], dass Primzahlen Hintertüren enthalten können.

[^FN_PRIME_BACKDOOR]: Cryptanalysis of 1024-bit trapdoored primes: <http://caramba.inria.fr/hsnfs1024.html>

Ein weiteres Beispiel welches die Komplexität der Lage darstellt, ist eine
aktuelle Warnung vom BSI[^FN_BSI_NORTON] bei welcher »Sicherheitssoftware«
aufgrund von gravierenden Sicherheitslücken als Einfallstor für Schadsoftware
missbraucht werden kann.

[^FN_BSI_NORTON]:  BSI Warn-- und Informationsdienste: <https://www.cert-bund.de/advisoryshort/CB-K16-1797>

Weiterhin macht es keinen Sinn und ist auch oft wirtschaftlich untragbar alle
finanziellen Mittel in die Sicherheit eines Softwareproduktes zu investieren.
Laut [@martin2012everyday], S. 10 f. ist es in der Regel eine Abwägung zwischen möglichen
Risikofaktoren und finanziellem sowie zeitlichem Aufwand. Es macht so gesehen
keinen Sinn, mehrere Millionen Euro in ein Softwareprodukt zu investieren,
welches beispielsweise nur Daten im Wert von ein paar tausend Euro schützt.
Weiterhin ist es auch wichtig »realistische« Gefahren zu identifizieren und
nicht unnötig Ressourcen in sicherheitstechnische Details zu investieren.

## Angriffsfläche bei »brig« {#sec:SEC05_ANGRIFFSFLAECHE_BEI_BRIG}

### Allgemein

Ziel dieser Arbeit ist es praxisrelevante Gefahren/Risiken für ein
Software--Produkt und einen Entwicklungsprozess wie er bei »brig« vorliegt zu
definieren und mögliche Verbesserungskonzepte zu erarbeiten.

Hierbei wird in erster Linie angenommen, dass die meisten Sicherheitsprobleme durch
Benutzerfehler oder durch mangelnde Kenntnis/Sicherheitsvorkehrungen zustande
kommen. Primär spielen in der Arbeit praxisorientierte Ansätze eine wichtige
Rolle, theoretische Sicherheitsmängel sind diesen untergeordnet und werden, auf
Grund der hohen Komplexität der Thematik, nur am Rande behandelt.

Zu den theoretischen Problemen gehören im Umfeld dezentraler Softwaresysteme
primär Angriffe wie beispielsweise die Sybil--Attacke, bei welcher es für einen
Angreifer möglich ist, mit einer großen Anzahl von Pseudonymen einen
überproportional großen Einfluss in einem dezentralen Netzwerk zu erlangen.
Möglichkeiten, die diesen Angriff entgegenwirken sind in erster Linie zentrale
Authentifizierungsinstanzen. Der Angriff wird unter [@peer2peer], S. 200 ff. genauer
erläutert. Das von »brig« verwendete IPFS--Netzwerk verwendet Teile des
S/Kademlia--Protokolls, welches es prinzipiell erschwert eine
Sybil--Attacke[^FN_IPFS_SYBIL_ATTACK] durchzuführen. Unter [@BIB_SKADEMLIA]
wird S/Kademlia bezüglich der Angriffe auf dezentrale Architekturen
genauer untersucht.

[^FN_IPFS_SYBIL_ATTACK]: IPFS -- Content Addressed, Versioned, P2P File System:

	<https://blog.acolyer.org/2015/10/05/ipfs-content-addressed-versioned-p2p-file-system/>

### Praxisorientierte Herausforderungen an die Software

Zu den praxisorientierten Problemen bei der Entwicklung einer Software wie
»brig« gehören in erster Linie folgende Punkte, auf welche primär in der Arbeit
eingegangen wird:

**Passwortmanagement:** Menschen sind schlecht darin, gute Passwörter zu
vergeben. Erweiterte Technologien ermöglichen es, immer schneller gestohlene
Passwörter--Datenbanken zu knacken und in Systeme einzubrechen. *Bruce
Schneier* und *Dan Goodin* beschreiben in ihren Artikeln »A Really Good Article
on How Easy it Is to Crack Passwords«[^FN_BRUCE_PW] und »Why passwords have
never been weaker --- and crackers have never been stronger«[^FN_CRACKHARDWARE]
die Problematik detaillierter und geben Empfehlungen. Für weitere Details siehe
auch @sec:SEC07_REPOSITORY_ZUGRIFF.

[^FN_BRUCE_PW]: A Really Good Article on How Easy it Is to Crack Passwords:

	<https://www.schneier.com/blog/archives/2013/06/a_really_good_a.html>

[^FN_CRACKHARDWARE]: Why passwords have never been weaker --- and crackers have never been stronger:

	<http://arstechnica.com/security/2012/08/passwords-under-assault/>

**Schlüsselmanagement:** Die sichere Kommunikation von kryptographischen
Schlüsseln stellt eines der größten Probleme im digitalen Zeitalter dar.
(@martin2012everyday, S. 326 ff.). In jüngster Vergangenheit wurde
beispielsweise beim FreeBSD--Projekt mittels gestohlener kryptographischer
Schlüssel eingebrochen[^FN_FREEBSD_SSH_MALWARE]. Laut
Berichten[^FN_SSH_MALWARE][^FN_PRIV_KEY_MALWARE][^FN_PRIV_KEY_MALWARE_2]
expandiert der Malware--Markt in dieser Richtung, es wird zunehmend Malware für
das Ausspähen kryptographischer Schlüssel entwickelt.

[^FN_FREEBSD_SSH_MALWARE]: Hackers break into FreeBSD with stolen SSH key: <http://www.theregister.co.uk/2012/11/20/freebsd_breach/>
[^FN_SSH_MALWARE]: Malware & Hackers Collect SSH Keys to Spread Attacks: <https://www.ssh.com/malware/>
[^FN_PRIV_KEY_MALWARE]: Are Your Private Keys and Digital Certificates a Risk to You?:

	<https://www.venafi.com/blog/are-your-private-keys-and-digital-certificates-a-risk-to-you>

[^FN_PRIV_KEY_MALWARE_2]: Active attacks using stolen SSH keys:

	<https://isc.sans.edu/forums/diary/Active+attacks+using+stolen+SSH+keys+UPDATED/4937/>

**Authentifizierung:** Wie weiss der Benutzer, dass sein Kommunikationspartner
der ist für den er sich ausgibt? Hier sollen mögliche Konzepte erarbeitet
werden, um Angriffe durch »fremde« Kommunikationspartner identifizieren zu können.

**Softwareverteilung:** Der Benutzer muss sicherstellen
können, dass die aus dem Internet bezogene Open--Source--Software keine Malware
ist. Weiterhin ist es wichtig, Software auf einem aktuellen Stand zu halten, um
bekannte Sicherheitslücken zu schließen.

**Entwicklungsumgebung bei Open--Source--Projekten:**  Wie können
Softwareentwickler das Risiko von unerwünschten Manipulationen am eigenen
Projekt minimieren? Wie sichern Softwareentwickler ihren »Arbeitsprozess« ab?
