# **SQL**

## OPERACJE
### Tworzenie nowej tabeli
```sql
CREATE TABLE table (column type, ...);

Example:
CREATE TABLE genres (
	show_id INTEGER, 
	genre TEXT NOT NULL, 
	FOREIGN KEY(show_id) REFERENCES shows(id)
);
```
### Dodanie wiersza tabeli
```sql
INSERT INTO genres (show_id, genre) VALUES(159, "Comedy");
```

### Zmiana istniejącej wartości
```sql
UPDATE favorites SET title = "The Office" WHERE title = "Thevoffice";
```
Przy zmianie wartości kluczowa jest klauzula WHERE - bez niej wszystkie rekordy w bazie danych zostaną nadpisane nową wartością pola.

### Tworzenie indeksów
```sql
CREATE INDEX "title_index" ON "shows" ("title");
```
Indeks to struktura danych podobna do B-tree, gdzie dzięki zorganizowaniu węzłów jak na rysunku poniżej nie ma potrzeby wyszukiwać elementów liniowo. 

![tree with root node and four child nodes, each with two or three child nodes](https://cs50.harvard.edu/x/2022/notes/7/b_tree.png)
