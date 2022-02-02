# Biblesearch
Biblesearch ist eine Klasse mit der man Bibelverse von der Seite bibleserver.com nachschlagen kann.

# Benutzung
Die Klasse kann auf 2 Wege genutzt werden: Bei der Erstellung und im nachhinein. In beiden Fällen greifen Kontrollmechanismen, die bei Falscheingabe eine weitere Nutzereingabe erfordern.

## Eingabeformat
Die Eingabe kann im Format BUCH KAPITEL, VERS-VERS erfolgen. Das Buch kann auch in seiner Abkürzung angegeben werden.
```python
#Beispiele
vers = "Johannes 3, 16"
vers = "1. Mose 5, 6-8"
vers = DEUT4, 9
```

## Direkter Request bei der Erstellung
```python
# Direkter Request bei der Erstellung
bibleverse = BibleSearch("Johannes 3, 16")
```

## Nutzung nach der Erstellung
```python
# Request nach der Erstellung
bibleverse = BibleSearch()
bibleverse.Set_Verse()
```

## Ausgabe des Verses / der Verse
Die Ausgabe kann mit verschiedenen Möglichkeiten erfolgen. über die Print Funtkion wird die Bibelstelle und der Vers / die Verse ausgegeben. Ansonsten werden die Ausgaben über die Variablen location und verse ausgegeben
```python
#Ausgabe des Ortes (Wo steht es in der Bibel)
print(bibleverse.location)

#Ausgabe des Verses / der Verse
print(bibleverse.verse)
```

## Bibelversion
Die standartisierte Bibelversion ist die Lutherbibel (Abgekürzt LUT). Die Abkürzungen können auf www.bibleserver.com nachgeschlagen werden. Geändert wird die Übersetzung bei der Erstellung oder im Nachhinein über die Variable version.
```python
#Version bei Erstellung setzen
bibleverse = BibleSearch(version="ELB")

#Version im Nachhinein
bibleverse.version = "ELB"
```