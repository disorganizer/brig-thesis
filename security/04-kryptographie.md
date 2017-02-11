# Kryptographische Primitiven und Protokolle {#sec:SEC04_KRYPTOGRAPHISCHE_PRIMITIVEN_UND_PROTOKOLLE}

## Einleitung {#sec:SEC04_EINLEITUNG}

Software--Entwickler sind in der Regel keine Sicherheitsexperten. Nicht nur
Fehler in der Software gefährden ganze Systeme und Benutzerdaten, sondern auch
der fehlerhafte Einsatz von Kryptographie ist immer wieder für katastrophale
Sicherheitsprobleme verantwortlich. Es ist *sehr schwer* Kryptographie
*korrekt* zu implementieren. Sogar der früher weit verbreitete Standard IEEE
802.11, *WEP (Wired Equivalent Privacy)*, zur verschlüsselten drahtlosen
Kommunikation, weist gleich mehrere Designschwächen auf. Eine
Analyse[^FN_WEP_ANALYSIS] kommt zu der Einschätzung, dass kryptographische
Primitiven missverstanden und auf ungünstige Art kombiniert wurden. Weiterhin
ist es ein Hinweis dafür, dass man Experten aus dem Bereich der Kryptographie
hätte einbeziehen sollen, um solche Fehler zu vermeiden (vgl. auch
[@martin2012everyday], S. 430).

[^FN_WEP_ANALYSIS]: WEP Analysis: <http://www.isaac.cs.berkeley.edu/isaac/wep-faq.html>

Sogar bei Unternehmen welche explizit mit *starker Kryptographie* für ihre
Produkte werben[^FN_HDD_ENCRYPTION_FAIL] und auch für welche Kryptographie zum
Tagesgeschäft gehört, machen immer wieder fatale Fehler bei der Implementierung
ihrer Produkte.

[^FN_HDD_ENCRYPTION_FAIL]: Festplattenverschlüsselung: <http://www.heise.de/security/artikel/Verschusselt-statt-verschluesselt-270058.html>

Die oben genannten Beispiele zeigen, dass selbst Systeme, die von Experten
entwickelt werden, genauso kritische Fehler aufweisen können. Das *BSI* (Bundesamt
für Sicherheit in der Informationstechnik) hat aus diesem Grund einen Leitfaden
(vgl. [@bsi]) für die Implementierung kryptographischer Verfahren
zusammengestellt. Im Leitfaden wird explizit darauf hingewiesen, dass der Leitfaden je
nach Anwendungsfall nicht blind angewendet werden darf und dass bei
sicherheitskritischen Systemen stets Experten zu Rate zu ziehen sind.

Selektiv gewählte Sicherheitsprinzipien werden betrachtet, um zu sensibilisieren
jedoch viel mehr um einen »sinnvollen« Einsatz für »brig« definieren zu können.

## Verschlüsselung {#sec:SEC04_VERSCHLUESSELUNG}

### Symmetrische Verschlüsselungsverfahren {#sec:SEC04_SYMMETRISCHE_VERSCHLUESSELUNGSVERFAHREN}

#### Grundlegende Funktionsweise {#sec:SEC04_GRUNDLEGENDE_FUNKTIONSWEISE_SYM}

[@fig:img-symmetric] zeigt die Verschlüsselung von Daten mittels symmetrischer
Kryptographie. Bei symmetrischer Kryptographie wird der gleiche Schlüssel zum
Ver-- und Entschlüsseln der Daten verwendet.

Beim Datenaustausch über unsichere Netze, muss der Schlüssel zuerst zwischen
den Kommunikationspartnern ausgetauscht werden. In [@fig:img-symmetric]
verschlüsselt *Alice* die Daten mit einem *gemeinsamen Schlüssel*. Anschließend
sendet Sie die verschlüsselten Daten an *Bob*, welcher den *gemeinsamen
Schlüssel* verwendet, um die Daten wieder zu entschlüsseln.

Symmetrische Verfahren sind im Vergleich zu asymmetrischen Verfahren sehr
Ressourceneffizient. Die Grundlage für symmetrische Algorithmen, stellen
Manipulationen (Substitutionen, Permutationen[^FN_SUB_PERM_NETWORK] oder
Feistelrunden[^FN_FEISTEL]) auf Bit--Ebene dar, welche ohne Schlüssel nicht
effizient umkehrbar sind.

[^FN_FEISTEL]: Feistelchiffre: <https://de.wikipedia.org/w/index.php?title=Feistelchiffre&oldid=159236443>
[^FN_SUB_PERM_NETWORK]: Substitutions--Permutations--Netzwerk:

	<https://de.wikipedia.org/w/index.php?title=Substitutions-Permutations-Netzwerk&oldid=150385470>

Das grundsätzliche Problem, welches bei der Anwendung symmetrischer Verschlüsselung
besteht, ist der *sichere* Schlüsselaustausch.

![Konzept beim Austausch von Daten über einen unsicheren Kommunikationsweg unter Verwendung symmetrischer Kryptographie. *Alice* und *Bob* teilen einen *gemeinsamen Schlüssel*, um die Daten zu ver-- und entschlüsseln.](images/symmetric.png){#fig:img-symmetric width=85%}

#### Unterschied zwischen Block-- und Stromverschlüsselung {#sec:SEC04_UNTERSCHIED_ZWISCHEN_BLOCK_UND_STROMVERSCHLUESSELUNG}

Das symmetrische Verschlüsseln unterteilt sich in die beiden
Verschlüsselungsverfahren Stromverschlüsselung und Blockverschlüsselung. Bei
der Stromverschlüsselung wird direkt jedes Zeichen (Bit) des Klartextes mittels
eines kryptografischen Schlüssels direkt (XOR) in ein Geheimtextzeichen
umgewandelt.

Bei der Blockverschlüsselung hingegen sind die Daten in Blöcke einer bestimmten
Größe unterteilt. Die Verschlüsselung funktioniert auf Blockebene. Wie oder ob
die Datenblöcke untereinander abhängig sind und welche Informationen bei der
Verschlüsselung neben dem Schlüssel mit in die Verschlüsselung einfließen,
bestimmt die sogenannte Betriebsart. [@fig:img-streamblock] zeigt exemplarisch
den Unterschied zwischen Strom-- und Blockverschlüsselung.

![Unterschied in der Arbeitsweise zwischen Block-- und Stromchiffre. Die Blockchiffre verschlüsselt die Daten blockweise, eine Stromchiffre hingegen verschlüsselt den Datenstrom »on--the--fly«.](images/streamblock.png){#fig:img-streamblock width=80%}

#### Betriebsarten der Blockverschlüsselung {#sec:SEC04_BETRIEBSARTEN_DER_BLOCKVERSCHLUESSELUNG}

Die Betriebsart beschreibt auf welche Art und Weise die Blöcke verschlüsselt
werden. Dies ist insofern wichtig, da sich durch die Betriebsart die
Eigenschaften und somit der Einsatzzweck ändern kann. Folgend zwei
Betriebsarten zu besserem Verständnis:

**Electronic Code Book Mode (ECB):** Bei dieser Betriebsart werden die
Klartextblöcke unabhängig voneinander verschlüsselt. Dies hat den Nachteil,
dass gleiche Klartextblöcke immer gleiche Geheimtextblöcke, bei Verwendung
des gleichen Schlüssels, ergeben. [@fig:img-ecbvschaining] zeigt eine
»Schwäche« dieses Verfahrens.

![Bild zur graphischen Verdeutlichung des ECB--Modus im Vergleich zu einem block chaining cipher.[^FN_TUX_ECB]](images/ecbvschaining.png){#fig:img-ecbvschaining width=80%}

[^FN_TUX_ECB]:Bildquelle *ECB*: <https://de.wikipedia.org/w/index.php?title=Electronic_Code_Book_Mode&oldid=159557291>

**Cipher Feedback Mode (CFB):** Beim *CFB*--Modus fließt, neben dem Schlüssel,
der Geheimtextblock vom Vorgänger ein. Durch diese Arbeitsweise haben im
Gegensatz zum *ECB*--Modus gleiche Klartextblöcke unterschiedliche
Geheimtextblöcke. Weiterhin wird bei dieser Arbeitsweise aus der
Blockverschlüsselung eine Stromverschlüsselung.

[@fig:img-ciphermode] zeigt den Unterschied zwischen den beiden genannten Modi.

![ECB--Modus (links): Datenblöcke werden unabhängig voneinander verschlüsselt. CFB--Modus (rechts): Datenblöcke hängen beim Verschlüsseln voneinander ab.](images/ciphermode.png){#fig:img-ciphermode width=100%}

Neben den genannten Betriebsarten gibt es noch weitere die sich in der
Funktionsweise unterscheiden beziehungsweise für bestimmte Anwendungen
konzipiert sind. Je nach Betriebsart ist ein paralleles Ver-- und Entschlüsseln
oder auch ein wahlfreier Zugriff möglich.  Weiterhin variiert auch die
Fehleranfälligkeit und Sicherheit. [@tbl:t-betriebsarten] zeigt gängige
Betriebsarten und ihre Eigenschaften.

----------------------------------------------------------
*Eigenschaft/Betriebsart*          ECB  CBC  CFB  CTR OFB
--------------------------------   ---  ---- ---- --- ----
*Verschlüsseln parallelisierbar*   ja   nein nein ja  nein

*Entschlüsseln parallelisierbar*   ja   ja   ja   ja  nein

*Wahlfreier Zugriff möglich*       ja   ja   ja   ja  nein
----------------------------------------------------------

Table: Laut ISO 10116 Standard definierte Betriebsarten für blockorientierte
Verschlüsselungsalgorithmen. {#tbl:t-betriebsarten}

#### Gängige Algorithmen, Schlüssellängen und Blockgrößen {#sec:SEC04_GAENGIGE_ALGORITHMEN_SCHLUESSELLAENGEN_UND_BLOCKGROESSEN}

Der ursprünglich seit Ende der 70er--Jahre verwendete *DES (Data Encryption
Standard)*, welcher eine effektive Schlüssellänge von 56  Bit hatte, war Ende
der 90er--Jahre nicht mehr ausreichend sicher gegen *Brute--Force*--Angriffe.
In einer öffentlichen Ausschreibung wurde ein Nachfolger, der Advanced
Encryption Standard (kurz *AES*) bestimmt. Gewinner des Wettbewerbs sowie der
heutige »Quasistandard« wurde der Rijndael--Algorithmus.

Neben dem bekanntem *AES (Rijndael)*--Algorithmus, gibt es noch weitere
Algorithmen, die heutzutage Verwendung finden. Zu den *AES*--Finalisten gehören
weiterhin *MARS*, *RC6*, *Serpent* und der von *Bruce Schneier* entwickelte
*Twofish*. Alle genannten Algorithmen arbeiten mit einer Blockgröße von 128 Bit
und unterstützen jeweils die Schlüssellängen 128 Bit, 192 Bit und 256 Bit.

*AES* ist die aktuelle Empfehlung vom *BSI (vgl. [@bsi] S.22 f.)*.

### Asymmetrische Verschlüsselungsverfahren {#sec:SEC04_ASYMMETRISCHE_VERSCHLUESSELUNGSVERFAHREN}

#### Grundlegende Funktionsweise {#sec:SEC04_GRUNDLEGENDE_FUNKTIONSWEISE_ASYM}

Im Vergleich zur symmetrischen Verschlüsselung, werden bei der asymmetrischen
Verschlüsselung die Daten mit einem unterschiedlichen Schlüssel ver-- und
entschlüsselt. Der Vorteil zu symmetrischen Verschlüsselung ist, dass die
kommunizierenden Parteien keinen gemeinsamen Schlüssel kennen müssen.

Um Daten mittels asymmetrischer Verschlüsselung auszutauschen,  müssen die
beiden Kommunikationspartner *Alice* und *Bob* ein Schlüsselpaar, bestehend aus
einem *privaten* und einem *öffentlichen* Schlüssel, erstellen. Anschließend
tauschen beide Parteien den *öffentlichen* Schlüssel aus. Der *private*
Schlüssel ist geheim und darf nicht weitergegeben werden. [@fig:img-asymmetric]
zeigt die Funktionsweise bei asymmetrischer Verschlüsselung.

![Prinzip asymmetrischer Verschlüsselung. Verschlüsselt wird mit dem *öffentlichen* Schlüssel des Empfängers. Der Empfänger entschlüsselt mit seinem *privaten* Schlüssel die Nachricht. Die Signatur erfolgt mit dem *privaten* Schlüssel des Senders, validiert wird diese mit dem *öffentlichen* Schlüssel des Senders.](images/asymmetric.png){#fig:img-asymmetric width=100%}

Im Unterschied zu symmetrischen Verfahren, beruht die asymmetrische
Verschlüsselung auf der Basis eines mathematischen Problems, welches eine
Einwegfunktion ist. Das heißt, dass die Berechnung in die eine Richtung sehr
leicht ist, die Umkehrfunktion jedoch sehr schwierig zu berechnen ist. Die
zugrundeliegenden mathematischen Probleme sind das Faktorisierungsproblem
(*RSA*--Verfahren) großer Primzahlen und das diskrete Logarithmusproblem
(*ElGamal*--Verfahren).

#### Gängige Algorithmen, Einsatzzwecke und Schlüssellängen {#sec:SEC04_GAENGIGE_ALGORITHMEN_EINSATZZWECKE_UND_SCHLUESSELLAENGEN}

Zu den gängigen Algorithmen der asymmetrischen Verschlüsselungsverfahren
gehören *RSA* und *ElGamal*. Beide Verfahren ermöglichen sowohl die Ver-- und
Entschlüsselung von Daten sowie das Signieren von Daten. Zu den
Signatur--Verfahren gehören die RSA--Signatur und *DSA (ElGamal--Signatur)*.

Weiterhin gibt es eine Variante des *DSA*--Verfahrens, welche
Elliptische--Kurven--Kryptographie verwendet, das *ECDSA (elliptic curve DSA)*.
Die Verfahren auf elliptischen Kurven haben den Vorteil, dass die
Schlüssellängen um Faktor 6--30 kleiner sind, was bei vergleichbarem
Sicherheitsniveau Ressourcen sparen kann, obwohl die Operationen auf
elliptischen Kurven aufwendiger zu berechnen sind als Operationen in
vergleichbar großen endlichen Körpern.

Heutzutage typische Schlüssellängen bei asymmetrischer Verschlüsselung sind
1024 Bit, 2048 Bit und 4096 Bit. Die Schlüssellängen sind nicht direkt mit den
der symmetrischen Verschlüsselungsverfahren vergleichbar. [@tbl:t-keys] zeigt
die Schlüssellängen der verschiedenen Verschlüsselungsverfahren im Vergleich zu
ihren äquivalenten Vertretern der symmetrischen Verfahren. Die Daten
entsprechen der empfohlenen ECRYPTII--Einschätzung[^FN_ECRYPTII].

---------------------------------------------------------------------------------
*RSA modulus* 	*ElGamal Gruppengröße* 	*Elliptische Kurve* 	*sym. Äquivalent*
-------------  -----------------------  -------------------     -----------------
480            480                      96                      48

640            640                      112                     56

816            816                      128                     64

1248           1248                     160                     80

2432           2432                     224                     112

3248           3248                     256                     128

5312           5312                     320                     160

7936           7936                     384                     192

15424          15424                    512                     256
---------------------------------------------------------------------------------

Table: Auf ECRYPTII--Einschätzung basierende effektive Schlüsselgrößen
asymmetrischer und symmetrischer Verfahren im direkten Vergleich. {#tbl:t-keys}

[^FN_ECRYPTII]:ECRYPT II Yearly Report on Algorithms and Key Lengths (2012):

	<http://www.ecrypt.eu.org/ecrypt2/documents/D.SPA.20.pdf>

### Hybride Verschlüsselungsverfahren {#sec:SEC04_HYBRIDE_VERSCHLUESSELUNGSVERFAHREN}

Asymmetrische Verschlüsselungsverfahren sind im Vergleich zu symmetrischen
Verschlüsselungsverfahren sehr langsam, haben jedoch den Vorteil, dass kein
*gemeinsamer* Schlüssel für die verschlüsselte Kommunikation bekannt sein muss.
Symmetrische Verfahren hingegen sind sehr effizient, ein Hauptproblem, welches
sie jedoch haben ist der Austausch eines gemeinsamen Schlüssels zum Ver-- und
Entschlüsseln.

Bei der hybriden Verschlüsselung macht man sich die Vorteile beider Systeme zu
Nutzen. Bevor *Alice* und *Bob* kommunizieren können, tauschen sie mittels
Public--Key--Kryptographie (asymmetrische Kryptographie) den *gemeinsamen*
Schlüssel, welchen Sie anschließend für die symmetrische Verschlüsselung
verwenden, aus.

## Diffie--Hellman--Schlüsseltausch {#sec:SEC04_DIFFIE_HELLMANN_SCHLUESSELAUSTAUSCH}

Aus dem Diffie--Hellman--Schlüsselaustausch (kurz *DH*) geht das
ElGamal--Verschlüsselungsverfahren hervor. *DH* ist ein
Schlüsselaustauschprotokoll, welches es zwei Kommunikationspartnern ermöglicht,
einen *gemeinsamen* Schlüssel zu bestimmen, ohne diesen über den potentiell
unsicheren Kommunikationskanal austauschen zu müssen.

![Grafische Darstellung, Ablauf des Diffie--Hellman--Schlüsseltausch.](images/dh.png){#fig:img-dh width=75%}

[@fig:img-dh] zeigt Ablauf des *DH*--Protokolls:

1) *Alice* und *Bob* einigen sich auf große Primzahl $p$ und natürliche Zahl $g$, die kleiner ist als $p$.
2) *Alice* und *Bob* generieren jeweils eine geheime Zufallszahl $a$ und $b$.
3) *Alice* berechnet $A=g^{a} (\mod p)$  und schickt $A$ an *Bob* (dies
   entspricht im Grunde einem temporärem *ElGamal* Schlüsselpaar: $a$ = privater
   Schlüssel, $g^a$ = öffentlicher Schlüssel)
4) *Bob* berechnet $B=g^{b}(\mod p)$ und schickt  $B$ an *Alice*.
5) *Alice* erhält $B$ von *Bob* und berechnet mit $a$ die Zahl $K_{1}=B^{a} (\mod p)$.
6) *Bob* berechnet analog $K_{2}=A^{b}(\mod p)$.

Beide haben den gleichen Schlüssel berechnet, da gilt:

$$ K_{1} = B^{a} = (g^{b})^{a} = (g^{a})^{b} = A^{b} = K_{2} $$

## Hashfunktionen {#sec:SEC04_HASHFUNKTIONEN}

### Kryptographische Hashfunktionen {#sec:SEC04_KRYPTOGRAPHISCHE_HASHFUNKTIONEN}

Hashfunktionen werden in der Informatik verwendet, um eine beliebige endliche
Eingabemenge auf einer Prüfsumme (Hashwert) einer bestimmten Länge abzubilden.
Prüfsummen können verwendet werden, um beispielsweise die Integrität von Daten
zu validieren. Ein Praxisbeispiel wäre die Korrektheit von übertragenen Daten
zu validieren, beispielsweise nach dem Download eines *Linux*--Images.

Kryptographische Hashfunktionen sind spezielle Formen von Hashfunktionen, welche
folgende Eigenschaften bieten:

* Einwegfunktion
* Schwache Kollisionsresistenz: Praktisch unmöglich *zu gegebenen Wert* $x$ ein
  $y$ zu finden, welches den selben Hashwert besitzt: $h(x) = h(y), x \ne y$
* Starke Kollisionsresistenz: Praktisch unmöglich, *zwei verschiedene
  Eingabewerte* $x$ und $y$ mit dem gleichen Hashwert zu finden $h(x) = h(y), x
  \ne y$ zu finden

### Message Authentification Codes {#sec:SEC04_MESSAGE_AUTHENTIFICATION_CODES}

Um nicht nur die Integrität der Daten, sondern auch deren Quelle zu
validieren, werden sogenannte Message Authentification Codes (kurz MAC)
verwendet. *MACs* sind schlüsselabhängige Hashfunktionen. Neben Hashfunktionen
werden auch Blockchiffren verwendet. [@fig:img-hmac] zeigt die Übertragung von
Daten mit einer *Keyed-Hash Message Authentication Code (HMAC)*.

![Message--Übertragung mit HMAC.](images/hmac.png){#fig:img-hmac width=85%}

## Authentifizierungsverfahren {#sec:SEC04_AUTHENTIFIZIERUNGSVERFAHREN}

Bei den praktischen Authentifizierungsverfahren ist das Passwort immer noch
eine sehr weit verbreitete Möglichkeit der Authentifizierung. Passwörter sind
eine sehr problematische Möglichkeit der Authentifizierung, weil sie auf gute
»Entropie« angewiesen sind. Das heißt, dass Passwörter möglichst »zufällig«
sein müssen. Passwörter die leicht zu erraten sind, sind *de facto* schlechte
Authentifizierungsmechanismen.

Die Problematik mit den Passwörtern kennt heutzutage jedes Unternehmen. Sind
die Passwort--Richtlinien zu kompliziert, werden die Passwörter oft von
Benutzern aufgeschrieben. Gibt es keine Passwort--Richtlinien, dann verwenden
Menschen oft schwache Passwörter, oft auch das gleiche »einfache« Passwort für
mehrere Anwendungen.

Die Situation lässt sich jedoch auf recht einfache Art und Weise durch den
Einsatz eines zusätzlichen *Authentifizierungsfaktors* verbessern. Diese Art der
Authentifizierung wird Multi--Faktor-- oder auch im speziellen Zwei--Faktor--Authentifizierung
genannt. Als zweiter *Faktor* kann beispielsweise ein biometrisches Merkmal
verwendet werden. Eine weitere Form der Zwei--Faktor--Authentifizierung wäre
beispielsweise die Chipkarte der Bank. Hierbei wird einerseits die *PIN* (etwas
das man weiß) und die Chipkarte (etwas das man hat) benötigt. Eine
erfolgreiche Authentifizierung findet in dem Fall nur bei korrekter *PIN* unter
Verwendung der Chipkarte der Bank statt.

## Keymanagement {#sec:SEC04_KEYMANAGEMENT}

Das Keymanagement (Schlüsselverwaltung) ist einer der sensibelsten Bereiche bei
der Implementierung eines Systems. Sind die Schlüssel unzureichend geschützt
oder die Einsatzweise der Schlüssel fraglich, so kann ein System meist einfach
kompromittiert werden. Neben sicherer Verwaltung der Schlüssel, ist auch die
Beschränkung auf einen bestimmten Einsatzzweck essentiell.
