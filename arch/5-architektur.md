# Architektur {#sec:architektur}

In diesem Kapitel wird die grundlegende Architektur von ``brig`` erklärt. Dabei
wird vor allem das »Kernstück« beleuchtet: Das zugrundeliegende Datenmodell in
dem alle Metadaten abgespeichert und in Relation gesetzt werden.
Dazu wird auf die zuvor erklärten Internas von ``ipfs`` und ``git`` eingegangen.

Basierend darauf werden die umgebenden Komponenten beschrieben, die um den Kern
von ``brig`` gelagert sind. Am Ende des Kapitels werden zudem noch einmal alle
Einzelkomponenten in einer Übersicht gezeigt. Mögliche Erweiterungen werden in
[@sec:evaluation] (*Evaluation*) diskutiert. Die technische Umsetzung des
Prototypen hingegen wird in [@sec:implementierung] (*Implementierung*)
besprochen.

## Datenmodell von ``brig``

Die Einsatzziele von ``brig`` und ``git`` unterscheiden sich: ``git`` ist
primär eine Versionsverwaltugssoftware, mit der man auch synchronisieren kann.
``brig`` kann man hingegen eher als eine Synchronisationssoftware sehen, die
auch Versionierung beherrscht. Aus diesem Grund wurde das Datenmodell von
``git`` für den Einsatz in ``brig`` angepasst und teilweise vereinfacht. Die
Hauptunterschiede sind dabei wie folgt:

- **Strikte Trennung zwischen Daten und Metadaten:** Metadaten werden von ``brig``'s
  Datenmodell verwaltet, während die eigentlichen Daten lediglich per Prüfsumme
  referenziert und von ``ipfs`` gespeichert werden.
  So gesehen ist  ``brig`` ein Versionierungsaufsatz für ``ipfs``.
* **Lineare Versionshistorie:** Jeder *Commit* hat maximal einen Vorgänger und
  exakt einen Nachfolger. Dies macht die Benutzung von *Branches*[^BRANCH_EXPL]
  unmöglich, bei der ein *Commit* zwei Nachfolger haben kann, beziehungsweise
  sind auch keine Merge--Commits möglich, die zwei Vorgänger besitzen. Diese
  Vereinfachung ist nicht von der Architektur vorgegeben und könnte nachgerüstet
  werden. Allerdings hat die Benutzung dieses Features
  »Verwirrungspotenzial«[^DETACHED_HEAD] für gewöhnliche Nutzer, die gedanklich
  eher von einer linearen Historie ihrer Dokumente ausgehen.
* **Synchronisationspartner müssen keine gemeinsame Historie haben:[^DOUBLE_ROOT]**
  Es wird bei ``brig`` davon ausgegangen, dass unterschiedliche
  Dokumentensammlungen miteinander synchronisiert werden sollen, während bei
  ``git`` davon ausgegangen wird, dass eine einzelne Dokumentensammlung immer
  wieder modifiziert und zusammengeführt wird. Haben die Partner keine gemeinsame
  Historie, wird einfach angenommen, dass alle Dokumente synchronisiert werden müssen.
  Aus diesen Grund kennt ``brig`` auch keine ``clone`` und ``pull``--Operation.
  Diese werden durch »``brig sync <with>``« ersetzt.

[^BRANCH_EXPL]: *Branches* dienen bei ``git`` dazu, um einzelne Features oder Fixes separat entwickeln zu können.
[^DETACHED_HEAD]: So ist es bei ``git`` relativ einfach möglich in den
sogenannten *Detached HEAD* Modus zu kommen, in dem durchaus Daten verloren
gehen können. Siehe auch: <http://gitfaq.org/articles/what-is-a-detached-head.html>
[^DOUBLE_ROOT]: Streng genommen ist dies bei ``git`` auch nicht nötig, allerdings sehr unüblich.


![Das Datenmodell von ``brig``. Checkpoints von Verzeichnissen wurden ausgelassen.](images/4/brig-data-model.pdf){#fig:brig-data-model}

[@fig:brig-data-model] zeigt das oben verwendete Beispiel in ``brig``'s
Datenmodell. Es werden prinzipiell die gleichen Objekttypen verwendet, die auch
``git`` verwendet:

* **File:** Speichert die Metadaten einer einzelnen, regulären Datei. Zu den Metadaten gehört die aktuelle Prüfsumme,
  die Dateigröße, der letzte Änderungszeitpunkt und der kryptografische Schlüssel mit dem die Datei verschlüsselt ist.
  Anders als ein *Blob* speichert ein *File* die Daten nicht selbst, sondern referenziert diese nur im ``ipfs``--Backend.
* **Directory:**  Speichert wie ein *Tree* einzelne *Files* und weitere *Directories*. Die Prüfsumme des Verzeichnisses $H_{directory}$ ergibt sich auch hier
  aus der XOR--Verknüpfung ($\oplus$) der Prüfsumme des Pfades $H_{path}$ mit den Prüfsummen der direkten Nachfahren $x$: $$
	H_{directory}(x) = \begin{cases}
			H_{path} & \text{für } x = () \\
			x_1 \oplus f(x_{(x_2, \ldots, x_n)}) & \text{sonst}
		   \end{cases}
  $$

    Die Verwendung der XOR--Verknüpfung hat dabei den Vorteil, dass sie selbstinvers und kommutativ ist. Wendet man sie also zweimal an,
    so erhält man das neutrale Element $0$. Analog dazu führt die Anwendung auf ein vorheriges Ergebnis wieder zur ursprünglichen Eingabe:

    $$x \oplus x = 0 \text{  (Auslöschung)}$$
    $$y = y \oplus x \oplus x = x \oplus y \oplus x = x \oplus x \oplus y \text{  (Kommutativität)}$$

    Diese Eigenschaft kann man sich beim Löschen einer Datei zunutze machen,
    indem die Prüfsumme jedes darüberliegenden Verzeichnisses mit der Prüfsumme
    der zu löschenden Datei XOR--genommen wird. Der resultierende Graph hat die gleiche Prüfsumme wie vor
    dem Einfügen der Datei.

* **Commits:** Analog zu ``git``; dienen aber bei ``brig`` nicht nur der
  logischen Kapselung von mehreren Änderungen, sondern werden auch automatisiert
  von der Software nach einem bestimmten Zeitintervall erstellt. Daher ist ihr
  Zweck eher mit den *Snapshots* vieler Backup--Programme vergleichbar, welche
  dem Nutzer einen Sicherungspunkt zu einem bestimmten Zeitpunkt in der
  Vergangenheit bieten. Als Metadaten speichert er als Referenz die Prüfsumme des
  Wurzelverzeichnisses, eine Commit--Nachricht sowie dessen Autor und eine
  Referenz auf den Vorgänger. Aus diesen Metadaten wird durch Konkatenation
  derselben eine weitere Prüfsumme errechnet, die den Commit selbst eindeutig
  referenziert. In diese Prüfsumme ist nicht nur die Integrität des aktuellen
  Standes gesichert, sondern
  auch aller Vorgänger.
* **Refs:** Analog zu ``git`` dienen sie dazu, bestimmten *Commits* einen Namen
  zu geben. Es gibt zwei vordefinierte Referenzen, welche von ``brig``
  aktualisiert werden: ``HEAD``, welche auf den letzten vollständigen *Commit*
  zeigt und ``CURR``, welche auf den aktuellen Commit zeigt (meist dem *Staging
  Commit*, dazu später mehr). Da es keine Branches gibt, ist eine Unterscheidung zwischen
  *Refs* und *Tags* wie bei ``git`` nicht mehr nötig.

![Jeder Knoten muss von dem aktuellen Wurzelverzeichnis aus neu aufgelöst werden, selbst wenn nur der Elternknoten gesucht wird.](images/4/path-resolution.pdf){#fig:path-resolution width=90%}

*Directories* und *Files* speichern zudem zwei weitere gemeinsame Attribute:

* **Ihren eigenen Namen und den vollen Pfad des darüber liegenden Knoten**. Zusammen ergibt dieser den vollen
  Pfad der Datei oder des Verzeichnisses. Dieser Pfad ist nötig, um den jeweiligen Elternknoten zu erreichen.
  In einem gerichteten, azyklischen Graphen darf es keine Rückkanten nach »oben« geben, deswegen scheidet
  die direkte Referenzierung des Elternknotens mittels seiner Prüfsumme aus. Wie in [@fig:path-resolution] gezeigt
  ist es daher nötig, beispielsweise den Elternknoten eines beliebigen Knotens vom aktuellen Wurzelknoten neu aufzulösen.
* **Eine eindeutige Nummer** (*Unique Identifier*, ``UID``), welche die Datei oder das Verzeichnis
  eindeutig kennzeichnet. Diese Nummer bleibt auch bei Modifikation und
  Verschieben der Datei gleich. Neben der Prüfsumme
  (referenziert einen bestimmten Inhalt) und dem Pfad (referenziert eine
  bestimmte Lokation) ist die Nummer ein weiterer Weg eine Datei zu referenzieren
  (referenziert ein veränderliches »Dokument«) und ist grob mit dem Konzept einer
  *Inode--Nummer* bei Dateisystemen[^INODE] vergleichbar.

[^INODE]: Siehe auch: <https://de.wikipedia.org/wiki/Inode>

![Jede Datei und jedes Verzeichnis besitzt eine Liste von Checkpoints.](images/4/file-history.pdf){#fig:file-history width=50%}

Davon abgesehen fällt auf, dass zwei zusätzliche Strukturen eingeführt wurden:

* **Checkpoints:** Jeder Datei ist über ihre ``UID`` eine Historie von mehreren, sogenannten *Checkpoints* zugeordnet.
  Jeder Einzelne dieser Checkpoints beschreibt eine atomare Änderung an der Datei. Da keine
  partiellen Änderungen[^PARTIAL] möglich sind, müssen nur vier verschiedene Operation
  unterschieden werden: ``ADD`` (Datei wurde initial oder erneut hinzugefügt), ``MODIFY`` (Prüfsumme hat sich verändert),
  ``MOVE`` (Pfad hat sich verändert) und ``REMOVE`` (Datei wurde entfernt). Eine beispielhafte Historie findet sich
  in [@fig:file-history]. Werden mehrere Checkpoints eingepflegt, die den
  gleichen Typen haben (beispielsweise mehrere ``MODIFY``--Operationen), so
  wird nur die letzte ``MODIFY``--Operation in der Historie abgespeichert.
  Jeder Checkpoint kennt den Zustand der Datei zum Zeitpunkt der Modifikation,
  sowie einige Metadaten wie einen Zeitstempel, der Dateigröße, dem Änderungstyp, dem Vorgänger
  und dem Urheber der Änderung. Der Vorteil einer dateiabhängigen Historie
  ist die Möglichkeit, umbenannte Dateien zu erkennen, sowie Dateien zu erkennen, die gelöscht und dann
  wieder hinzugefügt worden sind. Ein weiterer Vorteil ist, dass zur Ausgabe der Historie einer Datei,
  nur die *Checkpoints* betrachtet werden müssen. Es muss nicht wie bei ``git`` jeder Commit betrachtet werden, um
  nachzusehen ob eine Änderung an einer bestimmten Datei stattgefunden hat.

* **Staging--Commit:** Es existiert immer ein sogenannter *Staging--Commit*. Dieser
  beinhaltet alle Knoten im MDAG, die seit dem letzten »vollwertigen« Commit
  modifiziert worden sind. [@fig:staging-area] zeigt den Staging--Bereich von
  ``git`` und ``brig`` im Vergleich. Im Falle von ``git`` handelt es sich um eine
  eigene, vom eigentlichen Graphen unabhängige, Datenstruktur, in die der Nutzer
  mittels ``git add`` explizit Dokumente aus dem Arbeitsverzeichnis hinzufügt.
  Bei ``brig`` hingegen gibt es kein Arbeitsverzeichnis und daher keine
  Unterscheidung zwischen »Unstaged Files« und »Staged Files«. Die Daten kommen
  entweder von einer externen Datei, welche mit ``brig stage <filename>``{.bash}
  dem Staging--Bereich hinzugefügt wurde, oder die Datei wurde direkt im
  FUSE--Dateisystem von ``brig`` modifiziert.
  In beiden Fällen wird die neue oder modifizierte Datei in den *Staging--Commit*
  eingegliedert, welcher aus diesem Grund eine veränderliche Prüfsumme aufweist
  und nach jeder inhaltlichen Modifikation auf ein anderes Wurzelverzeichnis verweist.

[^CHATTR_NOTE]: In Zukunft ist ein weiterer Zustand ``CHATTR`` möglich, welche die Änderung eines Dateiattributes abbildet.

[^PARTIAL]: Es wird nicht zwischen der Änderung eines einzelnen Bytes oder der gesamten Datei unterschieden wie bei ``git``.

![Der Staging--Bereich im Vergleich zwischen ``git`` und ``brig``](images/4/staging-area.pdf){#fig:staging-area}

Da ein *Commit* nur einen Vorgänger haben kann, muss ein anderer Mechanismus
eingeführt werden, um die Synchronisation zwischen zwei Partnern festzuhalten.
Bei ``git`` wird dies mittels eines sogenannten *Merge--Commit* gelöst, welcher
aus den Änderungen des Synchronisationspartners besteht. Hier wird das Konzept eines
*Merge--Points* eingeführt. Innerhalb eines *Commit* ist das ein spezieller
Marker, der festhält mit wem synchronisiert wurde und welchen Stand er zu
diesem Zeitpunkt hatte. Bei einer späteren Synchronisation muss daher lediglich
der Stand zwischen dem aktuellen *Commit* (»``CURR``«) und dem letzten
Merge--Point verglichen werden. Basierend auf diesem Vergleich wird ein neuer
*Commit* (der *Merge--Commit*) erstellt, der alle (möglicherweise nach der
Konfliktauflösung zusammengeführten) Änderungen des Gegenübers enthält und als
neuer *Merge--Point* dient.

### Operationen auf dem Datenmodell

Die Gesamtheit aller *Files*, *Directories*, *Commits*, *Checkpoints* und
*Refs* wird im Folgenden als *Store* bezeichnet. Da ein *Store* nur aus
Metadaten besteht, ist er selbst leicht auf andere Geräte übertragbar. Er
kapselt den Objektgraphen und kümmert sich um die Verwaltung der Objekte.
Basierend auf dem Store werden insgesamt elf verschiedene atomare Operationen
implementiert, die jeweils den aktuellen Graphen nehmen und einen neuen und
veränderten Graphen erzeugen.

Es gibt sechs Operationen, die die Benutzung des Graphen als gewöhnliches Dateisystem ermöglichen:

[^SYSCALL_NOTE]: Von der Funktionsweise sind diese angelehnt an die entsprechenden »Syscall« im POSIX--Standard.
               Dies sollte im späteren Verlauf die Implementierung des FUSE--Layers erleichtern.

``STAGE``: Fügt ein Dokument dem Staging--Bereich hinzu oder aktualisiert die
Version eines vorhandenen Dokuments. Der Pfad entscheidet dabei wo das Dokument
eingefügt wird, beziehungsweise welches existierende Dokument modifiziert wird.
[@fig:op-add] zeigt die Operationen, die zum Einfügen einer Datei notwendig
sind. Als Vorarbeit muss allerdings erst die gesamte Datei gelesen werden und
in das ``ipfs``--Backend eingefügt werden. Die Datei wird zudem gepinnt. Als
Ergebnis dieses Teilprozesses wird die Größe und Prüfsumme der
verschlüsselten und komprimierten Datei zurückgeliefert.
Handelt es sich bei dem hinzuzufügenden Objekt um ein Verzeichnis, wird der gezeigte Prozess
für jede darin enthaltene Datei wiederholt.

![Die Abfolge der ``STAGE``-Operation im Detail](images/4/op-add){#fig:op-add}

``REMOVE:`` Entfernt eine vorhandene Datei aus dem Staging--Bereich. Der Pin
der Datei oder des Verzeichnisses und all seiner Kinder wird entfernt. Die
gelöschten Daten werden möglicherweise beim nächsten Durchgang der $Cleanup$
Operation aus dem lokalen Speicher von ``ipfs`` entfernt. Die Prüfsumme der
entfernten Datei wird aus den darüber liegenden Verzeichnissen herausgerechnet.
Handelt es sich dabei um ein Verzeichnis, wird der Prozess *nicht* rekursiv für
jedes Unterobjekt ausgeführt. Es genügt die Prüfsumme des zu löschenden
Verzeichnisses aus den Eltern mittels der XOR--Operation herauszurechnen und
die Kante zu dem Elternknoten zu kappen.

``LIST:`` Entspricht konzeptuell dem Unix--Werkzeug ``ls``. Besucht alle Knoten
unter einem bestimmten Pfad rekursiv (breadth-first) und gibt diese aus.

``MKDIR:`` Erstellt ein neues, leeres Verzeichnis. Die initiale Prüfsumme des neuen
Verzeichnisses ergibt sich aus dem Pfad des neuen Verzeichnisses. Diese wird in den
Elternknoten eingerechnet. Die Referenz auf das Wurzelverzeichnis wird im
Staging--Commit angepasst.
Eventuell müssen noch dazwischenliegende Verzeichnisse erstellt werden. Diese
werden einzeln von oben nach unten mit den eben beschriebenen Prozess erstellt.

``MOVE:`` Verschiebt eine Quelldatei oder Verzeichnis zu einem
Zielpfad. Es muss eine Fallunterscheidung getroffen werden, je nachdem ob
und welcher Knoten im Zielpfad vorhanden ist:

1) *Ziel existiert noch nicht:* Quelldaten werden zum neuen Pfad verschoben.
2) *Ziel existiert und ist eine Datei:* Vorgang wird abgebrochen, es sei denn die
   Aktion wird »forciert«.
3) *Ziel existiert und ist ein Verzeichnis:* Quelldaten werden direkt unter das
   Zielverzeichnis verschoben, sofern darunter noch kein Verzeichnis mit diesem Namen
   existiert. Andernfalls wird die Aktion mit einem Fehler abgebrochen.

In jedem Fall entspricht diese Operation technisch dem, möglicherweise
mehrfachen, sequentiellen Ausführen der Operationen ``REMOVE`` und ``ADD``. Im
Unterschied dazu ist sie im Ganzen atomar und erstellt einen Checkpoint mit dem
Typen ``MOVED`` für alle verschobenen Knoten.

``CAT:`` Gibt ein Dokument als einen Datenstrom aus. Der Name lehnt sich dabei an
das Unix--Tool ``cat`` an, welches ebenfalls Dateien ausgeben kann. Es wird lediglich
wie in [@fig:path-resolution] gezeigt der gesuchte Knoten per Pfad aufgelöst
und die darin enthaltene Prüfsumme wird vom ``ipfs``--Backend aufgelöst. Die
ankommenden Daten werden entschlüsselt und dekomprimiert bevor sie dem
Nutzer präsentiert werden.

Neben den oben stehenden Operationen, gibt es noch fünf weitere, die
zur Versionskontrolle dienen und in dieser Form normalerweise nicht von
Dateisystemen implementiert werden:

``UNSTAGE:`` Entfernt ein Dokument aus dem Staging--Bereich und setzt den Stand
auf den zuletzt bekannten Wert zurück (also der Stand der in ``HEAD`` präsent war). Die
Prüfsumme des entfernten Dokumentes wird aus den Elternknoten herausgerechnet
und dafür die alte Prüfsumme wieder eingerechnet.

*Anmerkung:* Die Benennung der Operationen ``STAGE``, ``UNSTAGE`` und
``REMOVE`` ist anders als bei den semantisch gleichen ``git``--Werkzeugen
``add``, ``reset`` und ``rm``. Die Benennung nach dem ``git``--Schema ist
irreführend, da ``git add`` nicht nur neue Dateien hinzufügt, sondern auch modifizierte
Dateien aktualisiert. Zudem ist ``git add`` nicht das Gegenteil von ``git
rm``[^GIT_FAQ_RM], wie man vom Namen annehmen könnte. Das eigentliche
Gegenteil ist ``git reset``. Eine mögliche Alternative zu ``brig stage`` wäre
vermutlich auch ``brig track``, beziehungsweise ``brig untrack`` statt ``brig rm``.

[^GIT_FAQ_RM]: Selbstkritik des ``git``--Projekts: <https://git.wiki.kernel.org/index.php/GitFaq#Why_is_.22git_rm.22_not_the_inverse_of_.22git_add.22.3F>

``COMMIT:`` Erstellt einen neuen Commit, basierend auf dem Inhalt des
*Staging--Commits* (siehe auch [@fig:op-commit] für eine Veranschaulichung).
Dazu werden die Prüfsummen des aktuellen und des Wurzelverzeichnisses im
letzten Commit (``HEAD``) verglichen. Unterscheiden sie sich nicht, wird
abgebrochen, da keine Veränderung vorliegt. Im Anschluss wird der
*Staging--Commit* finalisiert, indem die angegebene *Commit--Message* und der
Autor in den Metadaten des Commits gesetzt werden. Basierend darauf wird die
finale Prüfsumme berechnet und der entstandene Commit abgespeichert. Ein neuer
*Staging-Commit* wird erstellt, welcher im unveränderten Zustand auf das selbe
Wurzelverzeichnis zeigt wie sein Vorgänger. Zuletzt werden die Referenzen von
``HEAD`` und ``CURR`` jeweils um einen Platz nach vorne verschoben.

![Die Abfolge der ``COMMIT``--Operation im Detail. Links der vorige Stand, rechts der Stand nach der ``COMMIT``--Operation.](images/4/op-commit.pdf){#fig:op-commit}

``CHECKOUT:`` Stellt einen alten Stand wieder her. Dabei kann die Operation
eine alte Datei oder ein altes Verzeichnis basierend auf der
alten Prüfsumme oder den Stand eines gesamten, in der Vergangenheit liegenden,
Commits wiederherstellen.

Im Gegensatz zu ``git`` ist es allerdings nicht vorgesehen, in der
Versionshistorie »herumzuspringen«. Soll ein alter *Commit* wiederhergestellt
werden, so wird der Staging--Commit so verändert, dass er dem gewünschten,
alten Stand entspricht (siehe auch Abbildung [@fig:op-checkout]). Das Verhalten
von ``brig`` entspricht an dieser Stelle also nicht dem Namensvetter ``git
checkout`` sondern eher dem wiederholten Anwenden von ``git revert`` zwischen
dem aktuellen und dem Nachfolger des gewünschten Commits.

![Die Abfolge der ``CHECKOUT``--Operation im Detail.](images/4/op-checkout.pdf){#fig:op-checkout width=75%}

Begründet ist dieses Verhalten darin, dass kein sogenannter »Detached
HEAD«--Zustand entstehen soll, da dieser für den Nutzer irreführend sein kann.
Dieser Zustand kann in ``git`` erreicht werden, indem man in einen früheren
*Commit* springt ohne einen neuen *Branch* davon abzuzweigen. Der ``HEAD``
zeigt dann nicht mehr auf einen benannten Branch, sondern auf die Prüfsumme des
neuen Commits, der vom Nutzer nur noch durch die Kenntnis derselben erreichbar
ist.
Macht man in diesem Zustand Änderungen, ist es möglich die
geänderten Daten zu verlieren[^DETACHED_HEAD]. Um das zu vermeiden, hält ``brig``
die Historie stets linear und unveränderlich.
Dies stellt keine Einschränkung der Architektur an sich dar.

``LOG/HISTORY:`` Zeigt alle Commits, bis auf den Staging--Commit. Begonnen wird
die Ausgabe mit ``HEAD`` und beendet wird sie mit dem initialen Commit.
Alternativ kann auch die Historie eines einzelnen Verzeichnisses oder einer
Datei angezeigt werden. Dabei werden statt Commits alle Checkpoints dieser
Datei, beginnend mit dem Aktuellsten, ausgegeben.

``STATUS:`` Zeigt den Inhalt des aktuellen Staging--Commits (analog zu ``git
status``) und damit aller geänderten Dateien und Verzeichnisse im Vergleich zu
``HEAD``. Es gibt keine eigene ``DIFF``--Operation, da es keine
partiellen Differenzen gibt. Eine Übersicht der Änderung erhält man durch
Anwendung der ``STATUS`` und ``HISTORY``--Operationen.

## Synchronisation

Ähnlich wie ``git`` speichert ``brig`` für jeden Nutzer seinen zuletzt
bekannten *Store* ab. Mithilfe dieser Informationen können dann
Synchronisationsentscheidungen größtenteils automatisiert getroffen werden.
Welche Stores dabei lokal zwischengespeichert werden, entscheiden die Einträge
der sogenannten *Remote--Liste*.

### Die Remote--Liste {#sec:remote-list}

Jeder Teilnehmer mit dem synchronisiert werden soll, muss zuerst in eine
spezielle Liste von ``brig`` eingetragen werden, damit dieser dem System
bekannt wird. Dies ist vergleichbar mit der Liste die ``git remote -v``
erzeugt: Eine Zuordnung eines menschenlesbaren Namen zu einer eindeutigen
Referenz zum Synchronisationspartner. Im Falle von ``git`` ist das eine URL,
bei ``brig`` handelt es sich um die öffentliche Identität des Partners, also
einer Prüfsumme. Wie später gezeigt wird, ist dieses explizite Hinzufügen des
Partners eine Authentifizierungsmaßnahme, die bewusst eingefügt wurde.
Unter [@sec:user-management] wird das Konzept genauer erläutert.
Dadurch, dass nur mit authentifizierten Knoten Verbindungen aufgebaut werden,
bildet ``brig`` ein *Private-Peer--to--Peer*--Netzwerk[^PP2P] auf Basis von ``ipfs``.

[^PP2P]: Siehe auch: <https://en.wikipedia.org/wiki/Private_peer-to-peer>

![Remote--Liste von vier Repositories und verschiendenen Synchronisationsrichtungen.](images/4/multiple-repos.pdf){#fig:multiple-repos}

Wie in [@fig:multiple-repos] gezeigt wird, können alle Knoten miteinander
synchronisieren, die sich gegenseitig in die Liste eingetragen haben, da von
diesen jeweils der zuletzt bekannte Store übertragen wurde. Die Synchronisation
ist dabei, wie ein ``git pull``, nicht bidirektional. Lediglich die eigenen
Daten werden mit den Fremddaten zusammengeführt. Es gibt kein Äquivalent zu
``git push``, welches die eigenen Daten zu einem Partner überträgt. Jeder
Partner entscheidet selbst, mit welchen anderen Teilnehmern er synchronisiert,
ohne dass seine eigenen Daten überschrieben werden können. In der Grafik wird
zudem ein spezieller Anwendungsfall gezeigt: Das Repository
``rabbithole@wonderland`` ist eine gemeinsame Datenablage für zwei Parteien,
die stets online verfügbar ist[^HOST]. Dieses kann durch ein Skript
automatisiert stets die Änderungen aller bekannten Teilnehmer synchronisieren
und auch weitergeben, wenn der eigentliche Nutzer gerade offline ist. Dieses
Vorgehen bietet sich vor allem dann an, wenn aufgrund der Zeitverschiebung zwei
Nutzer selten zur selben Zeit online sind.

[^HOST]: Typischerweise würde ein solches Repository in einem Rechenzentrum liegen,
       oder auf einem privaten Server.

### Synchronisation einzelner Dateien {#sec:sync-single-file}

In seiner einfachsten Form nimmt ein Synchronisationsalgorithmus als Eingabe
die Metadaten zweier Dateien von zwei Synchronisationspartnern. Als Ausgabe
trifft der Algorithmus auf dieser Basis eine der folgenden Entscheidungen:

1) Die Datei existiert nur bei Partner A.
2) Die Datei existiert nur bei Partner B.
3) Die Datei existiert bei beiden und ist gleich.
4) Die Datei existiert bei beiden und ist verschieden.

Je nach Entscheidung kann für diese Datei eine entsprechende Aktion ausgeführt werden:

1) Die Datei muss zu Partner B übertragen werden (falls bidirektionale Synchronisation gewünscht ist).
2) Die Datei muss zu Partner A übertragen werden.
3) Es muss nichts weiter gemacht werden.
4) Konfliktsituation: Auflösung nötig.

Bis auf den vierten Schritt ist die Implementierung trivial und kann von
einem Computer erledigt werden. Das Kriterium, ob die Datei gleich ist, kann
entweder durch einen direkten Vergleich der Daten gelöst werden (aufwendig) oder durch
den Vergleich der Prüfsummen beider Dateien (schnell, aber vernachlässigbares
Restrisiko durch Kollision). Manche Werkzeuge wie ``rsync`` setzen
sogar auf Heuristiken, indem sie in der Standardkonfiguration aus Geschwindigkeitsgründen nur
das Änderungsdatum und die Dateigröße vergleichen.

Für die Konfliktsituation hingegen kann es keine perfekte, allumfassende Lösung
geben, da die optimale Lösung von der jeweiligen Datei und der Absicht des
Nutzers abhängt. Bei Quelltext--Dateien möchte der Anwender vermutlich, dass
beide Stände möglichst automatisch zusammengeführt werden, bei großen Videodateien ist
das vermutlich nicht seine Absicht. Selbst wenn die Dateien nicht automatisch zusammengeführt werden sollen
(englisch »to merge«), ist fraglich was mit der Konfliktdatei des Partners geschehen soll.
Soll die eigene oder die fremde Version behalten werden? Dazwischen sind auch weitere Lösungen denkbar,
wie das Anlegen einer Konfliktdatei (``photo.png:conflict-by-bob-2015-10-04_14:45``), so wie es beispielsweise
Dropbox macht.[^DROPBOX_CONFLICT_FILE]
Alternativ könnte der Nutzer auch bei jedem Konflikt befragt werden. Dies wäre
allerdings im Falle von ``brig`` nach Meinung des Autors der Usability
stark abträglich.

Im Falle von ``brig`` müssen nur die Änderungen von ganzen Dateien betrachtet werden, aber keine partiellen Änderungen
darin. Eine Änderung der ganzen Datei kann dabei durch folgende Aktionen des Nutzers entstehen:

1) Der Dateiinhalt wurde modifiziert, ergo muss sich die Prüfsumme geändert haben (``MODIFY``).
2) Die Datei wurde verschoben, ergo muss sich der Pfad geändert haben (``MOVE``).
3) Die Datei wurde gelöscht, ergo ist sie im *Staging--Commit* nicht mehr vorhanden (``REMOVE``).
4) Die Datei wurde (initial oder erneut nach einem ``REMOVE``) hinzugefügt (``ADD``).

Der vierte Zustand (``ADD``) ist dabei der Initialisierungszustand. Nicht alle dieser
Zustände führen dabei automatisch zu Konflikten. So sollte beispielsweise ein guter
Algorithmus kein Problem erkennen, wenn ein Partner die Datei modifiziert und
der andere sie nicht verändert, sondern lediglich umbenennt. Eine Synchronisation der entsprechenden
Datei sollte den neuen Inhalt mit dem neuen Dateipfad zusammenführen.
[@tbl:sync-conflicts] zeigt welche Operationen zu Konflikten führen und welche
verträglich sind. Die einzelnen Möglichkeiten sind dabei wie folgt:

* »\xmark«: Die beiden Aktionen sind nicht miteinander verträglich, es sei denn ihre Prüfsummen sind gleich.
            Sind die Prüfsummen gleich, heißt das, dass die exakt gleiche Änderung auf beiden Seiten gemacht wurde.
* »\qmark«: Die Aktion ist prinzipiell verträglich, hängt aber von der Konfiguration ab.
            Entweder wird die Löschung oder die Umbenennung vom Gegenüber propagiert (Standard) oder die eigene Datei wird behalten.
* »\cmark«: Die beiden Aktionen sind verträglich.


| **A/B**      | ``ADD``           | ``REMOVE``        | ``MODIFY``        | ``MOVE``           |
| :----------: | ----------------- | ----------------- | ----------------- | ------------------ |
| ``ADD``      | \xmark            | \qmark            | \xmark            | \xmark             |
| ``REMOVE``   | \qmark            | \cmark            | \qmark            | \qmark             |
| ``MODIFY``   | \xmark            | \qmark            | \xmark            | \cmark             |
| ``MOVE``     | \xmark            | \qmark            | \cmark            | \xmark             |

: Verträglichkeit der atomaren Operationen untereinander für die Partner **A** und **B**. {#tbl:sync-conflicts}

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

	// Prüfe, ob historyA mit den Checkpoints von historyB beginnt.
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
			// können automatisch aufgelöst werden.
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

Die naive Herangehensweise wäre, den obigen Algorithmus für jede Datei im
Verzeichnis zu wiederholen[^SYNC_ONLY_FILE]. Der beispielhafte Verzeichnisbaum
in [@fig:tree-sync] zeigt allerdings bereits ein Problem dabei: Die Menge an
Pfaden, die Alice besitzt wird sich selten ganz mit denen decken, die Bob
besitzt. So kann natürlich Alice Pfade besitzen, die Bob nicht hat und
umgekehrt. Im Beispiel synchronisiert Alice mit Bob. Das heißt, Alice möchte
die Änderungen von Bob empfangen.

![Unterteilung der zu synchronisierenden Pfade in drei Gruppen.](images/4/tree-sync.pdf){#fig:tree-sync}

[^SYNC_ONLY]: Es werden nur reguläre Dateien und leere Verzeichnisse bei der Synchronisation berücksichtigt.

Man könnte also das »naive« Konzept weiterführen und die Menge der zu
synchronisierenden Pfade in drei Untermengen unterteilten. 
Jede dieser Untermengen hätte dann  eine unterschiedliche Semantik:

- Pfade die beide haben ($X = Paths_{A} \bigcap Paths_{B}$): Konfliktpotenzial.
Führe obigen Algorithmus für jede Datei aus. Pfade die nur Alice hat ($Y
= Paths_{A} \setminus Paths_{B}$): Brauchen keine weitere Behandlung. - Pfade
die nur Bob hat ($Z = Paths_{B} \setminus Paths_{A}$): Müssen nur hinzugefügt
werden.

Wie in [@fig:tree-sync] angedeutet, sind diese Mengen allerdings schwerer zu
bestimmen als durch eine simple Vereinigung, beziehungsweise Differenz.
Zwei Beispiele verdeutlichen dies:

* Löscht Bob eine Datei, während Alice sie nicht verändert, würde der Pfad trotzdem in der Menge $Y$ landen.
  Dies hätte zur Folge, dass die Löschung nicht zu Alice propagiert wird.
* Verschiebt Bob eine Datei zu einem neuen Pfad, muss dieser neue Pfad trotzdem
  mit dem alten Pfad von Alice verglichen werden, um die Umbenennung
  zusammenzuführen. In [@fig:tree-sync] sollte also der blaue Knoten mit dem
  grünen verglichen werden.

Es muss also eine Abbildungsfunktion gefunden werden, die jedem Pfad von Alice einen
Pfad von Bob zuordnet. Die Wertemenge dieser Funktion entspricht der Menge $X$,
also aller Pfade die einer speziellen Konfliktauflösung bedürfen. Die Menge $Z$
(also alle Pfade die Bob hat, aber Alice nicht) ergibt sich dann einfach durch
$Z = Paths_{B} \setminus X$. Für die Abbildung der Pfade von Alice zu Bob's Pfaden
funktioniert die Abbildungsfunktion folgendermaßen:

1) Aus Bob's Store werden alle Knoten gesammelt, die sich seit dem letzten gemeinsamen Merge--Point verändert haben.
   Falls es noch keinen gemeinsamen Merge--Point gab, werden alle Knoten angenommen.
2) Aus Bob's Store wird für jeden Knoten die Historie ($=$ Liste aller Checkpoints) seit dem letzten Merge--Point gesammelt, oder
   die gesamte Historie ($=$ alle Checkpoints) falls es noch keinen Merge--Point gab.
3) Es wird eine Abbildung (als assoziatives Array) erstellt, die alle bekannten
   Pfade von Bob der jeweiligen Historie zuordnen, in dem der Pfad vorkommt. Mehr
   als ein Pfad kann dabei auf die gleiche Historie zeigen, wenn Verschiebungen
   vorkamen. Innerhalb dieser Spanne gelöschte Dateien sind in der Abbildung
   unter ihrem zuletzt bekannten Pfad zu finden.
4) Für alle Pfade, die Alice momentan besitzt (Alle Pfade unter ``HEAD``), wird
   der Algorithmus in [@lst:sync-map] ausgeführt. Dieser ordnet jedem Pfad von
   Alice, einem Pfad von Bob zu oder meldet, dass er kein passendes Gegenstück
   finden konnte.

```{#lst:sync-map .go}
// Ein assoziatives Array mit dem Pfad zu der Historie
// seit dem letzten gemeinsamen Merge-Point.
type PathToHistory map[string]History

// BobMapping enthält alle Pfade;
// also auch Pfade die entfernt wurden (unter ihrem letzten Namen)
// Wurden Pfade verschoben, so enthält das Mapping auch alle Zwischenschritte.
func MapPath(HistA History, BobMapping PathToLastHistory) (string, error) {
	// Iteriere über alle Zwischenpfade, die `HistA` hatte.
	// In den meisten Fällen (ohne Verschiebungen) also nur ein einziger.
	for _, path := range HistA.AllPaths() {
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
welche von Bob's Pfaden noch nicht in der errechneten Wertemenge der Abbildung vorkommen.
Diese Pfade können dann in einem zweiten Schritt dem Stand von Alice hinzugefügt werden.

Darüber hinaus gibt es noch einen Spezialfall, der vor der eigentlichen
Synchronisation abgeprüft werden muss. Hat einer der beiden Partner keine
Änderungen gemacht und haben beide Partner eine gemeinsame Historie, kann der
Stand »vorgespult« werden. Das heißt, alle Änderungen der Gegenseite können
direkt übernommen werden. Dieses Vorgehen ist bei ``git`` auch als
*Fast--Forward--Merge* bekannt (``git merge --ff``). Anders als bei ``git``
wird bei ``brig`` allerdings immer ein Merge--Point erstellt, weswegen
dies nur eine algorithmische Optimierung darstellt.

### Austausch der Metadaten {#sec:metadata-exchange}

Um die Metadaten nun tatsächlich synchronisieren zu können, muss ein Protokoll
etabliert werden, mit dem zwei Partner ihren Store über das Netzwerk austauschen können.
Im Folgenden wird diese Operation, analog zum gleichnamigen ``git``--Kommando[^TRANSFER_PROTOCOL], ``git fetch`` genannt.

[^TRANSFER_PROTOCOL]: <https://git-scm.com/book/be/v2/Git-Internals-Transfer-Protocols>

![Das Protokoll das bei der ``FETCH``--Operation ausgeführt wird.](images/4/fetch-protokoll.pdf){#fig:fetch-protocol}

Wie in [@fig:fetch-protocol] gezeigt, besteht das Protokoll aus drei Teilen:

* Alice schickt eine ``FETCH``--Anfrage zu Bob, der den Namen des zu holenden Stores enthält.
  Im Beispiel ist dies Bob's eigener Store, ``bob@realworld.org``.
* Falls Alice in Bob's Remote--Liste steht, wandelt Bob seinen eigenen Store in eine
  exportierbare Form um, die aus einer großen serialisierten Nachricht[^EXPORT] besteht, die alle notwendigen Daten enthält.
- Die serialisierte Form des Stores wird über den Transfer--Layer von ``brig`` (siehe [@sec:transfer-layer])
  zurück an ``alice@wonderland.lit`` geschickt.
- Alice importiert die serialisierte Form in einen neuen, leeren Store und speichert
  das Ergebnis in der Liste der Stores ihrer Kommunikationspartner.
  Eine Synchronisation der beiden Metadatensätze kann nun lokal bei Alice erfolgen.

[^EXPORT]: Die Form des serialisierten Export--Formattes ist nicht weiter interessant und kann im Anhang [@sec:data-model]
         eingesehen werden (Message: *Store*).

Aus Zeitgründen ist dieses Protokoll momentan noch sehr einfach gehalten und
beherrscht keine differentiellen Übertragungen. Da hier nur Metadaten
übertragen werden sollte das nur bedingt ein Problem sein. In der Tat müssten
aber nur die Commits seit dem letzten gemeinsamen Merge--Point übertragen
werden.

Auch sind zum momentanen Stand noch keine *Live--Updates* möglich. Hierfür
müssten sich die einzelnen Knoten bei jeder Änderung kleine *Update--Pakete*
schicken, welche einen einzelnen *Checkpoint* beinhalten würden.
Diese Checkpoints müssten dann jeweils in den aktuellen Staging--Bereich eingepflegt
werden. Dadurch wären Änderungen in »Echtzeit« auf anderen Knoten verfügbar.
Aus Zeitgründen wird an dieser Stelle aber nur auf diese Möglichkeit verwiesen;
eine konzeptuelle Implementierung hierzu steht noch aus.


### Abgrenzung zu anderen Synchronisationswerkzeugen

In der Fachliteratur (vgl. unter anderem [@cox2005file])
findet sich zudem die Unterscheidung zwischen *informierter* und
*uninformierter* Synchronisation. Der Hauptunterschied ist, dass bei ersterer
die Änderungshistorie jeder Datei als zusätzliche Eingabe zur Verfügung steht.
Auf dieser Basis können dann intelligentere Entscheidungen bezüglich der
Konflikterkennung getroffen werden. Insbesondere können dadurch aber leichter
die Differenzen zwischen den einzelnen Ständen ausgemacht werden: Für jede
Datei muss dabei lediglich die in [@lst:file-sync] gezeigte Sequenz abgelaufen
werden, die von beiden Synchronisationspartnern unabhängig ausgeführt werden
muss. Werkzeuge wie ``rsync`` oder ``unison`` betreiben eine *uninformierte
Synchronisation*. Sie müssen bei jedem Programmlauf Metadaten über beide
Verzeichnisse sammeln und darauf arbeiten.

### Speicherquoten

Werden immer mehr Modifikationen gespeichert, so steigt der Speicherplatz immer
weiter an, da ohne ein Differenzmechanismus jede Datei pro Version einmal voll
abgespeichert werden muss. Die Anzahl der Objekte die dabei gespeichert werden
können, hängt von dem verfügbaren Speicherplatz ab. Sehr alte Versionen werden
dabei typischerweise nicht mehr benötigt und können bei Platzbedarf gelöscht
werden. Diese Aufgabe wird derzeit nicht von ``brig`` selbst übernommen,
sondern vom ``ipfs``--Backend. Dieses unterstützt mit dem Befehl ``ipfs gc``
eine Bereinigung von Objekten, die keinen Pin mehr haben. Zudem kann ``brig``
den Konfigurationswert ``Datastore.StorageMax`` von ``ipfs`` auf eine maximale
Höhe (minus einen kleinen Puffer für ``brig``--eigene Dateien) setzen. Wird
dieser überschritten, geht der Garbage--Collector aggressiver vor und löscht
nicht gepinnte Objekte sofort. In der momentanen Architektur und
Implementierung sind allerdings zu diesem Zeitpunkt noch keine Speicherquoten
vorhanden.

Eine Möglichkeit Speicher zu reduzieren, wäre die Einführung von
*Packfiles*, wie ``git`` sie implementiert[^PACKFILES_GIT]. Diese komprimieren nicht eine
einzelne Datei, sondern packen mehrere Objekte in ein zusammengehöriges Archiv.
Dies kann die Kompressionsrate stark erhöhen wenn viele ähnliche Dateien
(beispielsweise viele subtil verschiedene Versionen der gleichen Datei)
zusammen gepackt werden. Nachteilig sind die langsameren Zugriffszeiten.
Eine Implementierung dieser Lösung müsste zwischen eigentlichem Datenmodell
und dem ``ipfs``--Backend eine weitere Schicht einschieben, welche
transparent und intelligent passende Dateien in ein Archiv verpackt und umgekehrt
auch wieder entpacken kann. Diese Idee wird in [@sec:verbesserungen] noch einmal
aufgegriffen.

[^PACKFILES_GIT]: Mehr Details zur ``git``--Implementierung hier: <https://git-scm.com/book/uz/v2/Git-Internals-Packfiles>

## Architekturübersicht

Um den eigentlichen Kern des Store sind alle anderen Funktionalitäten gelagert.
[@fig:arch-overview] zeigt diese in einer Übersicht. Die einzelnen Unterdienste
werden im Folgenden besprochen.

![Übersicht über die Architektur von ``brig``.](images/4/architecture-overview.pdf){#fig:arch-overview}

### Lokale Aufteilung in Client und Daemon

``brig`` ist architektonisch in einem langlebigen Daemon--Prozess und einem
kurzlebigen Kontroll--Prozess aufgeteilt, welche im Folgenden jeweils ``brigd``
und ``brigctl`` genannt werden[^BRIGCTL_NOTE]. Beide Prozesse kommunizieren
dabei über das Netzwerk mit einem speziellen Protokoll, welches auf einen
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
sein. Abgesehen davon ist es aus Effizienzgründen förderlich, wenn nicht bei
jedem eingetippten Kommando das gesamte Repository geladen werden muss. Auch
ist es durch die Trennung möglich, dass ``brigd`` auch von anderen
Programmiersprachen und Prozessen auf dem selben Rechner aus gesteuert werden
kann. Verbindungen von außen sollten aus Sicherheitsgründen nicht angenommen
werden. Unter unixoiden Betriebssystemen wäre eine Alternative zu normalen
Netzwerksockets die Nutzung von Unix--Domain--Sockets[^UNIX_DOMAIN]. Diese sind
als Datei im Dateisystem erreichbar und können daher mit entsprechenden
Zugriffsrechten nur von bestimmten Nutzern benutzt werden.

[^UNIX_DOMAIN]: Siehe auch: <https://en.wikipedia.org/wiki/Unix_domain_socket>

[^BRIGCTL_NOTE]: Tatsächlich gibt es derzeit keine ausführbaren Dateien mit
diesen Namen. Die Bezeichnungen ``brigctl`` und ``brigd`` dienen lediglich der
Veranschaulichung.
[^PROTOBUF]: Mehr Informationen unter: <https://developers.google.com/protocol-buffers>

### ``brigctl``: Aufbau und Aufgabe {#sec:client}

Zusammengefasst ist ``brigctl`` eine »Fernbedienung« für ``brigd``, welche im
Moment exklusiv von der Kommandozeile aus bedient wird. In den meisten Fällen
verbindet sich der Kommando--Prozess ``brigctl`` beim Start zu ``brigd``,
sendet ein mittels *Protobuf* serialisiertes Kommando und wartet auf die
dazugehörige Antwort welche dann deserialisiert wird. Nachdem die empfangene
Antwort, je nach Art, ausgewertet wurde, beendet sich der Prozess wieder.

**Protobuf Protokoll:** Das Protokoll ist dabei so aufgebaut, dass
für jede Aufgabe, die ``brigd`` erledigen soll ein separates Kommando
existiert. Neben einer allgemeinen Typbezeichnung, können auch vom Kommando
abhängige optionale und erforderliche Parameter enthalten sein. Ein gekürzter
Auszug aus der Protokollspezifikation veranschaulicht dies in [@lst:proto-command].

```{#lst:proto-command .c}
enum MessageType {
	ADD = 0;
	// ...
}

message Command {
	// Typ des Kommandos
	required MessageType command_type = 1;

	message AddCmd {
		// Absoluter Pfad zur Datei auf der Festplatte des Nutzers.
		required string file_path = 1;

		// Pfad innerhalb von brig (/photos/me.png)
		required string repo_path = 2;

		// Füge Verzeichnisse rekursiv hinzu? (Standard: Ja)
		optional bool recursive = 3;
	}
	// ... weitere Subkommandos ...

	// Falls der Typ ADD war, lese von 'add_commando'
	optional AddCmd add_command = 2;
	// ... weitere Kommandoeinträge ...
}
```

Analog dazu kann ``brigd`` mit einer *Response* auf ein *Command* antworten. In
[@lst:proto-response] wird beispielhaft die Antwortspezifikation
(``OnlineStatusResp``) auf ein ``OnlineStatusCmd``--Kommando gezeigt, welches
prüft, ob ``brigd`` Verbindungen von Außen annimmt.

```{#lst:proto-response .c}
message Response {
	// Typ der Antwort
    required MessageType response_type = 1;

	// Wahr, falls es keine Fehlerantwort ist
    required bool success = 2;

	// Bei einem Fehler wird ein optionale Fehlerbeschreibung angegeben.
	optional string error = 3;

	// Detaillierter Fehlercode (noch nicht benutzt)
	optional id errno = 4;

	message OnlineStatusResp {
    	required bool is_online = 1;
	}
	// ... Mehr Unterantworten ...

	optional OnlineStatusResp online_status_resp = 5;
	// ... Mehr Antworteinträge ...
}
```

Neben der Kommunikation mit  ``brigd`` muss ``brigctl`` noch drei andere Aufgaben erledigen:

* **Initiales Anlegen eines Repositories:** Bevor ``brigd`` gestartet werden kann,
  muss die in [@fig:brig-repo-tree] gezeigte Verzeichnisstruktur angelegt werden.
* **Bereitstellung des User--Interfaces:** Das zugrundeliegende Protokoll wird so gut
  es geht vom Nutzer versteckt und Fehlermeldungen müssen möglichst gut beschrieben werden.
* **Autostart von ``brigd``:** Damit der Nutzer nicht explizit ``brigd`` starten
  muss, sollte der Daemon--Prozess automatisch im Hintergrund gestartet werden,
  falls er noch nicht erreichbar ist. Dies setzt ``brigctl`` um, indem es dem
  Nutzer nach dem Passwort zum Entsperren eines Repositories fragt und das
  Passwort beim Start an ``brigd`` weitergibt, damit der Daemon--Prozess das
  Repository entsperren kann.

### ``brigd``: Aufbau und Aufgabe

Der Daemon--Prozess implementiert alle Kernfunktionalitäten.
Die einzelnen Komponenten werden in [@sec:einzelkomponenten] beschrieben.

Als Netzwerkdienst muss ``brigd`` auf einen bestimmten Port (momentan
standardmäßig Port ``6666`` auf ``127.0.0.1``) auf Anfragen warten. Es werden keine Anfragen von
außen angenommen, da über diese lokale Verbindung fast alle
sicherheitskritischen Informationen ausgelesen werden können.
Für den Fall, dass ein Angreifer den lokalen Netzwerkverkehr mitlesen kann wird
der gesamte Netzwerkverkehr zwischen ``brigctl`` und ``brigd`` mit AES256
verschlüsselt. Der Schlüssel wird beim Verbindungsaufbau mittels
Diffie--Hellmann ausgetauscht. Die Details des Protokolls werden in
[@cpiechula] beschrieben.

Die Anzahl der gleichzeitig offenen Verbindungen wird auf ein Maximum von ``50``
limitiert und Verbindungen werden nach Inaktivität mit einer Zeitüberschreitung von 10
Sekunden automatisch getrennt. Diese Limitierungen soll verhindern, dass
fehlerhafte Clients den Hintergrundprozess zu stark auslasten.

Im selben Prozess wie ``brigd`` läuft auch der ``ipfs``--Daemon und nutzt dabei
standardmäßig den Port ``4001``, um sich mit dem Netzwerk zu verbinden.
Nachteilig an diesem Vorgehen ist, dass ein Absturz oder eine Sicherheitslücke
in ``ipfs`` auch ``brigd`` betreffen kann. Längerfristig sollten beide Prozesse
möglichst getrennt werden, auch wenn dies aus Effizienzgründen nachteilig ist.

## Einzelkomponenten {#sec:einzelkomponenten}

Im Folgenden werden die einzelnen Komponenten von ``brigd`` aus
architektonischer Sicht erläutert. Genauere Angaben zu Implementierungsdetails,
insbesondere zum FUSE--Dateisystem, folgen im nächsten Kapitel.

### Dateiströme

Im ``ipfs``--Backend werden nur verschlüsselte und zuvor komprimierte
Datenströme gespeichert. Verschlüsselung ist bei ``brig`` nicht optional. Hat
ein Angreifer die Prüfsumme einer Datei erbeutet, so kann er die Datei aus dem
``ipfs``--Netzwerk empfangen. Solange die Datei aber verschlüsselt ist, so wird
der Angreifer alleine mit den verschlüsselten Daten ohne den dazugehörigen
Schlüssel nichts anfangen können.
In der Tat unterstützt er das ``ipfs``--Netzwerk sogar, da der Knoten des
Angreifers auch wieder seine Bandbreite zum Upload anbieten muss, da der Knoten
sonst ausgebremst wird.
Aus diesem Grund ist es aus Sicherheitsperspektive keine Notwendigkeit,
``brig`` in einem abgeschotteten Netzwerk zu betreiben. Standardmäßig verbindet
sich ``brig`` mit dem weltweiten ``ipfs``--Netzwerk, indem es die standardmäßig
eingetragenen Bootstrap--Knoten kontaktiert.

Nachteilig an einer »zwangsweisen« Verschlüsselung ist, dass die
Deduplizierungsfähigkeit von ``ipfs`` ausgeschaltet wird. Wird die selbe Datei
mit zwei unterschiedlichen Schlüsseln verschlüsselt, so werden die
resultierenden Daten (bis auf ihre Größe) keine Ähnlichkeit besitzen, sind also
kaum deduplizierbar. Trotzdem ist die Unterteilung in Blöcke durch ``ipfs``
sinnvoll, da dadurch bereits heruntergeladene Blöcke nicht ein zweites Mal
besorgt werden müssen. So lässt sich der Download von großen Dateien
unterbrechbar und wieder fortsetzbar gestalten.

Eine mögliche Lösung wäre ein Verfahren namens *Convergent
Encryption*[@douceur2002reclaiming]. Dabei wird der Schlüssel der zu
verschlüsselten Datei aus der Prüfsumme derselben Datei abgeleitet. Dies hat
den Vorteil, dass gleiche Dateien auch den gleichen (deduplizierbaren)
Ciphertext generieren. Der Nachteil ist, dass ein Angreifer feststellen kann,
ob jemand eine Datei (beispielsweise Inhalte mit urhebergeschützen Inhalten)
besitzt. Im Protoypen werden die Dateischlüssel daher zufällig generiert,
was die Deduplizierungsfunktion von ``ipfs`` momentan ausschaltet.
Dies hat auch zur Folge, dass die Synchronisation von zwei unabhängig
hinzugefügten, aber sonst gleichen Dateien zwangsweise dazu führt, dass diese
unterschiedlich sind, da auf beiden Seiten jeweils ein anderer Schlüssel
generiert wird. Die Vor- und Nachteile dieses Verfahrens wird weiter in [@cpiechula]
diskutiert.

#### Verschlüsselung {#sec:encryption}

Für ``brig`` wurde ein eigenes Containerformat für verschlüsselte Daten
eingeführt, welches wahlfreien Zugriff auf beliebige Bereiche der
verschlüsselten Datei erlaubt, ohne die gesamte Datei entschlüsseln zu müssen.
Dies ist eine wichtige Eigenschaft für die Implementierung des
FUSE--Dateisystems und ermöglicht zudem aus technischer Sicht das Streaming von
großen, verschlüsselten Dateien wie Videos. Zudem kann das Format durch den
Einsatz von *Authenticated Encryption (AE*, [@bellare2000authenticated]) die Integrität der verschlüsselten
Daten sichern.

Es werden lediglich reguläre Dateien verschlüsselt. Verzeichnisse existieren
nur als Metadaten und werden nicht von ``ipfs`` gespeichert. Die Details und
Entscheidungen zum Design des Formats werden in [@cpiechula] dargestellt.

![Aufbau des Verschlüsselungs--Dateiformats](images/4/format-encryption.pdf){#fig:format-encryption}

**Enkodierung:** [@fig:format-encryption] zeigt den Aufbau des Formats. Ein
roher Datenstrom (dessen Länge nicht bekannt sein muss) wird an den Enkodierer 
gegeben. Als weitere Eingabe muss ein Algorithmus ausgewählt werden und ein
entsprechend dimensionierter, symmetrischer Schlüssel mitgegeben werden.
Werden die ersten Daten geschrieben, so schreibt der Kodierer zuerst einen
36--Byte großen Header. In diesem finden sich folgende Felder:

* Eine *Magic--Number*[^MAGIC_NUMBER] (8 Byte, ASCII--Repräsentation von
  ``moosecat``) zur schnellen Identifikation einer
  von ``brig`` geschriebenen Datei.
* Die *Versionsnummer* (2 Byte) des vorliegenden Formats. Standardmäßig »``0x01``«.
  Sollten Änderungen am Format nötig sein,
  so müssen nur die ersten 10 Byte beibehalten werden und die Versionsnummer inkrementiert
  werden. Für die jeweilige Version kann dann ein passender Dekodierer genutzt werden.
* Die verwendete *Blockchiffre* (siehe [@cpiechula]) (2 Byte) zur
  Verschlüsselung. Standardmäßig wird *ChaCha20/Poly1305* (siehe
  [@nir2015chacha20]) eingesetzt, aber es kann auch AES (siehe [@everyday_crypto], S.
  116 ff.) mit 256 Bit Schlüssellänge im Galois--Counter--Modus (GCM, siehe [@cpiechula]) verwendet werden.
* Die *Länge* (4 Byte) des verwendeten Schlüssels in Bytes.
* Die *maximale Blockgröße* (4 Byte) der nachfolgenden Blöcke in Bytes.
* Ein *Message--Authentication--Code (MAC, siehe auch [@everyday_crypto], S. 205 ff.)* (16 Byte)
  der die Integrität des Headers sicherstellt.

[^MAGIC_NUMBER]: Siehe auch: <https://de.wikipedia.org/wiki/Magische_Zahl_(Informatik)>

Nachdem der Header geschrieben wurde, sammelt der Enkodierer in einem internen
Puffer ausreichend viele Daten, um einen zusammenhängenden Block zu schreiben
(standardmäßig 64 Kilobyte). Ist diese Datenmenge erreicht wird der Inhalt des
Puffers verschlüsselt und ein kompletter Block ausgegeben. Dieser enthält
folgende Felder:

* Eine *Nonce* (siehe auch [@everyday_crypto], S. 263) (8 Byte). Diese
  eindeutige Nummer wird bei jedem
  geschriebenen Block inkrementiert und stellt daher die Blocknummer dar. Sie
  wird benutzt, um die Reihenfolge des geschriebenen Datenstroms zu validieren
  und wird zudem als öffentlich bekannte Eingabe für den
  Verschlüsselungsalgorithmus benutzt.
* Die eigentlichen, verschlüsselten Daten. Diese sind maximal so lang wie die
  maximale Blockgröße, können aber im Falle des letzten Blockes kleiner sein.
* Am Ende kann, je nach Algorithmus, ein gewisse Überlänge durch *Padding* entstehen.
  Zudem wird an jeden Block eine weitere MAC angehängt, welche die Integrität
  der Nonce und der nachfolgenden, verschlüsselten Daten sicherstellt.

So wird blockweise weiter verfahren, bis alle Daten des Ursprungsdatenstroms aufgebraucht
worden sind. Der letzte Block darf als einziger kleiner als die maximale Blockgröße sein.
Der resultierende Datenstrom ist etwas größer als der Eingabedatenstrom. Seine Größe lässt
sich wie in [@eq:enc-size] gezeigt mithilfe der Eingabegröße $s$ der Datei in Bytes und der Blockgröße $b$ berechnen:

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
dem eigentlichen Datenblock und dem Schlüssel mitgegeben. Dieser überprüft ob die Integrität des
Datenblocks korrekt ist und entschlüsselt diesen im Erfolgsfall. Anhand der
Position im Datenstrom wird zudem überprüft ob die Blocknummer zum Wert in der
Nonce passt. Stimmen diese nicht überein, wird die Entschlüsselung verweigert,
da ein Angreifer möglicherweise die Reihenfolge der Blöcke hätte vertauschen können.

**Wahlfreier Zugriff:** Wurde der Header bereits gelesen, so kann ein
beliebiger Block im Datenstrom gelesen werden, sofern der unterliegende
Datenstrom wahlfreien Zugriff (also die Anwendung von ``Seek()``) erlaubt. Die
Anfangsposition des zu lesenden Blocks kann mit [@eq:seek-off] berechnet
werden, wobei $o$ der Offset im unverschlüsselten Datenstrom ist.

$$f_{\text{offset}}(o) = 36 + \left\lceil\frac{o}{b}\right\rceil\times(8 + 16 + b)$$ {#eq:seek-off}

Der Block an dieser Stelle muss komplett gelesen und entschlüsselt werden, auch
wenn nur wenige Bytes innerhalb des Blocks angefragt werden. Da typischerweise
die Blöcke aber fortlaufend gelesen werden, ist das aus Sicht des Autors ein
vernachlässigbares Problem.

Die einzelnen Blocks des vorgestellten Formats ähneln der *Secretbox* der freien
NaCL--Bibliothek[^NACL_LIB]. Diese erlaubt allerdings keinen wahlfreien
Zugriff. Abgesehen handelt es sich um eine Neuentwicklung, die auch außerhalb
von ``brig`` eingesetzt werden kann.

[^NACL_LIB]: Siehe auch: <https://nacl.cr.yp.to/secretbox.html>

#### Kompression

Bevor Datenströme verschlüsselt werden, werden diese von ``brig`` auch
komprimiert[^ANDERSRUM]. Auch hier wurde ein eigenes Containerformat
entworfen, welches in [@fig:format-compression] gezeigt wird.

[^ANDERSRUM]: Rein technisch ist es auch andersherum möglich, aber aufgrund der
            prinzipbedingten, hohen Entropie von verschlüsselten Texten
			wären in dieser Reihenfolge die Kompressionsraten sehr gering.

![Aufbau des Kompressions--Dateiformats.](images/4/format-compression.pdf){#fig:format-compression}

Nötig war dieser Schritt auch hier wieder weil kein geeignetes Format gefunden
werden konnte, welches wahlfreien Zugriff im komprimierten Datenstrom zulässt,
ohne dass dabei die ganze Datei entpackt werden muss.

**Enkodierung:** Der Eingabedatenstrom wird in gleich große Blöcke unterteilt
(standardmäßig maximal 64KB), wobei nur der letzte Block kleiner sein darf.
Nachdem der Header geschrieben wurde, folgt jeder Eingabeblock als
komprimierter Block mit variabler Länge. Am Schluss wird ein Index geschrieben,
der beschreibt welcher Eingabeblock mit welchem komprimierten Block
korrespondiert. Der Index kann nur am Ende geschrieben werden, da die genauen
Offsets innerhalb dieses Indexes erst nach dem Komprimieren bekannt sind. Für
eine effiziente Nutzung dieses Formats ist es also nötig, dass der Datenstrom
einen effizienten, wahlfreien Zugriff am Ende der Datei bietet.
Glücklicherweise unterstützt dies ``ipfs``. Datenströme wie ``stdin`` unter
Unix unterstützen allerdings keinen wahlfreien Zugriff, weshalb das
vorgestellte Format für solche Anwendungsfälle eher ungeeignet ist.

Der Index besteht aus zwei Teilen: Aus dem eigentlichen Index und einem
sogenannten »Trailer«, der die Größe des Indexes enthält. Zusätzlich enthält
dieser Trailer noch die verwendete Blockgröße, in die der unkomprimierte
Datenstrom unterteilt wurde. Der eigentliche Index besteht aus einer Liste von
64--Bit Offset--Paaren. Jedes Paar enthält einmal den unkomprimierten und
einmal den komprimierten Offset eines Blocks als Absolutwert gemessen vom
Anfang des Datenstroms. Am Ende wird ein zusätzliches Paar eingefügt, welches
zu keinen realen Block verweist. Dieses letzte Paar beschreibt die Größe des
unkomprimierten und komprimierten Datenstroms.

Der vorangestellte Header enthält alle Daten, die definitiv vor der Kompression
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
    gab es zu diesen Zeitpunkten noch keine vernünftig nutzbaren Bibliotheken.

**Dekodierung:** Bevor der erste Block dekodiert werden kann muss sowohl der Header
als auch der Index geladen werden. Dazu müssen die ersten 12 Bytes des
Datenstroms gelesen werden. Im Anschluss muss fast an das Ende (Ende minus
12 Byte) des Datenstroms gesprungen werden, um dort den Trailer zu lesen. Mit der
darin enthaltenen Größe des Indexes kann die Anfangsposition des Indexes
bestimmt werden (Ende minus 12 Byte minus Indexgröße). Alle Offset--Paare im Index
werden in eine sortierte Liste geladen. Die Blockgröße eines
komprimierten/unkomprimierten Blocks an der Stelle ergibt sich dabei aus der
Differenz des Offset--Paars an der Stelle $n+1$ und seines Vorgängers an der
Stelle $n$. Mithilfe der Blockgröße kann ein entsprechend dimensioniertes Stück vom
komprimierten Datenstrom gelesen und dekomprimiert werden.

**Wahlfreier Zugriff:** Um auf einen beliebigen Offset $o$ im unkomprimierten
Datenstrom zuzugreifen muss dieser zunächst in den komprimierten Offset
übersetzt werden. Dazu muss mittels binärer Suche im Index der passende, Anfang
des unkomprimierten Blocks gefunden werden. Wurde der passende Block bestimmt,
ist auch der Anfangsoffset im komprimierten Datenstrom bekannt. Dadurch kann
der entsprechende Block ganz geladen und dekomprimiert werden. Innerhalb der
dekomprimierten Daten kann dann vom Anfangsoffset $a$ noch zum Zieloffset $o-a$
gesprungen werden.

### Transfer--Layer {#sec:transfer-layer}

Damit Metadaten ausgetauscht werden können, ist ein sicherer Steuerkanal nötig,
der unabhängig vom Datenkanal ist, über den die eigentlichen Daten ausgetauscht werden.
Über diesen muss ein *Remote--Procedure--Call* (RPC[^RPC]) ähnliches Protokoll
implementiert werden, damit ein Teilnehmer Anfragen an einen anderen stellen kann.

[^RPC]: Siehe auch: <https://de.wikipedia.org/wiki/Remote_Procedure_Call>

Die Basis dieses sicheren Steuerkanals wird von ``ipfs`` gestellt. Dabei wird kein
zusätzlicher Netzwerkport für den RPC--Dienst in Anspruch genommen, da alle
Kommunikation über den selben Kanal laufen, wie die eigentliche Datenübertragung. Es
findet also eine Art »Multiplexing« statt.

Dies wird durch das fortgeschrittenes Netzwerkmodell von ``ipfs`` möglich[^LIP2P],
welches in [@fig:ipfs-net] gezeigt werden. Nutzer des gezeigten Netzwerkstacks
können eigene Protokolle registrieren, die mittels eines *Muxing--Protokolls*
namens *Multistream*[^MULTISTREAM] in einer einzigen, gemeinsamen
physikalischen Verbindung zusammengefasst werden. Der sogenannte *Swarm* hält
eine Verbindung zu allen zu ihm verbundenen Peers und macht es so möglich jeden
Netzwerkpartner von der Protokollebene aus über seine Peer--ID anzusprechen.
Der eigentliche Verbindungsaufbau geschieht dann, wie in [@sec:ipfs-attrs]
beschrieben auch über NAT--Grenzen hinweg.

![Der Netzwerkstack von ``ipfs`` im Detail[^NET_SOURCE].](images/4/ipfs-network.pdf){#fig:ipfs-net width=60%}

[^MULTISTREAM]: Siehe auch: <https://github.com/multiformats/multistream>
[^NET_SOURCE]: Diese Grafik ist eine Aufbereitung von: <https://github.com/libp2p/go-libp2p/tree/master/p2p/net>
[^LIP2P]: Implementiert als eigene Bibliothek »libp2p«: <https://github.com/libp2p/go-libp2p>

Im Falle von ``brig`` wird ein eigenes Protokoll registriert, um mit anderen
Teilnehmern zu kommunizieren. Dieses ist ähnlich aufgebaut wie das Protokoll
zwischen Daemon und Client (siehe [@sec:client]), unterstützt aber
andere Anfragen und hat erhöhte Sicherheitsanforderungen.
Eine genauere Beschreibung des Protokolls wird in [@cpiechula] gegeben,
hier werden nur kurz die wichtigsten Eigenschaften genannt:

- Authentifizierung mittels Remote--Liste bei jedem Verbindungsaufbau.
* Anfragen und Antworten werden als Protobuf--Nachricht enkodiert.
  Die eigentliche Protokolldefinition kann in [@sec:rpc-proto] eingesehen werden.
* Kompression der gesendeten Nachrichten mittels Snappy.
- Zusätzliche Verschlüsselung der Verbindung, mittels eines via *Elliptic Curve Diffie Hellman* ausgetauschten Schlüssels.
- Senden von »Broadcast«--Nachrichten zu allen bekannten, verbundenen Teilnehmern.
  Es wird keine Antwort auf Broadcast--Nachrichten erwartet. Diese sind daher
  eher für Status--Updates geeignet.

Im momentanen Zustand wird nur eine einzige Anfrage unterstützt.
Dies ist die in [@sec:metadata-exchange] beschriebene ``FETCH``--Anfrage. Zukünftig
ist die Einführung weiterer Anfragen geplant. Um beispielsweise
Echtzeit--Synchronisation zu unterstützen, müssten zwei weitere Nachrichten eingeführt werden:

- ``UPDATE``: Eine Nachricht die aktiv an alle Teilnehmer in der Remote--Liste
  geschickt wird. Sie enthält einen einzelnen Checkpoint. Die darin beschriebene
  atomare Änderung sollte dann auf Empfängerseite direkt in den Staging--Bereich
  eingegliedert werden.
* ``DIFF <COMMIT_HASH>:`` Wie ``FETCH``, gibt aber nur die Änderungen seit dem 
  angegebenen ``COMMIT_HASH`` zurück.

### Benutzermanagement {#sec:user-management}

In den Anforderungen in [@sec:requirements] wird eine menschenlesbare
Identität gefordert, mit der Kommunikationspartner einfach erkennbar sind. Der von ``ipfs``
verwendete Identitätsbezeichner ist allerdings eine für Menschen schwer zu
merkende Prüfsumme (die »Peer--ID«).

Es wurden in dieser Arbeit bereits einige Identifikationsbezeichner
beispielhaft verwendet. Diese entsprechen einer abgeschwächten Form der
Jabber--ID[^JID] (*JID*, vgl. auch [@xmpp], S. 14). Diese hat, ähnlich wie eine
E--Mail Adresse, die Form ``user@domain/resource``. Beim Jabber/XMPP Protokoll
ist der Teil hinter dem »``/``« optional, der Rest ist zwingend erforderlich.
Als Abschwächung ist bei ``brig`` auch der Teil hinter dem »``@``« optional.
Darüber hinaus sollen folgende Regeln gelten:

[^JID]: Mehr Details unter: <https://de.wikipedia.org/wiki/Jabber_Identifier>

- Es sind keine Leerzeichen erlaubt.
- Ein leerer String ist nicht valide.
* Groß- und Kleinschreibung wird nicht unterschieden. Es wird empfohlen den Namen klein zu schreiben,
  so wie es bei Mailadressen und URLs der Fall ist.
- Der String muss valides UTF8[^UTF8] sein.
- Der String muss der »UTF-8 Shortest Form[^SHORTEST]« entsprechen
- Der String darf durch die »UTF-8 NKFC Normalisierung[^NORMALIZATION]« nicht verändert werden.
- Alle Charaktere müssen druckbar und auf dem Bildschirm darstellbar sein.

Insbesondere die letzten vier Punkte dienen der Sicherheit, da ein Angreifer
versuchen könnte eine Unicode--Sequenz zu generieren, welche visuell genauso
aussieht wie die eines anderen Nutzers, aber einer anderen Byte--Reihenfolge
und somit einer anderen Identität entspricht.

[^UTF8]: Siehe auch: <https://de.wikipedia.org/wiki/UTF-8>
[^SHORTEST]: Siehe auch: <http://unicode.org/versions/corrigendum1.html>
[^NORMALIZATION]: Siehe auch: <http://www.unicode.org/reports/tr15/\#Norm_Forms>

Valide Identitätsbezeichner wären also beispielsweise:

- ``alice``
- ``alice@company``
- ``alice@company.de``
- ``alice@company.de/laptop``
- ``böb@subdomain.company.de/desktop``

Die Wahl der JID als Basis hat einige Vorteile:

- Eine E--Mail Adresse  oder eine JID ist gleichzeitig ein valider
  Identitätsbezeichner.
- Der Nutzer kann eine fast beliebige Unicode Sequenz als Name verwenden, was
  beispielsweise für Nutzer des kyrillischen Alphabetes nützlich ist.
- Unternehmen können die Identifikationsbezeichner hierarchisch gliedern. So
  kann *Alice* der Bezeichner ``alice@security.google.com`` zugewiesen werden,
  wenn sie im Sicherheitsteam arbeitet.
- Der *Ressourcen*--Teil hinter dem »``/``« ermöglicht die Nutzung desselben
  Nutzernamens auf verschiedenen Geräten, wie beispielsweise ``desktop`` oder ``laptop``.

Eine Nutzung des ``domain`` und ``resource``--Teils ist kein Zwang, wird aber
als Konvention empfohlen, da es eine Unterteilung in Gruppen und Geräte
ermöglicht.

Um den Identifikationsbezeichner im Netzwerk auffindbar zu machen, wendet
``brig`` einen »Trick« an. Jeder ``brig``--Knoten veröffentlicht einen
einzelnen ``blob`` in das ``ipfs``--Netzwerk mit dem Inhalt
``brig#user:<username>``. Dieses Verfahren wird *Publishing* genannt. Ein Nutzer der nun einen solchen menschenlesbaren  Namen
zu einer Netzwerkadresse  auflösen möchte, kann den Inhalt des obigen
Datensatzes generieren und daraus eine Prüfsumme bilden. Mit der entstandenen
Prüfsumme kann wie in [@lst:user-hash] mittels dem folgenden
Verfahren[^GO_MULTIHASH] herausgefunden werden, welche Knoten diesen Datensatz
anbieten:

[^GO_MULTIHASH]: Benötigt das ``multihash`` Werkzeug: <https://github.com/multiformats/go-multihash/tree/master/multihash>

```{#lst:user-hash .bash}
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
Das Unternehmen spiegelt sich in auch in ihren Identitätsbezeichnern wieder:

- ``alice@corp.de/server``
- ``bob@corp.de/laptop``
- ``charlie@corp.de/desktop``

Neben den gesamten Nutzernamen, können diese drei Nutzer auch ihren
Unternehmensnamen (``corp.de``) *publishen*, beziehungsweise auch ihren Nutzernamen ohne
den ``resource``--Zusatz. So ist es beispielsweise wie in [@lst:corp-hash] möglich
die öffentlichen Identitäten alle Unternehmensmitglieder aufzulösen:

```{#lst:corp-hash .bash}
$ CORP_HASH=$(printf 'brig#domain:%s' corp.de | multihash -)
$ ipfs dht findprovs $CORP_HASH
<PEER_ID_OF_POSSIBLE_CORP_MEMBER_1>
<PEER_ID_OF_POSSIBLE_CORP_MEMBER_2>
...
```

Die einzelnen IDs können dann, sofern bekannt, zu den »Klarnamen« aufgelöst
werden die in der Remote--Liste jedes Teilnehmers stehen. Insgesamt können
folgende sinnvolle Kombinationen (falls möglich, da optional) von ``brig``
*published* werden, die jeweils eine spezielle Semantik hätten:

- ``user``: Finden des Nutzernamens alleine.
- domain: Finden des Gruppennamen.
- ``user@domain``: Alle Geräte eines Nutzers.
- ``user@domain/resource``: Spezifisches Gerät eines Nutzers.

Das besondere an dieser Vorgehensweise ist, dass kein Nutzer sich an einer
zentralen Stelle registriert. Trotzdem können sich die Nutzer gegenseitig im
Netzwerk mit einem aussagekräftigen Namen finden und trauen nicht
einer zentralen Instanz, sondern entscheiden selbst welchen Knoten sie trauen.
Diese Eigenschaften entsprechen den drei Ecken von *Zooko's Dreieck*[@wiki:zooko],
von denen gesagt wird, dass immer nur zwei Ecken gleichzeitig erfüllbar sind
(siehe [@fig:zooko]). Allerdings ist die oben gezeigte Technik als Alternative
für Techniken wie *DNS* kaum einsetzbar und ist daher keine allgemeine Lösung für *Zooko's
Dilemma*.

![Bildliche Darstellung von Zooko's Dreieck](images/4/zooko.pdf){#fig:zooko width=50%}

Aus Sicht der Usability ist dabei die initiale Authentifizierung ein Problem.
Diese kann nicht von ``brig`` automatisiert erledigt werden, da ``brig`` nicht wissen
kann welche Prüfsumme die »richtige« ist. Es wird im aktuellen Entwurf vom Nutzer
erwartet, dass er über einen sicheren Seitenkanal (beispielsweise durch ein persönliches Treffen) die angepriesene Prüfsumme überprüft.

Die oben vorgestellte Idee kann aber auch in Richtung eines *Web of
Trust*[^WEB_OF_TRUST] erweitert werden. Als Anwendungsfall könnte man
eine geschlossene Gruppe von Nutzern betrachten, die sich nur teilweise bekannt sind.
Vergrößert sich die Gruppe mit einem neuen Teilnehmer, so muss dieser alle anderen
Teilnehmer authentifizieren und gegenseitig auch von diesen authentifiziert werden.
Ab einer bestimmten Gruppengröße wird dies ein sehr aufwendige Aufgabe.
Eine logische Lösung wäre das Anlegen eines *Blessed Repository*, dem alle Gruppenteilnehmer trauen und das von einem respektierten Teilnehmer der Gruppe
betrieben wird. Möchte man diesen zentralen Ansatz nicht, so kann man wie beim *Web
of Trust*, ein System einführen, das einem neuen Nutzer automatisch traut, wenn
eine ausreichende Anzahl anderer Gruppenteilnehmer dem Neuling vertraut hat.

[^WEB_OF_TRUST]: <https://de.wikipedia.org/wiki/Web_of_Trust>

Daneben sind noch weitere Strategien denkbar, wie das automatische Akzeptieren
neuer Teilnehmer (anwendbar, wenn beispielsweise ein Dozent Vorlesungsmaterial
verteilen will), oder ein Frage--Antwort--Verfahren wie bei
*Off--The--Record--Messaging (OTR)*. Dabei stellen sich beide Teilnehmer eine
Frage, die sie jeweils korrekt beantworten müssen. Weitere Konzepte zur
Authentifizierung werden in [@cpiechula] beschrieben.
