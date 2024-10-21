# Websockets

> Sources: 
> 1. https://testdriven.io/courses/django-celery/websockets/#H-2-websocket
> 2. https://testdriven.io/courses/taxi-react/websockets-part-two/#H-5-review


## WebSocket
WebSocket is a computer communications protocol, providing full-duplex communication channels over a single TCP connection.

When a web client establishes a WebSocket connection with a server, the connection stays alive and the client and server can send messages to each other.

## ASGI vs WSGI

> ASGI is a spiritual successor to WSGI, the long-standing Python standard for compatibility between web servers, frameworks, and applications.

In short, ASGI was created to add support for WebSockets, HTTP/2, and async/await, none of which are supported by WSGI. Like WSGI, it's an interface between Django and a web server (like Nginx).

![asgi](_images/001_asgi.png)

As you can see, ASGI handles:

1. Standard HTTP requests from the web server to a Django view and returns HTTP responses back to the web server.
2. WebSocket connections between the web server and WebSocket Consumers for sending and receiving messages.

The WebSocket protocol works differently than HTTP. Whereas HTTP requests only last as long as the request/response cycle, WebSockets live until one of the two parties involved breaks the connection. Both the client and the server can send each other messages independently over the open connection.

With Django Channels, when the client sends a message to the server, the server sends a message back. The server can also send messages to other connected clients through mechanisms known as channel layers and groups. If a message is broadcast to a group, the server sends the message to every channel in that group.

