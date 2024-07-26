# Order Dockerfile Commands Appropriately

Source: https://testdriven.io/blog/docker-best-practices/#order-dockerfile-commands-appropriately

Docker caches each step (or layer) in a particular Dockerfile to speed up subsequent builds. When a step changes, the cache will be invalidated not only for that particular step but all succeeding steps.

```dockerfile
FROM python:3.12.2-slim

WORKDIR /app

COPY sample.py .

COPY requirements.txt .

RUN pip install -r requirements.txt
```

In this Dockerfile, we copied over the application code before installing the requirements. Now, each time we change sample.py, the build will reinstall the packages. This is very inefficient, especially when using a Docker container as a development environment. Therefore, it's crucial to keep the files that frequently change towards the end of the Dockerfile.

So, in the above Dockerfile, you should move the COPY sample.py . command to the bottom:

```dockerfile
FROM python:3.12.2-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY sample.py .
```
Notes:

* Always put layers that are likely to change as low as possible in the Dockerfile.
* Combine RUN apt-get update and RUN apt-get install commands. (This also helps to reduce the image size. We'll touch on this shortly.)
* If you want to turn off caching for a particular Docker build, add the --no-cache=True flag.