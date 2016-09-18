# Architektur {#sec:architektur}

In diesem Kapitel wird die grundlegende Architektur von ``brig`` erklärt.
Dabei wird vor allem das »Kernstück« beleuchtet: Das zugrundeliegende Datenmodell
in dem alle Metadaten abgespeichert und in Relation gesetzt werden. Basierend
darauf werden die umgebenden Komponenten beschrieben, die um diesen Kern
gelagert sind. Am Ende des Kapitels werden zudem noch einmal alle
Einzelkomponenten in einer Übersicht gezeigt. Es wird dabei stets vom Stand des
aktuellen Prototypen ausgegangen. Mögliche Erweiterungen werden in Kapitel
[@sec:evaluation] (*Evaluation*) diskutiert. Die technische Umsetzung der
jeweiligen Komponenten hingegen wird in [@sec:implementierung]
(*Implementierung*) besprochen.

Eine berechtigte Frage soll vorher geklärt werden: ``ipfs`` hat bereits ein
Datenmodell (siehe ``ipfs`` Whitepaper, [@benet2014ipfs], S.7 ff.), welches Verzeichnisse abbilden kann. Warum wurde also nicht dieses
als Basis verwendet? Der Grund dafür liegt in der bereits erwähnten Entkopplung
von Daten und Metadaten. Würden die Dateien und Verzeichnisse direkt in
``ipfs`` gespeichert, so wäre diese Teilung nicht mehr gegeben. Dies hätte zur
Folge, dass ein Angreifer zwar nicht die verschlüsselten Daten lesen könnte,
aber problemlos die Verzeichnisstruktur betrachten könnte, sobald er die
Prüfsumme des Wurzelknotens hat. Dies würde den Sicherheitsversprechen von
``brig`` widersprechen. Abgesehen davon wurde ein eigenes Datenmodell
entwickelt, um mehr Freiheiten beim Design zu haben.

## Architektur von git

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
wird an dieser Stelle über eine gesonderte Einführung verzichtet.

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

Die ersten drei Objekte werden in einem gerichteten, azyklischen Graphen
(Merkle--DAG) (TODO: prüfen ob das vorher erklärt wurde) untereinander in
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

1) **Prüfsummenalgorithmus nicht veränderbar:** Ein auf einem Merkle--DAG basierenden Versionsverwaltungssystem muss
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

* **Commits:** Analog zu ``git``, dienen aber bei ``brig`` nicht nur der logischen Kapselung von mehreren Änderungen, sondern
  werden auch automatisiert von der Software nach einen bestimmten Zeitintervall erstellt. Daher ist ihr Zweck eher
  mit den *Snapshots* vieler Backup--Programme vergleichbar, welche dem Nutzer
  einen Sicherungspunkt zu einem bestimmten Zeitpunkt in der Vergangenheit
  bietet. Ein *Commit* kapselt eine Prüfsumme, die sich aus der Prüfsumme seines Vorgängers, der Commit--Nachricht,
  der Autoren--ID berechnet. Er speichert einen 
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

Davon abgesehen fällt auf dass zwei zusätzliche Strukturen eingeführt wurden:

* **Checkpoints:** Jeder Datei ist über ihre ``UID`` ein Historie von sogenannten *Checkpoints* zugeordnet.
  Jeder einzelne dieser Checkpoints beschreiben eine atomare Änderung an der Datei. Da keine
  partiellen Änderungen möglich sind (wie ``git diff``), müssen nur vier verschiedene Operation
  unterschieden werden: ``ADD`` (Datei wurde initial oder erneut hinzugefügt), ``MODIFY`` (Prüfsumme hat sich verändert),
  ``MOVE`` (Pfad hat sich geändert) und ``REMOVE`` (Datei wurde entfernt).
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

TODO: Noch folgende Punkte verarzten:

Problem: Metadaten wachsen schnell, Angreifer könnte sehr viele kleine änderungen sehr schnell machen.
Mögliche Lösung : Delayed Checkpoints, Checkpoint Squashing, Directory Checkpoints?

### Operationen auf dem Datenmodell

Die Gesamtheit aller *Files*, *Directories*, *Commits*, *Checkpoints* und
*Refs* wird im Folgenden als *Store* bezeichnet. Da ein *Store* nur aus
Metadaten besteht, ist er selbst leicht übertragbar. Er kapselt den Objektgraph
und kümmert sich, um die Verwaltung auf der Objekte. Basierend auf dem *Store*
werden insgesamt 10 verschiedene atomare Operationen implementiert, die jeweils
den aktuellen Graphen nehmen und einen neuen und (mit Ausnahme von ``LIST``, ``CAT``,
``LOG`` und ``HISTORY``) veränderten Graphen erzeugen.

Es gibt sechs Operationen, die die Benutzung des Graphen als gewöhnliches Dateisystem ermöglichen:

[^SYSCALL_NOTE]: Von der Funktionsweise sind diese angelehnt an die entsprechenden »Syscall« im POSIX--Standard.
               Dies sollte im späteren Verlauf die Implementierung des FUSE--Layers erleichtern.

``ADD``: Fügt ein Dokument dem Staging--Bereich hinzu oder aktualisiert die
Version eines vorhandenen Dokuments. Der Pfad entscheidet dabei wo das Dokument
eingefügt wird, bzw. welches existierendes Dokument modifiziert wird.
[@fig:op-add] zeigt die Operationen, die zum Einfügen einer Datei notwendig
sind. Als Vorarbeit muss allerdings erst die gesamte Datei gelesen werden und
in das ``ipfs``--Backend eingefügt werden. Die Datei wird zudem gepinnt. Als
Ergebnis dieses Teilprozesses wird die Größe und Prüfsumme der
unverschlüsselten und unkomprimierten Datei zurückgeliefert.
Handelt es sich bei dem hinzuzufügenden Objekt um ein Verzeichnis, wird der gezeigte Prozess
für jede darin enthaltene Datei wiederholt.

![Die Abfolge der ``ADD``-Operation im Detail](images/4/staging-area.pdf){#fig:staging-area}

TODO: wurde pin schon erklärt?

``REMOVE:`` Entfernt eine vorhandene Datei aus dem Staging--Bereich. Der Pin
der Datei oder des Verzeichnisses und all seiner Kinder werden entfernt.
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
Elternknoten eingerechnet. Eventuell müssen noch dazwischen liegende
Verzeichnisse erstellt werden. Diese werden von oben nach unten, Stück für
Stück mit den eben beschriebenen Prozess erstellt.

TODO: Grafik für mkdir falls nötig ist?

``MOVE:`` Verschiebt eine Datei oder ein Verzeichnis zu einem neuen Pfad. Diese
Operation entspricht technisch einem ``REMOVE`` und einem ``ADD``. Im
Unterschied dazu ist sie im Ganzen atomar und erstellt einen Checkpoint für
alle verschobenen Knoten einen Checkpoint mit dem Typen ``MOVED``.

``CAT:`` Gibt ein Dokument auf einen Stream aus. Der Name lehnt sich dabei an
das Unix Tool ``cat`` an, welches ebenfalls Dateien ausgibt. Es wird lediglich
wie in [@fig:path-resolution] gezeigt der gesuchte Knoten per Pfad aufgelöst
und der darin enthaltene Hash wird vom ``ipfs``--Backend aufgelöst. Die
ankommenden Daten werden noch entschlüsselt und dekomprimiert bevor sie dem
Nutzer präsentiert werden.

Neben den obenstehenden Operationen, gibt es noch vier Operationen, die zur Versionskontrolle dienen:

``COMMIT:`` Erstellt einen neuen Commit, basierend auf den Inhalt des
*Staging--Commits*. Dazu werden die Prüfsummen des aktuellen und des
Wurzelverzeichnisses im letzten Commit (``HEAD``) verglichen. Unterscheiden sie
sich nicht, wird abgebrochen, da keine Veränderung vorliegt. Im Anschluss wird
der *Staging--Commit* finalisiert, indem die angegebene *Commit--Message* und
der Autor in den Metadaten des Commits gesetzt werden. Basierend darauf wird
die finale Prüfsumme berechnet und der entstandene Commit abgespeichert. Ein
neuer *Staging-Commit* wird erstellt, welcher im unveränderten Zustand auf das
selbe Wurzelverzeichnis zeigt wie der vorige. Zuletzt werden die Referenzen von
``HEAD`` und ``CURR`` jeweils um ein Platz nach vorne verschoben.

TODO: Grafik für Commit.

``CHECKOUT:`` Stellt einen alten Stand wieder her. Dabei kann die Operation
eine alte Datei oder ein altes Verzeichnis wiederherstellen (basierend auf der
alten Prüfsumme) oder den Stand eines gesamten, in der Vergangenheit liegenden
Commits wiederherstellen.
Im Gegensatz zu ``git`` ist es allerdings nicht vorgesehen in der Versionshistorie »herumzuspringen«.
Soll ein alter *Commit* wiederhergestellt werden, so wird ein neuer *Commit* erzeugt, welcher
den aktuellen Stand so verändert, dass er dem gewünschten, alten Stand entspricht.
Das Verhalten von ``brig`` entspricht an dieser Stelle also nicht ``git checkout`` sondern eher
dem wiederholten Anwenden von ``git revert`` zwischen dem aktuellen und dem Nachfolger
des gewünschten Commits.
Begründet ist dieses Verhalten darin, dass kein sogenannter »Detached HEAD«--Zustand
entstehen soll, da dieser für den Nutzer verwirrend sein kann. Dieser Zustand
kann in ``git`` erreicht werden, indem man in einen alten *Commit* springt ohne
einen neuen *Branch* davon abzuzweigen.
Macht man in diesem Zustand Änderungen ist es prinzipiell
möglich die geänderten Daten zu verlieren. (TODO: ref)
Um das zu vermeiden, setzt ``brig`` darauf die Historie stets linear und
unveränderlich zu halten, auch wenn das keine Einschränkung der Architektur an
sich darstellt.


TODO: Grafik für CHECKOUT

``LOG/HISTORY:`` Zeigt alle Commits, bis auf den Staging Commits. Begonnen wird
die Ausgabe mit ``HEAD`` und beendet wird sie mit dem initial Commit.
Alternativ kann auch die Historie eines einzelnen Verzeichnisses oder einer
Datei angezeigt werden. Dabei werden statt Commits alle Checkpoints dieser
Datei, beginnend mit dem aktuellsten ausgegeben.

``STATUS:`` Zeigt den Inhalt des aktuellen Staging--Commits (analog zu ``git
status``) und damit aller geänderten Dateien und Verzeichnisse im Vergleich zu
``HEAD``.

## Architektur von IPFS

TODO: Weiter nach hinten verschieben oder in das kapitel mit dem rest von ipfs packen?

 Da ``brig`` eine Art »Frontend« für das »Backend« ``IPFS`` ist, wird dessen
Architektur hier kurz schematisch erklärt.

- Bitswap
- For the swarm!

TODO: Komponentendiagramm

Aufbau der Software aus funktionaler Sicht.
Eher blackbox, was kommt rein was kommt raus.

- Berührungspunkte mit Nutzer.

## Synchronisation

Ähnlich wie ``git`` speichert ``brig`` für jeden Nutzer seinen zuletzt bekannten *Store*
ab. Mithilfe dieser Informationen können dann Synchronisationsentscheidungen
größtenteils automatisiert getroffen werden. Welcher *Store* dabei lokal
zwischengespeichert wird, entscheiden die Einträge in die sogenannte *Remote List* (TODO)

### Die Remote Liste

TODO: Grafik mit verschiedenen Stores und Remote listen sowie Sync-Richtungen.

Anders als bei ``git`` kennt jedes ``brig``--Repository den Stand aller
Teilnehmer (beziehungsweise den zuletzt verfügbaren), die ein Nutzer in seiner
Remote--Liste gespeichert hat. Da es sich dabei nur um Metadaten handelt, wird
dabei nicht viel Speicherplatz in Anspruch genommen.

TODO: Absatz okay, aber fehl am platz.

Da ein *Commit* nur ein Vorgänger haben kann, musste ein anderer Mechanismus eingeführt werden,
um die Synchronisation zwischen zwei Partnern festzuhalten. Bei ``git`` wird
dies mittels eines sogenannten Merge--Commit gelöst, welcher aus den Änderungen der
Gegenseite besteht. Hier wird das Konzept eines *Merge--Points* eingeführt.
Innerhalb eines *Commit* ist das ein spezieller Marker, der festhält mit wem synchronisiert wurde
und mit welchen Stand er zu diesem Zeitpunkt hatte. Bei einer späteren Synchronisation muss
daher lediglich der Stand zwischen dem aktuellen *Commit* (»``CURR``«) und dem letzten Merge--Point
verglichen werden. Basierend auf diesen Vergleich wird ein neuer *Commit* (der
*Merge--Commit*) erstellt, der alle (möglicherweise nach der Konfliktauflösung zusammengeführten)
Änderungen des Gegenübers enthält und als neuer *Merge--Point* dient.


### Synchronisation einzelner Dateien

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
(englisch >>to merge<<), ist fraglich was mit der Konfliktdatei des Partners geschehen soll.
Soll die eigene oder die fremde Version behalten werden? Dazwischen sind auch weitere Lösungen denkbar,
wie das Anlegen einer Konfliktdatei (``photo.png:conflict-by-bob-2015-10-04_14:45``), so wie es beispielsweise
Dropbox macht.[^DROPBOX_CONFLICT_FILE]
Alternativ könnte der Nutzer auch bei jedem Konflikt befragt werden. Dies wäre
allerdings im Falle von ``brig`` nach Meinung des Autors der Benutzbarkeit
stark abträglich.

Im Falle von ``brig`` müssen nur die Änderung von ganzen Dateien betrachtet werden, aber keine partiellen Änderungen
darin. Eine Änderung der ganzen Datei kann dabei durch folgende Aktionen des Nutzers entstehen:

1) Der Dateinhalt wurde modifiziert, ergo muss sich die Prüfsumme geändert haben (``MODIFY``).
2) Die Datei wurde verschoben (``MOVE``).
3) Die Datei wurde gelöscht (``REMOVE``).
4) Die Datei wurde (initial oder erneut) hinzugefügt (``ADD``).

Der vierte Zustand (``ADD``) ist dabei der Initialisierungszustand. Nicht alle dieser
Zustände führen dabei automatisch zu Konflikten. So sollte ein guter
Algorithmus kein Problem, erkennen, wenn ein Partner die Datei modifiziert und
der andere sie lediglich umbenennt. Eine Synchronisation der entsprechenden
Datei sollte den neuen Inhalt mit dem neuen Dateipfad zusammenführen.
[@tbl:sync-conflicts] zeigt welche Operationen zu Konflikten führen und welche
verträglich sind.


| A/B          | ``ADD``          | ``REMOVE``       | ``MODIFY``       | ``MOVE``         |
| :----------: | -----------------| -----------------| -----------------|------------------|
| ``ADD``      | ?                | \cmark[^DEPENDS] | ?                | ?                |
| ``REMOVE``   | \cmark[^DEPENDS] | \cmark           | \cmark[^DEPENDS] | \cmark[^DEPENDS] |
| ``MODIFY``   | ?                | \cmark           | ?                | ?                |
| ``MOVE``     | ?                | \cmark[^DEPENDS] | ?                | ?                |

: Verträglichkeit {#tbl:sync-conflicts}

TODO: Fragezeichen in Tabelle erklären.

[^DEPENDS]: Die Aktion hängt von der Konfiguration ab. Entweder wird die Löschung propagiert oder
          die eigene Datei wird behalten.

[^RSYNC]: <https://de.wikipedia.org/wiki/Rsync>
[^DROPBOX_CONFLICT_FILE]: Siehe <https://www.dropbox.com/help/36>

### Synchronisation von Verzeichnissen

Prinzipiell lässt sich die
Synchronisation einer Datei auf Verzeichnisse übertragen, indem einfach obiger
Algorithmus auf jede darin befindliche Datei angewandt wird. In der
Fachliteratur (vergleiche unter anderem [@cox2005file]) findet sich zudem die
Unterscheidung zwischen *informierter* und *uninformierter* Synchronisation.
Der Hauptunterschied ist, dass bei ersterer die Änderungshistorie jeder Datei
als zusätzliche Eingabe zur Verfügung steht. Auf dieser Basis können dann
intelligentere Entscheidungen bezüglich der Konflikterkennung getroffen werden.
Insbesondere können dadurch aber leichter die Differenzen zwischen den
einzelnen Ständen ausgemacht werden: Für jede Datei muss dabei lediglich die in
[@lst:file-sync] gezeigte Sequenz abgelaufen werden, die von beiden
Synchronisationspartnern unabhängig ausgeführt werden muss. Unten stehender
Go--Pseudocode ist eine modifizierte Version aus Russ Cox' Arbeit »File
Synchronization with Vector Time Pairs«[@cox2005file], welcher für ``brig``
angepasst wurde.

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
	// -> Konfliktstrategie muss angewandt werden.
	return Conflict
}
```

Werkzeuge wie ``rsync`` betreiben eher eine *uninformierte Synchronisation*.
Sie müssen bei jedem Programmlauf Metadaten über beide Verzeichnisse sammeln
und darauf arbeiten. TODO: mehr worte verlieren
Im Gegensatz zu Timed Vector Pair Sync, informierter Austausch, daher muss nicht jedesmal
der gesamte Metadatenindex übertragen werden.

**Synchronisation über das Netzwerk:** Um die Metadaten nun tatsächlich
austauschen zu können, muss ein Protokoll etabliert werden, mit dem diese
zwischen zwei Partnern übertragen werden. Aus Zeitgründen ist dieses Protokoll
im Moment sehr einfach und wird bei größeren Datenmengen nicht optimal
funktionieren. Für einen Proof--of--Concept reicht es aber aus. Wie in Grafik TODO gezeigt besteht das Protokoll
aus drei Teilen.

* encode
- fetch.
- decode

Nachteilig ist dabei natürlich, dass momentan der gesamte Metadatenindex
übertragen werden muss. Mit etwas mehr Aufwand könnte vorher der eigentlichen
Übertragung der letzte gemeinsame Stand ausgehandelt werden, um nur die
Änderungen seit diesem Stand zu übertragen zu müssen.

Auch sind zum momentanen Stand noch keine *Live*--Updates möglich. Hierfür müssten sich die
einzelnen Knoten bei jeder Änderung kleine *Update*--Pakete schicken, welche prinzipiell
einen einzelnen *Checkpoint* beeinhalten würden. Dies ist technisch bereits möglich,
wurde aus Zeitgründen aber noch nicht umgesetzt.

TODO: Erkennung von renames?

TODO: Garbage collector

## Architekturübersicht

![Übersicht über die Architektur von ``brig``](images/4/architecture-overview.pdf){#fig:arch-overview}

TODO: Komponentendiagramm

TODO: Repository begriff irgendwo einführen?

``brig`` ist architektonisch in einem langlebigen Daemon--Prozess und einem
kurzlebigen Kontroll--Prozess aufgeteilt, welche im Folgenden jeweils ``brigd``
und ``brigctl`` genannt werden.[^BRIGCTL_NOTE] Beide Prozesse kommunizieren
dabei über Netzwerk mit einem speziellen Protokoll, welches auf einen
Serialisierungsmechanismus  von Google namens *Protobuf*[^PROTOBUF] basiert.
Dabei wird basierend auf einer textuellen Beschreibung des Protokolls (in einer
``.proto``--Datei mit eigener Syntax) Quelltext generiert in der gewünschten
Zielsprache generiert. Dieser Quelltext ist dann in der Lage Datenstrukturen
von der Zielsprache in ein serialisiertes Format zu überführen, beziehungsweise
dieses wieder einzulesen. Als Format steht dabei wahlweise eine
speichereffiziente, binäre Repräsentation der Daten zur Verfügung, oder eine
menschenlesbare Darstellung als JSON--Dokument.

Die Aufteilung in zwei Programmteile ist dabei inspiriert von ``MPD`` und
``IPFS``. (TODO) Nötig ist die Aufteilung vor allem, da ``brigd`` im
Hintergrund als Netzwerkdienst laufen muss, um Anfragen von außen verarbeiten
zu können. Abgesehen davon ist es aus Effizienz--Gründen förderlich, wenn nicht
bei jedem eingetippten Kommando das gesamte Repository geladen werden muss.
Auch ist es durch die Trennung möglich, dass ``brigd`` auch von anderen
Programmiersprachen und Prozessen auf dem selben Rechner aus gesteuert werden
kann.

[^BRIGCTL_NOTE]: Tatsächlich gibt es derzeit keine ausführbaren Dateien mit
diesen Namen. Die Bezeichnungen ``brigctl`` und ``brigd`` dienen lediglich der
Veranschaulichung.
[^PROTOBUF]: Mehr Informationen unter: <https://developers.google.com/protocol-buffers>

### Aufbau von ``brigctl``

Kurz gesagt ist ``brigctl`` eine »Fernbedienung« für ``brigd``, welche momentan
exklusiv von der Kommandozeile aus bedient wird. In den meisten Fällen
verbindet sich der Kommando--Prozess ``brigctl`` sich beim Start zu ``brigd``,
sendet ein mittels *Protobuf* serialisiertes Kommando und wartet auf die
dazugehörige Antwort welche er dann deserialisiert. Nachdem die empfangene
Antwort je nach Art ausgewertet wurde, beendet sich der Prozess wieder.

**Protobuf Protokoll:** Das Protokoll ist dabei so, aufgebaut, dass
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

**Initiales Anlegen eines Repositories:** Bevor ``brigd`` gestatertet werden kann,
muss die in TODO: ref gezeigte Verzeichnisstruktur angelegt werden.

**Bereitstellung des User--Interfaces:** Das zugrundeliegende Protokoll wird so gut
es geht vom Nutzer versteckt und Fehlermeldungen müssen möglichst gut beschrieben werden.

**Autostart von ``brigd``:** Damit der Nutzer nicht explizit ``brigd`` starten
muss, sollte der Daemon--Prozess automatisch im Hintergrund gestartet werden,
falls er noch nicht erreichbar ist. Dies besorgt ``brigctl`` indem es dem
Nutzer nach dem Passwort zum Entsperren eines Repositories fragt und das
Passwort beim Start an ``brigd`` weitergibt, damit der Daemon--Prozess das
Repository entsperren kann.

### Aufbau von ``brigd``

Der Daemon--Prozess implementiert alle sonstigen Funktionalitäten, die nicht
von ``brigctl`` erfüllt werden. Die einzelnen Komponenten werden in
[@sec:einzelkomponenten] beschrieben. In diesem Abschnitt werden nur
die Eigenschaften von ``brigd`` als Hintergrundprozess beschrieben.

Ist gleichzeitig IPFS im selben Prozess.

Nach Start des Daemons, lauscht dieser als Netzwerkdienst auf einem
Port  

Global config zur Bestimmung des Ports.

## Einzelkomponenten {#sec:einzelkomponenten}


### Dateiströme

https://en.wikipedia.org/wiki/Convergent_encryption

Schaubild mit den relevanten io.Reader/io.Writer

#### Verschlüsselung

![Aufbau des Verschlüsselungs--Dateiformats](images/4/format-encryption.pdf){#fig:format-encryption}

Verschlüsselung ist nur für einzelne Dateien. Verzeichnisse sind Metadaten.

Auf Schwäbisch: "Metadate is alls wasch nüscht koscht"

https://bcache.evilpiepirate.org/Encryption

TODO: NaCL Secretbox erwähnen, Unterschiede

#### Kompression

![Aufgbau des Kompressions--Dateiformat](images/4/format-compression.pdf){#fig:format-compression}

### Dateisystemordner

FUSE

### Deduplizierung

- Miller Rabin Chunking
- Rolling Hash

### Benutzermanagement

![Überprüfung eines Benutzernamens](images/4/id-resolving.pdf){#fig:arch-overview}

### Gateway

### Sonstiges

Logging

Konfiguration
