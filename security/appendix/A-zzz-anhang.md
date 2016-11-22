# Anhang A: Umfang IPFS--Codebasis {#sec:APP_IPFS_LOC }

Nach einem frischen `git clone` vom *IPFS*--Repository wurde der Umfang des
Projekts ermittelt indem alle Abhängigkeiten mit `x install --global=false`
beschafft wurden. Im Anschluss wurden alle erkenntlichen
Drittanbieter--Bibliotheken in ein separates *3rd*--Verzeichnis verschoben. Für
die Analyse wurde das Werkzeug `cloc`[^cloc] verwendet. Bei Analyse wurden die
autogenerieren Quelltextdateien (*Protobuf*, Endung »pb.go«) ausgeschlossen.
Die Analyse wurde auf die in der Programmiersprache *Go* geschriebenen Teile
begrenzt.

[^cloc]: Github--Seite des Projektes: <https://github.com/AlDanial/cloc>

Umfang *IPFS*--Projekt:

~~~sh

freya :: src/github.com/ipfs » cloc $(find ./go-ipfs -iname '*.go' -type f | \
                               grep -v 'pb.go')
     858 text files.
     844 unique files.
      14 files ignored.

github.com/AlDanial/cloc v 1.70  T=0.82 s (1026.5 files/s, 155950.9 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Go                             844          19983          10605          97639
-------------------------------------------------------------------------------
SUM:                           844          19983          10605          97639
-------------------------------------------------------------------------------
~~~

Umfang vom *IPFS*--Projekt genutzter Drittanbieter--Bibliotheken:

~~~sh
freya :: src/github.com/ipfs » cloc $(find ./3rd -iname '*.go' -type f | \ 
                               grep -v 'pb.go')
    1975 text files.
    1742 unique files.
     233 files ignored.

github.com/AlDanial/cloc v 1.70  T=6.02 s (289.3 files/s, 157793.5 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Go                            1742          57033          70893         822177
-------------------------------------------------------------------------------
SUM:                          1742          57033          70893         822177
-------------------------------------------------------------------------------
~~~
