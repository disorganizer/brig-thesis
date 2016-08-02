# Erweiterungen

- *Semantisch durchsuchbares* Tag-basiertes Dateisystem[^TAG].

[^TAG]: Mit einem ähnlichen Ansatz wie \url{https://en.wikipedia.org/wiki/Tagsistant}

## Was ``brig`` *nicht* ist

Auch wenn ``brig`` sehr flexibel einsetzbar ist, ist und soll es keineswegs die
beste Alternative in allen Bereichen sein. Keine Software kann eine »eierlegende
Wollmilchsau« sein und sollte auch nicht als solche benutzt werden.

Besonders im Bereich Effizienz kann es nicht mit hochperformanten
Cluster--Dateisystemen wie Ceph[^CEPH] oder GlusterFS[^GLUSTER] mithalten.  Das
liegt besonders an der sicheren Ausrichtung von ``brig``, welche oft
Rechenleistung zugunsten von Sicherheit eintauscht. Auch kann ``brig`` keine
Echtzeit--Garantien geben. 

Auch wenn ein ``brig``--Repository in der geschlossenen Form als sicherer
»Datensafe« einsetzbar ist, so bietet ``brig`` nicht die Eigenschaft der
»glaubhaften Abstreitbarkeit«[^ABSTREIT], die Werkzeuge wie Veracrypt (TODO: ref) bieten.

Im Gegensatz zu Versionsverwaltungssystemen wie ``git``, kann ``brig`` keine
Differenzen zwischen zwei Ständen anzeigen, da es nur auf den Metadaten von
Dateien arbeitet. Auch muss auf der Gegenseite ein ``brig``--Daemon--Prozess
laufen, um mit der Gegenseite zu kommunizieren.

[^CEPH]: Webpräsenz: \url{http://ceph.com}
[^GLUSTER]: Webpräsenz: \url{https://www.gluster.org}
[^ABSTREIT]: Siehe auch: \url{https://de.wikipedia.org/wiki/VeraCrypt\#Glaubhafte_Abstreitbarkeit}

## Fehlende Anforderungen

## Zukünftige Erweiterungen

Update Mechanismus?
