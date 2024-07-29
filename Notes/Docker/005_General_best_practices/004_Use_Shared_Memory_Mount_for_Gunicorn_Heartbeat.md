# Use a Shared Memory Mount for Gunicorn Heartbeat

Source: https://testdriven.io/blog/docker-best-practices/#use-a-shared-memory-mount-for-gunicorn-heartbeat

Gunicorn uses a file-based heartbeat system to ensure that all of the forked worker processes are alive.

In most cases, the heartbeat files are found in "/tmp", which is often in memory via tmpfs. Since Docker does not leverage tmpfs by default, the files will be stored on a disk-backed file system. This can cause problems, like random freezes since the heartbeat system uses os.fchmod, which may block a worker if the directory is in fact on a disk-backed filesystem.

Fortunately, there is a simple fix: Change the heartbeat directory to a memory-mapped directory via the --worker-tmp-dir flag.

```commandline
gunicorn --worker-tmp-dir /dev/shm config.wsgi -b 0.0.0.0:8000
```