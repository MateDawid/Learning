# Tworzenie nowej tabeli
```sql
CREATE TABLE table (column type, ...);

Example:
CREATE TABLE genres (
	show_id INTEGER, 
	genre TEXT NOT NULL, 
	FOREIGN KEY(show_id) REFERENCES shows(id)
);
```