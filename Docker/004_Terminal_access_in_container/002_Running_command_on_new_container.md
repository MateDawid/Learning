# Komenda w nowo uruchomionym kontenerze  
```commandline 
docker container run -it nginx bash  
```  
Pierwsze uruchomienie najnowszego (nginx:**latest**) obrazu nginx oraz wywołanie na nim komendy **bash**, która uruchamia konsolę wewnątrz kontenera.  
  
Jeżeli po nazwie kontenera nie podamy komendy, jaka ma zostać wywołana, użyta zostanie domyślnie zdefiniowana w kontenerze komenda.  
  
W celu opuszczenia konsoli kontenera należy wpisać komendę **exit**  