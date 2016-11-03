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

## Authentifizierungskonzept mittels Yubikey

* Speicherung von Schlüsseln auf YubiKey möglich? Wie?

## Schlüssel--Hierarchie

* Master--Key auf Yubikey
* Subkeys für Daten, Sitzung, Repo?
* Backup--Keys für Hierarchie?
* Dateiverschlüsselung mittels Ableitung?

## Crypto--Layer Performance

* Benchmark mit AES--NI Port von GO
* Benchmark mit https://git.schwanenlied.me/yawning/chacha20
* https://calomel.org/aesni_ssl_performance.html
