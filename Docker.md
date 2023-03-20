
# **DOCKER**  
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

## DOCKERFILE
### PODSTAWA OBRAZU
Klauzula **FROM** specyfikuje obraz, z którego nowo budowany obraz będzie korzystał. 
```commandline 
FROM alpine:3.8
...
```  
```commandline 
FROM --platform=linux/amd64 python:3.8.13-bullseye
...
```  
### WYKONYWANIE KOMEND
Klauzula **RUN** pozwala na wykonywanie komend wewnątrz obrazu. Każdorazowe wykonanie klauzuli **RUN** tworzy nową warstwę w obrazie. Znak \ pozwala na oddzielenie poszczególnych komend, aby zostały wykonane w pojedynczej warstwie.
```commandline 
RUN apt-get update && apt-get -y upgrade  \  
&& apt-get -y install  apt-transport-https\  
curl\  
gettext \  
nginx \  
``` 
### KOPIOWANIE PLIKÓW
Klauzula **COPY** pozwala na przekopiowanie wskazanych na hoście plików do obrazu.
```commandline 
COPY <HOST FILE OR DIR> <IMAGE FILE OR DIR>

EXAMPLE:
COPY ./my_app/ /app/my_app/
``` 

### BUDOWANIE OBRAZU
```commandline 
docker image build
``` 
## PRZECHOWYWANIE DANYCH
### VOLUMES
Volume to przestrzeń w kontenerze, gdzie mogą być wykonywane trwałe operacje na plikach, które będą widoczne nawet po usunięciu kontenera. Aby określić ścieżkę do volume'a należy użyć klauzuli **VOLUME** w Dockerfile:
```commandline 
VOLUME [<PATH 1>, ... <PATH n>]
``` 
Przykład:
```commandline 
VOLUME ["/appdata"]
``` 
Aby sprawdzić, istniejące volume'y należy użyć komendy poniżej. Zwrócone zostaną dane o driverze i nazwie volume'a.
```commandline 
docker volume ls
``` 
Aby uruchomić nowy kontener z wykorzystaniem istniejącego volume'a należy użyć flagi **mount**:
```commandline 
docker container run ... --mount 'src=<VOLUME_NAME>, dst=<VOLUME_PATH>' ...
``` 
**VOLUME_NAME** to nazwa volume'a pobrana z komendy *docker volume ls*, natomiast **VOLUME_PATH** to ścieżka zdefiniowana przez nas w Dockerfile'u.

### BIND MOUNTS
Podłączenie konkretnego folderu z używanego hosta do obraz (np. konkretnej ścieżki do folderu na komputerze, gdzie kontener jest uruchomiony lokalnie).
```commandline 
docker container run ... <HOST_PATH>:<CONTAINER_PATH> ...
``` 
**HOST_PATH** to ścieżka, z której mają zostać załadowane pliki współdzielone z kontenerem. **CONTAINER_PATH** to ścieżka w kontenerze, do której mają zostać załadowane pliki ze ścieżki hosta. 

Synchronizacja działa w dwie strony. Jeżli plik zostanie utworzony w kontenerze, to również zostanie przeniesiony do hosta.

## DOCKER COMPOSE
Plik *docker-compose.yaml* pozwala na zdefiniowanie zależności między kontenerami, wolumenami i sieciami w uporządkowany sposób. 
### PLIK
Schemat pliku:
```dockerfile
version: '3.7'

services: # definicja kontenerów (odpowiednik docker container run)
	servicename1: # nazwa serwisu (np. elasticsearch), będzie to także DNS serwisu w sieci
		image: # nazwa obrazu którego użyć do uruchomienia kontenera (opcjonalny w przypadku użycia build)
		environment: # zmienne środowiskowe przekazywane do kontenera przy jego uruchomieniu
			KEY: value
			KEY2: value2
			# - KEY=value
			# - KEY2=value2
		env_file: # zmienne środowiskowe z pliku
			- a.env
		command: # nadpisanie domyślnego polecenia kontenera/obrazu
		volumes: # odpowiednik -v z docker run (wsparcie zarówno starszej jak i nowszej składni)
	servicename2: # kolejny serwis

volumes: # definicja wolumenu (docker volume create)

networks: # definicja sieci (docker network create)
``` 

Przykładowe zastosowanie docker-compose do uruchomienia obrazu Elasticsearch.
```dockerfile
version: '3.7'

# docker container run -p 9200:9200 -e cluster.name=kursdockera -v $(pwd)/esdata:/usr/share/elasticsearch/data docker.elastic.co/elasticsearch/elasticsearch:6.5.4

services:
	elasticsearch:
		container_name: elasticsearch
		image: docker.elastic.co/elasticsearch/elasticsearch:6.5.4
		volumes:
			- ./esdata:/usr/share/elasticsearch/data
		environment:
			- cluster.name=kursdockera
		ports:
			- 9200:9200
```
### KOMENDY
```commandline 
docker compose up
``` 
Tworzy wszystkie sieci, wolumeny, uruchamia wszystkie kontenery.
```commandline 
docker compose ps
``` 
Lista uruchomionych kontenerów w docker-compose.
```commandline 
docker compose stop
``` 
Zastopowanie wszystkich kontenerów.
```commandline 
docker compose down
``` 
Zatrzymanie i usunięcie konterów, usunięcie sieci.
