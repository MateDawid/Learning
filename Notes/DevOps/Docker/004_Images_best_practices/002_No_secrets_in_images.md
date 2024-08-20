# Don't Store Secrets in Images

Source: https://testdriven.io/blog/docker-best-practices/#dont-store-secrets-in-images

Secrets are sensitive pieces of information such as passwords, database credentials, SSH keys, tokens, and TLS certificates, to name a few. These should not be baked into your images without being encrypted since unauthorized users who gain access to the image can merely examine the layers to extract the secrets.

Do not add secrets to your Dockerfiles in plaintext, especially if you're pushing the images to a public registry like Docker Hub:

```dockerfile
FROM python:3.12.2-slim

ENV DATABASE_PASSWORD "SuperSecretSauce"
```

Instead, they should be injected via:

* Environment variables (at run-time)
* Build-time arguments (at build-time)
* An orchestration tool like Docker Swarm (via Docker secrets) or Kubernetes (via Kubernetes secrets)

Also, you can help prevent leaking secrets by adding common secret files and folders to your .dockerignore file:
```commandline
**/.env
**/.aws
**/.ssh
```
Finally, be explicit about what files are getting copied over to the image rather than copying all files recursively:
```dockerfile
# BAD
COPY . .

# GOOD
copy ./app.py .
```

Being explicit also helps to limit cache-busting.

## Environment Variables
You can pass secrets via environment variables, but they will be visible in all child processes, linked containers, and logs, as well as via docker inspect. It's also difficult to update them.

```commandline
$ docker run --detach --env "DATABASE_PASSWORD=SuperSecretSauce" python:3.9-slim

d92cf5cf870eb0fdbf03c666e7fcf18f9664314b79ad58bc7618ea3445e39239


$ docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' d92cf5cf870eb0fdbf03c666e7fcf18f9664314b79ad58bc7618ea3445e39239

DATABASE_PASSWORD=SuperSecretSauce
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LANG=C.UTF-8
GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
PYTHON_VERSION=3.9.7
PYTHON_PIP_VERSION=21.2.4
PYTHON_SETUPTOOLS_VERSION=57.5.0
PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/c20b0cfd643cd4a19246ccf204e2997af70f6b21/public/get-pip.py
PYTHON_GET_PIP_SHA256=fa6f3fb93cce234cd4e8dd2beb54a51ab9c247653b52855a48dd44e6b21ff28b
```

This is the most straightforward approach to secrets management. While it's not the most secure, it will keep the honest people honest since it provides a thin layer of protection, helping to keep the secrets hidden from curious wandering eyes.

Passing secrets in using a shared volume is a better solution, but they should be encrypted, via Vault or AWS Key Management Service (KMS), since they are saved to disc.

## Build-time Arguments

You can pass secrets in at build-time using build-time arguments, but they will be visible to those who have access to the image via docker history.

```dockerfile
FROM python:3.12.2-slim

ARG DATABASE_PASSWORD
```

```commandline
$ docker build --build-arg "DATABASE_PASSWORD=SuperSecretSauce" .
```

If you only need to use the secrets temporarily as part of the build -- e.g., SSH keys for cloning a private repo or downloading a private package -- you should use a multi-stage build since the builder history is ignored for temporary stages:

```dockerfile
# temp stage
FROM python:3.12.2-slim as builder

# secret
ARG SSH_PRIVATE_KEY

# install git
RUN apt-get update && \
    apt-get install -y --no-install-recommends git

# use ssh key to clone repo
RUN mkdir -p /root/.ssh/ && \
    echo "${PRIVATE_SSH_KEY}" > /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts &&
    ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts
RUN git clone git@github.com:testdrivenio/not-real.git


# final stage
FROM python:3.12.2-slim

WORKDIR /app

# copy the repository from the temp image
COPY --from=builder /your-repo /app/your-repo

# use the repo for something!
```
The multi-stage build only retains the history for the final image. Keep in mind that you can use this functionality for permanent secrets that you need for your application, like a database credential.

You can also use the new --secret option in Docker build to pass secrets to Docker images that do not get stored in the images.
```dockerfile
# "docker_is_awesome" > secrets.txt

FROM alpine

# shows secret from default secret location:
RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
```
This will mount the secret from the secrets.txt file.

Build the image:

```commandline
docker build --no-cache --progress=plain --secret id=mysecret,src=secrets.txt .

# output
...
#4 [1/2] FROM docker.io/library/alpine
#4 sha256:665ba8b2cdc0cb0200e2a42a6b3c0f8f684089f4cd1b81494fbb9805879120f7
#4 CACHED

#5 [2/2] RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
#5 sha256:75601a522ebe80ada66dedd9dd86772ca932d30d7e1b11bba94c04aa55c237de
#5 0.635 docker_is_awesome#5 DONE 0.7s

#6 exporting to image
```

Finally, check the history to see if the secret is leaking:

```commandline
❯ docker history 49574a19241c
IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
49574a19241c   5 minutes ago   CMD ["/bin/sh"]                                 0B        buildkit.dockerfile.v0
<missing>      5 minutes ago   RUN /bin/sh -c cat /run/secrets/mysecret # b…   0B        buildkit.dockerfile.v0
<missing>      4 weeks ago     /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
<missing>      4 weeks ago     /bin/sh -c #(nop) ADD file:aad4290d27580cc1a…   5.6MB
```
