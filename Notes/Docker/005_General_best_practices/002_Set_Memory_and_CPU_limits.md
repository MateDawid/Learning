# Set Memory and CPU Limits

Source: https://testdriven.io/blog/docker-best-practices/#set-memory-and-cpu-limits

It's a good idea to limit the memory usage of your Docker containers, especially if you're running multiple containers on a single machine. This can prevent any of the containers from using all available memory and thereby crippling the rest.

The easiest way to limit memory usage is to use --memory and --cpu options in the Docker CLI:

```commandline
$ docker run --cpus=2 -m 512m nginx
```

The above command limits the container usage to 2 CPUs and 512 megabytes of main memory.

You can do the same in a Docker Compose file like so:

```yaml
version: "3.9"
services:
  redis:
    image: redis:alpine
    deploy:
      resources:
        limits:
          cpus: 2
          memory: 512M
        reservations:
          cpus: 1
          memory: 256M
```

Take note of the `reservations` field. It's used to set a soft limit, which takes priority when the host machine has low memory or CPU resources.

