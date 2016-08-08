# Implementierung {#sec:implementierung}

Dieses Kapitel... hat Pocken. TODO.

## Wahl der Sprache

Als Sprache zur Implementierung wurde die relativ junge Programmiersprache *Go* ausgewählt.
*Go* ist eine an *C* angelehnte Sprache, die von Ken Thompson, Rob Pike und Robert Griesemer
initiiert wurde und mittlerweile von Google getragen und weiterentwickelt wird.
Für dieses spezielle Projekt bietet die Sprache aus unserer Sicht folgende Vorteile:

**Garbage Collector:** Erleichtert die Entwicklung lang laufender Dienste.
**Hohe Grundperformanz:** Zwar erreicht diese nicht die Performanz von C, liegt
aber zumindest in der selben Größenordnung (vgl. [@pike2009go], S. 37).

**Weitläufige Standardbibliothek:** Es sind wenige externe Bibliotheken nötig.
Insbesondere für die Entwicklung von Netzwerk- und Systemdiensten gibt es eine
breite Auswahl von gut durchdachten Angeboten.

**Schneller Kompiliervorgang:** Selbst große Anwendungen werden in wenigen
Sekunden in eine statische Binärdatei ohne Abhängigkeiten übersetzt. Kleinere
bis mittlere Anwendungen können ähnlich wie bei einer Skriptsprache direkt
mittels des ``go run`` Befehls ausgeführt werden.

**Cross--Kompilierung:** Anwendungen können für viele verschiedene Systeme
von einem Entwicklungsrechner aus gebaut werden. Da die entstehende Binärdatei
statisch gelinkt ist, werden zudem keine weiteren Abhängigkeiten benötigt.
Dadurch ist es möglich für verschiedene Systeme bereits gebaute Binärdateien anzubieten.

**Eingebauter Scheduler:** Parallele und nebenläufige Anwendungen wie
Netzwerkserver sind sehr einfach zu entwickeln ohne für jede Aufgabe einen
dedizierten Thread starten zu müssen. Stattdessen wechseln sich viele
Koroutinen[@conway1963design] (*Go-Routinen* genannt) auf einer typischerweise
geringeren Anzahl von Threads ab. Dadurch entfällt die Implementierung eines
expliziten Mainloops und das Starten von Threads per Hand.

**Hohe Portabilität:** Die meisten Programme lassen sich ohne Anpassung auf den
gängigsten Desktop--Betriebssystemen kompilieren. Die Möglichkeit native Anwendungen
für Android und iOS zu entwickeln ist ebenfalls in der Entwicklung[^MOBILE].

**Große Anzahl mitgelieferter Werkzeuge:** Im Gegensatz zu anderen Sprachen
umfasst das *Go*--Paket nicht nur die Sprache, sondern auch ein Buildsystem,
ein Race--Condition--Checker, ein Testrunner, ein Dokumentationsgenerator, ein
Static Checker, eine Formattierungshilfe und eine Art Paketmanager.

**Einfache Installation und rapides Prototyping:** Durch das ``go
get``--Wekzeug ist es möglich direkt Bibliotheken und Anwendungen von
Plattformen wie *GitHub* zu installieren. Gleichzeitig ist es sehr simpel
möglich dort eigene Bibliotheken und Anwendungen einzustellen.
(TODO: online-build websites?)

*Einheitliche Formattierung* Durch das ``go fmt`` Werkzeug und strikte
Stilrichtlinien sieht jeder *Go*--Quelltext ähnlich und damit vertraut aus.
Dies ermöglicht externen Entwicklern den Einstieg.

**Geringe Sprachkomplexität:** Die Sprache verzichtet bewusst auf Konstrukte, die
die Implementierung des Compilers verlangsamen würden oder das Verständnis des
damit produzierten Quelltextes erschweren würde. Daher ist *Go* eine Sprache,
die zwar relativ repetitiv und gesprächig ist, aber dadurch gleichzeitig auch
sehr einfach zu lesen ist.

[^MOBILE]: Siehe dazu: <https://golang.org/wiki/Mobile>

Natürlich ist auch *Go* keine Lösung für alles. Daher werden untenstehend
einige kleinere Nachteile (sowie unsere Lösung) angeführt, die aber in Summe
nicht gegen die Vorteile aufzuwiegen sind:

**Schwergewichtige Binärdateien:** Da bei *Go* alles statisch gelinkt wird ist die
entstehende Binärdatei relativ groß. Im Falle des ``brig``--Prototypen sind das
momentan etwa 35 Megabyte. Werkzeuge wie ``upx`` können dies allerdings auf
rund 8 Megabyte reduzieren, ohne dass der Anwender die Binärdatei entpacken
muss.

**Vendor:** Der »Paketmanager« von ``go`` namens ``go get`` beherrscht nicht die
Installation einer bestimmten Paketversion. (TODO: erklären warum?) Stattdessen
wird einfach immer die momentan aktuelle Version installiert. Viele Projekte,
``brig`` eingeschlossen, brauchen und bevorzugen aber einen definierten
Versionsstand, der von den Entwicklern getestet werden konnte. Dienste wie
*gopkg.in*[^GOPKG] versuchen eine zusätzliche Versionierung anzubieten, der
aktuelle »Standard« ist die Nutzung des ``vendor`` Verzeichnisses. Diese Lösung
läuft darauf hinaus alle benötigten Abhängigkeiten in der gewünschten Version
in das eigene Quelltext--Repository zu kopieren. Dies zwar durchaus unelegante
aber gut funktionierende Lösung verfolgt auch ``brig``[^VENDOR].

[^GOPKG]: <http://labix.org/gopkg.in>
[^VENDOR]: <https://github.com/disorganizer/brig-vendor>

**Keine modernen Sprachfeatures:** 
Fehlende Generics und ein paar moderne Sprachfeatures TODO

[^UPX]: Ein Packprogramm Mehr Informationen unter <http://upx.sourceforge.net>

## Entwicklungsumgebung

Travis, git, nvim, glide

## FUSE Layer

## Algorithmik

(Flaschenhälse)

## Historisches

- XMPP
- MQTT

## Übersicht

Konzeptueller überblick über die Go-Pakete.

Portbelegung... 

## Problemstellungen

Hürden bei entwicklung

- Pull requests bei ipfs projekt
 und andere

(DefaultHash und Help fix)

## Benchmarks

## Testsuite
