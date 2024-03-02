# Plik docker_compose
Plik *docker-compose.yaml* pozwala na zdefiniowanie zależności między kontenerami, wolumenami i sieciami w uporządkowany sposób. 

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