# Authenticating Socket Connections

> Source: https://testdriven.io/courses/taxi-react/websockets-part-one/#H-3-authenticating-socket-connections

Establishing a WebSocket connection starts with a "handshake" between the client and the server over HTTP. Anything that can be sent with an HTTP request can be sent with the handshake -- i.e., headers and cookies, query string parameters, and request bodies. Unfortunately, the JavaScript WebSocket API does not support custom headers. That means we need to find a different way to authenticate our WebSocket connection than an authorization header.

We have several different ways to get around the custom headers limitation, but the community at large seems to agree that sending the access token in a query string parameter is the way to go. Keep in mind that in a production environment, you need to be careful to protect the access token from bad actors.

Let's write a test to show that a connection fails if the handshake request does not include a valid access token.

```python
# server/trips/tests/test_websocket.py

async def test_cannot_connect_to_socket(self, settings):
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    communicator = WebsocketCommunicator(
        application=application,
        path='/taxi/'
    )
    connected, _ = await communicator.connect()
    assert connected is False
    await communicator.disconnect()
```

Create a new server/taxi/middleware.py file with the following code:

```python
# server/taxi/middleware.py

from urllib.parse import parse_qs

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from channels.auth import AuthMiddleware
from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware, SessionMiddleware
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


@database_sync_to_async
def get_user(scope):
    close_old_connections()
    query_string = parse_qs(scope['query_string'].decode())
    token = query_string.get('token')
    if not token:
        return AnonymousUser()
    try:
        access_token = AccessToken(token[0])
        user = User.objects.get(id=access_token['id'])
    except Exception as exception:
        return AnonymousUser()
    if not user.is_active:
        return AnonymousUser()
    return user


class TokenAuthMiddleware(AuthMiddleware):
    async def resolve_scope(self, scope):
        scope['user']._wrapped = await get_user(scope)


def TokenAuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(TokenAuthMiddleware(inner)))
```

Our new middleware class plucks the JWT access token from the query string and retrieves the associated user. Once the WebSocket connection is opened, all messages can be sent and received without verifying the user again. Closing the connection and opening it again requires re-authorization.

Let's implement the middleware. Open the server/taxi/asgi.py file and make the following changes:

```python
# server/taxi/asgi.py

import os

from django.core.asgi import get_asgi_application
from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taxi.settings')

from taxi.middleware import TokenAuthMiddlewareStack # new
from trips.consumers import TaxiConsumer

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': TokenAuthMiddlewareStack( # changed
        URLRouter([
            path('taxi/', TaxiConsumer.as_asgi()),
        ])
    ),
})
```

Here, we're wrapping our URL router in our middleware stack, so all incoming connection requests will go through our authentication method.

With the middleware in place, let's edit our consumer to reject any connection that does not have an authenticated user.

```python
# server/trips/consumers.py

async def connect(self): # changed
    user = self.scope['user']
    if user.is_anonymous:
        await self.close()
    else:
        await self.channel_layer.group_add(
            group='test',
            channel=self.channel_name
        )
        await self.accept()
```

We need to add one more `mark` to our `pytest` test class in order to access the database.

```python
# server/trips/tests/test_websocket.py

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True) # new
class TestWebSocket: ...
```

We need to refactor our other WebSocket tests to pass a JWT access token in the query string when connecting. Add the following create_user() helper function after TEST_CHANNEL_LAYERS and before TestWebSocket:

```python
# server/trips/tests/test_websocket.py
...
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
...

@database_sync_to_async
def create_user(username, password):
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    access = AccessToken.for_user(user)
    return user, access
```

```python
# server/trips/tests/test_websocket.py

async def test_can_connect_to_server(self, settings):
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    _, access = await create_user(  # new
        'test.user@example.com', 'pAssw0rd'
    )
    communicator = WebsocketCommunicator(
        application=application,
        path=f'/taxi/?token={access}' # changed
    )
    connected, _ = await communicator.connect()
    assert connected is True
    await communicator.disconnect()
```

Make the same change to the next two functions -- e.g., call the create_user() function to get the access token and then pass it as a query string parameter in the communicator's path.

```python
# server/trips/tests/test_websocket.py

import pytest
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

from taxi.asgi import application

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


@database_sync_to_async
def create_user(username, password):
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    access = AccessToken.for_user(user)
    return user, access


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'pAssw0rd'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'pAssw0rd'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_can_send_and_receive_broadcast_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'pAssw0rd'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send('test', message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_cannot_connect_to_socket(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path='/taxi/'
        )
        connected, _ = await communicator.connect()
        assert connected is False
        await communicator.disconnect()
```