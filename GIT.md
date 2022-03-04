# **GIT**
## SPIS TREŚCI
* [DEFINICJE](#DEFINICJE)
* [KOMENDY](#KOMENDY)
	* [git config](#git-config)
	* [git init](#git-init)
	* [git remote](#git-remote)
	* [git clone](#git-clone)
	* [git status](#git-status)
	* [git log](#git-log)
	* [git branch](#git-branch)
	* [git add](#git-add)
	* [git commit](#git-commit)
	* [git push](#git-push)
	* [git pull](#git-pull)
	* [git fetch](#git-fetch)
	* [git checkout](#git-checkout)
	* [git reset](#git-reset)
	* [git merge](#git-merge)
	* [git rebase](#git-rebase)
* [INTERAKTYWNY REBASE](#INTERAKTYWNY-REBASE)
	* [Uruchomienie interaktywnego rebase](#Uruchomienie-interaktywnego-rebase)
	* [Zmiana nazwy commita](#Zmiana-nazwy-commita)
	* [Łączenie commitów](#Łączenie-commitów)
* [DOBRE PRAKTYKI](#DOBRE-PRAKTYKI)
	* [rebase czy merge?](#rebase-czy-merge?)
  
##  DEFINICJE  
`GIT` - rozproszony system kontroli wersji  
`remote (origin)` - centralne repozytorium  
`local` - lokalne repozytorium  
`working directory` - kod, nad którym wciąż pracujemy znajduje się w tym obszarze. Aby przenieść go do staging area, należy użyć komendy **git add**  
`staging area` - przestrzeń, w której znajdują się pliki, które planujemy dodać do commita. Jest to krok pośredni między pracą nad plikiem, a wysłaniem do go centralnego repozytorium  
  
##   KOMENDY  
### git config  
```bash  
git config --global user.name "<username>"git config --global user.email "<email>"
```  
### git init  
```bash  
git init
```  
  ### git remote  
```bash  
git remote add origin "<remote_repository_url>"
```  
### git clone  
Klonowanie repozytorium z podanego linka  
```bash  
git clone "<remote_repository_url>"
```  
### git status  
Stan aktualnego brancha w porównaniu do ostatniego commita  
```bash  
git status
```  
### git log  
Historia commitów na aktualnym branchu (od najnowszego do najstarszego)  
```bash  
git log
```  
### git branch  
Lista branchy w lokalnym repozytorium oraz wyświetlenia nazwy aktualnego brancha  
```bash  
git branch
```  
### git add  
Dodanie plików do z working directory do staging area,  
```bash  
git add <nazwa_pliku> [<kolejne_nazwy_plików>]git add --all
```  
### git commit  
Dodanie plików do z working directory do staging area,  
```bash  
git commit -m "<nazwa_commita>"   // tworzy commit z nadaną nazwągit commit -am "<nazwa_commita>"  // dodaje wszystkie ZMIENIONE pliki na staging i tworzy commit z nadaną nazwą. NOWE pliki należy dodać do commita ręcznie przy użyciu git add
```  
### git push  
Wypychanie zmian na aktualnym branchu z lokalnego repozytorium do repozytorium centralnego   
```bash  
git push
```  
### git pull  
Aktualizowanie lokalnego repozytorium o nowe commity z repozytorium centralnego z aktualnego brancha   
```bash  
git pull
git pull --rebase
```  
### git fetch  
Aktualizowanie lokalnego repozytorium o nowe branche powstałe w repozytorium zewnętrznym  
```bash  
git fetch
```  
### git checkout  
```bash  
git checkout <nazwa_brancha>        // przełączenie się na inną, istniejącą gałąźgit checkout  -b "<nazwa_brancha>"  // stworzenie nowego brancha na bazie aktualnego brancha i przełączenie się na niegogit checkout -                      // przełączenie się na wcześniej używanego brancha
git checkout <nazwa_pliku>          // zresetowanie zawartości brancha do tej, z ostatniego commita
```  
  
### git reset  
```bash  
git reset --hard // cofnięcie gałęzi do stanu z ostatniego commita
```  
### git merge  
Ta komenda łączy wszystkie zmiany powstałe we wskazanej w komendzie gałęzi w jeden wspólny commit (merge commit) i dołącza je do brancha, na którym obecnie się znajdujemy, jako najnowszy commit.  
```bash  
git merge <nazwa-brancha>
```  
  
### git rebase  
Komenda zaciąga historię commitów oraz zmiany ze wskazanego brancha, a zmiany, które commity, które zostały w międzyczasie utworzone na obecnej gałęzi przesunięte są w historii commitów jako najnowsze  
```bash  
git rebase <nazwa-brancha>
```  
## INTERAKTYWNY REBASE
### Uruchomienie interaktywnego rebase
Interaktywny rebase pozwala na edytowanie historii commitów, łączenie wielu commitów w jeden commit, usuwanie niechcianych commitów.
```bash  
git rebase -i <hash commita poprzedzającego commit od którego chcemy edytować historię>
```  
Po wykonaniu powyższej komendy znajdziemy się w interaktywnej powłoce, gdzie jest do wyboru kilka opcji. Aby przejść do trybu edycji należy nacisnąć **A**.

Na liście commitów na górze powłoki domyślnie ustawione są komendy **pick**, które pozostawiają commit w niezmienionej formie. Przykład:
```bash  
pick cd7ab52 Commit 1
pick xd7ab12 Commit 2
pick cz2ac42 Commit 3
``` 
### Zmiana nazwy commita
Jeżeli chcemy zmienić nazwę któregoś z commitów komendę **pick** należy zamienić na komendę **reword** lub **r** i zatwierdzić zmiany poprzez kliknięcie **ESC** oraz wpisanie **:wq**
```bash  
pick cd7ab52 Commit 1
r xd7ab12 Commit 2
pick cz2ac42 Commit 3
``` 
W nowym oknie wchodzimy do trybu edycji, podajemy nową nazwę commita i zatwierdzamy zmiany poprzez kliknięcie **ESC** oraz wpisanie **:wq**
### Łączenie commitów
Jeżeli chcemy połączyć wskazany commit z commitem znajdującym się powyżej, komendę **pick** należy zamienić na komendę **fixup** lub **f** i zatwierdzić zmiany poprzez kliknięcie **ESC** oraz wpisanie **:wq**
```bash  
pick cd7ab52 Commit 1
f xd7ab12 Commit 2
pick cz2ac42 Commit 3
``` 
##   DOBRE PRAKTYKI  
### rebase czy merge?  
Aby zachować liniową historię commitów najlepiej zastosować podany zestaw komend przed zmergowaniem zmian na branch master. Mergując zmiany bez wcześniejszego wykonania rebase'a  tworzymy tzw. merge commita, który burzy liniową strukturę historii commitów i tworzy w niej rozgałęzienia, które trudniej potem rozwiązać.  
```bash  
git checkout feature-branch // przeniesienie na aktualnego brancha
git rebase master           // zaciągnięcie historii zmian z mastera do aktualnego brancha
git checkout master         // przeniesienie na aktualnego brancha
git merge feature-branch    // dodanie zmian z feature-brancha na branch master
```
