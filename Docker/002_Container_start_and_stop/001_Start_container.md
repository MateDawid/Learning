# Uruchomienie kontenera

## docker container run
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

## docker container start

Uruchomienie kontenera ze wskazanym CONTAINER ID  
```commandline 
docker container start <CONTAINER ID>  
```  