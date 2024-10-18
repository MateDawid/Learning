# Websocket setup

> Source: https://testdriven.io/courses/taxi-react/websockets-part-one/

## Connecting to the Server

Clients and servers using the HTTP Protocol establish a single connection per request. The client initiates communication and the server responds. It never works the other way around. After the request/response cycle finishes, the connection closes.

On the other hand, clients and servers using the WebSocket protocol establish just one connection total. Both the client and the server can send messages to each other over the same open connection until it disconnects.

```python
# server/trips/tests/test_websocket.py

import pytest
from channels.testing import WebsocketCommunicator

from taxi.asgi import application

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


@pytest.mark.asyncio
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path='/taxi/'
        )
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()
```

One of the first things you'll probably notice is that we're using pytest instead of the built-in Django testing tools. We're also using coroutines that were introduced with the asyncio module in Python 3.4. Django Channels mandates the use of both pytest and asyncio.

Pay attention to the fact that we're including a TEST_CHANNEL_LAYERS constant at the top of the file after the imports. We're using that constant in the first line of our test along with the settings fixture provided by pytest-django. This line of code effectively overwrites the application's settings to use the InMemoryChannelLayer instead of the configured RedisChannelLayer. Doing this allows us to focus our tests on the behavior we are programming rather than the implementation with Redis. Rest assured that when we run our server in a non-testing environment, Redis will be used.

```python
# server/taxi/asgi.py

import os

from django.core.asgi import get_asgi_application
from django.urls import path # new

from channels.routing import ProtocolTypeRouter, URLRouter # changed

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taxi.settings')

from trips.consumers import TaxiConsumer

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    # new
    'websocket': URLRouter([
        path('taxi/', TaxiConsumer.as_asgi()),
    ]),
})
```
```python
# server/trips/consumers.py

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TaxiConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        await super().disconnect(code)
```

A Channels consumer is like a Django view with extra steps to support the WebSocket protocol. Whereas a Django view can only process an incoming request, a Channels consumer can send and receive messages and react to the WebSocket connection being opened and closed.

For now, we're explicitly accepting all connections.

