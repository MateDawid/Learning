# Przygotowanie projektu
Żeby uruchomić aplikację reactową we własnym środowisku konieczne jest zainstalowanie [Node.js](https://nodejs.org/en).
Po jego instalacji w konsoli możliwe jest użycie polecenia, które zbuduje podstawowy schemat aplikacji.
```commandline
npx create-react-app <nazwa-aplikacji>
```
Gdy aplikcja jest już gotowa, możliwe jest jej uruchomienie na lokalnym serwerze:
```
  npm start
```
Tak przygotowany projekt pozwala na utworzenie single page app poprzez edycję pliku **nazwa-aplikacji/src/App.js**, którego zawartość jest eksportowana do **nazwa-aplikacji/src/index.js**, który to jest wykorzystwany w **nazwa-aplikacji/public/index.html**.

