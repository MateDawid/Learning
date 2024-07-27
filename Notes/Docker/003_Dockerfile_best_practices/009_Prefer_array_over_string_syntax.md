# Prefer Array Over String Syntax

Source: https://testdriven.io/blog/docker-best-practices/#prefer-array-over-string-syntax

You can write the CMD and ENTRYPOINT commands in your Dockerfiles in both array (exec) or string (shell) formats:

```dockerfile
# array (exec)
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app"]

# string (shell)
CMD "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app"
```

Both are correct and achieve nearly the same thing; however, you should use the exec format whenever possible. From the Docker documentation:

1. Make sure you're using the exec form of CMD and ENTRYPOINT in your Dockerfile.
2. For example use ["program", "arg1", "arg2"] not "program arg1 arg2". Using the string form causes Docker to run your process using bash, which doesn't handle signals properly. Compose always uses the JSON form, so don't worry if you override the command or entrypoint in your Compose file.

So, since most shells don't process signals to child processes, if you use the shell format, CTRL-C (which generates a SIGTERM) may not stop a child process.

```dockerfile
FROM ubuntu:24.04

# BAD: shell format
ENTRYPOINT top -d

# GOOD: exec format
ENTRYPOINT ["top", "-d"]
```

Try both of these. Take note that with the shell format flavor, `CTRL-C` won't kill the process. Instead, you'll see `^C^C^C^C^C^C^C^C^C^C^C`.

