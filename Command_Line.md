# **COMMAND LINE**
## SPIS TREŚCI
* [UNIX COMMANDS](#UNIX-COMMANDS)
	* [pwd](#pwd)
	* [ls](#ls)
	* [mkdir](#mkdir)
	* [cd](#cd)
	* [touch](#touch)
	* [cp](#cp)
	* [mv](#mv)
	* [rm](#rm)
	* [cat](#cat)
## UNIX COMMANDS
### pwd
Komenda zwracająca katalog, w którym obecnie się znajdujemy (rozwinięcie skrótu - Print Working Directory).
### ls
Komenda zwracająca wylistowaną zawartość bieżącego katalogu
```commandline 
ls       // simple list
ls -a    // list including hidden files
ls -l    // list with details (file sizes, modification dates, etc.)
ls -al   // list with hidden files and details (file sizes, modification dates, etc.)
``` 
### mkdir
Komenda tworząca katalog w bieżącym katalogu.
```commandline 
mkdir dirname                                // creates dir 'dirname' 
mkdir -p directory1/directory2/directory3    // creates nested directory with all parent directories (if they don't exists)
``` 
### cd
Komenda przenosząca do innego katalogu.
```commandline 
cd ..       // goes to the parent directory
cd dirname  // goes to 'dirname' directory (if exists) 
``` 
### touch
Komenda tworząca nowy plik
```commandline 
touch newfile1.txt      // creates new file
``` 
### cp
Komenda kopiująca wskazany plik do wskazanego folderu
```commandline 
cp newfile1.txt testdir     // copies newfile1.txt to testdir
``` 
### mv
Komenda przenosząca wskazany plik do wskazanego folderu. Może również służyć do zmiany nazwy wskazanych plików.
```commandline 
mv newfile1.txt testdir     // moves newfile1.txt to testdir
mv newfile1.txt cheese.txt  // changes newfile1.txt name to cheese.txt
``` 
### rm
Komenda usuwająca wskazany plik/folder
```commandline 
rm test.txt      // deletes test.txt file
rm -rf testdir   // removes testdir and all it contents. Flag -rf is needed to delete directory
``` 
### cat
Komenda służąca do konkatenacji (łączenia) plików, ale może być również wykorzystana do wyświetlenia plików czy stworzenia nowego pliku.
```commandline 
$ cat plik1.txt plik2.txt
```

Powyższy przykład wyświetli na ekranie połączone dwa pliki.  
Możemy wynik tego działania zapisać do nowego pliku:

```commandline 
$ cat plik1.txt plik2.txt > plik3.txt
```
