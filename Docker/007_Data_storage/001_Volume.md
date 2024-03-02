# Volume
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
