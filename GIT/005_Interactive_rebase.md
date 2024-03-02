# Interaktywny rebase
## Uruchomienie interaktywnego rebase
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
## Zmiana nazwy commita
Jeżeli chcemy zmienić nazwę któregoś z commitów komendę **pick** należy zamienić na komendę **reword** lub **r** i zatwierdzić zmiany poprzez kliknięcie **ESC** oraz wpisanie **:wq**
```bash  
pick cd7ab52 Commit 1
r xd7ab12 Commit 2
pick cz2ac42 Commit 3
``` 
W nowym oknie wchodzimy do trybu edycji, podajemy nową nazwę commita i zatwierdzamy zmiany poprzez kliknięcie **ESC** oraz wpisanie **:wq**
## Łączenie commitów
Jeżeli chcemy połączyć wskazany commit z commitem znajdującym się powyżej, komendę **pick** należy zamienić na komendę **fixup** lub **f** i zatwierdzić zmiany poprzez kliknięcie **ESC** oraz wpisanie **:wq**
```bash  
pick cd7ab52 Commit 1
f xd7ab12 Commit 2
pick cz2ac42 Commit 3
``` 