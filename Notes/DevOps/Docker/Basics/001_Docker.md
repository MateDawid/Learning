# Docker
Source: https://testdriven.io/blog/docker-for-beginners

## Docker Engine
When people refer to Docker, they're typically referring to Docker Engine.

Docker Engine is the underlying open source containerization technology for building, managing, and running containerized applications. It's a client-server application with the following components:

1. Docker daemon (called dockerd) is a service that runs in the background that listens for Docker Engine API requests and manages Docker objects like images and containers.
2. Docker Engine API is a RESTful API that's used to interact with Docker daemon.
3. Docker client (called docker) is the command line interface used for interacting with Docker daemon. So, when you use a command like docker build, you're using Docker client, which in turn leverages Docker Engine API to communicate with Docker daemon.

## Docker Desktop

These days, when you try to install Docker, you'll come across Docker Desktop. While Docker Engine is included with Docker Desktop, it's important to understand that Docker Desktop is not the same as Docker Engine. Docker Desktop is an integrated development environment for Docker containers. It makes it much easier to get your operating system configured for working with Docker.

## Docker Concepts

At the heart of Docker, there are three core concepts:

1. Dockerfile - a text file that serves as a blueprint for your container. In it, you define a list of instructions that Docker uses to build an image.
2. Image - a read-only embodiment of the Dockerfile. It's built out of layers -- each layer corresponds to a single line of instructions from a Dockerfile.
3. Container - running a Docker image produces a container, which is a controlled environment for your application. If we draw parallels with object-oriented programming, a container is an instance of a Docker image.