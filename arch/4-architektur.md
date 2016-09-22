# Architektur {#sec:architektur}

In diesem Kapitel wird die grundlegende Architektur von ``brig`` erklärt. Dabei
wird vor allem das »Kernstück« beleuchtet: Das zugrundeliegende Datenmodell in
dem alle Metadaten abgespeichert und in Relation gesetzt werden. Dazu ist
zuerst ein Exkurs zu den Internas von ``ipfs`` nötig und später ein Exkurs zur
Funktionsweise des freien Versionsverwaltungssystem ``git``.

Basierend darauf werden die umgebenden Komponenten beschrieben, die um den
Kern von ``brig`` gelagert sind. Am Ende des Kapitels werden zudem noch einmal alle
Einzelkomponenten in einer Übersicht gezeigt. Es wird dabei stets vom Stand des
aktuellen Prototypen ausgegangen. Mögliche Erweiterungen werden in Kapitel
[@sec:evaluation] (*Evaluation*) diskutiert. Die technische Umsetzung der
jeweiligen Komponenten hingegen wird in [@sec:implementierung]
(*Implementierung*) besprochen.

## Datenmodell von ``ipfs``

Wie bereits beschrieben ist ``brig`` ein »Frontend«, welches ``ipfs`` zum
Speichern und Teilen von Dokumenten nutzt. Die Dokumente werden dabei einzig
und allein über ihre Prüfsumme (``QmXYZ...``) referenziert. Aus
architektonischer Sicht kann man ``ipfs`` als eine verteilte Datenbank sehen, die vier simple Operationen
beherrscht:

- $Put(\text{Stream}) \rightarrow \text{Hash}$: Speichert einen endlichen Datenstrom in der Datenbank und liefert die Prüfsumme als Ergebnis zurück.
* $Get(\text{Hash}) \rightarrow \text{Stream}$: Holt einen endlichen Datenstrom aus der Datenbank der durch seine Prüfsumme referenziert wurde und gibt ihn aus.
* $Pin(\text{Hash}, \text{COUNT})$: Pinnt einen Datenstrom wenn $\text{COUNT}$ größer $0$ ist oder unpinnt ihn wenn er negativ ist.
                                  Im Falle von $0$ wird nichts getan. In jedem Fall wird der neue Status zurückgeliefert.
* $Cleanup$: Lässt einen »Garbage--Collector«[^GC_WIKI] laufen, der Datenströme aus dem lokalen Speicher löscht, die nicht gepinned wurden.

[^GC_WIKI]: Siehe auch <https://de.wikipedia.org/wiki/Garbage_Collection>

Das besondere ist, dass die ``GET`` Operation von jedem verbundenen Knoten
ausgeführt werden, wodurch die Nutzung von ``ipfs`` als verteilte Datenbank
möglich wird. Die oben geschilderte Sicht ist rein die Art und Weise in der
``ipfs`` von ``brig`` benutzt wird. Die Möglichkeiten, die ``ipfs`` bietet,
sind tatsächlich sehr viel weitreichender als »nur« eine Datenbank
bereitzustellen. Intern hat es ein mächtiges Datenmodell, das viele Relationen
wie eine Verzeichnisstruktur, Versionsverwaltung, ein alternatives World--Wide--Web oder gar eine
Blockchain[^BLOCKCHAIN_NOTE] gut abbilden kann: Der *Merkle--DAG* (Direkter
azyklischer Graph), im Folgenden kurz *MDAG* oder *Graph* genannt.
Diese Struktur ist eine Erweiterung des Merkle--Trees[@wiki:merkle], bei der ein Knoten
mehr als einen Elternknoten haben kann.

![Beispielhafter MDAG der eine Verzeichnisstruktur abbildet. Die Attribute entsprechen den ``ipfs`` Internas.](images/4/ipfs-merkledag.pdf){#fig:ipfs-merkledag}

In [@fig:ipfs-merkledag] ist ein beispielhafter Graph gezeigt, der eine
Verzeichnishierarchie modelliert. Gerichtet ist der Graph deswegen, weil es
keine Schleifen und keine Rückkanten zu den Elternknoten geben darf. Jeder
Knoten wird durch eine Prüfsumme referenziert und kann wiederum mehrere andere
Knoten über dieselbe referenzieren. Im Beispiel sieht man zwei
Wurzelverzeichnisse, bei dem das erste ein Unterverzeichnis ``/photos``
enthält, welches wiederum drei einzelne Dateien (``cat.png``, ``me.png`` und
``small.mkv``) enthält. Das zweite Wurzelverzeichnis beinhaltet ebenfalls
dieses, referenziert als zusätzliche Datei aber noch eine größere Datei namens
``big.mkv``. Die Besonderheit ist dabei, dass die Dateien jeweils in einzelne Blöcke
(``blobs``) zerlegt werden, die automatisch dedupliziert abgespeichert werden.
In der Grafik sieht man das dadurch, dass ``big.mkv`` bereits aus zwei Blöcken
von ``small.mkv`` besteht und der zweite Wurzelknoten auf ``/photos`` referenziert,
ohne dessen Inhalt zu kopieren.

Im Datenmodell von ``ipfs`` ([@benet2014ipfs, S.7 ff.] gibt es drei
unterschiedliche Strukturen:

- ``blob:`` Ein Datensatz mit definierter Größe und Prüfsumme.  Wird teilweise auch *Chunk* genannt.
- ``list:`` Eine geordnete Liste von ``blobs`` oder weiteren ``lists``. Wird benutzt um große Dateien
        in kleine, deduplizierbare Teile herunterzubrechen.
* ``tree:`` Ein Abbildung von Dateinamen zu Prüfsummen.
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
Dateien und Verzeichnisse direkt in ``ipfs`` gespeichert, so wäre diese Teilung
nicht mehr gegeben, da trotzdem alle Daten in einem gemeinsamen Speicher
liegen. Dies hätte zur Folge, dass ein Angreifer zwar nicht die verschlüsselten
Daten lesen könnte, aber problemlos die Verzeichnisstruktur betrachten könnte,
sobald er die Prüfsumme des Wurzelknotens hat. Dies würde den
Sicherheitsversprechen von ``brig`` widersprechen. Abgesehen davon wurde ein
eigenes Datenmodell entwickelt, um mehr Freiheiten beim Design zu haben.

Zusammengefasst lässt sich also sagen, dass ``ipfs`` in dieser Arbeit als
Content--Adressed--Storage Datenbank verwendet wird, die sich im Hintergrund
um die Speicherung von Datenströmen und deren Unterteilung in kleine Blöcke
mittels *Chunking* kümmert. Die Aufteilung geschieht dabei entweder simpel,
indem die Datei in gleichgröße Blöcke unterteilt wird, oder indem ein intelligenter
Algorithmus wie Rabin--Karp--Chunking[@wiki:rabin-karp] angewandt wird.

## Datenmodell von ``git``

Der interne Aufbau von ``brig`` ist relativ stark von ``git`` inspiriert.
Deshalb werden im Folgenden immer wieder Parallelen zwischen den beiden
Systemen gezogen, um die jeweiligen Unterschiede aufzuzeigen und zu erklären
warum ``brig`` letztlich einige wichtige Differenzen aus architektonischer
Sicht aufweist. Was die Benutzbarkeit angeht, soll allerdings aufgrund der
relativ unterschiedlichen Ziele kein Vergleich gezogen werden.

Im Folgenden ist ein gewisses Grundwissen über ``git`` nützlich. Es wird bei
Unklarheiten die Lektüre des Buches *Git --- Verteile Versionsverwaltung für Code
und Dokumente*[@git] empfohlen. Alternativ bietet auch die offizielle
Projektdokumentation[^GITBOOK] einen sehr guten Überblick. Aus Platzgründen
wird an dieser Stelle über eine gesonderte Einführung verzichtet, da es
diese in ausreichender Menge frei verfügbar gibt.

[^GITBOOK]: Offizielle Projektdokumentation von ``git``: <https://git-scm.com/doc>

Kurz beschrieben sind beide Projekte »*stupid content
tracker*«[^TORVALDS_ZITAT], die Änderungen an tatsächlichen Dateien auf
Metadaten abbilden, welche in einer dafür geeigneten Datenbank ablegen. Die
eigentlichen Daten werden dabei nicht mittels eines Pfades abgespeichert,
sondern werden durch  eine Prüfsumme referenziert (im Falle von ``git`` mittels
``sha1``). Im Kern lösen beide Programme also Pfade in Prüfsummen auf und
umgekehrt. Um diese Auflösung einfach und effizient möglich zu machen nutzte
``git`` ein ausgeklügeltes Datenmodell, mit dem sich Änderungen natürlich
abbilden lassen. Dabei werden, anders als bei anderen
Versionsverwaltungssystemen (wie Subversion), Differenzen »on-the-fly«
berechnet und nicht separat abgespeichert (daher die Bezeichnung »stupid«).
Abgespeichert werden, wie in [@fig:git-data-model] gezeigt, nur vier
verschiedene *Objekte*:

![Vereinfachte Darstellung des Datenmodell von ``git``.](images/4/git-data-model.pdf){#fig:git-data-model width=80%}

[^TORVALDS_ZITAT]: Zitat von Linus Torvalds. Siehe auch: <https://git-scm.com/docs/git.html>

- **Blob:** Speichert Daten einer bestimmten Größe (möglicherweise) komprimiert
  ab und assoziiert diese mit einer ``sha1``--Prüfsumme des (unkomprimierten)
  Dateiinhaltes.
- **Tree:** Speichert *Blobs* oder weitere *Trees*, modelliert also eine Art »Verzeichnis«.
  Seine Prüfsumme ergibt sich, indem eine Prüfsumme aus den Prüfsummen der Kinder gebildet wird.
  Zusammen mit *Blobs* lässt sich bereits ein »unixoides Dateisystem« modellieren, bei dem alle
  Dateien von einem Wurzelknoten (ein *Tree* ohne Vorgänger) aus mittels eines Pfades erreichbar sind.
- **Commit:** Ein *Commit* speichert den Zustand des »Dateisystems«, indem es
  seinen Wurzelknoten referenziert. Zudem hat ein *Commit* mindestens einen
  Vorgänger (meist *Parent* genannt, kann beim initialen *Commit* leer sein) und
  speichert eine vom Nutzer verfasste Änderungszusammenfassung ab, sowie den
  Namen des Nutzers. Seine Prüfsumme ergibt sich indem eine Konkatenation von
  Wurzelprüfsumme, Vorgängerprüfsumme, Nutzernamen und
  Commit--Nachricht.[^COMMIT_HASH]
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
Konsequenz ändert sich die Prüfsumme des darüber liegenden Verzeichnisses (in
diesem Fall das Wurzelverzeichnis »``/``«). Bemerkenswert ist hier aber, dass auf
das das neue »``/``«--Verzeichnis trotzdem auf das ``/photos``--Verzeichnis des
vorherigen *Commits* verlinkt, da dieses sich in der Zwischenzeit nicht
geändert hat.

Jede Änderung bedingt daher eine Veränderung der Prüfsumme des »``/``«--Verzeichnisses.
Daher sichert dies die Integrität aller darin enthaltenen Dateien ab. Aufgrund dessen
kann ein darüber liegender *Commit* einfach ein *Wurzelverzeichnis* referenzieren, um
eine Momentaufnahme der Daten zu erzeugen. Jeder *Commit* lässt in seine eigene
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

Dies ist ein signifikanter Unterschied zu Versionsverwaltungssystemen wie ``svn``, die
jeweils die aktuellste Datei ganz und ein oder mehrere »Reverse-Diff« abspeichern. Mithilfe
des *Reverse-Diff* ist es möglich die alten Stände wiederherzustellen.
Obwohl das auf den ersten Blick wie ein Vorteil von ``svn`` wirkt, so nutzt dieses
in der Praxis deutlich mehr Speicherplatz für ein Repository[^MORE_SPACE] und ist signifikant
langsamer als ``git`` (insbesondere da Netzwerkzugriffe nötig sind, während ``git`` lokal arbeitet).
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
  durch die gute Dokumentation gut zugänglich und nötigenfalls reparierbar. Zudem ist das Arbeitsverzeichnis
  ein ganz normales Verzeichnis, in dem der Benutzer arbeiten kann ohne von ``git`` gestört zu werden.
* Die gespeicherten Daten sind durch kryptografische Prüfsummen gegen Veränderungen geschützt.
  Ein potentieller Angreifer müsste ein *Blob* generieren, der die von ihm gewünschten Daten enthält *und*
  die gleiche Prüfsumme, wie der bereits vorhandene *Blob* erzeugt. Obwohl ``sha1`` nicht mehr empfohlen wird[^SCHNEIER_SHA1],
  wäre das ein sehr rechenintensiver Angriff.

[^SCHNEIER_SHA1]: Siehe unter anderem: <https://www.schneier.com/blog/archives/2005/02/sha1_broken.html>

Aus Sicht des Autors hat ``git`` einige, kleinere Schwächen aus architektonischer Sicht:

1) **Prüfsummenalgorithmus nicht veränderbar:** Ein auf einem MDAG basierenden Versionsverwaltungssystem muss
   eine Abwägung zwischen der Prüfsummenlänge (länger ist typischerweise rechenaufwendiger, braucht mehr Speicher und
   ist unhandlicher für den Benutzer) und der Kollisionsresistenz der Prüfsumme. Tritt trotzdem eine Kollision auf,
   so können Daten überschrieben werden.[^VERSION_CONTROL_BY_EXAMPLE] Solche Kollisionen sind zwar heutzutage noch
   sehr unwahrscheinlicher, werden mit steigender Rechenleistungen aber wahrscheinlicher. Leider kann ``git``
   den genutzten Prüfsummenalgorithmus (``sha1``) nicht mehr ohne hohen Aufwand ändern[^LWM_HASH]. Bei ``brig`` ist dies möglich,
   da das Prüfsummenformat von *IPFS* die Länge und Art des Algorithmus in der Prüfsumme selbst abspeichert.
2) **Keine nativen Renames:** ``git`` behandelt das Verschieben einer Datei als eine Sequenz aus dem Löschen und anschließendem
   Hinzufügen der Datei[^GIT_FAQ_RENAME]. Der Nachteil dabei ist, dass ``git`` dem Nutzer die Umbenennung nicht mehr als solche präsentiert,
   was für diesen verwirrend sein kann wenn er nicht sieht, dass die Datei anderswo neu hinzugefügt wurde.
   Neuere ``git`` Versionen nutzen probabilistische Methoden, um Umbenennungen zu finden (Pfad wurde gelöscht, Prüfsumme der Datei tauchte
   aber anderswo auf). Diese können zwar nicht alle Fälle abdecken (umbenannt, dann modifiziert) leisten aber in der Praxis
   zugegebenermaßen gute Dienste.
3) **Probleme mit großen Dateien:** Da ``git`` für die Verwaltung von Quelltextdateien entwickelt wurde, ist es nicht auf die Verwaltung großer Dateien ausgelegt.
   Jede Datei muss dann einmal im ``.git``--Verzeichnis und einmal im
   Arbeitsverzeichnis gespeichert werden, was den Speicherverbrauch mindestens verdoppelt. Da Differenzen zwischen Binärdateien
   nur wenig Aussagekraft haben (da Differenz--Algorithmen normal zeilenbasiert arbeiten) wird bei jeder Modifikation
   jeweils noch eine Kopie angelegt. Nutzer, die ein solches Repository »*clonen*« (also sich eine eigene Arbeitskopie besorgen wollen),
   müssen zudem alle Kopien lokal zu sich kopieren. Werkzeuge wie ``git-annex`` versuchen das Problem zu lösen, indem sie statt den Dateien,
   nur symbolische Links versionieren, die zu den tatsächlichen Dateien zeigen[^GIT_ANNEX]. Symbolische Links sind allerdings wenig portabel,
   weshalb diese Lösung vom Autor eher als »Hack« angesehen wird.
4) **Kein Tracking von leeren Verzeichnissen:** Es können keine leeren
   Verzeichnisse zu ``git`` hinzugefügt werden. Damit ein Verzeichnis von ``git``
   verfolgt werden kann, muss sich mindestens eine Datei darin empfinden. Das ist
   weniger eine Einschränkung des Datenmodells von ``git``, als viel mehr ein
   kleinerer Designfehler[^GIT_FAQ_EMPTY_DIR], der bisher als zu unwichtig galt,
   um korrigiert zu werden.
5) **Keine einzelne History pro Datei:** Es gibt nur eine gesamte *History*,
   die durch die Verkettung von *Commits* erzeugt wird. Bei einem Befehl wie ``git
   log <filename>`` (»Zeige alle Commits, in denen ``<filename>`` verändert
   wurde«) müssen alle *Commits* betrachtet werden, auch wenn ``<filename>`` nur
   in wenigen davon tatsächlich geändert wurde. Eine mögliche Lösung wäre das
   Anlegen einer *History* für einzelne Dateien.

[^VERSION_CONTROL_BY_EXAMPLE]: Siehe auch: http://ericsink.com/vcbe/html/cryptographic_hashes.html
[^LWM_HASH]: Mehr zum Thema unter: <https://lwn.net/Articles/370907>
[^GIT_FAQ_RENAME]: <https://git.wiki.kernel.org/index.php/GitFaq#Why_does_Git_not_.22track.22_renames.3F>
[^GIT_FAQ_EMPTY_DIR]: <https://git.wiki.kernel.org/index.php/GitFaq#Can_I_add_empty_directories.3F>
[^GIT_FAQ_SLOW_LOG]: <https://git.wiki.kernel.org/index.php/GitFaq#Why_is_.22git_log_.3Cfilename.3E.22_slow.3F>
[^GIT_ANNEX]: <https://git-annex.branchable.com/direct_mode>

Zusammengefasst lässt sich sagen, dass ``git`` ein extrem flexibles und
schnelles Werkzeug für die Verwaltung von Quelltext und kleinen Dateien ist,
aber weniger geeignet für eine allgemeine Dateisynchronisationssoftware ist,
die auch große Dokumente effizient behandeln können muss.

## Datenmodell von ``brig``

``git`` ist primär ein Werkzeug das von Entwicklern und technisch versierten
Nutzern eingesetzt wird. ``brig`` hingegen soll möglichst generell von allen
Anwendern als Synchronisationslösung eingesetzt werden, weswegen die Funktionsweise der Software
zugrundeliegenden Konzepte möglichst einfach nachvollziehbar sein sollen.
Die Einsatzziele unterscheiden sich also: ``git`` ist primär eine
Versionsverwaltugssoftware, mit der man auch synchronisieren kann. ``brig``
hingegen ist eine Synchronisationssoftware, die auch Versionierung beherrscht.
Aus diesem Grund wurde das Datenmodell von ``git`` für den Einsatz in ``brig``
angepasst und teilweise vereinfacht. Die Hauptunterschiede sind dabei wie
folgt:

- **Strikte Trennung zwischen Daten und Metadaten:** Metadaten werden von ``brig``'s
  Datenmodell verwaltet, während die eigentlichen Daten werden lediglich per Prüfsumme
  referenziert und von einem Backend (aktuell *IPFS*) gespeichert werden.
  So gesehen ist  ``brig`` ein Versionierungsaufsatz für ``ipfs``.
* **Lineare Versionshistorie:** Jeder *Commit* hat maximal einen Vorgänger und
  exakt einen Nachfolger. Dies macht die Benutzung von *Branches*[^BRANCH_EXPL]
  unmöglich, bei der ein *Commit* zwei Nachfolger haben kann, beziehungsweise
  sind auch keine Merge--Commits möglich, die zwei Vorgänger besitzen. Diese
  Vereinfachung ist nicht von der Architektur vorgegeben und könnte nachgerüstet
  werden. Allerdings hat die Benutzung dieses Features potenzielles
  »Verwirrungspotenzial«[^DETACHED_HEAD] für gewöhnliche Nutzer, die gedanklich
  von einer linearen Historie ihrer Dokumente ausgehen.
* **Synchronisationspartner müssen keine gemeinsame Historie haben:[^DOUBLE_ROOT]**
  Es würde bei ``brig`` davon ausgegangen, dass unterschiedliche
  Dokumentensammlung miteinander synchronisiert werden sollen, während bei
  ``git`` davon ausgegangen wird, dass eine einzelne Dokumentensammlung immer
  wieder modifiziert und zusammengeführt wird. Haben die Partner keine gemeinsame
  Historie, wird einfach angenommen, dass alle Dokumente synchronisiert werden müssen.
  Aus diesen Grund kennt ``brig`` auch keine ``clone`` und ``pull``--Operation.
  Diese werden durch ``brig sync <with>`` ersetzt.

[^BRANCH_EXPL]: *Branches* dienen bei ``git`` um einzelne Features oder Fixes separat entwickeln zu können. (TODO: Schaubild eher?)
[^DETACHED_HEAD]: So ist es bei ``git`` relativ einfach möglich in den sogenannten *Detached HEAD* Modus zu kommen, in dem durchaus Daten verloren gehen können.
[^DOUBLE_ROOT]: Streng genommen ist dies bei ``git`` auch nicht nötig, allerdings eher unüblich und braucht spezielle Kenntnisse. (TODO: ref)


![Das Datenmodell von ``brig``](images/4/brig-data-model.pdf){#fig:brig-data-model}

[@fig:brig-data-model] zeigt das oben verwendete Beispiel in ``brig``'s
Datenmodell. Es werden die selben Objekttypen verwendet, die auch ``git``
verwendet:

* **File:** Speichert die Metadaten einer einzelnen, regulären Datei. Zu den Metadaten gehört die aktuelle Prüfsumme,
  die Dateigröße, der letzte Änderungszeitpunkt und der kryptografische Schlüssel mit dem die Datei verschlüsselt ist.
  Anders als ein *Blob* speichert ein *File* die Daten nicht selbst, sondern referenziert diese nur im *ipfs*--Backend.
* **Directory:**  Speichert wie ein *Tree* einzelne *Files* und weitere *Directories*. Die Prüfsumme des Verzeichnisses $H_{directory}$ ergibt sich auch hier
  aus der XOR--Verknüpfung ($\oplus$) der Prüfsumme des Pfades $H_{path}$ mit den den Prüfsummen der direkten Nachfahren $x$: $$
	H_{directory}(x) = \begin{cases}
			H_{path} & \text{für } x = () \\
			x_1 \oplus f(x_{(x_2, \ldots, x_n)}) & \text{sonst}
		   \end{cases}
  $$

    Die Verwendung der XOR--Verknüpfung hat dabei den Vorteil, dass sie selbstinvers und kommutativ ist. Wendet man sie also zweimal an,
    so erhält man das neutrale Element $0$. Analog dazu führt die Anwendung auf ein vorheriges Ergebnis wieder zur ursprünglichen Eingabe:

    $$x \oplus x = 0 \text{  (Auslöschung)}$$
    $$y = y \oplus x \oplus x = x \oplus y \oplus x = x \oplus x \oplus y$$

    Diese Eigenschaft kann man sich beim Löschen einer Datei zunutze machen,
    indem die Prüfsumme jedes darüber liegenden Verzeichnisses mit der Prüfsumme
    der zu löschenden Datei XOR--genommen wird. Der resultierende Graph hat die gleichen Prüfsumme wie vor
    dem Einfügen der Datei.

* **Commits:** Analog zu ``git``, dienen aber bei ``brig`` nicht nur der
  logischen Kapselung von mehreren Änderungen, sondern werden auch automatisiert
  von der Software nach einen bestimmten Zeitintervall erstellt. Daher ist ihr
  Zweck eher mit den *Snapshots* vieler Backup--Programme vergleichbar, welche
  dem Nutzer einen Sicherungspunkt zu einem bestimmten Zeitpunkt in der
  Vergangenheit bietet. Als Metadaten speichert er als Referenz die Prüfsumme des
  Wurzelverzeichnisses, eine Commit--Nachricht sowie dessen Autor und eine
  Referenz auf seinen Vorgänger. Aus diesen Metadaten wird durch Konkatenation
  derselben eine weitere Prüfsumme errechnet, die den Commit selbst eindeutig
  referenziert. In diese Prüfsumme ist nicht nur die Integrität des aktuellen
  Standes gesichert, sondern
  auch aller Vorgänger.
* **Refs:** Analog zu ``git`` dienen sie dazu bestimmten *Commits* einen Namen
  zu geben. Es gibt zwei vordefinierte Referenzen, welche von ``brig``
  aktualisiert werden: ``HEAD``, welche auf den letzten vollständigen *Commit*
  zeigt und ``CURR``, welche auf den aktuellen *Commit* zeigt (meist dem *Staging
  Commit*, dazu später mehr). Da es keine Branches gibt, ist eine Unterscheidung zwischen
  *Refs* und *Tags* wie bei ``git`` nicht mehr nötig.

![Jeder Knoten muss von aktuellen Wurzelverzeichnis neu aufgelöst werden, selbst wenn nur der Elternknoten gesucht wird.](images/4/path-resolution.pdf){#fig:path-resolution width=90%}

*Directories* und *Files* speichern zudem zwei weitere gemeinsame Attribute:

* Ihren eigenen Namen und den vollen Pfad des darüber liegenden Knoten. Zusammen ergibt dieser den vollen
  Pfad der Datei oder des Verzeichnisses. Dieser Pfad ist nötig, um den jeweiligen Elternknoten zu erreichen.
  In einem gerichteten, azyklischen Graphen darf es keine Rückkanten nach »oben« geben, deswegen scheidet
  die direkte Referenzierung des Elternknotens mittels seiner Prüfsumme aus. Wie in [@fig:path-resolution] gezeigt
  ist es daher beispielsweise den Elternknoten eines beliebigen Knotens vom aktuellen Wurzelknoten neu aufzulösen.
* Eine eindeutige Nummer (``UID``), welche die Datei oder das Verzeichnis
  eindeutig kennzeichnet. Diese Nummer bleibt auch bei Modifikation und
  Verschieben der Datei gleich und kann daher genutzt werden, Neben der Prüfsumme
  (referenziert einen bestimmten Inhalt) und dem Pfad (referenziert eine
  bestimmte Lokation) ist die Nummer ein weiterer Weg eine Datei zu referenzieren
  (referenziert ein veränderliches »Dokument«) und ist grob mit dem Konzept einer
  INode--Nummer bei Dateisystemen[^INODE] vergleichbar.

[^INODE]: Siehe auch: https://de.wikipedia.org/wiki/Inode

![Jede Datei und Verzeichnis besitzt eine Liste von Checkpoints](images/4/file-history.pdf){#fig:file-history width=50%}

Davon abgesehen fällt auf dass zwei zusätzliche Strukturen eingeführt wurden:

* **Checkpoints:** Jeder Datei ist über ihre ``UID`` ein Historie von sogenannten *Checkpoints* zugeordnet.
  Jeder einzelne dieser Checkpoints beschreiben eine atomare Änderung an der Datei. Da keine
  partiellen Änderungen möglich sind (wie ``git diff``), müssen nur vier verschiedene Operation
  unterschieden werden: ``ADD`` (Datei wurde initial oder erneut hinzugefügt), ``MODIFY`` (Prüfsumme hat sich verändert),
  ``MOVE`` (Pfad hat sich geändert) und ``REMOVE`` (Datei wurde entfernt). Ein beispielhafte Historie findet sich
  in [@fig:file-history].
  Jeder Checkpoint kennt den Zustand der Datei zum Zeitpunkt der Modifikation,
  sowie einige Metadaten wie ein Zeitstempel, der Dateigröße, dem Änderungstyp,
  dem Urheber der Änderung und seinem Vorgänger. Der Vorteil einer dokumentabhängigen Historie
  ist die Möglichkeit umbenannte Dateien zu erkennen, sowie Dateien zu erkennen, die gelöscht und dann
  wieder hinzugefügt worden sind. Ein weiterer Vorteil ist, dass zur Ausgabe der Historie einer Datei,
  nur die *Checkpoints* betrachtet werden. Es muss nicht wie bei ``git`` jeder *Commit* betrachtet werden, um
  nachzusehen ob eine Änderung an einer bestimmten Datei stattgefunden hat.

* **Stage Commit:** Es existiert immer ein sogenannter *Staging Commit*. Dieser beinhaltet alle Knoten im Graph,
  die seit dem letzten »vollwertigen« Commit modifiziert worden sind.
  [@fig:staging-area] zeigt den Staging--Bereich von ``git`` und ``brig`` im Vergleich. Im Falle von ``git`` handelt
  es sich um eine eigene, vom eigentlichen Graphen unabhängige, Datenstruktur, in die der Nutzer mittels ``git add``
  explizit Dokumente aus dem Arbeitsverzeichnis hinzufügt. Bei ``brig`` hingegen gibt es kein Arbeitsverzeichnis.
  Die Daten kommen entweder von einer externen Datei, welche mit ``brig add <filename>``{.bash} dem Staging--Bereich hinzugefügt wurde,
  oder die Datei wurde direkt im FUSE--Layer (TODO: später mehr oder vorher erklären?) von ``brig`` modifiziert.
  In beiden Fällen wird die neue oder modifizierte Datei in den *Staging--Commit* eingegliedert, welcher
  aus diesem Grund eine veränderliche Prüfsumme besitzt und nach jeder Modifikation auf einen anderes Wurzelverzeichnis verweist.

[^CHATTR_NOTE]: In Zukunft ist ein weiterer Zustand ``CHATTR`` möglich, welche die Änderung eines Dateiattributes abbildet.

![Der Staging Bereich im Vergleich zwischen ``git`` und ``brig``](images/4/staging-area.pdf){#fig:staging-area}

Da ein *Commit* nur ein Vorgänger haben kann, muss ein anderer Mechanismus
eingeführt werden, um die Synchronisation zwischen zwei Partnern festzuhalten.
Bei ``git`` wird dies mittels eines sogenannten Merge--Commit gelöst, welcher
aus den Änderungen der Gegenseite besteht. Hier wird das Konzept eines
*Merge--Points* eingeführt. Innerhalb eines *Commit* ist das ein spezieller
Marker, der festhält mit wem synchronisiert wurde und mit welchen Stand er zu
diesem Zeitpunkt hatte. Bei einer späteren Synchronisation muss daher lediglich
der Stand zwischen dem aktuellen *Commit* (»``CURR``«) und dem letzten
Merge--Point verglichen werden. Basierend auf diesen Vergleich wird ein neuer
*Commit* (der *Merge--Commit*) erstellt, der alle (möglicherweise nach der
Konfliktauflösung zusammengeführten) Änderungen des Gegenübers enthält und als
neuer *Merge--Point* dient.

TODO: Noch folgende Punkte verarzten:

Problem: Metadaten wachsen schnell, Angreifer könnte sehr viele kleine änderungen sehr schnell machen.
Mögliche Lösung : Delayed Checkpoints, Checkpoint Squashing, Directory Checkpoints?

### Operationen auf dem Datenmodell

Die Gesamtheit aller *Files*, *Directories*, *Commits*, *Checkpoints* und
*Refs* wird im Folgenden als *Store* bezeichnet. Da ein *Store* nur aus
Metadaten besteht, ist er selbst leicht übertragbar. Er kapselt den Objektgraph
und kümmert sich, um die Verwaltung auf der Objekte. Basierend auf dem *Store*
werden insgesamt 11 verschiedene atomare Operationen implementiert, die jeweils
den aktuellen Graphen nehmen und einen neuen und (mit Ausnahme von ``LIST``, ``CAT``,
``LOG`` und ``HISTORY``) veränderten Graphen erzeugen.

Es gibt sechs Operationen, die die Benutzung des Graphen als gewöhnliches Dateisystem ermöglichen:

[^SYSCALL_NOTE]: Von der Funktionsweise sind diese angelehnt an die entsprechenden »Syscall« im POSIX--Standard.
               Dies sollte im späteren Verlauf die Implementierung des FUSE--Layers erleichtern.

``STAGE``: Fügt ein Dokument dem Staging--Bereich hinzu oder aktualisiert die
Version eines vorhandenen Dokuments. Der Pfad entscheidet dabei wo das Dokument
eingefügt wird, bzw. welches existierendes Dokument modifiziert wird.
[@fig:op-add] zeigt die Operationen, die zum Einfügen einer Datei notwendig
sind. Als Vorarbeit muss allerdings erst die gesamte Datei gelesen werden und
in das ``ipfs``--Backend eingefügt werden. Die Datei wird zudem gepinnt. Als
Ergebnis dieses Teilprozesses wird die Größe und Prüfsumme der
unverschlüsselten und unkomprimierten Datei zurückgeliefert.
Handelt es sich bei dem hinzuzufügenden Objekt um ein Verzeichnis, wird der gezeigte Prozess
für jede darin enthaltene Datei wiederholt.

![Die Abfolge der ``STAGE``-Operation im Detail](images/4/op-add){#fig:op-add}

TODO: wurde pin schon erklärt?

``REMOVE:`` Entfernt eine vorhandene Datei aus dem Staging--Bereich. Der Pin
der Datei oder des Verzeichnisses und all seiner Kinder werden entfernt. Die
gelöschten Daten werden möglicherweise beim nächsten Durchgang der ``CLEANUP`` Operation aus
dem lokalen Speicher entfernt.
Wie in [@fig:op-remove] gezeigt wird, wird die Prüfsumme der entfernten Datei
aus den darüber liegenden Verzeichnissen herausgerechnet. Handelt es sich dabei
um ein Verzeichnis, wird der Prozess *nicht* rekursiv für jedes Unterobjekt
ausgeführt. Es genügt die Prüfsumme des zu löschenden Verzeichnisses aus den
Eltern herauszurechnen und die Kante zu dem Elternknoten zu kappen.

TODO: Grafik für remove (rekursiv für teilbaum)

``LIST:`` Entspricht konzeptuell dem Unix--Werkzeug ``ls``. Besucht alle Knoten unter einem bestimmten Pfad
rekursiv (breadth-first) und gibt diese aus.

``MKDIR:`` Erstellt ein neues, leeres Verzeichnis. Die Prüfsumme des neuen
Verzeichnisses (ergibt sich aus dem Pfad des neuen Verzeichnisses) wird in die
Elternknoten eingerechnet. Die Referenz auf das Wurzelverzeichnis wird im
Staging--Commit angepasst.

Eventuell müssen noch dazwischen liegende
Verzeichnisse erstellt werden. Diese werden von oben nach unten, Stück für
Stück mit den eben beschriebenen Prozess erstellt.

TODO: Grafik für mkdir falls nötig ist?

``MOVE:`` Verschiebt eine Quelldatei oder Verzeichnis zu einem
Zielpfad. Es muss eine Fallunterscheidung getroffen wird, je nachdem ob
und welcher Knoten im Zielpfad vorhanden ist:

1) Ziel existiert noch nicht: Quelldaten werden zum neuen Pfad verschoben.
2) Ziel existiert und ist eine Datei: Vorgang wird abgebrochen, es sei denn die Aktion wird »forciert«.
3) Ziel existiert und ist ein Verzeichnis: Quelldaten werden direkt unter das Zielverzeichnis verschoben.

In jedem Fall entspricht diese Operation technisch dem sequentiellen Ausführen der
Operationen ``REMOVE`` und ``ADD``. Im Unterschied dazu ist sie im Ganzen
atomar und erstellt einen Checkpoint für alle verschobenen Knoten einen
Checkpoint mit dem Typen ``MOVED``.

``CAT:`` Gibt ein Dokument auf einen Datenstrom aus. Der Name lehnt sich dabei an
das Unix Tool ``cat`` an, welches ebenfalls Dateien ausgibt. Es wird lediglich
wie in [@fig:path-resolution] gezeigt der gesuchte Knoten per Pfad aufgelöst
und der darin enthaltene Hash wird vom ``ipfs``--Backend aufgelöst. Die
ankommenden Daten werden noch entschlüsselt und dekomprimiert bevor sie dem
Nutzer präsentiert werden.

Neben den obenstehenden Operationen, gibt es noch fünf weitere Operationen, die
zur Versionskontrolle dienen und in dieser Form normalerweise nicht von
Dateisystemen implementiert werden:

``UNSTAGE:`` Entfernt ein Dokument aus dem Staging--Bereich und setzt den Stand
auf den zuletzt bekannten Wert zurück (der Stand innerhalb von ``HEAD``). Die
Prüfsumme des entfernten Dokumentes wird aus den Elternknoten herausgerechnet
und dafür die die alte Prüfsumme wieder eingerechnet.

*Anmerkung:* Die Benennung der Operationen ``STAGE``, ``UNSTAGE`` und
``REMOVE`` ist anders als bei semantisch gleichen ``git``--Werkzeugen  ``add``,
``reset`` und ``rm``. Die Benennung nach dem ``git``--Schema ist verwirrend, da
``git add`` auch modifizierte Dateien »hinzufügt« (als auch neue Dateien) und
nicht das Gegenteil von ``git rm`` ist.[^GIT_FAQ_RM].

[^GIT_FAQ_RM]: Selbstkritik des ``git``--Projekts: <https://git.wiki.kernel.org/index.php/GitFaq#Why_is_.22git_rm.22_not_the_inverse_of_.22git_add.22.3F>

``COMMIT:`` Erstellt einen neuen Commit, basierend auf den Inhalt des
*Staging--Commits* (siehe auch [@fig:op-commit] für eine Veranschaulichung).
Dazu werden die Prüfsummen des aktuellen und des Wurzelverzeichnisses im
letzten Commit (``HEAD``) verglichen. Unterscheiden sie sich nicht, wird
abgebrochen, da keine Veränderung vorliegt. Im Anschluss wird der
*Staging--Commit* finalisiert, indem die angegebene *Commit--Message* und der
Autor in den Metadaten des Commits gesetzt werden. Basierend darauf wird die
finale Prüfsumme berechnet und der entstandene Commit abgespeichert. Ein neuer
*Staging-Commit* wird erstellt, welcher im unveränderten Zustand auf das selbe
Wurzelverzeichnis zeigt wie der vorige. Zuletzt werden die Referenzen von
``HEAD`` und ``CURR`` jeweils um ein Platz nach vorne verschoben.

![Die Abfolge der ``COMMIT``-Operation im Detail](images/4/op-commit.pdf){#fig:op-commit}

``CHECKOUT:`` Stellt einen alten Stand wieder her. Dabei kann die Operation
eine alte Datei oder ein altes Verzeichnis wiederherstellen (basierend auf der
alten Prüfsumme) oder den Stand eines gesamten, in der Vergangenheit liegenden
Commits wiederherstellen.

Im Gegensatz zu ``git`` ist es allerdings nicht vorgesehen in der
Versionshistorie »herumzuspringen«. Soll ein alter *Commit* wiederhergestellt
werden, so wird ein neuer *Commit* erzeugt, welcher den aktuellen Stand so
verändert, dass er dem gewünschten, alten Stand entspricht. Das Verhalten von
``brig`` entspricht an dieser Stelle also nicht dem Namensvetter ``git
checkout`` sondern eher dem wiederholten Anwenden von ``git revert`` zwischen
dem aktuellen und dem Nachfolger des gewünschten Commits.

Begründet ist dieses Verhalten darin, dass kein sogenannter »Detached
HEAD«--Zustand entstehen soll, da dieser für den Nutzer verwirrend sein kann.
Dieser Zustand kann in ``git`` erreicht werden, indem man in einen früheren
*Commit* springt ohne einen neuen *Branch* davon abzuzweigen. Der ``HEAD``
zeigt dann nicht mehr auf einen benannten Branch, sondern auf die Prüfsumme des
neuen Commits, der vom Nutzer nur noch durch die Kenntnis derselben erreichbar
ist.
Macht man in diesem Zustand Änderungen ist es prinzipiell möglich die
geänderten Daten zu verlieren. (TODO: ref) Um das zu vermeiden, setzt ``brig``
darauf die Historie stets linear und unveränderlich zu halten, auch wenn das
keine Einschränkung der Architektur an sich darstellt.

TODO: Grafik für CHECKOUT

``LOG/HISTORY:`` Zeigt alle Commits, bis auf den Staging Commits. Begonnen wird
die Ausgabe mit ``HEAD`` und beendet wird sie mit dem initial Commit.
Alternativ kann auch die Historie eines einzelnen Verzeichnisses oder einer
Datei angezeigt werden. Dabei werden statt Commits alle Checkpoints dieser
Datei, beginnend mit dem aktuellsten ausgegeben.

``STATUS:`` Zeigt den Inhalt des aktuellen Staging--Commits (analog zu ``git
status``) und damit aller geänderten Dateien und Verzeichnisse im Vergleich zu
``HEAD``. Anmerkung: Es gibt keine eigene ``DIFF``--Operationen, da es keine
partiellen Diffs gibt. Diese kann durch ``STATUS`` und ``HISTORY`` ersetzt
werden.

## Synchronisation

Ähnlich wie ``git`` speichert ``brig`` für jeden Nutzer seinen zuletzt
bekannten *Store* ab. Mithilfe dieser Informationen können dann
Synchronisationsentscheidungen größtenteils automatisiert getroffen werden.
Welcher *Store* dabei lokal zwischengespeichert wird, entscheiden die Einträge
in die sogenannte *Remote--Liste*.

### Die Remote--Liste

Jeder Teilnehmer mit dem synchronisiert werden soll, muss zuerst in eine
spezielle Liste von ``brig`` eingetragen werden, damit dieser dem System
bekannt wird. Dies ist vergleichbar mit der Liste die ``git remote -v``
erzeugt: Eine Zuordnung eines menschenlesbarem Namen zu einer eindeutigen
Referenz zum Synchronisationspartner (Im Falle von ``git`` eine URL, bei
``brig`` eine Prüfsumme). Wie später gezeigt wird, ist dieses explizite
Hinzufügen des Partners eine Authentifizierungsmaßnahme die bewusst eingefügt
wurde und durch die automatische Entdeckung von Synchronisationspartnern zwar
unterstützt, aber nicht ersetzt werden kann[@sec:user-management].

![Beispielhafte Remote Liste mit vier Repositories und verschienden Synchronisationsrichtungen.](images/4/multiple-repos.pdf){#fig:multiple-repos}

Wie in [@fig:multiple-repos] gezeigt, kann jeder Knoten mit einem anderen
Knoten synchronisieren, der in der Liste steht, da von diesen jeweils der
zuletzt bekannte Store übertragen wurde. Die Synchronisation ist dabei, wie ein
``git pull``, nicht bidirektional. Lediglich die eigenen Daten werden mit den
Fremddaten zusammengeführt. Es gibt prinzipbedingt keine direkte Analogie zu
``git push``, da jedes Repository aus Sicherheitsgründen die Hoheit über den
Zustand seiner Daten behält. In der Grafik wird zudem ein spezieller Anwendungsfall
gezeigt: Das Repository ``rabbithole@wonderland`` ist eine gemeinsame Datenablage für
beide Parteien, die stets online verfügbar ist[^HOST]. Dieses kann durch ein Skript
automatisiert stets die Änderungen aller bekannten Teilnehmer synchronisieren und
auch weitergeben, wenn der eigentliche Nutzer gerade nicht online ist.
Dieses Vorgehen bietet sich vor allem dann an, wenn aufgrund der Zeitverschiebung
zwei Nutzer selten zur selben Zeit online sind.

[^HOST]: Typischerweise würde ein solches Repository in einem Rechenzentrum liegen,
       oder auf einem privaten Server.

### Synchronisation einzelner Dateien {#sec:sync-single-file}

In seiner einfachsten Form nimmt ein Synchronisationsalgorithmus als Eingabe
die Metadaten zweier Dateien von zwei Synchronisationspartnern und trifft als
auf dieser Basis als Ausgabe eine der folgenden Entscheidungen:

1) Die Datei existiert nur bei Partner A.
2) Die Datei existiert nur bei Partner B.
3) Die Datei existiert bei beiden und ist gleich.
4) Die Datei existiert bei beiden und ist verschieden.

Je nach Entscheidung kann für diese Datei eine entsprechende Aktion ausgeführt werden:

1) Die Datei muss zu Partner B übertragen werden.
2) Die Datei muss zu Partner A übertragen werden.
3) Es muss nichts weiter gemacht werden.
4) Konfliktsituation: Auflösung nötig; eventuell Eingabe vom Nutzer erforderlich.

Bis auf den vierten Schritt ist die Implementierung trivial und kann leicht von
einem Computer erledigt werden. Das Kriterium, ob die Datei gleich ist, kann
entweder durch einen direkten Vergleich gelöst werden (aufwendig) oder durch
den Vergleich der Prüfsummen beider Dateien (schnell, aber vernachlässigbares
Restrisiko durch Kollision TODO: ref). Manche Werkzeuge wie ``rsync`` setzen
sogar auf probabilistische Ansätze, indem sie in der Standardkonfiguration aus Geschwindigkeitsgründen nur
ein Teil des Dateipfades, eventuell das Änderungsdatum und die Dateigröße vergleichen.

Für die Konfliktsituation hingegen kann es keine perfekte, allumfassende Lösung
geben, da die optimale Lösung von der jeweiligen Datei und der Absicht des
Nutzers abhängt. Bei Quelltext--Dateien möchte der Anwender vermutlich, dass
beide Stände automatisch zusammengeführt werden, bei großen Videodateien ist
das vermutlich nicht seine Absicht. Selbst wenn die Dateien nicht automatisch zusammengeführt werden sollen
(englisch »to merge«), ist fraglich was mit der Konfliktdatei des Partners geschehen soll.
Soll die eigene oder die fremde Version behalten werden? Dazwischen sind auch weitere Lösungen denkbar,
wie das Anlegen einer Konfliktdatei (``photo.png:conflict-by-bob-2015-10-04_14:45``), so wie es beispielsweise
Dropbox macht.[^DROPBOX_CONFLICT_FILE]
Alternativ könnte der Nutzer auch bei jedem Konflikt befragt werden. Dies wäre
allerdings im Falle von ``brig`` nach Meinung des Autors der Benutzbarkeit
stark abträglich.

Im Falle von ``brig`` müssen nur die Änderung von ganzen Dateien betrachtet werden, aber keine partiellen Änderungen
darin. Eine Änderung der ganzen Datei kann dabei durch folgende Aktionen des Nutzers entstehen:

1) Der Dateinhalt wurde modifiziert, ergo muss sich die Prüfsumme geändert haben (``MODIFY``).
2) Die Datei wurde verschoben, ergo muss sich der Pfad geändert haben. (``MOVE``).
3) Die Datei wurde gelöscht, ergo sie ist im *Staging--Commit* nicht mehr vorhanden. (``REMOVE``).
4) Die Datei wurde (initial oder erneut nach einem ``REMOVE``) hinzugefügt (``ADD``).

Der vierte Zustand (``ADD``) ist dabei der Initialisierungszustand. Nicht alle dieser
Zustände führen dabei automatisch zu Konflikten. So sollte beispielsweise ein guter
Algorithmus kein Problem, erkennen, wenn ein Partner die Datei modifiziert und
der andere sie lediglich umbenennt. Eine Synchronisation der entsprechenden
Datei sollte den neuen Inhalt mit dem neuen Dateipfad zusammenführen.
[@tbl:sync-conflicts] zeigt welche Operationen zu Konflikten führen und welche
verträglich sind. Die einzelnen Möglichkeiten sind dabei wie folgt:

* »\xmark«: Die beiden Aktionen sind nicht miteinander verträglich, es sei denn ihre Prüfsummen sind gleich.
* »\qmark«: Die Aktion ist prinzipiell verträglich, hängt aber von der Konfiguration ab.
            Entweder wird die Löschung vom Gegenüber propagiert oder die eigene Datei wird behalten (Standard).
* »\cmark«: Die beiden Aktionen sind verträglich (nur wenn beide Dateien gelöscht wurden).


| A/B          | ``ADD``           | ``REMOVE``        | ``MODIFY``        | ``MOVE``           |
| :----------: | ----------------- | ----------------- | ----------------- | ------------------ |
| ``ADD``      | \xmark            | \qmark            | \xmark            | \xmark             |
| ``REMOVE``   | \qmark            | \cmark            | \qmark            | \qmark             |
| ``MODIFY``   | \xmark            | \qmark            | \xmark            | \xmark             |
| ``MOVE``     | \xmark            | \qmark            | \xmark            | \xmark             |

: Verträglichkeit {#tbl:sync-conflicts}

[^DEPENDS]: Die Aktion hängt von der Konfiguration ab. Entweder wird die Löschung propagiert oder
          die eigene Datei wird behalten.

[^RSYNC]: <https://de.wikipedia.org/wiki/Rsync>
[^DROPBOX_CONFLICT_FILE]: Siehe <https://www.dropbox.com/help/36>

Zusammenfassend wird der in [@lst:file-sync] gezeigte Pseudo--Code von beiden
Teilenehmern ausgeführt, um zwei Dateien synchron zu halten. Unten stehender
Go--Pseudocode ist eine modifizierte Version aus Russ Cox' Arbeit »File
Synchronization with Vector Time Pairs«[@cox2005file], welcher für ``brig``
angepasst wurde. Die Funktionen ``HasConflictingChanges()`` und ``ResolveConflict()``
prüfen dabei die Verträglichkeit mithilfe von [@tbl:sync-conflicts].

```{#lst:file-sync .go caption="Synchronisationsalgorithmus für eine einzelne Datei"}
// historyA ist die Historie der eigenen Datei A.
// historyB ist die Historie der fremden Datei B mit gleichem Pfad.
func sync(historyA, historyB History) Result {
	if historyA.Equal(historyB) {
		// Keine weitere Aktion nötig.
		return NoConflict
	}

	if historyA.IsPrefix(historyB) {
		// B hängt A hinterher.
		return NoConflict
	}

	if historyB.IsPrefix(historyA) {
		// A hängt B hinterher. Kopiere B zu A.
		copy(B, A)
		return NoConflict
	}

	if root := historyA.FindCommonRoot(historyB); root != nil {
		// A und B haben trotzdem eine gemeinsame Historie,
		// haben sich aber auseinanderentwickelt.
		if !historyA.HasConflictingChanges(historyB, root) {
			// Die Änderungen sind verträglich und
			/  können automatisch aufgelöst werden.
			ResolveConflict(historyA, historyB, root)
			return NoConflict
		}
	}

	// Keine gemeinsame Historie.
	// -> Nicht automatisch zusammenführbar.
	// -> Eine Konfliktstrategie muss angewandt werden.
	return Conflict
}
```

### Synchronisation von Verzeichnissen

Die naive Herangehensweise wäre den obigen Algorithmus für jede Datei im Verzeichnis
zu wiederholen. Der beispielhafte Verzeichnisbaum in [@fig:tree-sync] zeigt allerdings bereits ein Problem dabei:
Die Menge an Pfaden, die Alice besitzt wird sich selten mit denen decken, die Bob besitzt.
So kann natürlich Alice Pfade besitzen, die Bob nicht hat und umgekehrt.

![Unterteilung der zu synchronisierenden Pfade in drei Gruppen.](images/4/tree-sync.pdf){#fig:tree-sync}

Man könnte also das »naive« Konzept weiterführen und die Menge der zu
synchronisierenden Pfade in drei Untermengen unterteilten. Jede dieser
Untermengen hätten dann  eine unterschiedliche Semantik:

- Pfade die beide haben ($X = Paths_{A} \bigcap Paths_{B}$): Konfliktpotenzial. Führe obigen Algorithmus für jede Datei aus.
- Pfade die nur Alice hat ($Y = Paths_{A} \setminus Paths_{B}$): Brauchen keine weitere Behandlung.
- Pfade die nur Bob hat ($Z = Paths_{B} \setminus Paths_{A}$): Müssen nur hinzugefügt werden.

Wie in [@fig:tree-sync] angedeutet, sind diese Mengen allerdings schwerer zu
bestimmen als durch eine simple Vereinigung, beziehungsweise Differenz.
Zwei Beispiele verdeutlichen dies:

* Löscht Bob eine Datei, während Alice sie nicht verändert würde der Pfad trotzdem in der Menge $Y$ landen.
  Dies hätte zur Folge, dass die Löschung nicht zu Alice propagiert wird.
* Verschiebt Alice eine Datei zu einem neuen Pfad, muss dieser neue Pfad
  trotzdem mit dem alten Pfad von Bob verglichen werden.

Es muss also eine Abbildungsfunktion gefunden werden, die jedem Pfad von Alice einen
Pfad von Bob zuordnet. Die Wertemenge dieser Funktion entspricht der Menge $X$,
also aller Pfade die einer speziellen Konfliktauflösung bedürfen. Die Menge $Z$
(also alle Pfade die Bob hat, aber Alice nicht) ergibt sich dann einfach durch
$Z = Paths_{B} \ X$. Für die Abbildung von Alice' Pfaden zu Bob's Pfaden
funktioniert die Abbildungsfunktion folgendermaßen:

1) Auf Bob's Store werden alle Knoten gesammelt, die sich seit dem letzten gemeinsamen Merge--Point verändert haben.
   Falls es noch keinen gemeinsamen Merge--Point gab, werden alle Knoten angenommen.
2) Auf Bob's Store wird für jeden Knoten die Historie ($=$ Liste aller Checkpoints) seit dem letzten Merge--Point gesammelt, oder
   die gesamte Historie ($=$ alle Checkpoints) falls es noch keinen Merge--Point gab.
3) Es wird eine Abbildung (als assoziatives Array) erstellt, die alle bekannten
   Pfade von Bob der jeweiligen Historie zuordnen, in dem der Pfad vorkommt. Mehr
   als ein Pfad kann dabei auf die gleiche Historie zeigen, wenn Verschiebungen
   vorkamen. Gelöschte Dateien sind in der Abbildung unter ihrem zuletzt bekannten
   Pfad zu finden.
4) Für alle Pfade, die Alice momentan besitzt (Alle Pfade unter ``HEAD``), wird
   der Algorithmus in [@lst:sync-map] ausgeführt. Dieser ordnet jedem Pfad von
   Alice, einem Pfad von Bob zu oder meldet dass er kein passendes Gegenstück
   gefunden werden konnte.

```{#lst:sync-map .go}
// Ein assoziatives Array mit dem Pfad zu der Historie
// seit dem letzten gemeinsamen Merge-Point.
type PathToHistory map[string]*History

// BobMapping enthält alle Pfade;
// also auch Pfade die entfernt wurden (unter ihrem letzten Namen)
// Wurden Pfade verschoben, so enthält das Mapping auch alle Zwischenschritte.
func MapPath(HistA, BobMapping PathToLastHistory) (string, error) {
	// Iteriere über alle Zwischenpfade, die `HistA` hatte.
	// In den meisten Fällen (ohne Verschiebungen) also nur ein einziger.
	for _, path := range NodeA.AllPaths() {
		HistB, ok := BobMapping[path]

		// Diesen Pfad hatte Bob nicht.
		if !ok {
			continue
		}

		// Erfolg! Gebe den aktuellsten Pfad von Bob zurück.
		// Also der Pfad an dem die Datei zuletzt bei Bob war,
		// beziehungsweise der Pfad des aktuellsten Checkpoints.
		return HistB.MostCurrentPath(), nil
	}

	// Bob hat diesen Pfad nirgends.
	// -> Es muss ein Pfad sein, den nur Alice hat.
	return "", ErrNoMappingFound
}
```

Das Ergebnis dieses Vorgehens ist eine Abbildung aller Pfade von Alice zu den Pfaden von Bob.
Damit wurde eine eindeutige Zuordnung erreicht und die einzelnen Dateien können mit dem Algorithmus
unter [@sec:sync-single-file] synchronisiert werden. Die Dateien, die Bob
zusätzlich hat (aber Alice nicht) können nun leicht ermittelt werden, indem geprüft wird
welche von Bob's Pfaden noch nicht in der errechneten Hashtabelle vorkommen.
Diese Pfade können dann in einem zweiten Schritt dem Stand von Alice hinzugefügt werden.

### Austausch der Metadaten {sec:metadata-exchange}

Um die Metadaten nun tatsächlich synchronisieren zu können, muss ein Protokoll
etabliert werden, mit dem zwei Partner ihren Store über Netzwerk austauschen können.
Im Folgenden wird diese Operation, analog zum gleichnamigen ``git``--Kommando[^TRANSFER_PROTOCOL], ``fetch`` genannt.

[^TRANSFER_PROTOCOL]: <https://git-scm.com/book/be/v2/Git-Internals-Transfer-Protocols>

![Das Protokoll das bei der ``FETCH`` Operation ausgeführt wird.](images/4/fetch-protokoll.pdf){#fig:fetch-protocol}

Wie in [@fig:fetch-protocol] gezeigt, besteht das Protokoll aus drei Teilen:

* Alice schickt eine ``FETCH``--Anfrage zu Bob, der den Namen des zu holenden Stores enthält.
  Im Beispiel ist dies Bob's eigener Store, ``bob@realworld.org``.
* Falls Alice in Bob's Remote--Liste steht, wandelt Bob seinen eigenen Store in eine
  exportierbare Form um, die aus einer großen serialisierten Nachricht[^EXPORT] besteht, die alle notwendigen Daten enthält.
- Die serialisierte Form des Stores wird über den Transfer--Layer von ``brig`` (siehe [@sec:transfer-layer])
  zurück an ``alice@wonderland.lit`` geschickt.
- Alice importiert die serialisierte Form in einen leeren Store und speichert
  das Ergebnis in der Liste ihrer Stores. Eine Synchronisation der beiden
  Datensätze kann nun lokal bei Alice erfolgen.

[^EXPORT]: Die Form des serialisierten Export--Formattes ist nicht weiter interessant und kann im Anhang [@sec:data-model]
         eingesehen werden (Message: *Store*).

Aus Zeitgründen ist dieses Protokoll momentan noch sehr einfach gehalten und
beherrscht keine differentiellen Übertragungen. Da hier nur Metadaten
übertragen werden sollte das nur bedingt ein Problem sein. In der Tat müssten
aber nur die Commits seit dem letzten gemeinsamen Merge--Point übertragen
werden.

Auch sind zum momentanen Stand noch keine *Live*--Updates möglich. Hierfür
müssten sich die einzelnen Knoten bei jeder Änderung kleine *Update*--Pakete
schicken, welche prinzipiell einen einzelnen *Checkpoint* beeinhalten würden.
Diese Checkpoints müssten dann jeweils in den aktuellen Staging--Bereich eingepflegt
werden. Dadurch wären Änderungen in »Echtzeit« auf anderen Knoten verfügbar.
Aus Zeitgründen wird an dieser Stelle aber nur auf diese Möglichkeit verwiesen;
eine konzeptuelle Implementierung steht noch aus.


### Abgrenzung zu anderen Synchronisationswerkzeugen

TODO: Ist das wichtig?

In der Fachliteratur (vergleiche unter anderem [@cox2005file])
findet sich zudem die Unterscheidung zwischen *informierter* und
*uninformierter* Synchronisation. Der Hauptunterschied ist, dass bei ersterer
die Änderungshistorie jeder Datei als zusätzliche Eingabe zur Verfügung steht.
Auf dieser Basis können dann intelligentere Entscheidungen bezüglich der
Konflikterkennung getroffen werden. Insbesondere können dadurch aber leichter
die Differenzen zwischen den einzelnen Ständen ausgemacht werden: Für jede
Datei muss dabei lediglich die in [@lst:file-sync] gezeigte Sequenz abgelaufen
werden, die von beiden Synchronisationspartnern unabhängig ausgeführt werden
muss.

Werkzeuge wie ``rsync`` oder ``unison`` betreiben eher eine *uninformierte
Synchronisation*. Sie müssen bei jedem Programmlauf Metadaten über beide
Verzeichnisse sammeln und darauf arbeiten. TODO: mehr worte verlieren Im
Gegensatz zu Timed Vector Pair Sync, informierter Austausch, daher muss nicht
jedesmal der gesamte Metadatenindex übertragen werden.

-> Nicht besser oder schlechter. Aber anders.

### Speicherquoten

Werden immer mehr Modifikationen gespeichert, so steigt der Speicherplatz immer
weiter an, da jede Datei pro Version einmal voll abgespeichert werden muss. Die
Anzahl der Objekte die dabei gespeichert werden können, hängt von dem
verfügbaren Speicherplatz ab. Sehr alte Versionen werden dabei typischerweise
nicht mehr benötigt und können gelöscht werden. Diese Aufgabe wird derzeit
nicht von ``brig`` selbst übernommen, sondern vom ``ipfs``--Backend. Dieses
unterstützt mit dem Befehl ``ipfs gc`` eine Bereinigung von Objekten, die
keinen Pin mehr haben. Zudem kann ``brig`` den Konfigurationswert
``Datastore.StorageMax`` von ``ipfs`` auf eine maximale Höhe (minus einen
kleinen Puffer für ``brig``--eigene Dateien) setzen. Wird dieser überschritten,
geht der Garbage--Collector aggressiver vor und löscht auch Objekte aus dem
Cache. (TODO: Eigentlich schauen was ipfs da macht.)

In der momentanen Architektur und Implementierung wird noch nicht zwischen
harten und weichen Speicherquoten unterschieden. (TODO: ref zu anforderung)
Auch wird die maximale Grenze wird zwangsweise eingehalten, wenn mehr Dateien
gepinnt werden als Speicher verfügbar ist. 

TODO: Sinnvollere Herangehensweise: Dateien erst ab einer bestimmten Revision unpinnen?

TODO: In Evaluation packen: ?

Eine Möglichkeit Speicher zu reduzieren, wäre die Einführung von
*Packfiles*, wie ``git`` sie implementiert[^PACKFILES_GIT]. Diese komprimieren nicht eine
einzelne Datei, sondern packen mehrere Objekte in ein zusammengehöriges Archiv.
Dies kann die Kompressionsrate stark erhöhen wenn viele ähnliche Dateien
(beispielsweise viele subtil verschiedene Versionen der gleichen Datei)
zusammen gepackt werden. Nachteilig sind die etwas langsameren Zugriffsraten.
Eine Implementierung dieser Lösung müsste zwischen eigentlichem Datenmodell
und dem ``ipfs``--Backend eine weitere Schicht einschieben, welche
transparent und intelligent passende Dateien in ein Archiv verpackt und umgekehrt
auch wieder entpacken kann.

[^PACKFILES_GIT]: Mehr Details zur ``git``--Implementierung hier: <https://git-scm.com/book/uz/v2/Git-Internals-Packfiles>

## Architekturübersicht

Um den eigentlichen Kern des Store sind alle anderen Funktionalitäten gelagert.
[@fig:arch-overview] zeigt diese in einer Übersicht. Die einzelnen Unterdienste
werden im Folgenden besprochen.

![Übersicht über die Architektur von ``brig``](images/4/architecture-overview.pdf){#fig:arch-overview}

TODO: Repository begriff irgendwo einführen?

### Lokale Aufteilung in Client und Daemon

``brig`` ist architektonisch in einem langlebigen Daemon--Prozess und einem
kurzlebigen Kontroll--Prozess aufgeteilt, welche im Folgenden jeweils ``brigd``
und ``brigctl`` genannt werden.[^BRIGCTL_NOTE] Beide Prozesse kommunizieren
dabei über Netzwerk mit einem speziellen Protokoll, welches auf einen
Serialisierungsmechanismus  von Google namens *Protobuf*[^PROTOBUF] basiert.
Dabei wird basierend auf einer textuellen Beschreibung des Protokolls (einer
``.proto``--Datei mit eigener Syntax) Quelltext in der gewünschten
Zielsprache generiert. Dieser Quelltext ist dann in der Lage Datenstrukturen
von der Zielsprache in ein serialisiertes Format zu überführen, beziehungsweise
dieses wieder einzulesen. Als Format steht dabei wahlweise eine
speichereffiziente, binäre Repräsentation der Daten zur Verfügung, oder eine
menschenlesbare Darstellung als JSON--Dokument.

Nötig ist die Aufteilung vor allem, da ``brigd`` im Hintergrund als
Netzwerkdienst laufen muss, um Anfragen von außen verarbeiten zu können. Auch
läuft ``ipfs`` im selben Prozess wie ``brigd`` und muss daher stets erreichbar
sein. Abgesehen davon ist es aus Effizienz--Gründen förderlich, wenn nicht bei
jedem eingetippten Kommando das gesamte Repository geladen werden muss. Auch
ist es durch die Trennung möglich, dass ``brigd`` auch von anderen
Programmiersprachen und Prozessen auf dem selben Rechner aus gesteuert werden
kann.

[^BRIGCTL_NOTE]: Tatsächlich gibt es derzeit keine ausführbaren Dateien mit
diesen Namen. Die Bezeichnungen ``brigctl`` und ``brigd`` dienen lediglich der
Veranschaulichung.
[^PROTOBUF]: Mehr Informationen unter: <https://developers.google.com/protocol-buffers>

### Aufbau von ``brigctl`` {#sec:client-daemon-proto}

Zusammengefasst ist ``brigctl`` eine »Fernbedienung« für ``brigd``, welche im
Moment exklusiv von der Kommandozeile aus bedient wird. In den meisten Fällen
verbindet sich der Kommando--Prozess ``brigctl`` sich beim Start zu ``brigd``,
sendet ein mittels *Protobuf* serialisiertes Kommando und wartet auf die
dazugehörige Antwort welche dann deserialisiert wird. Nachdem die empfangene
Antwort, je nach Art, ausgewertet wurde, beendet sich der Prozess wieder.

**Protobuf Protokoll:** Das Protokoll ist dabei so aufgebaut, dass
für jede Aufgabe, die ``brigd`` erledigen soll ein separates Kommando
existiert. Neben einer allgemeinen Typbezeichnung, können auch vom Kommando
abhängige optionale und erforderliche Parameter enthalten sein. Ein gekürzter
Auszug aus der Protokollspezifikation veranschaulicht dies in [@lst:proto-command].

```{#lst:proto-command .protobuf}
enum MessageType {
	ADD = 0;
	// ...
}

message Command {
	// Type identifier of the Command
	required MessageType command_type = 1;

	message AddCmd {
		// Absolute path to the file on the user's disk.
		required string file_path = 1;

		// Path inside the brig repo (e.g. /photos/me.png)
		required string repo_path = 2;

		// Add directories recursively? Defaults to true.
		optional bool recursive = 3;
	}
	// ... more subcommands ...

	// If command_type is ADD, read from this field:
	optional AddCmd add_command = 2;
	// ... more command entries ...
}
```

Analog dazu kann ``brigd`` mit einer *Response* auf ein *Command* antworten. In
[@lst:proto-response] wird beispielhaft die Antwortspezifikation
(``OnlineStatusResp``) auf ein ``OnlineStatusCmd``--Kommando gezeigt, welches
prüft, ob ``brigd`` Verbindungen von Außen annimmt.

```{#lst:proto-response .protobuf}
message Response {
	// Type identifier to the response;
	// matches the associated command.
    required MessageType response_type = 1;

	// Everything fine?
    required bool success = 2;

	// If not, an optional error description might be provided.
	optional string error = 3;

	// Detailed error code (not yet used)
	optional id errno = 4;

	message OnlineStatusResp {
		// True if brigd is in online mode.
    	required bool is_online = 1;
	}
	// ... more sub responses ...

	optional OnlineStatusResp online_status_resp = 5;
	// ... more response entries ...
}
```

Neben der Kommunikation mit  ``brigd`` muss ``brigctl`` noch drei andere Aufgaben erledigen:

* **Initiales Anlegen eines Repositories:** Bevor ``brigd`` gestatertet werden kann,
  muss die in TODO: ref gezeigte Verzeichnisstruktur angelegt werden.
* **Bereitstellung des User--Interfaces:** Das zugrundeliegende Protokoll wird so gut
  es geht vom Nutzer versteckt und Fehlermeldungen müssen möglichst gut beschrieben werden.
* **Autostart von ``brigd``:** Damit der Nutzer nicht explizit ``brigd`` starten
  muss, sollte der Daemon--Prozess automatisch im Hintergrund gestartet werden,
  falls er noch nicht erreichbar ist. Dies besorgt ``brigctl`` indem es dem
  Nutzer nach dem Passwort zum Entsperren eines Repositories fragt und das
  Passwort beim Start an ``brigd`` weitergibt, damit der Daemon--Prozess das
  Repository entsperren kann.

### Aufbau von ``brigd``

Der Daemon--Prozess implementiert alle Kernfunktionalitäten.
Die einzelnen Komponenten werden in [@sec:einzelkomponenten] beschrieben.

Als Netzwerkdienst muss ``brigd`` auf einen bestimmten Port (momentan
standardmäßig Port ``6666``) auf Anfragen warten. Es werden keine Anfragen von
außen angenommen, da über diese lokale Verbindung fast alle
sicherheitskritische Informationen ausgelesen werden können.
Für den Fall, dass ein Angreifer zwar keinen Zugriff auf den lokalen Rechner hat,
dafür aber Zugriff auf den lokalen Netzwerkverkehr wird der gesamte Netzwerkverkehr
zwischen ``brigctl`` und ``brigd`` mit AES256 verschlüsselt. Der Schlüssel wird
beim Verbindungsaufbau mittels Diffie--Hellmann ausgetauscht. Die Details des
Protokolls werden in (TODO ref kitteh arbeit) erklärt.

Die Anzahl der gleichzeitig offenen Verbindungen wird auf ein Maximum ``50``
limitiert und Verbindungen werden nach Inaktivität mit einen Timeout von 10
Sekunden automatisch getrennt. Diese Limitierungen soll verhindern, dass
fehlerhafte Clients den Hintergrundprozess zu stark auslasten können.

Im selben Prozess wie ``brigd`` läuft auch der ``ipfs``--Daemon und nutzt dabei
standardmäßig den Port ``4001``, um sich mit dem Netzwerk zu verbinden.
Nachteilig an diesem Vorgehen ist, dass ein Absturz oder eine Sicherheitslücke
in ``ipfs`` auch ``brigd`` betreffen kann. Längerfristig sollte beide Prozesse
möglichst getrennt werden, auch wenn dies aus Effizienzgründen nachteilig ist.

TODO: Global config zur Bestimmung des Ports beschreiben?

## Einzelkomponenten {#sec:einzelkomponenten}

Im Folgenden werden die einzelnen Komponenten von ``brigd`` aus
architektonischer Sicht. Genauere Angaben zu Implementierungsdetails,
insbesondere zum FUSE--Dateisystem, folgen im nächsten Kapitel.

### Dateiströme

Im ``ipfs``--Backend werden nur verschlüsselte und (zuvor) komprimierte
Datenströme gespeichert. Verschlüsselung ist nicht optional bei ``brig``. Hat
ein Angreifer die Prüfsumme einer Datei erbeutet, so kann er die Datei aus dem
``ipfs``--Netzwerk empfangen. Solange die Datei aber verschlüsselt hat, so wird
der Angreifer alleine mit den verschlüsselten Daten ohne den dazugehörigen
Schlüssel nichts anfangen können. In der Tat unterstützt er das
``ipfs``--Netzwerk sogar, da der Knoten des Angreifers auch wieder seine
Bandbreite zum Upload anbieten muss, da der Knoten sonst ausgebremst wird
(TODO: ref?).

Nachteilig an einer »zwangsweisen« Verschlüsselung ist, dass die
Deduplizierungsfähigkeit von ``ipfs`` ausgeschalten wird. Wird die selbe Datei
mit zwei unterschiedlichen Schlüsseln verschlüsselt, so werden die
resultierenden Daten (bis auf ihre Größe) keine Ähnlichkeit besitzen,
sind also kaum deduplizierbar.

Eine mögliche Lösung wäre ein Verfahren namens *Convergent
Encryption*[@wiki:convergent-encryption]. Dabei wird der Schlüssel der zu
verschlüsselten Datei aus der Prüfsumme derselben Datei abgeleitet. Dies hat
den Vorteil, dass gleiche Dateien auch den gleichen (deduplizierbaren)
Ciphertext generieren. Der Nachteil ist, dass ein Angreifer feststellen kann,
ob jemand eine Datei (beispielsweise Inhalte mit urhebergeschützen Inhalten)
besitzt. Im Protoypen werden die Dateischlüssel daher zufällig generiert,
was die Deduplizierungsfunktion von ``ipfs`` momentan ausschaltet.
Die Vor- und Nachteile dieses Verfahrens wird in [@cpiechula], Kapitel TODO diskutiert.

#### Verschlüsselung

Für ``brig`` wurde ein eigenes Containerformat für verschlüsselte Daten
eingeführt, welches wahlfreien Zugriff auf beliebige Bereiche der
verschlüsselten Datei erlaubt, ohne die gesamte Datei entschlüsseln zu müssen.
Dies ist eine wichtige Eigenschaft für die Implementierung des
FUSE--Dateisystems und ermöglicht zudem aus technischer Sicht das Streaming von
großen, verschlüsselten Dateien wie Videos. Zudem kann das Format durch den
Einsatz von *Autenticated Encryption (AE)*[@wiki:aead] die Integrität der verschlüsselten
Daten sichern.

Es werden lediglich reguläre
Dateien verschlüsselt. Verzeichnisse existieren nur als Metadaten und werden
gesondert behandelt. Die Details und Entscheidungen zum Design des Formats
werden in [@cpiechula], Kapitel TODO dargestellt.

![Aufbau des Verschlüsselungs--Dateiformats](images/4/format-encryption.pdf){#fig:format-encryption}

**Enkodierung:** [@fig:format-encryption] zeigt den Aufbau des Formats. Ein
roher Datenstrom (dessen Länge nicht bekannt sein muss) wird an den Enkodierer 
gegeben. Als weitere Eingabe muss ein Algorithmus ausgewählt werden und ein
entsprechend dimensionierter, symmetrischer Schlüssel mitgegeben werden.
Werden die ersten Daten geschrieben, so schreibt der Kodierer zuerst einen
36--Byte großen Header. In diesem finden sich folgende Felder:

* Eine *Magic--Number*[@wiki:magic-number] (8 Byte, ASCII--Repräsentation von ``moosecat``) zur schnellen Identifikation einer
  von ``brig`` geschriebenen Datei.
* Die *Versionsnummer* (2 Byte) des vorliegenden Formats. Standardmäßig »``0x01``«.
  Sollten Änderungen am Format nötig sein,
  so muss nur die ersten 10 Byte beibehalten werden und die Versionsnummer inkrementiert
  werden. Für die jeweilige Version kann dann ein passender Dekodierer genutzt werden.
* Die verwendete *Blockchiffre* (2 Byte) zur Verschlüsselung. Standardmäßig wird *ChaCha20/Poly1305*[@nir2015chacha20]
  eingesetzt, aber es kann auch AES (TODO: ref zu crypto buch) mit 256 Bit im Galois--Counter--Modus (GCM) verwendet werden.
* Die *Länge* (4 Byte) des verwendeten Schlüssels in Bytes.
* Die *maximale Blockgröße* (4 Byte) der nachfolgenden Blöcke in Bytes.
* Ein *Message--Authentication--Code (MAC)* (TODO: ref zu crypto buch) (16 Byte)
  der die Integrität des Headers sicherstellt.

Nach dem der Header geschrieben wurde, sammelt der Enkodierer in einem internen Puffer ausreichend viele
Daten, um einen zusammenhängende Block zu schreiben (standardmäßig 64 Kilobyte). Ist diese
Datenmenge erreicht wird der Inhalt des Puffers verschlüsselt und ein kompletter Block ausgegeben.
Dieser enthält folgende Felder:

* Eine *Nonce*[@wiki:nonce] (8 Byte). Diese eindeutige Nummer wird bei jedem
  geschriebenen Block inkrementiert und stellt daher die Blocknummer dar. Sie
  wird benutzt, um die Reihenfolge des geschriebenen Datenstroms zu validieren
  und wird zudem als öffentlich bekannte Eingabe für den
  Verschlüsselungsalgorithmus benutzt.
* Der eigentliche *Ciphertext*. Er ist maximal so lang wie der Puffer, kann
  aber im Falle des letzten Blockes kleiner sein.
* Am Ende kann, je nach Algorithmus, ein gewisser Overhead durch *Padding* entstehen.
  Zudem wird an jeden Block eine weitere MAC angehängt, welche die Integrität
  der Nonce und der nachfolgenden Daten sicherstellt.

So wird blockweise weiter verfahren, bis alle Daten des Ursprungsdatenstroms aufgebraucht
worden sind. Der letzte Block darf als einziger kleiner als die Blockgröße sein.
Der resultierende Datenstrom ist etwas größer als der Eingabedatenstrom. Seine Größe lässt
sich wie in [@eq:enc-size] gezeigt mithilfe der Eingabegröße $s$ und der Blockgröße $b$ berechnen:

$$f_{\text{size}}(s) = 36 + s + \left\lceil\frac{s}{b}\right\rceil\times(8 + 16)$$ {#eq:enc-size}

Was den Speicherplatz angeht, hält sich der »Overhead« in Grenzen. Zwar wächst
eine fast leere Datei von 20 Byte Originalgröße auf 80 Byte nach der
Verschlüsselung, aber bereits eine 20 Megabyte große Datei wächst nur noch
um zusätzliche 7.5 Kilobyte ($+0.03\%$).

**Dekodierung:** Beim Lesen der Datei wird zuerst der Header ausgelesen und
auf Korrektheit geprüft. Korrekt ist er wenn eine Magic--Number vorhanden ist,
alle restlichen Felder erlaubte Werte haben und die Integrität des Headers
bis Byte 20 durch die darauffolgende MAC überprüft werden konnte. Konnte die
Integrität nicht überprüft werden, wurden entweder Daten im Header verändert oder
ein falscher Schlüssel wurde übergeben.

Jeder zu lesende Block wird im Anschluss komplett in einen Puffer gelesen. Die
Nonce wird ausgelesen und dem Entschlüsselungsalgorithmus als Eingabge neben
dem eigentlichen Datenblock mitgegeben. Dieser überprüft ob die Integrität des
Datenblocks korrekt war und entschlüsselt diesen im Erfolgsfall. Anhand der
Position im Datenstrom wird zudem überprüft ob die Blocknummer zur Wert in der
Nonce passt. Stimmen diese nicht überein, wird die Entschlüsselung verweigert,
da ein Angreifer möglicherweise die Reihenfolge Blöcke hätte vertauschen können.

**Wahlfreier Zugriff:** Wurde der Header bereits gelesen, so kann ein
beliebiger Block im Datenstrom gelesen werden sofern der unterliegende
Datenstrom wahlfreien Zugriff (also die Anwendung von ``Seek()``) erlaubt. Die
Anfangsposition des zu lesenden Blocks kann mit [@eq:seek-off] berechnet
werden, wobei $o$ der Offset im unverschlüsselten Datenstrom ist.

$$f_{\text{offset}}(o) = 36 + \left\lceil\frac{o}{b}\right\rceil\times(8 + 16 + b)$$ {#eq:seek-off}

Der Block an dieser Stelle muss komplett gelesen und entschlüsselt werden, auch
wenn nur wenige Bytes innerhalb des Blocks angefragt worden. Da typischerweise
die Blöcke aber fortlaufend gelesen werden, ist das aus Sicht des Autors ein
vernachlässigbares Problem.

Das vorgestellte Format ähnelt etwas dem Verschlüsselungsformat[^BCACHEFS_ENC],
welches das (relativ neue) Dateisystem ``bcachefs`` verwendet und basiert auf
den Ideen der *Secretbox* der freien NaCL--Bibliothek.[^NACL_LIB] Davon abgesehen
handelt es sich um eine Neuimplementierung mit eigenen Code, der auch außerhalb
von ``brig`` eingesetzt werden kann.

[^BCACHEFS_ENC]: Siehe auch: <https://bcache.evilpiepirate.org/Encryption>
[^NACL_LIB]: Siehe auch: <https://nacl.cr.yp.to/secretbox.html>

#### Kompression

Bevor Datenströme verschlüsselt werden, werden diese von ``brig`` auch
komprimiert.[^ANDERSRUM] Auch hier wurde ein eigenes Containerformat
entworfen, welches in [@fig:format-compression] gezeigt wird.

[^ANDERSRUM]: Rein technisch ist es auch andersherum möglich, aber aufgrund der
            prinzipbedingten, hohen Entropie von verschlüsselten Texten
			wären in dieser Reihenfolge die Kompressionsraten sehr gering.

![Aufgbau des Kompressions--Dateiformat](images/4/format-compression.pdf){#fig:format-compression}

Nötig war dieser Schritt auch hier wieder weil kein geeignetes Format gefunden
werden konnte, welches wahlfreien Zugriff im komprimierten Datenstrom zulässt,
ohne dass dabei die ganze Datei entkomprimiert werden muss.

**Enkodierung:** Der Eingabedatenstrom wird in gleich größe Blöcke unterteilt
(maximal 64KB standardmäßig) wobei nur der letzte Block kleiner sein darf.
Nachdem der Header geschrieben wurde, folgt jeder Eingabeblock als
komprimierter Block mit variabler Länge. Am Schluss wird ein Index geschrieben,
der beschreibt welche Eingabeblock mit welchem komprimierten Block
korrespondiert. Der Index kann nur am Ende geschrieben werden, da die genauen
Offsets innerhalb dieses Indexes erst nach dem Komprimieren bekannt sind. Für
eine effiziente Nutzung dieses Formats ist es also nötig, dass der Datenstrom
einen effizienten, wahlfreien Zugriff am Ende der Datei bietet.
Glücklicherweise unterstützt dies ``ipfs``. Datenströme wie ``stdin`` unter
Unix unterstützen allerdings keinen wahlfreien Zugriff, weshalb das
vorgestellte Format für dieses Anwendungsfälle eher ungeeignet ist.

Der Index besteht aus zwei Teilen: Aus dem eigentlichen Index und einem
sogenannten »Trailer«, der die Größe des Indexes enthält. Zusätzlich enthält
dieser Trailer noch die verwendete Blockgröße, in die der unkomprimierte
Datenstrom unterteilt wurde. Der eigentliche Index besteht aus einer Liste von
64--Bit Offset--Paaren. Jedes Paar enthält einmal den unkomprimierten und
einmal den komprimierten Offset eines Blocks als Absolutwert gemessen vom
Anfang des Stroms. Am Ende wird ein zusätzliches Paar eingefügt (das zu keinen
realen Block zeigt), welches die Größe des unkomprimierten und komprimierten
Datenstroms anzeigt.

Der vorangestellte Header enthält alle Daten die definitiv vor der Kompression
des ersten Blockes vorhanden sind:

- Eine *Magic--Number* (8 Byte, ASCII Repräsentation von ``elchwald``).
  Wie beim Verschlüsselungsformat dient diese zur schnellen Erkennung dieses Formats.
- Eine *Formatversion* (2 Byte, momentan »``0x01``«). Kann analog zum Verschlüsselungsformat
  bei Änderungen inkrementiert werden.
- Der verwendete *Algorithmustyp* (2 Byte, standardmäßig *Snappy*). Folgende Algorithmen
  werden momentan unterstützt:

    * Snappy[@wiki:snappy] (sehr schneller Algorithmus mit akzeptabler Kompressionsrate)
    * LZ4[@wiki:lz4] (etwas langsamer, aber deutlich höhere Kompressionsrate)
    * None (gar keine Kompression, Index wird trotzdem geschrieben)

    Weitere Algorithmen wie *Brotli*[@wiki:brotli] können problemlos hinzugefügt werden, allerdings
    gab es zu diesen Zeitpunkten noch keine vernünftig nutzbare Bibliotheken.

**Dekodierung:** Bevor der erste Block dekodiert werden kann muss sowohl der Header
als auch der Index geladen werden. Dazu müssen die ersten 12 Bytes des
Datenstroms gelesen werden. Im Anschluss muss fast an das Ende (Ende minus
12 Byte) des Datenstroms gesprungen werden, um dort den Trailer zu lesen. Mit der
darin enthaltenen Größe des Indexes kann die Anfangsposition des Indexes
bestimmt werden (Ende - 12 Byte - Indexgröße). Alle Offset--Werte im Index
werden in eine sortierte Liste geladen. Die Blockgröße eines
komprimierten/unkomprimierten Blocks an der Stelle ergibt sich dabei aus der
Differenz des Offset--Paars an der Stelle $n+1$ und seines Vorgänger an der
Stelle $n$. Mithilfe der Blockgröße kann ein entsprechendes Stück vom
komprimierten Datenstrom gelesen und dekomprimiert werden.

**Wahlfreier Zugriff:** Um auf einen Block in der Mitte zugreifen zu können (am
unkomprimierten Offset $o$), muss mittels binärer Suche im Index der passende, Anfang
des unkomprimierten Blocks gefunden werden. Wurde der passende Block bestimmt,
ist auch der Anfangsoffset im komprimierten Datenstrom bekannt. Dadurch kann
der entsprechende Block ganz geladen und dekomprimiert werden. Innerhalb der
dekomprimierten Daten kann dann vom Anfangsoffset $a$ noch zum Zieloffset $o-a$
gesprungen werden.

### Transfer--Layer {#sec:transfer-layer}

Damit Metadaten ausgetauscht werden können, ist ein sicherer Seitenkanal nötig,
der unabhängig vom Kanal ist über den die eigentlichen Daten ausgetauscht
Über diesen muss ein *Remote--Procedure--Call* (RPC[@wiki:rpc]) ähnliches Protokoll
implementiert werden, damit ein Teilnehmer Anfragen an einen anderen stellen kann.

Dieser sichere Seitenkanal wird von ``ipfs`` gestellt. Dabei wird kein
zusätzlicher Netzwerkport für den RPC--Dienst in Anspruch genommen, da alle
Daten über den selben Kanal laufen, wie die eigentliche Datenübertragung. Es
findet also eine Art »Multiplexing« statt.

Dies wird durch ``ipfs'`` fortgeschrittenes Netzwerkmodell möglich[^LIP2P],
welche in [@fig:ipfs-net] gezeigt werden. Nutzer des gezeigten Netzwerkstacks
können eigene Protokolle registrieren, die mittels eines *Muxing--Protokolls*
namens *Multistream*[^MULTISTREAM] in einer einzigen, gemeinsamen
physikalischen Verbindung zusammengefasst werden. Der sogenannte *Swarm* hält
eine Verbindung zu allen zu ihm verbundenen Peers und macht es so möglich jeden
Netzwerkpartner von der Protokollebene aus über seine Peer--ID anzusprechen.
Der eigentliche Verbindungsaufbau geschieht dann, wie in [@sec:ipfs-attrs]
beschrieben auch über NAT--Grenzen hinweg.

![Quelle: IPFS--Projekt[^NET_SOURCE]](images/4/ipfs-network.pdf){#fig:ipfs-net width=66%}

[^MULTISTREAM]: Siehe auch: <https://github.com/multiformats/multistream>
[^NET_SOURCE]: Diese Grafik ist eine Aufbereitung von: <https://github.com/libp2p/go-libp2p/tree/master/p2p/net>
[^LIP2P]: Implementiert als eigene Bibliothek »libp2p«: <https://github.com/libp2p/go-libp2p>

Im Falle von ``brig`` wird ein eigenes Protokoll registriert, um mit anderen
Teilnehmern zu kommunizieren. Dieses ist ähnlich aufgebaut wie das Protokoll
zwischen Daemon und Client (siehe [@sec:client-daemon-proto]), unterstützt aber
andere Anfragen und hat erhöhte Sicherheitsanforderungen.
Eine genauere Beschreibung des Protokolls wird in [@cpiechula], Kapitel TODO gegeben,
hier werden nur kurz die wichtigsten Eigenschaften genannt:

- Authentifizierung mittels Remote--Liste bei jedem Verbindungsaufbau.
* Anfragen und Antworten werden als Protobuf--Nachricht. 
  Die eigentliche Protokolldefinition kann in [@sec:rpc-proto] eingesehen werden.
* Kompression der gesendeten Nachrichten mittels Snappy.
- Zusätzliche Verschlüsselung der Verbindung.
- Senden von »Broadcast«--Nachrichten zu allen bekannten, verbundenen Teilnehmern.

Im momentanen Zustand wird nur eine einzige Anfrage unterstützt.
Dies die in [@sec:metadata-exchange] beschriebene ``FETCH``--Anfrage. Zukünftig
ist die Einführung weiterer Anfragen geplant. Um beispielsweise
Echtzeit--Synchronisation zu unterstützen, müsste zwei weitere Nachrichten eingeführt werden:

- ``UPDATE``: Eine Nachricht die aktiv an alle Teilnehmer in der Remote--Liste
  geschickt wird. Sie enthält einen einzelnen Checkpoint. Die darin beschrieben
  atomare Änderung sollte dann auf Empfängerseite direkt in den Staging--Bereich
  des Empfängers eingegliedert werden.
* ``DIFF <COMMIT_HASH>:`` Wie ``FETCH``, gibt aber nur die Änderungen seit dem 
  angegebenen ``COMMIT_HASH`` zurück.

### Benutzermanagement {#sec:user-management}

In den Anforderungen in [@sec:eigenschaften] wird eine menschenlesbare
Identität gefordert, mit der *Peers* einfach erkennbar sind. Der von ``ipfs``
verwendete Identitätsbezeichner ist allerdings eine für Menschen schwer zu
merkende Prüfsumme (die »Peer--ID«).

Um dieses Dilemma zu lösen, wendet ``brig`` einen »Trick« an. Jeder
``brig``--Knoten veröffentlicht einen einzelnen ``blob`` in das
``ipfs``--Netzwerk mit dem Inhalt ``brig:<username>``. Ein Nutzer der nun einen
solchen menschenlesbaren  Namen zu einem Netzwerkadresse  auflösen möchte, kann
d en Inhalt des obigen Datensatzes generieren und daraus eine Prüfsumme bilden.
Mit der entstandenen Prüfsumme kann mittels folgenden Verfahrens herausgefunden
werden, welche Knoten diesen Datensatz anbieten:

```bash
$ USER_HASH=$(printf 'brig#user:%s' alice  | multihash -)
$ echo $USER_HASH
QmdNdLHqc1ryoCU5LPEMMCrxkLSafgKuHzpVZ5DFdzZ61M
# Schlage Hash in der Distributed Hash Table nach:
$ ipfs dht findprovs $USER_HASH
<PEER_ID_OF_POSSIBLE_ALICE_1>
<PEER_ID_OF_POSSIBLE_ALICE_2>
...
```

![Überprüfung eines Benutzernamens mittels Peer--ID](images/4/id-resolving.pdf){#fig:id-resolving}

Da prinzipiell jeder Knoten sich als *Alice* ausgeben kann, wird aus den
möglichen Peers, derjenige ausgewählt, dessen ``ipfs``--Identitätsbezeichner
(bei ``brig`` wird dieser als *Fingerprint* bezeichnet) als vertrauenswürdig
eingestuft wurde. Vertrauenswürdig ist er, wenn der Fingerprint in der
Remote--Liste in der Kombination von Nutzernamen und Fingerprint auftaucht. In
diesem Fall muss der Nutzer explizit authentifiziert worden sein.
[@fig:id-resolving] zeigt dieses Verfahren noch einmal graphisch.

Analog kann das Konzept auch übertragen werden, um bestimmte Gruppen von
Nutzern zu finden. Angenommen, Alice, Bob und Charlie arbeiten im gleichen Unternehmen.
Das Unternehmen findet sich in auch in ihren Identitäten wieder:

- ``alice@corp.de/server``
- ``bob@corp.de/laptop``
- ``charlie@corp.de/desktop``

Neben den gesamten Nutzernamen, können diese drei Nutzer auch nur ihren
Unternehmensnamen veröffentlichen, beziehungsweise auch ihren Nutzernamen ohne
den ``resource``--Zusatz. So ist es dann beispielsweise folgenderweise möglich
alle Unternehmensmitglieder aufzulösen:

```bash
$ CORP_HASH=$(printf 'brig#domain:%s' corp.de | multihash -)
$ ipfs dht findprovs $CORP_HASH
<PEER_ID_OF_POSSIBLE_CORP_MEMBER_1>
<PEER_ID_OF_POSSIBLE_CORP_MEMBER_2>
...
```

Die einzelnen IDs können dann, sofern bekannt, zu den »Klarnamen« aufgelöst
werden die in der Remote--Liste jedes Teilnehmers stehen. Insgesamt können
folgende sinnvolle Kombinationen von ``brig`` veröffentlicht werden:

- ``user``
- domain[.tld]
- ``user@domain[.tld]``
- ``user@domain[.tld]/resource``

Das besondere an dieser Vorgehensweise ist, dass kein Nutzer sich an einer zentralen
Stelle registriert. Trotzdem können sich die Nutzer gegenseitig im Netzwerk finden
und trauen nicht einer zentralen Instanz sondern entscheiden selbst welchen Knoten
sie trauen.
