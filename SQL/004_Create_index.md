# Tworzenie indeksów
```sql
CREATE INDEX "title_index" ON "shows" ("title");
```
Indeks to struktura danych podobna do B-tree, gdzie dzięki zorganizowaniu węzłów jak na rysunku poniżej nie ma potrzeby wyszukiwać elementów liniowo. 

![tree with root node and four child nodes, each with two or three child nodes](https://cs50.harvard.edu/x/2022/notes/7/b_tree.png)
