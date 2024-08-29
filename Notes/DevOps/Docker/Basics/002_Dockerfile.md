# Dockerfile
Source: https://testdriven.io/blog/docker-for-beginners

Again, a Dockerfile is a text file that contains instructions for Docker on how to build an image. By default, a Dockerfile has no extension, but you can add one if you need more than one -- e.g., Dockerfile.prod.

```dockerfile
FROM python:3.10-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## CMD and ENTRYPOINT

Some Docker instructions are so similar it can be hard to understand why both commands are needed. One of those "couples" are CMD and ENTRYPOINT.

First, for the similarities:

* CMD and ENTRYPOINT both specify a command / an executable that will be executed when running a container. Unlike RUN, which executes the command right away (the result is used in the image layer), the CMD/ENTRYPOINT command in the build-up specifies the command that will be used only when the container starts.
* You can have only one CMD/ENTRYPOINT instruction in a Dockerfile, but it can point to a more complicated executable file.

There's actually only one difference between those instructions:

* CMD can easily be overridden from Docker CLI.

You should use CMD if you want the flexibility to run different executables depending on your needs when starting the container. If you want to clearly communicate that command is not meant to be overridden and prevent accidentally changing it, use ENTRYPOINT.

You may also use both CMD and ENTRYPOINT in the same Dockerfile, in which case CMD serves as the default argument for the ENTRYPOINT.

You can have only one CMD instruction in a Dockerfile, but it can point to a more complicated executable file. If you have more than one CMD, only the last CMD will take effect. The same goes for the ENTRYPOINT instruction.

There's a big chance you'll see the ENTRYPOINT argument as an executable file since commands that should be executed are often more than a one-liner.

Example of ENTRYPOINT as executable file usage:

```dockerfile
ENTRYPOINT ["./entrypoint.sh"]
```

And this is what the entrypoint.sh file might look like:

```bash
#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput
```

## ADD and COPY

Another pair similar to one another is ADD and COPY.

Both instructions copy new files or directories from the path to the filesystem of the image at the path:

```dockerfile
ADD <src> <dest>
COPY <src> <dest>
```

Additionally, ADD can copy from remote file URLs (for example, it allows adding a git repository to an image directly) and directly from a compressed archive (ADD will automatically unpack the contents to the given location).

You should prefer COPY over ADD unless you specifically need one of the two additional features of ADD -- i.e., downloading example files or unpacking a compressed file

Examples of ADD and COPY instruction usage:

```dockerfile
# copy local files on the host to the destination
COPY /source/path  /destination/path
COPY ./requirements.txt .

# download external file and copy to the destination
ADD http://external.file/url  /destination/path
ADD --keep-git-dir=true https://github.com/moby/buildkit.git#v0.10.1 /buildkit

# copy and extract local compresses files
ADD source.file.tar.gz /destination/path
```