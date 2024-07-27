# Use Unprivileged Containers

Source: https://testdriven.io/blog/docker-best-practices/#use-unprivileged-containers

By default, Docker runs container processes as root inside of a container. However, this is a bad practice since a process running as root inside the container is running as root in the Docker host. Thus, if an attacker gains access to your container, they have access to all the root privileges and can perform several attacks against the Docker host, like-
* copying sensitive info from the host's filesystem to the container
* executing remote commands

To prevent this, make sure to run container processes with a non-root user:

```dockerfile
RUN addgroup --system app && adduser --system --group app

USER app
```

You can take it a step further and remove shell access and ensure there's no home directory as well:
```dockerfile
RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

USER app
```

Verify:

```commandline
$ docker run -i sample id

uid=1001(app) gid=1001(app) groups=1001(app)
```

