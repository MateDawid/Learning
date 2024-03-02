# Podstawowe komendy
## git config

```bash  
git config --global user.name "<username>"
git config --global user.email "<email>"
```  
## git init  
```bash  
git init
```  
## git remote  
```bash  
git remote add origin "<remote_repository_url>"
```  
## git clone  
Klonowanie repozytorium z podanego linka  
```bash  
git clone "<remote_repository_url>"
```  
## git status  
Stan aktualnego brancha w porównaniu do ostatniego commita  
```bash  
git status
```  
## git log  
Historia commitów na aktualnym branchu (od najnowszego do najstarszego)  
```bash  
git log
```  
## git branch  
Lista branchy w lokalnym repozytorium oraz wyświetlenia nazwy aktualnego brancha  
```bash  
git branch
``` 
## git checkout  
```bash  
git checkout <nazwa_brancha>        // przełączenie się na inną, istniejącą gałąź
git checkout  -b "<nazwa_brancha>"  // stworzenie nowego brancha na bazie aktualnego brancha i przełączenie się na niego
git checkout -                      // przełączenie się na wcześniej używanego brancha
git checkout <nazwa_pliku>          // zresetowanie zawartości brancha do tej, z ostatniego commita
```  

## git reset  
```bash  
git reset --hard // cofnięcie gałęzi do stanu z ostatniego commita
```  