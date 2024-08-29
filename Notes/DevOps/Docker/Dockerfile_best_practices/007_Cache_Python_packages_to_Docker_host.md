# Cache Python Packages to the Docker Host

Source: https://testdriven.io/blog/docker-best-practices/#cache-python-packages-to-the-docker-host

When a requirements file is changed, the image needs to be rebuilt to install the new packages. The earlier steps will be cached, as mentioned in Minimize the Number of Layers. Downloading all packages while rebuilding the image can cause a lot of network activity and takes a lot of time. Each rebuild takes up the same amount of time for downloading common packages across builds.

You can avoid this by mapping the pip cache directory to a directory on the host machine. So for each rebuild, the cached versions persist and can improve the build speed.

Add a volume to the docker run as `-v $HOME/.cache/pip-docker/:/root/.cache/pip` or as a mapping in the Docker Compose file.

Moving the cache from the docker image to the host can save you space in the final image.

