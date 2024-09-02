# DRF Basics

Source: https://testdriven.io/courses/django-rest-framework/intro

## REST
An API, which stands for Application Programming Interface, is an interface for computers instead of people. It's a method of communication between two machines.

REST, which stands for Representational State Transfer, is an architectural style for providing standards between computer systems on the web. Its purpose is to make it easier for systems to communicate with each other.

For a system to be "RESTful" -- i.e., compliant with REST -- it needs to abide by some rules:

1. **Separation of Concerns**: The client and server are separated
2. **Stateless**: Each request from the client to the server is stateless. In other words, both the client and server can understand any request independently, without seeing any of the previous requests.
3. **Uniformed Interface**: All API endpoints should be accessible by the same approach.

## Methods

| HTTP   | Method  | 	CRUD Action	Scope | 	Purpose	                                | Structure of URL          |
|--------|---------|--------------------|------------------------------------------|---------------------------|
| GET    | 	Read   | 	collection        | 	Retrieve all resources in a collection	 | api/shopping-items/       |
| GET    | 	Read   | 	single resource   | 	Retrieve a single resource	             | api/shopping-items/<uuid> |
| POST   | 	Create | 	collection        | 	Create a new resource in a collection	  | api/shopping-items/       |
| PUT    | 	Update | 	single resource   | 	Update a single resource	               | api/shopping-items/<uuid> |
| PATCH  | 	Update | 	single resource   | 	Update a single resource	               | api/shopping-items/<uuid> |
| DELETE | 	Delete | 	single resource	  | Delete a single resource	                | api/shopping-items/<uuid> |