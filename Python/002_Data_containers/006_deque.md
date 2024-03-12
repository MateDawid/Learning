# deque
Nazwa to skrót od "double ended queue". Wykorzystuje wewnętrznie listę dwukierunkową. Deque może służyć np. do składowania historii operacji. 
Dla określonej liczby elementów deque zachowuje ich kolejność przy użyciu wskaźnika początkowego i końcowego. Przy dodaniu nowego elementu wskaźnik końcowy wskazuje na nowy element, za to wskaźnik początkowy przenosi się na następujący po dotychczasowym elemencie początkowym.
```python
from collections import deque

history = deque(maxlen=3)
# maxlen określa maksymalną długość kolejki

text = "Houston we have a problem"
for word in text.split():
	history.append(word)

# W czasie iteracji zmienna history będzie zawierać zawsze 3 elementy, gdzie dodanie nowego elementu będzie usuwać pierwszy element z listy, jeżeli będzie ona miała długość równą maxlen

history.popleft()
# Usuwa element z lewej (początkowej) strony kolejki
history.appendleft('not')
# Dodaje element na początku kolejki
```