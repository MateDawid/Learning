# Komenda w istniejącym kontenerze  

## NIEURUCHOMIONY KONTENER  
```commandline 
docker container start -ia <CONTAINER ID> <COMMAND>  
```  
Uruchomienie istniejącego obrazu o podanym CONTAINER ID oraz wywołanie na nim komendy.  
  
## URUCHOMIONY KONTENER  
```commandline 
docker container exec -it <CONTAINER ID> <COMMAND>  
```  
Komenda **exec** pozwala na wywołanie komend na już uruchomionym kontenerze.  
