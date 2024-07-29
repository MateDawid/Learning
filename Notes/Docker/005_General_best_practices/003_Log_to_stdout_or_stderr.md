# Log to stdout or stderr

Source: https://testdriven.io/blog/docker-best-practices/#log-to-stdout-or-stderr

Applications running within your Docker containers should write log messages to standard output (stdout) and standard error (stderr) rather than to a file.

You can then configure the Docker daemon to send your log messages to a centralized logging solution (like CloudWatch Logs or Papertrail).

