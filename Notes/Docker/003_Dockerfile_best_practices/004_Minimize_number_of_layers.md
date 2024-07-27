# Minimize the Number of Layers

Source: https://testdriven.io/blog/docker-best-practices/#minimize-the-number-of-layers

It's a good idea to combine the RUN, COPY, and ADD commands as much as possible since they create layers. Each layer increases the size of the image since they are cached. Therefore, as the number of layers increases, the size also increases.

You can test this out with the docker history command:

```commandline
$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
dockerfile   latest    180f98132d02   51 seconds ago   259MB

$ docker history 180f98132d02

IMAGE          CREATED              CREATED BY                                      SIZE      COMMENT
180f98132d02   58 seconds ago       COPY . . # buildkit                             6.71kB    buildkit.dockerfile.v0
<missing>      58 seconds ago       RUN /bin/sh -c pip install -r requirements.t…   35.5MB    buildkit.dockerfile.v0
<missing>      About a minute ago   COPY requirements.txt . # buildkit              58B       buildkit.dockerfile.v0
<missing>      About a minute ago   WORKDIR /app
...
```
Take note of the sizes. Only the RUN, COPY, and ADD commands add size to the image. You can reduce the image size by combining commands wherever possible. For example:
```dockerfile
RUN apt-get update
RUN apt-get install -y netcat
```
Can be combined into a single RUN command:

```dockerfile
RUN apt-get update && apt-get install -y netcat
```

While it's a good idea to reduce the number of layers, it's much more important for that to be less of a goal in itself and more a side-effect of reducing the image size and build times. In other words, focus more on the previous three practices -- multi-stage builds, order of your Dockerfile commands, and using a small base image -- than trying to optimize every single command.

Notes:

* RUN, COPY, and ADD each create layers.
* Each layer contains the differences from the previous layer.
* Layers increase the size of the final image.

Tips:

* Combine related commands.
* Remove unnecessary files in the same RUN step that created them.
* Minimize the number of times apt-get upgrade is run since it upgrades all packages to the latest version.
* With multi-stage builds, don't worry too much about overly optimizing the commands in temp stages.

```dockerfile
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    matplotlib \
    pillow  \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

Additionally, it's crucial to perform clean-up actions within the same RUN instruction to avoid unnecessary bloat in your Docker images. This approach ensures that temporary files or cache used during installation are not included in the final image layer, effectively reducing the image size. For example, after installing packages with apt-get, use && apt-get clean && rm -rf /var/lib/apt/lists/* to remove the package lists and any temporary files created during the installation process, as demonstrated above. This practice is essential for keeping your Docker images as lean and efficient as possible.