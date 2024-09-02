# API and Serializers

Source: https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#apis--serializers

## API

When using services & selectors, all of your APIs should look simple & identical.

When we are creating new APIs, we follow those general rules:

* Have 1 API per operation. This means, for CRUD on a model, having 4 APIs.
* Inherit from the most simple APIView or GenericAPIView.
* Avoid the more abstract classes, since they tend to manage things via serializers & we want to do that via services & selectors.
* Don't do business logic in your API.
* You can do object fetching / data manipulation in your APIs (potentially, you can extract that to somewhere else).
* If you are calling some_service in your API, you can extract object fetching / data manipulation to some_service_parse.
* Basically, keep the APIs as simple as possible. They are an interface towards your core business logic.

## Serialization

When we are talking about APIs, we need a way to deal with data serialization - both incoming & outgoing data.

Here are our rules for API serialization:

* There should be a dedicated input serializer & a dedicated output serializer.
* Input serializer takes care of the data coming in.
* Output serializer takes care of the data coming out.
* In terms of serialization, Use whatever abstraction works for you.

In case you are using DRF's serializers, here are our rules:

* Serializer should be nested in the API and be named either InputSerializer or OutputSerializer.
* Our preference is for both serializers to inherit from the simpler Serializer and avoid using ModelSerializer
  * This is a matter of preference and choice. If ModelSerializer is working fine for you, use it.
* If you need a nested serializer, use the inline_serializer util.
* Reuse serializers as little as possible.
  * Reusing serializers may expose you to unexpected behavior, when something changes in the base serializers.

## Naming convention

For our APIs we use the following naming convention: <Entity><Action>Api.

Here are few examples: UserCreateApi, UserSendResetPasswordApi, UserDeactivateApi, etc.