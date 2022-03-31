# **DOCKER**
## SPIS TREŚCI
* [PODSTAWOWE INFORMACJE](#PODSTAWOWE-INFORMACJE)
	* [IMAGE](#IMAGE)
	* [CONTAINER](#CONTAINER)
* [KOMENDY](#KOMENDY)
	* [docker container run](#docker-container-run)
	* [docker container ls](#docker-container-ls)
	* [docker container stop](#docker-container-stop)
	* [docker container start](#docker-container-start)
	* [docker container rm](#docker-container-rm)
	* [docker container logs](#docker-container-logs)
## PODSTAWOWE INFORMACJE
### IMAGE
Image Dockerowy jest wzorem/templatem dla poszczególnych kontenerów. Zdefiniowany jest w Dockerfile.
### CONTAINER
Kontener jest "obiektem" utworzonym na bazie Docker Image.
## KOMENDY
### docker container run
Komenda **docker container run** pobiera i uruchamia wskazany obraz. Flaga **--publish** pozwala na podanie portu hosta do którego ma być przekierowany port kontenera . 
```commandline 
docker container run --publish <port hosta>:<port kontenera> <nazwa-obrazu>
``` 
Przykład:
```commandline 
docker container run --publish 8080:80 nginx
``` 
Flaga **--detach**  pozwala na uruchomienie obrazu bez zamrażania konsoli.
```commandline 
docker container run --publish 8080:80 --detach nginx
``` 

Flaga **--name**  pozwala na nadanie kontenerowi własnej nazwy. W innym wypadku zostanie wygenerowana losowo.
```commandline 
docker container run --publish 8080:80 --name=<nazwa-kontenera> nginx
``` 
### docker container ls
Wyświetlenie listy wszystkich uruchomionych kontenerów wraz z parametrami: 
* CONTAINER ID,   
*  IMAGE,     
* COMMAND,
* CREATED,
* STATUS,
* PORTS
*  NAMES
```commandline 
docker container ls
``` 
Flaga **-a**  pozwala na wyświetlenie wszystkich kontenerów, włącznie z nieaktywnymi.
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
Flaga **-f**  pozwala na wymuszenie zatrzymania pracy kontenera i jego usunięcie.
```commandline 
docker container rm <CONTAINER ID> -f
``` 
### docker container logs
Wyświetlenie logów kontenera ze wskazanym CONTAINER ID lub nazwą
```commandline 
docker container logs <CONTAINER ID / name>
``` 