# **DOCKER**  
## SPIS TREŚCI  
* [PODSTAWOWE INFORMACJE](#PODSTAWOWE-INFORMACJE)  
   * [IMAGE](#IMAGE)  
   * [CONTAINER](#CONTAINER)  
* [URUCHAMIANIE, USUWANIE, ZATRZYMYWANIE KONTENERA](#URUCHAMIANIE,-USUWANIE,-ZATRZYMYWANIE-KONTENERA)  
   * [docker container run](#docker-container-run)  
   * [docker container ls](#docker-container-ls)  
   * [docker container stop](#docker-container-stop)  
   * [docker container start](#docker-container-start)  
   * [docker container rm](#docker-container-rm)  
   * [docker container logs](#docker-container-logs)  
* [MONITORING KONTENERÓW](#MONITORING-KONTENERÓW)  
   * [docker container top](#docker-container-top)  
   * [docker container inspect](#docker-container-inspect)  
   * [docker container stats](#docker-container-stats)  
* [URUCHAMIANIE KOMEND W KONTENERZE PRZEZ TERMINAL](#URUCHAMIANIE-KOMEND-W-KONTENERZE-PRZEZ-TERMINAL)  
   * [KOMENDY](#KOMENDY)  
   * [PRZYKŁAD - NOWO URUCHOMIONY KONTENER](#PRZYKŁAD---NOWO-URUCHOMIONY-KONTENER)  
   * [PRZYKŁAD - ISTNIEJĄCY, NIEURUCHOMIONY KONTENER](#PRZYKŁAD---ISTNIEJĄCY,-NIEURUCHOMIONY-KONTENER)  
   * [PRZYKŁAD - URUCHOMIONY KONTENER](#PRZYKŁAD---URUCHOMIONY-KONTENER)  
* [OBRAZY](#OBRAZY)  
   * [POBRANIE OBRAZU Z PODANYM TAGIEM](#POBRANIE-OBRAZU-Z-PODANYM-TAGIEM)  
   * [STWORZENIE WŁASNEGO OBRAZU Z INNEGO OBRAZU](#STWORZENIE-WŁASNEGO-OBRAZU-Z-INNEGO-OBRAZU)  
   * [PUSHOWANIE OBRAZU NA SERWER](#PUSHOWANIE-OBRAZU-NA-SERWER)  
   * [COMMITOWANIE ZMIAN W OBRAZIE](#COMMITOWANIE-ZMIAN-W-OBRAZIE)  
## PODSTAWOWE INFORMACJE  
### IMAGE  
Image Dockerowy jest wzorem/templatem dla poszczególnych kontenerów. Zdefiniowany jest w Dockerfile.  
### CONTAINER  
Kontener jest "obiektem" utworzonym na bazie Docker Image.  
## URUCHAMIANIE, USUWANIE, ZATRZYMYWANIE KONTENERA  
### docker container run  
Komenda **docker container run** pobiera i uruchamia wskazany obraz. Flaga **--publish** pozwala na podanie portu hosta do którego ma być przekierowany port kontenera .   
```commandline 
docker container run --publish <port hosta>:<port kontenera> <nazwa-obrazu>  
``` 
Przykład:  
```commandline 
docker container run --publish 8080:80 nginx  
``` 
Flaga **--detach** pozwala na uruchomienie obrazu bez zamrażania konsoli.  
```commandline 
docker container run --publish 8080:80 --detach nginx  
```   
Flaga **--name** pozwala na nadanie kontenerowi własnej nazwy. W innym wypadku zostanie wygenerowana losowo.  
```commandline 
docker container run --publish 8080:80 --name=<nazwa-kontenera> nginx  
```   
Flaga **--env-file** pozwala na wskazanie pliku zawierającego zmienne środowiskowe wykorzystane w obrazie budowanego kontenera.  
```commandline  
docker container run --env-file=<env-file> <image-id>  
```  
### docker container ls  
Wyświetlenie listy wszystkich uruchomionych kontenerów wraz z parametrami:   
* CONTAINER ID,     
* IMAGE,       
* COMMAND,  
* CREATED,  
* STATUS,  
* PORTS  
* NAMES  
```commandline 
docker container ls  
``` 
Flaga **-a** pozwala na wyświetlenie wszystkich kontenerów, włącznie z nieaktywnymi.  
```commandline 
docker container ls -a  
``` 
### docker container stop  
Zatrzymanie pracy kontenera ze wskazanym CONTAINER ID  
```commandline 
docker container stop <CONTAINER ID>  
``` 
### docker container start  
Uruchomienie kontenera ze wskazanym CONTAINER ID  
```commandline 
docker container start <CONTAINER ID>  
```   
### docker container rm  
Usunięcie nieuruchomionego kontenera ze wskazanym CONTAINER ID  
```commandline 
docker container rm <CONTAINER ID>  
``` 
Flaga **-f** pozwala na wymuszenie zatrzymania pracy kontenera i jego usunięcie.  
```commandline 
docker container rm <CONTAINER ID> -f  
``` 
### docker container logs  
Wyświetlenie logów kontenera ze wskazanym CONTAINER ID lub nazwą  
```commandline 
docker container logs <CONTAINER ID / name>  
```  
  
## MONITORING KONTENERÓW  
### docker container top  
Komenda do przeglądania procesów w kontenerze  
```commandline 
docker container top  
```  
  
### docker container inspect  
Komenda do pobierania pełnej konfiguracji kontenera  
```commandline 
docker container inspect  
```  
### docker container stats  
Komenda do pokazania statystyk live performance'u kontenera.  
```commandline 
docker container stats  
```  
  
## URUCHAMIANIE KOMEND W KONTENERZE PRZEZ TERMINAL  
  
### KOMENDY  
```commandline 
docker container run -i // new container  
***  
docker container start -i // existing container  
```  
Flaga **-i** umożliwia uruchomienie kontenera w trybie interaktywnym. oraz na wprowadzenie zmiennych do kontenera przez konsolę.  
```commandline 
docker container run -t  
```  
Flaga **-t** pozwala na uruchomienie terminala nowo utworzonego kontenera w konsoli.  
```commandline 
docker container start -a  
```  
Flaga **-a** pozwala na uruchomienie terminala uruchamianego kontenera w konsoli.  
  
### PRZYKŁAD - NOWO URUCHOMIONY KONTENER  
```commandline 
docker container run -it nginx bash  
```  
Pierwsze uruchomienie najnowszego (nginx:**latest**) obrazu nginx oraz wywołanie na nim komendy **bash**, która uruchamia konsolę wewnątrz kontenera.  
  
Jeżeli po nazwie kontenera nie podamy komendy, jaka ma zostać wywołana, użyta zostanie domyślnie zdefiniowana w kontenerze komenda.  
  
W celu opuszczenia konsoli kontenera należy wpisać komendę **exit**  
  
### PRZYKŁAD - ISTNIEJĄCY, NIEURUCHOMIONY KONTENER  
```commandline 
docker container start -ia <CONTAINER ID> <COMMAND>  
```  
Uruchomienie istniejącego obrazu o podanym CONTAINER ID oraz wywołanie na nim komendy.  
  
### PRZYKŁAD - URUCHOMIONY KONTENER  
```commandline 
docker container exec -it <CONTAINER ID> <COMMAND>  
```  
Komenda **exec** pozwala na wywołanie komend na już uruchomionym kontenerze.  
  
## OBRAZY  
### POBRANIE OBRAZU Z PODANYM TAGIEM  
```commandline 
docker image pull <APP>:<TAG>  
EXAMPLE:  
docker image pull ubuntu:latest  
```  
Komenda **pull ** pozwala na zaciągnięcie obrazu aplikacji z podanym tagiem np. latest, mainline, 1.1.1., itp.  
  
### STWORZENIE WŁASNEGO OBRAZU Z INNEGO OBRAZU  
```commandline 
docker image tag <APP>:<TAG> <MY_REPOSITORY>/<APP>:<TAG>  
EXAMPLE:  
docker image tag ubuntu:latest myuser/myubuntu  
```  
Zastosowanie powyższej komendy tworzy nowy obraz  na bazie wskazanego obrazu.  
   
### PUSHOWANIE OBRAZU NA SERWER  
```commandline 
docker image push <MY_REPOSITORY>/<APP>:<TAG> [<SERVER>]  
EXAMPLE:  
docker image push myuser/myubuntu:latest  
```  
Wypchnięcie obrazu do repozytorium (domyślnie do DockerHub). Jeżeli zmiany mają być wysłane na inny serwer, to należy podać tę informację w komendzie.  
  
### COMMITOWANIE ZMIAN W OBRAZIE  
```commandline 
docker container commit <CONTAINER ID> <MY_REPOSITORY>/<APP>:<NEW_TAG>  
EXAMPLE:  
docker container commit 5d9f888sfasl7 myuser/myubuntu:curl  
```  
Żeby zatwierdzić lokalne zmiany w obrazie należy wykonać commit na podobnej zasadzie jak przy używaniu GIT-a. Po zacommitowaniu zmian należy wykonać metodę push jak wyżej, aby potwierdzone zmiany trafiły na serwer z nowym tagiem.