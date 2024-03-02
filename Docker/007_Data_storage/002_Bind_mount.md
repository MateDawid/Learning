# Bind mount
Podłączenie konkretnego folderu z używanego hosta do obraz (np. konkretnej ścieżki do folderu na komputerze, gdzie kontener jest uruchomiony lokalnie).
```commandline 
docker container run ... <HOST_PATH>:<CONTAINER_PATH> ...
``` 
**HOST_PATH** to ścieżka, z której mają zostać załadowane pliki współdzielone z kontenerem. **CONTAINER_PATH** to ścieżka w kontenerze, do której mają zostać załadowane pliki ze ścieżki hosta. 

Synchronizacja działa w dwie strony. Jeżli plik zostanie utworzony w kontenerze, to również zostanie przeniesiony do hosta.
