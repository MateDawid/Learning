# Docker container

Source: https://testdriven.io/blog/docker-for-beginners/#container

## What container is?

The third concept you need to understand is a container, which is a controlled environment for your application. An image becomes a container when it's run on Docker Engine. It's the end goal: You use Docker so you can have a container for your application.

The main operations you can do with a container are

* running a container
* listing all the containers
* stopping a container
* removing a container

## Running

You can either create a new container of an image and run it, or you can start an existing container that was previously stopped.

The docker container run command actually combines two other commands, docker container create and docker container start.

```commandline
$ docker container run my_image

# the same as:

$ docker container create my_image
88ce9c60aeabbb970012b5f8dbae6f34581fa61ec20bd6d87c6831fbb5999263
$ docker container start 88ce9c60aeabbb970012b5f8dbae6f34581fa61ec20bd6d87c6831fbb5999263
```

Since you can override a number of the defaults, there are many options. You can see all of them in the official docs. The most important option is --publish/-p, which is used to publish ports to the outside world. Although it is technically possible to run a container without a port, it's not very useful since the service(s) running inside the container wouldn't be accessible outside the container. You can use --publish/-p for both the create and run commands:

```commandline
$ docker container run -p 8000:8000 my_image
```

You can run your container in detached mode by using --detach/-d, which lets you keep using the terminal.

```commandline
$ docker container run -p 8000:8000 -d my_image

0eb20b715f42bc5a053dc7878b3312c761058a25fc1efaffb7920b3b4e48df03
```

Your container gets a unique, quirky name by default, but you can assign your own name:

```commandline
$ docker container run -p 8000:8000 --name my_great_container my_image
```

To start a stopped or just created container, you use the docker container start command. Since with this command, you're starting an existing container, you have to specify the container instead of an image (as with `docker container run`).

Another difference from docker container run is that docker container start by default runs the container in the detached mode. You can attach it using --attach/-a (reverse from docker container run -d).

```commandline
$ docker container start -a reverent_sammet
```

## Listing

You can list all running containers with docker container ls.

```commandline
$ docker container ls

CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                    NAMES
0f21395ec96c   9973e9c65229   "/bin/sh -c 'gunicor…"   6 minutes ago   Up 6 minutes   0.0.0.0:80->8000/tcp     shopping
73bd69d041ae   my_image       "/bin/sh -c 'uvicorn…"   2 hours ago     Up 2 hours     0.0.0.0:8000->8000/tcp   my_great_container
```

If you want to also see the stopped containers, you can add the -a flag:

```commandline
$ docker container ls -a

CONTAINER ID   IMAGE          COMMAND                  CREATED              STATUS                     PORTS                    NAMES
0f21395ec96c   9973e9c65229   "/bin/sh -c 'gunicor…"   About a minute ago   Up About a minute          0.0.0.0:80->8000/tcp     shopping
73bd69d041ae   my_image       "/bin/sh -c 'uvicorn…"   2 hours ago          Up 2 hours                 0.0.0.0:8000->8000/tcp   my_great_container
0eb20b715f42   my_image       "/bin/sh -c 'uvicorn…"   2 hours ago          Exited (137) 2 hours ago                            agitated_gagarin
489a02b8cfac   my_image       "/bin/sh -c 'uvicorn…"   2 hours ago          Created                                             vigorous_poincare
```

1. CONTAINER ID (73bd69d041ae) and its NAMES (my_great_container) are both unique, so you can use them to access the container.
2. IMAGE (my_image) tells you which image was used to run the container.
3. CREATED is pretty self-explanatory: when the container was created (2 hours ago).
4. We already discussed the need for specifying a command for starting a container... COMMAND tells you which command was used ("/bin/sh -c 'uvicorn…").
5. STATUS is useful when you don't know why your container isn't working (Up 2 hours means your container is running, Exited or Created means it's not)

## Stopping

To stop a container, use docker container stop. The name or ID of the stopped container is then returned.

```commandline
$ docker container stop my_great_container
my_great_container

$ docker container stop 73bd69d041ae
73bd69d041ae
```

## Removing
Similar to images, to remove a container, you can either:

* remove one or more selected containers via docker container rm.
* remove all stopped containers via docker container prune

```commandline
$ docker container rm festive_euclid
festive_euclid
```

```commandline
$ docker container prune

WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
0f21395ec96c28b443bad8aac40197fe0468d24e0eed49e5f56011de1c81b589
80c693693f3d99999925eae5f4bbfc03236cde670db509797d83f50e732fcf31
0eb20b715f42bc5a053dc7878b3312c761058a25fc1efaffb7920b3b4e48df03
1273cf44c551f8ab9302e6d090e3c4e135ca6f7e1ab3d90a62bcbf5e83ba9342
```