# Wypchanie zmian na serwer
## git add  
Dodanie plików do z working directory do staging area,  
```bash  
git add <nazwa_pliku> [<kolejne_nazwy_plików>]
git add --all
```  
## git commit  
Dodanie plików do z working directory do staging area,  
```bash  
git commit -m "<nazwa_commita>"   // tworzy commit z nadaną nazwą
git commit -am "<nazwa_commita>"  // dodaje wszystkie ZMIENIONE pliki na staging i tworzy commit z nadaną nazwą. NOWE pliki należy dodać do commita ręcznie przy użyciu git add
```  
## git push  
Wypychanie zmian na aktualnym branchu z lokalnego repozytorium do repozytorium centralnego   
```bash  
git push
```  