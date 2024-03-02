# Komendy
## POBRANIE OBRAZU Z PODANYM TAGIEM  
```commandline 
docker image pull <APP>:<TAG>  
EXAMPLE:  
docker image pull ubuntu:latest  
```  
Komenda **pull ** pozwala na zaciągnięcie obrazu aplikacji z podanym tagiem np. latest, mainline, 1.1.1., itp.  
  
## STWORZENIE WŁASNEGO OBRAZU Z INNEGO OBRAZU  
```commandline 
docker image tag <APP>:<TAG> <MY_REPOSITORY>/<APP>:<TAG>  
EXAMPLE:  
docker image tag ubuntu:latest myuser/myubuntu  
```  
Zastosowanie powyższej komendy tworzy nowy obraz  na bazie wskazanego obrazu.  
   
## PUSHOWANIE OBRAZU NA SERWER  
```commandline 
docker image push <MY_REPOSITORY>/<APP>:<TAG> [<SERVER>]  
EXAMPLE:  
docker image push myuser/myubuntu:latest  
```  
Wypchnięcie obrazu do repozytorium (domyślnie do DockerHub). Jeżeli zmiany mają być wysłane na inny serwer, to należy podać tę informację w komendzie.  
  
## COMMITOWANIE ZMIAN W OBRAZIE  
```commandline 
docker container commit <CONTAINER ID> <MY_REPOSITORY>/<APP>:<NEW_TAG>  
EXAMPLE:  
docker container commit 5d9f888sfasl7 myuser/myubuntu:curl  
```  
Żeby zatwierdzić lokalne zmiany w obrazie należy wykonać commit na podobnej zasadzie jak przy używaniu GIT-a. Po zacommitowaniu zmian należy wykonać metodę push jak wyżej, aby potwierdzone zmiany trafiły na serwer z nowym tagiem.
