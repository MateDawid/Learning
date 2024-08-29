# Prefer COPY Over ADD

Source: https://testdriven.io/blog/docker-best-practices/#prefer-copy-over-add

Use COPY unless you're sure you need the additional functionality that comes with ADD.

Both commands allow you to copy files from a specific location into a Docker image:

```dockerfile
ADD <src> <dest>
COPY <src> <dest>
```

While they look like they serve the same purpose, ADD has some additional functionality:

* COPY is used for copying local files or directories from the Docker host to the image.
* ADD can be used for the same thing as well as downloading external files. Also, if you use a compressed file (tar, gzip, bzip2, etc.) as the <src> parameter, ADD will automatically unpack the contents to the given location.

```dockerfile
# copy local files on the host to the destination
COPY /source/path  /destination/path
ADD /source/path  /destination/path

# download external file and copy to the destination
ADD http://external.file/url  /destination/path

# copy and extract local compresses files
ADD source.file.tar.gz /destination/path
```