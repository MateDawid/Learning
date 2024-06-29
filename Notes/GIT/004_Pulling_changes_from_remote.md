# Pobieranie zmian z serwera
## git pull  
Aktualizowanie lokalnego repozytorium o nowe commity z repozytorium centralnego z aktualnego brancha   
```bash  
git pull
git pull --rebase
```  
## git fetch  
Aktualizowanie lokalnego repozytorium o nowe branche powstałe w repozytorium zewnętrznym  
```bash  
git fetch
```  
## git merge  
Ta komenda łączy wszystkie zmiany powstałe we wskazanej w komendzie gałęzi w jeden wspólny commit (merge commit) i dołącza je do brancha, na którym obecnie się znajdujemy, jako najnowszy commit.  
```bash  
git merge <nazwa-brancha>
```  
  
## git rebase  
Komenda zaciąga historię commitów oraz zmiany ze wskazanego brancha, a zmiany, które commity, które zostały w międzyczasie utworzone na obecnej gałęzi przesunięte są w historii commitów jako najnowsze  
```bash  
git rebase <nazwa-brancha>
```

## rebase czy merge?  
Aby zachować liniową historię commitów najlepiej zastosować podany zestaw komend przed zmergowaniem zmian na branch master. Mergując zmiany bez wcześniejszego wykonania rebase'a  tworzymy tzw. merge commita, który burzy liniową strukturę historii commitów i tworzy w niej rozgałęzienia, które trudniej potem rozwiązać.  
```bash  
git checkout feature-branch // przeniesienie na aktualnego brancha
git rebase master           // zaciągnięcie historii zmian z mastera do aktualnego brancha
git checkout master         // przeniesienie na aktualnego brancha
git merge feature-branch    // dodanie zmian z feature-brancha na branch master
```
