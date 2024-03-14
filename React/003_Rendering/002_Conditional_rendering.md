# Renderowanie warunkowe
Elementy mogą być wyświetlane lub nie w zależności od sprawdzanych warunków. Poza tradycyjną konstrukcją if / else możliwe jest użycie typowych dla JavaScriptu skrótów:
* `{cond ? <A /> : <B />}`  => jeżeli `cond`, wyświetl `<A />`, w innym wypadku wyświetl `<B />`
* `{cond && <A />}`  => jeżeli `cond`, wyświetl `<A />`, w innym wypadku nie wyświetlaj niczego