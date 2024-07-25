# Docker image

Source: https://testdriven.io/blog/docker-for-beginners/#image

## What image is?

An image might be the most confusing concept of the three. You create a Dockerfile and then use a container, but an image lies between those two.

So, an image is a read-only embodiment of a Dockerfile that's used to create a Docker container. It consists of layers -- each line in a Dockerfile makes one layer. You can't change an image directly; you change it by changing the Dockerfile. You don't directly use an image either; you use a container created from an image.

The most important image-related tasks are:

* building images from Dockerfiles
* listing all the built images
* removing images

## Building image

To build an image from a Dockerfile, you use the docker image build command. This command requires one argument: either a path or URL of the context.

This image will use the current directory as a context:

```commandline
$ docker image build .
```
There are a number of options you can provide. For example, -f is used to specify a specific Dockerfile when you have multiple Dockerfiles (e.g., `Dockerfile.prod`) or when the Dockerfile isn't in the current directory (e.g., `docker image build . -f docker/Dockerfile.prod`).

Probably the most important is the -t tag that is used to name/tag an image.

When you build an image, it gets assigned an ID. Contrary to what you might expect, the IDs are not unique. If you want to be able to easily reference your image, you should name/tag it. With -t, you can assign a name and a tag to it.

Here's an example of creating three images: one without the usage of -t, one with a name assigned, and one with a name and a tag assigned.

```commandline
$ docker image build .
$ docker image build . -t hello_world
$ docker image build . -t hello_world:67d19c27b60bd782c9d3600ae914604a94bddfd4

$ docker image ls
REPOSITORY    TAG                                        IMAGE ID       CREATED          SIZE
hello_world   67d19c27b60bd782c9d3600ae914604a94bddfd4   e03784993f22   25 minutes ago   181MB
hello_world   latest                                     e03784993f22   26 minutes ago   181MB
<none>        <none>                                     7a615d108866   29 minutes ago   181MB
```

Notes:
* For the image that was built without a name or tag, you can only reference it via its image ID. Not only is it difficult to remember, but, again, it might not be unique (which is the case above). You should avoid this.
* For the image that only has a name (-t hello_world), the tag is automatically set to latest. You should avoid this as well. For more, review Version Docker Images.

## Listing
The docker image ls command lists all built images.

Example:
```commandline
$ docker image ls

REPOSITORY      TAG       IMAGE ID       CREATED         SIZE
hello_world     latest    c50405e84d39   9 minutes ago   245MB
<none>          <none>    2700a62cd8f1   42 hours ago    245MB
alpine/git      latest    692618a0d74d   2 weeks ago     43.4MB
todo_app        test      999740882932   3 weeks ago     1.03GB
```

## Removing
There are two use cases for removing images:

* You want to remove one or more selected images
* You want to remove all the unused images (you don't care which images specifically)

For the first case, you use `docker image rm;` for the second, you use `docker image prune`.
