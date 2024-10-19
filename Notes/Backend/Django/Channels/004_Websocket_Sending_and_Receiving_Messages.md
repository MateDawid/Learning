# Websocket - Sending and Receiving Messages

> Source: https://testdriven.io/courses/taxi-react/websockets-part-one/#H-1-sending-and-receiving-messages

## Sending and Receiving Messages

```python
# server/trips/tests/test_websocket.py

async def test_can_send_and_receive_messages(self, settings):
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    communicator = WebsocketCommunicator(
        application=application,
        path='/taxi/'
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
```

In this test, after we establish a connection with the server, we send a message and wait to get one back. We expect the server to echo our message right back to us exactly the way we sent it. In fact, we need to program this behavior on the server.

```python
# server/trips/consumers.py

async def receive_json(self, content, **kwargs):
    message_type = content.get('type')
    if message_type == 'echo.message':
        await self.send_json({
            'type': message_type,
            'data': content.get('data'),
        })
```

The `receive_json()` function is responsible for processing all messages that come to the server. Our message is an object with a `type` and a `data` payload. Passing a `type` is a Channels convention that serves two purposes:
* It helps differentiate incoming messages and tells the server how to process them.
* The type maps directly to a consumer function when sent from another channel layer. (We'll talk about this use in the next section.)

## Sending and Receiving Broadcast Messages

We saw how to make the client and the server send each other messages through a single instance of an application. Now, let's learn how to make one application talk to another through broadcast messaging.

```python
# server/trips/tests/test_websocket.py
...
from channels.layers import get_channel_layer
...

async def test_can_send_and_receive_broadcast_messages(self, settings):
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    communicator = WebsocketCommunicator(
        application=application,
        path='/taxi/'
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
```

This new test looks a lot like the last test we wrote, but it has one important difference: It uses a channel layer to broadcast a message to a group. Whereas the last test modeled a user talking to himself in an empty room, this most recent test represents a user talking to a room full of people.

We need to modify our consumer in two ways to get our newest test passing. Add the code as shown below:

```python
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TaxiConsumer(AsyncJsonWebsocketConsumer):
    groups = ['test'] # new

    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        await super().disconnect(code)

    async def echo_message(self, message): # new
        await self.send_json({
            'type': message.get('type'),
            'data': message.get('data'),
        })

    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'echo.message':
            await self.send_json({
                'type': message_type,
                'data': content.get('data'),
            })
```

As stated, the message `type` maps to a consumer function. That statement is true when we're talking about messages that are broadcast to groups. When a message comes from a channel layer, Channels looks for a function on the receiving consumer whose name matches the message `type`. It also converts any `.` characters to `_` characters before it checks for the match.

Channel layers broadcast messages to specific groups, which are collections of other channel layers that are subscribed to the same topic. One way to subscribe to a group is by defining the membership in a class variable like the change we added above.

Make the following change to keep the same behavior while making group subscription more explicit:

```python
# server/trips/consumers.py

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TaxiConsumer(AsyncJsonWebsocketConsumer):
    groups = ['test']

    async def connect(self): # changed
        await self.channel_layer.group_add(
            group='test',
            channel=self.channel_name
        )
        await self.accept()

    async def disconnect(self, code): # changed
        await self.channel_layer.group_discard(
            group='test',
            channel=self.channel_name
        )
        await super().disconnect(code)

    async def echo_message(self, message):
        await self.send_json({
            'type': message.get('type'),
            'data': message.get('data'),
        })

    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'echo.message':
            await self.send_json({
                'type': message_type,
                'data': content.get('data'),
            })
```

With these changes, any client connected to the `TaxiConsumer` through WebSockets will automatically be subscribed to the `test` group. When a channel layer sends a broadcast message with the type `echo.message`, Channels will execute the `echo_message()` function for everyone in the `test` group.