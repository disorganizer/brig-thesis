# Fazit {#sec:SEC09_FAZIT}

## Zusammenfassung {#sec:SEC09_ZUSAMMENFASSUNG}

### Allgemein

Wie bereits unter [@cpahl], S. 104 erwähnt, ist mit dem aktuellen Stand von »brig« eine
solide Basis für ein sicheres und dezentrales Synchronisationswerkzeug entstanden.

Die übergreifende Anforderung an das Projekt, eine gute Balance zwischen
Sicherheit und Usability zu finden, kann noch nicht endgültig bewertet werden.
Die bisher getroffenen Entscheidungen bezüglich *IPFS* können durchaus positiv
bewertet werden, siehe @sec:SEC06_ZUSAMMENFASSUNG_IPFS_EVALUATION. Die
Datenhaltungsschicht bietet aufgrund des Merkle--DAG eine solide Basis mit
Fehlererkennung, die Netzwerkschicht auf CAN--Basis setzt den dezentralen
Ansatz von »brig« gut um. Die aktuell von »brig« umgesetzten Erweiterungen
machen aus dem *IPFS*--Unterbau eine sichere und vollständig dezentrale
Synchronisationslösung. Weiterhin wurden durch die Evaluation Fehler behoben
und Verbesserungen für die bisherige Implementierung identifiziert (siehe
@sec:SEC08_VERBESSERUNGEN_UND_ERWEITERUNGEN).

### Schlüsselverwaltung

Die erweiterte Evaluation von *IPFS* hat ergeben, dass die *IPFS*--Identität
(privater Schlüssel) im Klartext in der Konfigurationsdatei gespeichert wird
(siehe @sec:SEC06_IPFS_ID). Zukünftige Versionen von »brig« müssen diesen
kryptographischen Schlüssel sichern. Hier wurde ein mögliches Konzept für einen
transparenten verschlüsselten Zugriff auf Basis des *Virual Filesystem (VFS)*
vorgestellt (siehe @sec:SEC08_SICHERUNG_UND_BINDUNG_DER_KRYPTOGRAPHISCHEN_SCHLUESSEL_AN_EINE_IDENTITAET).

Um die *IPFS*--Identität zu sichern und die zukünftige Schlüsselverwaltung von
*IPFS* unabhängiger zu machen, wurde als Konzept eine »externe Identität«
eingeführt
(@sec:SEC08_SICHERUNG_UND_BINDUNG_DER_KRYPTOGRAPHISCHEN_SCHLUESSEL_AN_EINE_IDENTITAET).
Das Konzept mit dem Hauptschlüssel (externe Identität auf Basis eines
Public--Key--Schlüsselpaar) gibt »brig« auch bei zukünftigen Veränderungen an
der *IPFS*-Schlüsselverwaltung die Kontrolle über diese. Weiterhin wurde auf
der Basis dieser Identität ein erweitertes Authentifizierungskonzept
vorgestellt (siehe
@sec:SEC08_AUTHENTIFIZIERUNGSKONZEPT_AUF_BASIS_DES_WEB_OF_TRUST).

Die Kontrolle über die Identität ermöglicht eine feingranulare Kontrolle der
verwendeten kryptographischen Schlüssel. Dies ermöglicht eine Sicherung der
kryptographischen Schlüssel, beispielsweise auf einer Smartcard (siehe
@sec:SEC08_KRYPTOGRAPHISCHE_SCHLUESSEL_AUF_YUBIKEY_UEBERTRAGEN). 

Die Thematik der externen Identität wurde weiterhin auf Basis von *GnuPG*
anhand unterschiedlicher Konzepte und Möglichkeiten im Detail erläutert. Für
mögliche Probleme bei der Verwaltung des Schlüsselpaars wurden verschiedene
Lösungen evaluiert. Zusammengefasst stellt der Ansatz auf Basis der externen
Identität einen hohen Sicherheitszugewinn dar.

### Verschlüsselung

Die Sicherheitsentscheidungen, welche bisher für »brig« getroffen wurden, sind
größtenteils positiv zu bewerten. Die Datenverschlüsselungsschicht bietet
aktuell zwar mit der vorhanden *IPFS*--Transportlayerverschlüsselungsschicht
einen gewissen Overhead, befindet sich mit standardisierten Verfahren
(AES--GCM, ChaCha20/Poly1305) aber auf der sicheren Seite. 

Die Implementierung einer modularen Verschlüsselungsschicht macht den
Algorithmus leichter austauschbar. Die bisher gewählte Blockgröße der
Verschlüsselungsschicht könnte noch teilweise optimiert werden. Die bisherigen
Annahmen zur Algorithmuswahl konnten jedoch mit der Performance--Evaluation gut
bestätigt werden. Systeme ohne kryptographischer Befehlssatzerweiterung
profitieren vom *ChaCha20/Poly1305* (siehe @sec:SEC07_BENCHMARKS). Ab *Go v1.6*
profitieren Systeme mit kryptographischen Befehlserweiterungssatz stark
von den *AES--NI*--Optimierungen. Schwächere Systeme wie der *Raspberry Pi
Zero* haben trotz des recht performanten *ChaCha20/Poly1305*--Verfahrens eine
relativ schlechte Schreib-- und Lesegeschwindigkeit. Hier bedarf es noch
einiger Optimierungen.

### Authentifizierung

Die aktuelle Implementierung über die *zxcvbn*--Bibliothek setzt eine robuste
Passwortvalidierung um. Das Problem hierbei ist die schlechte Usability,
andererseits die alleinige Authentifizierung über ein Passwort --- bei einem System
mit Fokus auf Sicherheit --- als negativ zu bewerten (siehe @sec:SEC07_REPOSITORY_ZUGRIFF).

Hier wurden erweiterte Konzepte der Zwei--Faktor--Authentifizierung mit dem
*YubiKey* für Privatpersonen und Institutionen evaluiert (siehe
@sec:SEC08_SMARTCARDS_UND_RSA_TOKEN_ALS_ZWEI_FAKTOR_AUTHENTIFIZIERUNG).
Weiterhin wurde ein Konzept zur »einfachen Passworthärtung« mit dem *YubiKey*
vorgestellt (@sec:SEC08_YUBIKEY_FUER_PASSWORTHAERTUNG).

Im Bereich der Synchronisationspartnerauthentifizierung wurden verschiedene
Konzepte vorgestellt (siehe @sec:SEC08_AUTHENTIFIZIERUNGSKONZEPT), über welche
sich eine manuelle und automatisierte Authentifizierung des
Synchronisationspartners durchführen lässt.

### Softwareentwicklung und Softwareverteilung

Abschließend wurden Konzepte zur sicheren Verteilung der Software evaluiert.
Hierbei wurden neben Konzepten zum Update--Management (siehe
@sec:SEC08_UPDATEMANAGEMENT), auch Konzepte eines sicherheitsbewussten
Softwareentwicklungsprozesses evaluiert (siehe
@sec:SEC08_SIGNIEREN_VON_QUELLCODE). Weiterhin wurden unterschiedliche
Verfahren zur Authentifizierung (Zwei--Faktor--Authentifizierung,
Public--Key/Smartcard--Authentifizierung) gegenüber der *GitHub*--Plattform
evaluiert (siehe @sec:SEC08_SICHERE_AUTHENTIFIZIERUNG_FUER_ENTWICKLER). 


## Selbstkritik und aktuelle Probleme {#sec:SEC09_SELBSTKRITIK_AKTUELLE_PROBLEME}

Einige der unter @sec:SEC03_ANFORDERUNGEN gesetzten Anforderungen wurden schon
teilweise umgesetzt, teilweise existieren bereits Konzepte und ...

Auch wenn man bei der aktuellen Version weniger von einem Prototypen aus
Anwendersicht sprechen kann, so wurden  ...

TODO: Ausformulieren

* Ungelöst: Convergent Encryption
* Benutzerfreundlichkeit?
* Ist *IPFS* gute Wahl?
* Keymanagement in IPFS besser aufgehoben?
* Performance auf kleinen Systemen untragbar  aes-128 Bit Algorithmen?  Alternativen zu chacha.
* Nicht strikt an BSI gehalten


## Ausblick {#sec:SEC09_AUSBLICK}

Die Evaluation der Sicherheit von »brig« sowie die evaluierten
Sicherheitskonzepte für die weitere Entwicklungen stellen einen »Erstentwurf«
dar. Wie bereits unter @sec:SEC04_KRYPTOGRAPHISCHE_PRIMITIVEN_UND_PROTOKOLLE
und @sec:SEC05_SICHERHEIT_UND_ANGRIFFSSZENARIEN erläutert, ist die
Implementierung und Evaluierung von Sicherheit keine triviale Aufgabe.
Weiterhin kann auch die Umsetzung kryptographischer Elemente aufgrund von
Missverständnissen fehlerhaft implementiert sein. 

Da »brig« einen Schwerpunkt auf Sicherheit hat, ist es essentiell das in dieser
Arbeit Evaluierte System und die vorgestellten Konzepte von weiteren
unabhängigen Sicherheitsexperten --- beispielsweise von der HSASec[^FN_HSASEC]
--- beurteilen zu lassen und die vorgestellten Konzepte kritisch zu
diskutieren. Zusätzlich sollte unabhängige Sicherheitsaudits der
Implementierung vor der ersten offiziellen Veröffentlichung durchgeführt
werden.

[^FN_HSASEC]: HSASec: <https://www.hsasec.de/>

Weiterhin wäre für anknüpfende Arbeiten im Bereich von »brig« oder allgemein
von dezentralen und sicherheitsorientierten Dateiverteilungslösungen die
Evaluation von Plattformen wie *Keybase.io*[^FN_KEYBASE] als
Authentifizierungsplattform erwähnenswert.

[^FN_KEYBASE]: Keybase.io: <https://keybase.io/>

Die durchgeführten Benchmarks zur Geschwindigkeit zeigen ein
tendenzielles Verhalten auf bestimmten Plattformen. Hier wäre die Evaluation
weiterer Hardware--Systeme nötig um bessere Entscheidungen für Optimierungen
und bezüglich der Auswahl geeigneter Algorithmen treffen zu können.

Abschließend ist es wichtig zu erwähnen, dass unabhängig von den
Implementierten technischen Maßnahmen, der Benutzer eine essentielle Rolle in
jedem sicherheitskritischen System hat. Dieser muss immer wieder aufs Neue für
das Thema Sicherheit und Datenschutz sensibilisiert werden. Gerade in unser
heutigen digitalen Informationsgesellschaft ist die Auseinandersetzung mit
Sicherheit und den eigenen Daten wichtiger den je.
