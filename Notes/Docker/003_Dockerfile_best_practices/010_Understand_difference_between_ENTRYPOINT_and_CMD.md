# Understand the Difference Between ENTRYPOINT and CMD

Source: https://testdriven.io/blog/docker-best-practices/#understand-the-difference-between-entrypoint-and-cmd

There are two ways to run commands in a container:

```dockerfile
CMD ["gunicorn", "config.wsgi", "-b", "0.0.0.0:8000"]

# and

ENTRYPOINT ["gunicorn", "config.wsgi", "-b", "0.0.0.0:8000"]
```

Both essentially do the same thing: Start the application at `config.wsgi` with a Gunicorn server and bind it to `0.0.0.0:8000`.

The CMD is easily overridden. If you run `docker run <image_name> uvicorn config.asgi`, the above `CMD` gets replaced by the new arguments -- i.e., `uvicorn config.asgi`. Whereas to override the `ENTRYPOINT` command, one must specify the `--entrypoint` option:
```commandline
docker run --entrypoint uvicorn config.asgi <image_name>
```

Here, it's clear that we're overriding the entrypoint. So, it's recommended to use `ENTRYPOINT` over `CMD` to prevent accidentally overriding the command.

They can be used together as well.

```dockerfile
ENTRYPOINT ["gunicorn", "config.wsgi", "-w"]
CMD ["4"]
```

When used together like this, the command that is run to start the container is:

```commandline
gunicorn config.wsgi -w 4
```
As discussed above, CMD is easily overridden. Thus, CMD can be used to pass arguments to the ENTRYPOINT command. The number of workers can be easily changed like so:

```commandline
docker run <image_name> 6
```
This will start the container with six Gunicorn workers rather then four.

