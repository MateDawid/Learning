# Klauzula RUN
Klauzula **RUN** pozwala na wykonywanie komend wewnątrz obrazu. Każdorazowe wykonanie klauzuli **RUN** tworzy nową warstwę w obrazie. Znak \ pozwala na oddzielenie poszczególnych komend, aby zostały wykonane w pojedynczej warstwie.
```commandline 
RUN apt-get update && apt-get -y upgrade  \  
&& apt-get -y install  apt-transport-https\  
curl\  
gettext \  
nginx \  
``` 