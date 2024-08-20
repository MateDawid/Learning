# Include a HEALTHCHECK Instruction

Source: https://testdriven.io/blog/docker-best-practices/#include-a-healthcheck-instruction

Use a HEALTHCHECK to determine if the process running in the container is not only up and running, but is "healthy" as well.

Docker exposes an API for checking the status of the process running in the container, which provides much more information than just whether the process is "running" or not since "running" covers "it is up and working", "still launching", and even "stuck in some infinite loop error state". You can interact with this API via the HEALTHCHECK instruction.

For example, if you're serving up a web app, you can use the following to determine if the / endpoint is up and can handle serving requests:

```dockerfile
HEALTHCHECK CMD curl --fail http://localhost:8000 || exit 1
```

If you run `docker ps`, you can see the status of the HEALTHCHECK.

Healthy example:

```commandline
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS                            PORTS                                       NAMES
09c2eb4970d4   healthcheck   "python manage.py ru…"   10 seconds ago   Up 8 seconds (health: starting)   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   xenodochial_clarke
```

Unhealthy example:
```commandline
CONTAINER ID   IMAGE         COMMAND                  CREATED              STATUS                          PORTS                                       NAMES
09c2eb4970d4   healthcheck   "python manage.py ru…"   About a minute ago   Up About a minute (unhealthy)   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   xenodochial_clarke
```

You can take it a step further and set up a custom endpoint used only for health checks and then configure the 
`HEALTHCHECK` to test against the returned data. For example, if the endpoint returns a JSON 
response of `{"ping": "pong"}`, you can instruct the `HEALTHCHECK` to validate the response body.

Here's how you view the status of the health check status using docker inspect:

```commandline
❯ docker inspect --format "{{json .State.Health }}" ab94f2ac7889
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [
    {
      "Start": "2021-09-28T15:22:57.5764644Z",
      "End": "2021-09-28T15:22:57.7825527Z",
      "ExitCode": 0,
      "Output": "..."
```

You can also add a health check to a Docker Compose file:

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - '8000:8000'
    healthcheck:
      test: curl --fail http://localhost:8000 || exit 1
      interval: 10s
      timeout: 10s
      start_period: 10s
      retries: 3
```
Options:

* `test`: The command to test.
* `interval`: The interval to test for -- e.g., test every x unit of time.
* `timeout`: Max time to wait for the response.
* `start_period`: When to start the health check. It can be used when additional tasks are performed before the containers are ready, like running migrations.
* `retries`: Maximum retries before designating a test as failed.