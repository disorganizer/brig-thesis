# Sicherheit und Angriffsszenarien

## Beurteilung von Sicherheit

Wie bereits in der Einleitung von [@sec:CAP_CRYPTOGRAPHY] erwähnt ist das
Entwickeln von »sicherer« Software kein trivialer Prozess. Auch Systeme die von
Experten entwickelt wurden, können gravierende Sicherheitsmängel aufweisen.

Ein wichtiger Punkt, welcher von Experten oft geraten wird, ist die Verwendung
bekannter und »bewährter« Algorithmen und Protokolle wie beispielsweise AES,
RSA/DSA, TLS et cetera. Die Entwicklung neuer kryptographischer Algorithmen und
Protokolle sollte vermieden werden. Weiterhin werden kryptographische Elemente oftmals missverstanden oder es werden für den Einsatz von Sicherheit die falschen Werkzeuge eingesetzt. Beispiele hierfür wären (vlg. [@evertythin1hour]):

* Google Keyczar (timing side channel)[^FN_KEYCZAR_BUG]
* SSL (session renegotiation)[^FN_SSL_BUG]
* Amazon AWS signature method (non-collision-free signing)[^FN_AMAZON_AWS_BUG]
* Flickr API signatures (hash length-extension)[^FN_FLICKR_VUL]
* Intel HyperThreading (architectural side channel)[^FN_INTEL_VUL]

[^FN_KEYCZAR_BUG]: <https://rdist.root.org/2009/05/28/timing-attack-in-google-keyczar-library/>
[^FN_SSL_BUG]: <https://blog.ivanristic.com/2009/11/ssl-and-tls-authentication-gap-vulnerability-discovered.html>
[^FN_AMAZON_AWS_BUG]: <https://rdist.root.org/2009/05/20/amazon-web-services-signature-vulnerability/>
[^FN_FLICKR_VUL]: <http://netifera.com/research/flickr_api_signature_forgery.pdf>
[^FN_INTEL_VUL]: <http://www.daemonology.net/hyperthreading-considered-harmful/>

Erschwert kommt bei der Auswahl kryptographischer Algorithmen/Protokolle hinzu,
dass sich Experten nicht immer einig sind oder es kommt erschwerend hinzu dass
es nicht für jeden Anwendungsfall eine konkrete Empfehlung geben kann. Manchmal
muss auch zwischen Sicherheit und Geschwindigkeit abgewogen werden. Ein
Beispiel hierfür wäre die Abwägung ob man Betriebsmodi verwendet die
Authentifikation und Verschlüsselung unterstützen wie beispielsweise *GCM* oder
doch besser eine »Encrypt--than--MAC«--Komposition (vgl auch [@encryptthanmac]).

## Sicherheit--Aufwand--Abwägung

Weiterhin macht es keinen Sinn und ist auch oft wirtschaftlich untragbar alle
finanziellen Mittel in die Sicherheit eines Softwareproduktes zu investieren.
Laut [@martin2012everyday] ist es in der Regel eine Abwägung zwischen möglichen
Risikofaktoren und finanziellem und zeitlichen Aufwand. Es macht so gesehen
keinen Sinn mehrere Millionen Euro in ein Softwareprodukt zu investieren,
welches beispielsweise nur Daten im Wert von ein paar tausend Euro schützt.

Weiterhin ist es auch wichtig »realistische« Gefahren zu identifizieren und
nicht unnötig Ressourcen in sicherheitstechnische Details zu investieren.
