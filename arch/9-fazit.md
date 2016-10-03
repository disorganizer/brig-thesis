# Fazit {#sec:fazit}

## Zusammenfassung

Es wurde ein neuer, interdisziplinärer Ansatz für ein
Dateisynchronisationssystem vorgestellt, der viele bestehende Ideen in einem
stimmigen Konzept vereint. Eine funktionierende, quelloffene und für alle
zugängliche Implementierung wurde vorgestellt und dokumentiert. Die anfangs
gestellten Anforderungen konnte im Großen und Ganzen umgesetzt werden, auch
wenn die Implementierung den Konzepten etwas nachsteht. Aus Sicht der Entwicklern
ist dies aufgrund der hohen Ambitionen und des geringen Zeitrahmens zumindest
verständlich. Letztlich ist eine solide Basis für weitere Entwicklungen
entstanden, die in absehbarer Zeit einem größeren Publikum präsentiert werden
kann.
Eine Abgrenzung zu anderen, existierenden Werkzeugen ergibt sich vor allem
dadurch, dass die technischen Internas von ``brig`` vergleichsweise leicht
verständlich sind und auch von fortgeschrittenen Nutzern verstanden werden
können.

## Selbstkritik

Wie in [@sec:evaluation] diskutiert, ist noch Verbesserungspotenzial
vorhanden. In Retrospektive hätte man sich stärker auf die Kernfunktionalität
der Software und die zugrunde liegenden Konzepte konzentrieren müssen.
Zusatzmodule wie Verschlüsselung sind wichtig, hätten aber auch zu späteren
Zeitpunkten nachgerüstet werden können.

Weiterhin wäre im Nachhinein eine prototypischere Entwicklung angebracht
gewesen: Es wurde viel Zeit darauf verwandt, Konzepte in Quelltext zu gießen,
die letztlich keine Anwendung fanden oder nicht aufgingen. Das lässt sich
natürlich bei großen Projekten kaum vermeiden, aber das Testen neuer Konzepte
hätte auch mittels »unsauberer« Lösungen funktioniert. Hätte man die Software
beispielsweise, nach Unix--Philosophie (wie ``git``), als Sammlung kleiner
Werkzeuge konzipiert, hätte man diese kurzzeitig mit einer Skriptsprache wie
``bash`` zusammenschließen können, um Probleme in den eigenen Ideen
aufzudecken.

Obwohl der zeitliche Rahmen aufgrund der Suche nach Investoren, dem
zeitgleichen Abschließen des Studiums und privaten Problem sehr eng war, ist
mit ``brig`` eine erstaunlich flexible Idee entstanden, von der wir glauben,
dass sie wirklich nützlich ist und die Welt etwas verbessern könnte.

![Ist »brig« letztlich nur ein weiterer Standard?[^XKCD_STD_SOURCE]](images/8/xkcd-standards.png){#fig:xkcd-standards width=55%}

[^XKCD_STD_SOURCE]: <https://xkcd.com/927>

## Offene Fragen

Besonders fraglich ist wie gut das System in der Praxis funktioniert und auf
größere Nutzermengen skaliert. Da ``brig`` von technisch versierten Nutzern
entwickelt wurde, ist es auch fraglich ist wie gut verständlich es für neue,
unerfahrenere Benutzer ist. Aus Sicht der Usability gibt es
noch einige technische und konzeptuelle Probleme:

* Keine grafische Oberfläche, nur Kommandozeile.
- Initiale Authentifizierung von Hand nötig.
- Partner muss online sein, um mit ihm synchronisieren zu können.
* Noch keine automatische »Echtzeit«--Synchronisation.


Eine Veröffentlichung lohnt sich erst, wenn obige Punkte ansatzweise gelöst worden sind.

### Beziehung zum ``ipfs``--Projekt

Momentan wird ``brig`` vollkommen separat von ``ipfs`` entwickelt. Das hat vor allem
den Grund, dass zu Anfang des Projektes die Richtung der Entwicklung noch nicht klar war. Die komplette Separation als eigenes Projekt, macht es deutlich einfacher
mit verschiedenen Konzepten zu experimentieren.
In Zukunft spricht jedoch nichts dagegen Teile von ``brig``, sofern sie allgemein nützlich sind, auch dem ``ipfs``--Projekt anzubieten und dort zu integrieren.
Eine Zusammenarbeit wäre für beide Seiten vorteilhaft, da mehr Entwickler sich mit dem
Quelltext befassen können und die dazugehörigen Konzepte aufeinander abstimmen können.
Von ``ipfs``--Seite scheint eine Zusammenarbeit gern gesehen zu sein:

> *Yeah we want to get to this too and would love to support your efforts. I'd
> request that you consider contributing directly to go-ipfs since much of what
> you want we want too.*

--- *Juan Benet*, Kernentwickler von ``ipfs``[^JUAN_BENET_CIT]

[^JUAN_BENET_CIT]: Quelle: <https://github.com/ipfs/ipfs/issues/120>

Konkret wären folgende Module von ``brig`` für ``ipfs`` interessant:

- Das Verschlüsselungsformat.
- Das Kompressionsformat.
* Teile des Datenmodells, insbesondere die ``Commit``--Struktur und Versionsverwaltung.
* Die Implementierung eines beschreibbaren FUSE--Dateisystems[^IPFS_FUSE].

[^IPFS_FUSE]: ``ipfs`` implementiert momentan nur ein rein lesbares FUSE--Dateisystem.

### Zukunft der Autoren

Fraglich ist auch wie die Zukunft von ``brig`` aussieht, nachdem die
vorliegende Arbeit abgeschlossen wurde. Leider konnte für die weitere Förderung
des Projektes kein Sponsor verpflichtet werden. Trotz Motivation der Autoren
wird ``brig`` daher in der näheren Zukunft als Hobbyprojekt weitergeführt.
Durch die private Situation beider Autoren wird daher die
Entwicklung sich leider verlangsamen.

### Veröffentlichung der Software

Nichtsdestotrotz ist es unser Ziel bis spätestens Mitte des Jahres 2017 ``brig``
auf einen Stand zu bringen den man der Open--Source--Community präsentieren kann.
Bevor es so weit ist, ist nicht nur Feinschliff an der bestehenden Software
nötig, sondern es muss auch leicht zugängliche Dokumentation geschrieben werden und
die Software für verschiedene Betriebssysteme gepackt werden.

Folgende Plattformen erscheinen uns für eine Präsentation der Software geeignet:

- Ein »Linux Tag« (Beispielsweise der »Linux Info Tag« in Augsburg[^LUGA]).
  Dort wäre eine detaillierte Präsentation vor Publikum mit direkten Feedback möglich.
* Kleineres Forum mit technisch versierten Nutzern; beispielsweise ein Forum
  für fortgeschrittene Linux--User. Dort könnte auch eine Paketierung der Software
  angesprochen werden.
* Größere Newsportale wie *reddit*. Diese werden von einem sehr breiten Publikum
  besucht.

[^LUGA]: Siehe auch: <http://www.luga.de/Aktionen/LIT-2016>

Alle drei Möglichkeiten könnten auch zusammen in dieser Reihenfolge genutzt
werden. Bei der Veröffentlichung sollte explizit angemerkt werden, dass sich
Internas noch ändern können falls dazu Anlass bestehen sollte.

Auch wenn die Arbeit an ``brig`` persönlich sehr kräftezehrend war, haben wir
eine Menge dabei gelernt. Es stecken eine Menge guter Ideen in der Software und
aus unserer Sicht ist alleine die Zeit der limitierende Faktor, um ``brig`` zu
einem Produkt zu machen, dass mehr als ein »Standard« (im Sinne von
[@fig:xkcd-standards]) unter Vielen ist.
