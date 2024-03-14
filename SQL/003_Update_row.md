### Zmiana istniejącej wartości
```sql
UPDATE favorites SET title = "The Office" WHERE title = "Thevoffice";
```
Przy zmianie wartości kluczowa jest klauzula WHERE - bez niej wszystkie rekordy w bazie danych zostaną nadpisane nową wartością pola.
