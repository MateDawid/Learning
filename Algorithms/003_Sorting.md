# Sortowanie
## 1. Sortowanie bąbelkowe
Algorytm sortowania, który przegląda listę liczb, porównuje każdą liczbę z następną i zamienia je miejscami, jeśli są zapisane w nieodpowiedniej kolejności.
## 2. Sortowanie przez wstawianie
Stabilny algorytm sortowania, w którym dane są porządkowane w sposób przypominający sortowanie talii kart. W trakcie całego procesu zbiór dzieli się na dwie cześci - posortowaną i nieposortowaną. Na samym początku w części posortowanej znajduje się pierwszy element zbioru. Porównujemy pierwszy element listy nieposortowanej z ostatnim elementem listy posortowanej i zamieniamy je miejscami aż do momentu, gdy będą w odpowiedniej kolejności. Powtarzamy ten krok aż do ostatniego elementu listy nieposortowanej.
## 3. Sortowanie przez scalanie
Stabilny algorytm rekurencyjny (typu "dziel i rządź"), który dzieli listę na połowy tak długo, aż uzyska listy o długości jednego elementu, które następnie łączy w odpowiedniej kolejności.
### Algorytmy typu "Dziel i rządź"
Algorytmy, które rekurencyjnie dzielą problem na dwa lub więcej podproblemów, aż do momentu, gdy będą one na tyle proste, że będzie je można łatwo rozwiązać.
## 4. Timsort
Algorytm wykorzystywany we wbudowanych funkcja Pythona sort i sorted. Stanowi on hybrydowe połączenie sortowania przez scalanie oraz sortowania przez wstawianie.