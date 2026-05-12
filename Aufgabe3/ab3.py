from constraint import Problem, AllDifferentConstraint

#Für die Raumaufteilung am Albert-Einstein-Gymnasium bei den mündlichen Abiturprüfungen
# soll der Hausmeister einen Plan erstellen.
# Er hat folgende Informationen: Die vier Lehrer Maier, Huber, Müller und Schmid
# prüfen die Fächer Deutsch, Englisch, Mathe und Physik in den aufsteigend
# nummerierten Räumen 1, 2, 3 und 4.
# Jeder Lehrer prüft genau ein Fach in genau einem Raum.
# Außerdem weiß er folgendes über die Lehrer und ihre Fächer:
#
# 1. Herr Maier prüft nie in Raum 4.
# 2. Herr Müller prüft immer Deutsch.
# 3. Herr Schmid und Herr Müller prüfen nicht in benachbarten Räumen.
# 4. Frau Huber prüft Mathematik.
# 5. Physik wird immer in Raum 4 geprüft.
# 6. Deutsch und Englisch werden nicht in Raum 1 geprüft.
#
# Wer prüft was in welchem Raum?

