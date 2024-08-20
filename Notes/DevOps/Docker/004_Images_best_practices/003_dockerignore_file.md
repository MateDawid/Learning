## Use a .dockerignore File

Source: https://testdriven.io/blog/docker-best-practices/#use-a-dockerignore-file

his file is used to specify the files and folders that you don't want to be added to the initial build context sent to the Docker daemon, which will then build your image. Put another way, you can use it to define the build context that you need.

When a Docker image is built, the entire Docker context -- e.g., the root of your project -- is sent to the Docker daemon before the COPY or ADD commands are evaluated. This can be pretty expensive, especially if you have many dependencies, large data files, or build artifacts in your project. Plus, the Docker CLI and daemon may not be on the same machine. So, if the daemon is executed on a remote machine, you should be even more mindful of the size of the build context.

What should you add to the .dockerignore file?

* Temporary files and folders
* Build logs
* Local secrets
* Local development files like docker-compose.yml
* Version control folders like ".git", ".hg", and ".svn"

Example:

```commandline
**/.git
**/.gitignore
**/.vscode
**/coverage
**/.env
**/.aws
**/.ssh
Dockerfile
README.md
docker-compose.yml
**/.DS_Store
**/venv
**/env
```

In summary, a properly structured .dockerignore can help:

* Decrease the size of the Docker image
* Speed up the build process
* Prevent unnecessary cache invalidation
* Prevent leaking secrets