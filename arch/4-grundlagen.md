# Grundlagen {#sec:grundlagen}

Für das Verständnis der Architektur von ``brig`` ist die Erklärung einiger
Internas von ``ipfs`` und dem freien Versionsverwaltungssystem ``git`` nötig.
Diese werden im Folgenden gegeben.

## ``ipfs``: Das *Interplanetary Filesystem*

Anstatt das »Rad neu zu erfinden«, setzt ``brig`` auf das relativ junge
*Interplanetary Filesystem* (kurz ``ipfs``), welches von Juan Benet und seinen
Mitentwicklern unter der MIT--Lizenz in der Programmiersprache Go entwickelt
wird (siehe auch das Whitepaper[@benet2014ipfs]). Im Gegensatz zu den meisten
anderen verfügbaren Peer--to-Peer Netzwerken kann ``ipfs`` als
Software--Bibliothek genutzt werden. Dies ermöglicht es ``brig`` als,
vergleichsweise dünne Schicht, zwischen Benutzer und ``ipfs`` zu fungieren (wie in [@fig:fuse-brig-ipfs] dargestellt).

![Zusammenhang zwischen ``ipfs``, ``brig`` und FUSE.](images/3/fuse-brig-ipfs.pdf){#fig:fuse-brig-ipfs width=30%}

``ipfs`` stellt dabei ein *Content Addressed Network* (kurz *CAN*, [^CAN]) dar.
Dabei wird eine Datei, die in das Netzwerk gelegt wird nicht mittels eines
Dateinamen angesprochen, sondern mittels einer Prüfsumme, die durch eine vorher
festgelegte Hashfunktion berechnet wird. Andere Teilnehmer im Netzwerk können
mittels dieser Prüfsumme die Datei lokalisieren und empfangen. Anders als bei
einer HTTP--URL (*Unified Resource Locator*) steckt der Prüfsumme einer Datei
also nicht nur die Lokation der Datei, sondern sie dient auch
als eindeutiges Identifikationsmerkmal (ähnlich eines Pfads) und gleicht daher
eher einem Magnet Link[^MAGNET_LINK] als einer URL. Vereinfacht gesagt ist es
nun die Hauptaufgabe von ``brig`` dem Nutzer die gewohnte Abstraktionsschicht
eines Dateisystem zu geben, während im Hintergrund jede Datei zu einer
Prüfsumme aufgelöst wird.

[^MAGNET_LINK]: Mehr Informationen unter <https://de.wikipedia.org/wiki/Magnet-Link>

Im Vergleich zu zentralen Ansätzen können Dateien intelligent geroutet werden
und müssen nicht physikalisch auf allen Geräten verfügbar sein. Eine Datei kann
»im Netzwerk liegen«. Greift der Nutzer über ihre Prüfsumme darauf zu, wird sie
vom *CAN* intelligent aus dem Netzwerk geholt, sofern sie lokal nicht vorhanden
ist. Dabei wird die Datei typischerweise in kleine Blöcke unterteilt, welche
einzeln verteilt und geholt werden können. Daher müssen beispielsweise bei
einem Netzwerkfehler nur alle Blöcke noch heruntergeladen werden, die noch
fehlen.

Technisch basiert ``ipfs`` auf der Distributed--Hashtable *Kademlia* (vgl.
[@maymounkov2002kademlia] und [@peer2peer], S. 247), welches mit den
Erkenntnissen aus den Arbeiten *CoralDHST*[@freedman2004democratizing] (Ansatz
um das Routing zu optimieren) und *S/Kademlia*[@baumgart2007s] (Ansatz um das
Netzwerk gegen Angriffe zu schützen) erweitert und abgesichert wurde.
*S/Kademlia* verlangt dabei, dass jeder Knoten im Netzwerk über ein
Schlüsselpaar, bestehend aus einem öffentlichen und privaten Schlüssel verfügt.
Die Prüfsumme des öffentlichen Schlüssels dient dabei als einzigartige
Identifikation des Knotens und der private Schlüssel dient als Geheimnis mit
dem ein Knoten seine Identität nachweisen kann. Diese Kernfunktionalitäten sind
bei ``ipfs`` in einer separaten Bibliothek namens ``libp2p``[^LIBP2P]
untergebracht, welche auch von anderen Programmen genutzt werden können.

[^CAN]: Siehe auch: <https://en.wikipedia.org/wiki/Content_addressable_network> 
[^LIBP2P]: Mehr Informationen in der Dokumentation unter: <https://github.com/ipfs/specs/tree/master/libp2p>

### Eigenschaften des *Interplanetary Filesystems* {#sec:ipfs-attrs}

Im Folgenden werden die Eigenschaften von ``ipfs`` kurz vorgestellt, welche von
``brig`` genutzt werden. Einige interessante Features wie beispielsweise das
*Interplanetary Naming System* (IPNS) werden dabei ausgelassen, da sie für
``brig`` aktuelle keine praktische Bedeutung haben.

**Weltweites Netzwerk:** Standardmäßig bilden alle ``ipfs``--Knoten ein
zusammenhängendes, weltweites Netzwerk.
``ipfs`` verbindet sich beim Start mit
einigen, wohlbekannten *Bootstrap--Nodes*, deren
Adressen mit der Software mitgeliefert werden. Diese können dann wiederum den
neuen Knoten an ihnen bekannte, passendere Knoten vermitteln. Die Menge der so
entstandenen verbundenen Knoten nennt ``ipfs`` den *Swarm* (dt. Schwarm). Ein
Nachbarknoten wird auch *Peer* genannt.

Falls gewünscht, kann allerdings auch ein abgeschottetes Subnetz erstellt
werden. Dazu ist es lediglich nötig, die *Bootstrap*--Nodes durch Knoten
auszutauschen, die man selbst kontrolliert. Unternehmen könnten diesen Ansatz
wählen, falls ihr Netzwerk komplett von der Außenwelt abgeschottet sein soll. Wie in
[@sec:architektur] beleuchtet wird, ist eine Abschottung des Netzwerks
rein aus Sicherheitsgründen nicht zwingend nötig.

**Operation mit Prüfsummen:** ``ipfs`` arbeitet nicht mit herkömmlichen Dateipfaden,
sondern nur mit der Prüfsumme einer Datei. Im folgenden Beispiel
wird eine Fotodatei mittels der ``ipfs``--Kommandozeile in das Netzwerk
gelegt[^IPFS_DAEMON]:

```bash
$ ipfs add my-photo.png
QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG
```

Wird eine Datei modifiziert, so muss sie neu mittels ``ipfs add`` hinzugefügt
werden und wird in dieser Version unter einer anderen Prüfsumme erreichbar
sein. Im Gegensatz zu normalen Dateisystemen kann es keinen allgemeinen
Einstiegspunkt (wie das Wurzelverzeichnis ``/``) geben. Die Prüfsumme eines
Verzeichnisses definiert sich in ``ipfs`` durch die Prüfsummen seiner Inhalte.
Das Wurzelverzeichnis hätte also nach jeder Modifikation eine andere Prüfsumme.

``ipfs`` nutzt dabei ein spezielles Format um Prüfsummen zu
repräsentieren[^IPFS_HASH]. Die ersten zwei Bytes einer Prüfsumme
repräsentieren dabei den verwendeten Algorithmus und die Länge der darauf
folgenden, eigentlichen Prüfsumme. Die entstandene Byte--Sequenz wird dann
mittels ``base58``[^BASE58] enkodiert, um sie menschenlesbar zu machen. Da der momentane
Standardalgorithmus ``sha256`` ist, beginnt eine von ``ipfs`` generierte
Prüfsumme stets mit »``Qm``«. Abbildung [@fig:ipfs-hash-format] zeigt dafür ein
Beispiel.

![Layout der ``ipfs`` Prüfsumme.](images/2/ipfs-hash-layout.pdf){#fig:ipfs-hash-format width=80%}

[^BASE58]: <https://de.wikipedia.org/wiki/Base58>

[^IPFS_DAEMON]: Voraussetzung hierfür ist allerdings, dass der ``ipfs``--Daemon
vorher gestartet wurde und ein Repository mittels ``ipfs init`` erzeugt wurde.

[^IPFS_HASH]: Mehr Informationen unter: <https://github.com/multiformats/multihash>

Auf einem anderen Computer, mit laufenden ``ipfs``--Daemon, ist das Empfangen
der Datei möglich, indem die Prüfsumme an das Kommando ``ipfs cat`` gegeben wird. Dabei wird für
den Nutzer transparent über die DHT ein Peer ausfindig gemacht, der die Datei
anbieten kann und der Inhalt von diesem bezogen:

```bash
$ ipfs cat QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG > my-photo.png
```

**Public--Key Infrastructure:** Jeder Knoten im ``ipfs``--Netzwerk besitzt ein
RSA--Schlüsselpaar, welches beim Anlegen des Repositories erzeugt wird. Mittels
einer Prüfsumme  wird aus dem öffentlichen Schlüssel eine Identität berechnet
($ID = H_{sha256}(K_{Public})$). Diese kann dann dazu genutzt werden einen Knoten
eindeutig zu identifizieren und andere Nutzer im Netzwerk nachzuschlagen und
deren öffentlichen Schlüssel zu empfangen:

```bash
# Nachschlagen des öffentlichen Schlüssels eines zufälligen Bootstrap-Nodes:
$ ipfs id QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ
{
  "ID": "QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ",
  "PublicKey": "CAASpgIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK[...]",
  ...
}
```

Der öffentliche Schlüssel kann dazu genutzt werden, mit einem Peer mittels
asymmetrischer Verschlüsselung eine verschlüsselte Verbindung aufzubauen (siehe
[@cpiechula]). Von ``brig`` wird dieses Konzept weiterhin
genutzt, um eine Liste vertrauenswürdiger Knoten zu verwalten. Jeder Peer muss
bei Verbindungsaufbau nachweisen, dass er den zum öffentlichen Schlüssel passenden
privaten Schlüssel besitzt (für Details siehe [@cpiechula]).

**Pinning und Caching:** Das Konzept von ``ipfs`` basiert darauf, dass Knoten nur
das speichern, woran sie auch interessiert sind. Daten, die von außen zum
eigenen Knoten übertragen worden sind werden nur kurzfristig zwischengelagert.
Nach einiger Zeit bereinigt der eingebaute Garbage--Collector die Daten im
*Cache*.[^IPFS_MANUAL_GC]

Werden Daten allerdings über den Knoten selbst hinzugefügt, so bekommen sie
automatisch einen *Pin* (dt. Stecknadel). *Gepinnte* Daten werden automatisch
vom *Garbage-Collector* ignoriert und beliebig lange vorgehalten, bis sie
wieder *unpinned* werden. Möchte ein Nutzer sicher sein, dass die Datei im
lokalen Speicher bleibt, so kann er sie manuell pinnen:

```bash
$ ipfs pin add QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG
```

Wenn die Dateien nicht mehr lokal benötigt werden, können sie *unpinned* werden:

```bash
$ ipfs pin rm QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG
```

[^IPFS_MANUAL_GC]: Der Garbage--Collector kann auch manuell mittels ``ipfs repo gc`` von der Kommandozeile aufgerufen werden.

**Flexibler Netzwerkstack:** Einer der größten Vorteile von ``ipfs`` ist, dass
es auch über NAT--Grenzen hinweg funktioniert. Da aufgrund von
*UDP--Hole--Punching* kein *TCP* genutzt werden kann, wird *UDP* genutzt. Um
die Garantien, die *TCP* bezüglich der Paketzustellung gibt, zu erhalten nutzt
``ipfs`` das Anwendungs--Protokoll *UDT*. Insgesamt implementiert ``ipfs`` also
einige Techniken, um, im Gegensatz zu den meisten theoretischen Ansätzen, eine
leichte Usability zu gewährleisten. Speziell wäre hier zu vermeiden, dass ein
Anwender die Einstellungen seines Routers ändern muss, um ``brig`` zu nutzen.

[^UDT]: http://udt.sourceforge.net/

In Einzelfällen kann es natürlich trotzdem dazu kommen, dass die von ``ipfs``
verwendeten Ports durch eine besonders in Unternehmen übliche Firewall
blockiert werden. Dies kann nötigenfalls aber vom zuständigen Administrator
geändert werden.

**Übermittlung zwischen Internet und ``ipfs``:** Ein Client/Server--Betrieb
lässt sich mithilfe der ``ipfs``--*Gateways* emulieren. Gateways sind
zentrale, wohlbekannte Dienste, die zwischen dem »normalen Internet« und dem
``ipfs`` Netzwerk mittels HTTP vermitteln. Die Datei ``my-photo.png`` aus dem
obigen Beispiel kann von anderen Nutzern bequem über den Browser
heruntergeladen werden:

```bash
$ export PHOTO_HASH=QmPtoEEMMnbTSmzr28UEJFvmsD2dW88nbbCyyTrQgA9JR9
$ curl https://gateway.ipfs.io/ipfs/$PHOTO_HASH > my-photo.png
```

Auf dem Gateway läuft dabei ein Webserver, der intern dasselbe tut wie ``ipfs cat``,
aber statt auf der Kommandozeile die Daten auf eine HTTP--Verbindung ausgibt.
Standardmäßig wird bei jedem Aufruf von ``ipfs daemon`` ein Gateway auf der
Adresse <http://localhost:8080> gestartet.

## Datenmodell von ``ipfs``

Wie bereits beschrieben ist ``brig`` ein »Frontend«, welches ``ipfs`` zum
Speichern und Teilen von Dokumenten nutzt. Die Dokumente werden dabei einzig
und allein über ihre Prüfsumme (``QmXYZ...``) referenziert. Aus
architektonischer Sicht kann man ``ipfs`` als eine verteilte Datenbank sehen, die vier simple Operationen
beherrscht:

- $Put(\text{Stream}) \rightarrow \text{Hash}$: Speichert einen endlichen Datenstrom in der Datenbank und liefert die Prüfsumme als Ergebnis zurück.
* $Get(\text{Hash}) \rightarrow \text{Stream}$: Holt einen endlichen Datenstrom aus der Datenbank der durch seine Prüfsumme referenziert wurde und gibt ihn aus.
* $Pin(\text{Hash}, \text{Count})$: Pinnt einen Datenstrom wenn $\text{Count}$ größer $0$ ist oder unpinnt ihn wenn er negativ ist.
                                  Im Falle von $0$ wird nichts getan. In jedem Fall wird der neue Status zurückgeliefert.
* $Cleanup$: Lässt einen »Garbage--Collector«[^GC_WIKI] laufen, der Datenströme aus dem lokalen Speicher löscht, die nicht gepinned wurden.

[^GC_WIKI]: Siehe auch <https://de.wikipedia.org/wiki/Garbage_Collection>

Das besondere ist, dass die ``GET`` Operation von jedem verbundenen Knoten
ausgeführt werden kann, wodurch die Nutzung von ``ipfs`` als verteilte Datenbank
möglich wird. Die oben geschilderte Sicht ist rein die Art und Weise in der
``ipfs`` von ``brig`` benutzt wird. Die Möglichkeiten, die ``ipfs`` bietet,
sind tatsächlich sehr viel weitreichender als »nur« eine Datenbank
bereitzustellen. Intern hat es ein mächtiges Datenmodell, das viele Relationen
wie eine Verzeichnisstruktur, Versionsverwaltung, ein alternatives World--Wide--Web oder gar eine
Blockchain[^BLOCKCHAIN_NOTE] gut abbilden kann: Der *Merkle--DAG* (Direkter
azyklischer Graph), im Folgenden kurz *MDAG* oder *Graph* genannt.
Diese Struktur ist eine Erweiterung des Merkle--Trees[@wiki:szydlo2004merkle], bei der ein Knoten
mehr als einen Elternknoten haben kann.

![Beispielhafter MDAG der eine Verzeichnisstruktur abbildet.](images/4/ipfs-merkledag.pdf){#fig:ipfs-merkledag}

In [@fig:ipfs-merkledag] ist ein beispielhafter Graph gezeigt, der eine
Verzeichnishierarchie modelliert. Die gezeigten Attributnamen entsprechen 
den ``ipfs``--Internas. Gerichtet ist der Graph deswegen, weil es
keine Schleifen und keine Rückkanten zu den Elternknoten geben darf. Jeder
Knoten wird durch eine Prüfsumme referenziert und kann wiederum mehrere andere
Knoten über weitere Prüfsümmen referenzieren. Im Beispiel sieht man zwei
Wurzelverzeichnisse, bei denen das erste ein Unterverzeichnis ``/photos``
enthält, welches wiederum drei einzelne Dateien (``cat.png``, ``me.png`` und
``small.mkv``) enthält. Das zweite Wurzelverzeichnis beinhaltet ebenfalls
dieses, referenziert als zusätzliche Datei aber noch eine größere Datei namens
``big.mkv``. Die Besonderheit ist dabei, dass die Dateien jeweils in einzelne Blöcke
(``blobs``) zerlegt werden, die automatisch dedupliziert abgespeichert werden.
In der Grafik sieht man das dadurch, dass ``big.mkv`` bereits aus zwei Blöcken
von ``small.mkv`` besteht und der zweite Wurzelknoten auf ``/photos`` referenziert,
ohne dessen Inhalt zu kopieren.

Im Datenmodell von ``ipfs`` ([@benet2014ipfs, S.7 ff.]) gibt es drei
unterschiedliche Strukturen:

- ``blob:`` Ein Datensatz mit definierter Größe und Prüfsumme.  Wird teilweise auch *Chunk* genannt.
- ``list:`` Eine geordnete Liste von ``blobs`` oder weiteren ``lists``. Wird benutzt um große Dateien
        in kleine, deduplizierbare Teile herunterzubrechen.
* ``tree:`` Eine Abbildung von Dateinamen zu Prüfsummen.
        Modelliert ein Verzeichnis, das ``blobs``, ``lists`` oder andere ``trees`` beinhalten kann.
		Die Prüfsumme ergibt sich aus den Kindern.
* ``commit:`` Ein Snapshot eines der drei obigen Strukturen. In der Grafik nicht gezeigt, da
        diese Datenstrukutur noch nicht finalisiert ist.[^COMMIT_DISCUSS]

[^BLOCKCHAIN_NOTE]: Siehe auch die Erklärung hier: <https://medium.com/@ConsenSys/an-introduction-to-ipfs-9bba4860abd0#.t6mcryb1r>
[^COMMIT_DISCUSS]: Diskussion der Entwickler hier: <https://github.com/ipfs/notes/issues/23>

Wenn ``ipfs`` bereits ein Datenmodell hat, welches  Verzeichnisse abbilden
kann, ist es eine berechtigte Frage, warum ``brig`` ein eigenes Datenmodell
implementiert und nicht das vorhandene als Basis verwendet. Der Grund dafür
liegt in der bereits erwähnten Entkopplung von Daten und Metadaten. Würden die
Dateien und Verzeichnisse direkt in ``ipfs`` abgebildet, so wäre diese Teilung
nicht mehr gegeben, da trotzdem alle Daten in einem gemeinsamen Speicher
liegen. Dies hätte zur Folge, dass ein Angreifer zwar nicht die verschlüsselten
Daten lesen könnte, aber problemlos die Verzeichnisstruktur betrachten könnte,
sobald er die Prüfsumme des Wurzelknotens hat. Dies würde den
Sicherheitsversprechen von ``brig`` widersprechen. Abgesehen davon wurde ein
eigenes Datenmodell entwickelt, um mehr Freiheiten beim Design zu haben.

Zusammengefasst lässt sich also sagen, dass ``ipfs`` in dieser Arbeit als
Content--Adressed--Storage--Datenbank verwendet wird, die sich im Hintergrund
um die Speicherung von Datenströmen und deren Unterteilung in kleine Blöcke
mittels *Chunking* kümmert. Die Aufteilung geschieht dabei entweder simpel,
indem die Datei in gleichgröße Blöcke unterteilt wird, oder indem ein intelligenter
Algorithmus wie Rabin--Karp--Chunking[@karp1987efficient] angewandt wird.

## Datenmodell von ``git``

Der interne Aufbau von ``brig`` ist relativ stark von den Internas des freien
Versionsverwaltungssystem ``git`` inspiriert. Deshalb werden im Folgenden immer
wieder Parallelen zwischen den beiden Systemen gezogen, um die jeweiligen
Unterschiede aufzuzeigen und zu erklären warum ``brig`` letztlich einige
wichtige Differenzen aus architektonischer Sicht aufweist. Was die Usability
angeht, soll allerdings aufgrund der relativ unterschiedlichen Ziele kein
Vergleich gezogen werden.

Im Folgenden ist ein gewisses Grundwissen über ``git`` nützlich. Es wird bei
Unklarheiten das Buch »*Git --- Verteile Versionsverwaltung für Code
und Dokumente*[@git]« empfohlen. Alternativ bietet auch die offizielle
Projektdokumentation[^GITBOOK] einen sehr guten Überblick. Aus Platzgründen
wird an dieser Stelle über eine gesonderte Einführung verzichtet, da es
diese in ausreichender Menge frei verfügbar gibt.

[^GITBOOK]: Offizielle Projektdokumentation von ``git``: <https://git-scm.com/doc>

Kurz beschrieben sind beide Projekte »*stupid content
tracker*«[^TORVALDS_ZITAT], die Änderungen an tatsächlichen Dateien auf
Metadaten abbilden, welche in einer dafür geeigneten Datenbank abgelegt werden. Die
eigentlichen Daten werden dabei nicht mittels eines Pfades abgespeichert,
sondern werden durch  eine Prüfsumme referenziert (im Falle von ``git`` mittels
``sha1``). Im Kern lösen beide Programme also Pfade in Prüfsummen auf und
umgekehrt. Um diese Auflösung so einfach und effizient wie möglich zu machen nutzt
``git`` ein ausgeklügeltes Datenmodell, mit dem sich Änderungen
abbilden lassen. Dabei werden, anders als bei anderen
Versionsverwaltungssystemen (wie Subversion), Differenzen »on-the-fly«
berechnet und nicht zusätzlich abgespeichert, daher die Bezeichnung »stupid«.
Abgespeichert werden, wie in [@fig:git-data-model] gezeigt, nur vier
verschiedene *Objekte*:

![Vereinfachte Darstellung des Datenmodells von ``git``.](images/4/git-data-model.pdf){#fig:git-data-model width=80%}

[^TORVALDS_ZITAT]: Zitat von Linus Torvalds. Siehe auch: <https://git-scm.com/docs/git.html>

- **Blob:** Speichert Daten einer bestimmten Größe komprimiert
  ab und assoziiert diese mit einer ``sha1``--Prüfsumme des unkomprimierten
  Dateiinhaltes.
- **Tree:** Speichert *Blobs* oder weitere *Trees*, modelliert also eine Art »Verzeichnis«.
  Seine Prüfsumme ergibt sich, indem eine Prüfsumme aus den Prüfsummen der Kinder gebildet wird.
  Zusammen mit *Blobs* lässt sich bereits ein »unixoides Dateisystem« modellieren, bei dem alle
  Dateien von einem Wurzelknoten (ein *Tree* ohne Vorgänger) aus mittels eines Pfades erreichbar sind.
- **Commit:** Ein *Commit* speichert den Zustand des »Dateisystems«, indem es
  seinen Wurzelknoten referenziert. Zudem hat ein *Commit* mindestens einen
  Vorgänger (meist *Parent* genannt, kann beim initialen *Commit* leer sein) und
  speichert eine vom Nutzer verfasste Änderungszusammenfassung ab, sowie den
  Namen des Nutzers. Seine Prüfsumme ergibt sich indem eine Konkatenation der
  Wurzelprüfsumme, der Vorgängerprüfsumme, des Nutzernamen und
  der Commit--Nachricht.[^COMMIT_HASH]
- **Ref:** Eine Referenz auf einen bestimmten *Commit*. Er speichert lediglich dessen
  Prüfsumme und wird von ``git`` separat zu den eigentlichen Objekten gespeichert.
  In [@fig:git-data-model] verweist beispielsweise die Referenz ``HEAD`` stets
  auf den aktuellsten *Commit*.

[^COMMIT_HASH]: Mehr Details unter: <https://gist.github.com/masak/2415865>

Die ersten drei Objekte werden in einem MDAG
untereinander in
Relation gesetzt. Diese Struktur ergibt sich dadurch, dass bei Änderung einer
Datei in ``git`` sich sämtliche Prüfsummen der Verzeichnisse darüber ändern. In
Abbildung [@fig:git-data-model] wurde im zweiten Commit die Datei ``big.mkv``
verändert (Prüfsumme ändert sich von *QmR5AWs9* zu  *QmYYLnXi*). Als direkte
Konsequenz ändert sich die Prüfsumme des darüber liegenden Verzeichnisses, in
diesem Fall das Wurzelverzeichnis »``/``«. Bemerkenswert ist hier aber, dass auf
das neue »``/``«--Verzeichnis trotzdem auf das ``/photos``--Verzeichnis des
vorherigen *Commits* verlinkt, da dieses sich in der Zwischenzeit nicht
geändert hat.

Jede Änderung bedingt daher eine Veränderung der Prüfsumme des »``/``«--Verzeichnisses.
Daher sichert dies die Integrität aller darin enthaltenen Dateien ab. Aufgrund dessen
kann ein darüber liegender *Commit* einfach ein *Wurzelverzeichnis* referenzieren, um
eine Momentaufnahme aller Dateien zu erzeugen. Jeder *Commit* lässt in seine eigene
Prüfsumme zudem die Prüfsumme seines Vorgänger einfließen, weshalb jegliche
(absichtliche oder versehentliche) Modifikation der von ``git`` gespeicherten Daten
aufgedeckt werden kann.

Möchte ``git`` nun die Unterschiede zwischen zwei Dateiständen in zwei
verschiedenen Commits anzeigen, so geht es folgendermaßen vor:

1) Löse die Prüfsummen der beiden zu untersuchenden *Commits* auf.
2) Löse die Prüfsummen der darin enthaltenen Wurzelverzeichnisse auf.
3) Traversiere in beiden Wurzelverzeichnisse zum gewünschten *Blob*.
4) Lade beide *Blobs* und wende ein Algorithmus an, der Differenzen findet (z. B. ``diff`` von Unix).
5) Gebe Differenzen aus.

Dies ist ein signifikanter Unterschied zu zentralen Versionsverwaltungssystemen wie ``svn``, die
jeweils die aktuellste Datei ganz und ein oder mehrere »Reverse-Diff« abspeichern. Mithilfe
des *Reverse-Diff* ist es möglich die alten Stände wiederherzustellen.
Obwohl das auf den ersten Blick wie ein Vorteil von ``svn`` wirkt, so nutzt dieses
in der Praxis deutlich mehr Speicherplatz für ein Repository[^MORE_SPACE] und ist signifikant
langsamer als ``git``, insbesondere da Netzwerkzugriffe nötig sind, während
``git`` lokal arbeitet.
Insbesondere beim Erstellen von *Commits* und dem Wiederherstellen alter Stände ist ``git``
durch sein Datenmodell erstaunlich schnell. Tatsächlich speichert ``git`` auch nicht jeden *Blob*
einzeln, sondern fasst diese gelegentlich zu sogenannten *Packfiles* zusammen, welche
vergleichbar mit einem indizierten, komprimierten Archiv mehrerer Objekte sind[^PACK_FILES].

[^MORE_SPACE]: <https://git.wiki.kernel.org/index.php/GitSvnComparison#Smaller%20Space%20Requirements>
[^PACK_FILES]: Siehe auch: <https://git-scm.com/book/be/v2/Git-Internals-Packfiles>

Zusammengefasst hat ``git`` also aus architektonischer Sicht einige positive Eigenschaften:

* Objekte werden vollautomatisch und ohne weiteren Aufwand dedupliziert abgespeichert.
* Das Datenmodell ist minimalistisch gehalten und leicht für erfahrenere Benutzer verständlich.
* Nicht alle Objekte müssen beim Start von ``git`` geladen werden. Lediglich die benötigten Objekte werden von ``git`` geladen,
  was den Startvorgang beschleunigt.
* Das Bilden einer dezentralen Architektur liegt nahe, da das Datenmodell immer alle Objekte beinhalten muss.
* Alle Dateien liegen in einem separaten ``.git``--Verzeichnis und alle darin enthaltenen Internas sind
  durch die gute Dokumentation gut verständlich und nötigenfalls reparierbar. Zudem ist das Arbeitsverzeichnis
  ein ganz normales Verzeichnis, in dem der Benutzer arbeiten kann ohne von ``git`` gestört zu werden.
* Die gespeicherten Daten sind durch kryptografische Prüfsummen gegen Veränderungen geschützt.
  Ein potentieller Angreifer müsste ein *Blob* generieren, der die von ihm gewünschten Daten enthält *und*
  die gleiche Prüfsumme, wie der bereits vorhandene *Blob* erzeugt. Obwohl ``sha1`` nicht mehr empfohlen wird[^SCHNEIER_SHA1],
  wäre das ein sehr rechenintensiver Angriff.

[^SCHNEIER_SHA1]: Siehe unter anderem: <https://www.schneier.com/blog/archives/2005/02/sha1_broken.html>

Aus Sicht des Autors hat ``git`` einige, kleinere Schwächen aus architektonischer Sicht:

1) **Prüfsummenalgorithmus nicht veränderbar:** Ein MDAG--basiertes Versionsverwaltungssystem muss
   eine Abwägung zwischen der Prüfsummenlänge (länger ist typischerweise rechenaufwendiger, braucht mehr Speicher und
   ist unhandlicher für den Benutzer) und der Kollisionsresistenz der kryptografischen Prüfsumme treffen. Tritt trotzdem eine Kollision auf,
   so können Daten überschrieben werden[^VERSION_CONTROL_BY_EXAMPLE]. Unabsichtliche Kollisionen sind
   sehr unwahrscheinlich. Mit steigender Rechenleistungen wird die Berechnung einer absichtlichen Kollision aber denkbar. Leider kann ``git``
   den genutzten Prüfsummenalgorithmus (``sha1``) nicht mehr ohne hohen Aufwand ändern[^LWM_HASH]. Bei ``brig`` ist dies möglich,
   da das Prüfsummenformat von ``ipfs`` die Länge und Art des Algorithmus in der Prüfsumme selbst abspeichert.
2) **Keine nativen Renames:** ``git`` behandelt das Verschieben einer Datei als eine Sequenz aus dem Löschen und anschließendem
   Hinzufügen der Datei[^GIT_FAQ_RENAME]. Der Nachteil dabei ist, dass ``git`` dem Nutzer die Umbenennung nicht mehr als solche präsentiert,
   was für diesen verwirrend sein kann wenn er nicht sieht, dass die Datei anderswo neu hinzugefügt wurde.
   Neuere ``git`` Versionen nutzen Heuristiken, um Umbenennungen zu finden (Beispiel: Pfad wurde gelöscht, Prüfsumme der Datei tauchte
   aber anderswo auf). Diese können zwar nicht alle Fälle abdecken (umbenannt, dann modifiziert) leisten aber in der Praxis
   gute Dienste.
3) **Probleme mit großen Dateien:** Da ``git`` für die Verwaltung von Quelltextdateien entwickelt wurde, ist es nicht auf die Verwaltung großer Dateien ausgelegt.
   Jede Datei muss einmal im ``.git``--Verzeichnis und einmal im
   Arbeitsverzeichnis gespeichert werden, was den Speicherverbrauch mindestens verdoppelt. Da Differenzen zwischen Binärdateien
   nur wenig Aussagekraft haben (da Differenz--Algorithmen normal zeilenbasiert arbeiten) wird bei jeder Modifikation
   jeweils noch eine Kopie angelegt. Nutzer, die ein solches Repository »*clonen*« (also sich eine eigene Arbeitskopie besorgen wollen),
   müssen diese Kopien lokal bei sich speichern. Werkzeuge wie ``git-annex`` versuchen das Problem zu lösen, indem sie statt den Dateien,
   nur symbolische Links versionieren, die zu den tatsächlichen Dateien zeigen[^GIT_ANNEX]. Symbolische Links sind allerdings wenig portabel.
4) **Kein Tracking von leeren Verzeichnissen:** Es können keine leeren
   Verzeichnisse zu ``git`` hinzugefügt werden. Damit ein Verzeichnis von ``git``
   verfolgt werden kann, muss sich mindestens eine Datei darin befinden. Das ist
   weniger eine Einschränkung des Datenmodells von ``git``, als viel mehr ein
   kleiner Designfehler[^GIT_FAQ_EMPTY_DIR] in der Implementierung, der bisher als zu unwichtig galt,
   um korrigiert zu werden.
5) **Keine einzelne Historie pro Datei:** Es gibt nur eine gesamte *Historie*,
   die durch die Verkettung von *Commits* erzeugt wird. Bei einem Befehl wie ``git log <filename>``
   (Zeige alle Commits, in denen ``<filename>`` verändert wurde) müssen alle *Commits* betrachtet werden, auch wenn ``<filename>`` nur
   in wenigen davon tatsächlich geändert wurde. Eine mögliche Lösung wäre das
   Anlegen einer Historie für einzelne Dateien.

[^VERSION_CONTROL_BY_EXAMPLE]: Siehe auch: <http://ericsink.com/vcbe/html/cryptographic_hashes.html>
[^LWM_HASH]: Mehr zum Thema unter: <https://lwn.net/Articles/370907>
[^GIT_FAQ_RENAME]: <https://git.wiki.kernel.org/index.php/GitFaq#Why_does_Git_not_.22track.22_renames.3F>
[^GIT_FAQ_EMPTY_DIR]: <https://git.wiki.kernel.org/index.php/GitFaq#Can_I_add_empty_directories.3F>
[^GIT_FAQ_SLOW_LOG]: <https://git.wiki.kernel.org/index.php/GitFaq#Why_is_.22git_log_.3Cfilename.3E.22_slow.3F>
[^GIT_ANNEX]: <https://git-annex.branchable.com/direct_mode>

Zusammengefasst lässt sich sagen, dass ``git`` ein extrem flexibles und
schnelles Werkzeug für die Verwaltung von Quelltext und kleinen Dateien ist.
Weniger geeignet ist es für eine allgemeine Dateisynchronisationssoftware,
die auch große Dokumente effizient behandeln können muss.
