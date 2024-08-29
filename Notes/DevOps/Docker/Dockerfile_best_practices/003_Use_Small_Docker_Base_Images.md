# Use Small Docker Base Images

Source: https://testdriven.io/blog/docker-best-practices/#use-small-docker-base-images

Building, pushing, and pulling images is quicker with smaller images. They also tend to be more secure since they only include the necessary libraries and system dependencies required for running your application.

*Which Docker base image should you use?*

Unfortunately, it depends.

Here's a size comparison of various Docker base images for Python:

```commandline
REPOSITORY   TAG                    IMAGE ID         CREATED          SIZE
python       3.12.2-bookworm        939b824ad847     40 hours ago     1.02GB
python       3.12.2-slim            24c52ee82b5c     40 hours ago     130MB
python       3.12.2-slim-bookworm   24c52ee82b5c     40 hours ago     130MB
python       3.12.2-alpine          c54b53ca8371     40 hours ago     51.8MB
python       3.12.2-alpine3.19      c54b53ca8371     40 hours ago     51.8MB
```

While the Alpine flavor, based on Alpine Linux, is the smallest, it can often lead to increased build times if you can't find compiled binaries that work with it. As a result, you may end up having to build the binaries yourself, which can increase the image size (depending on the required system-level dependencies) and the build times (due to having to compile from the source).

In the end, it's all about balance. When in doubt, start with a *-slim flavor, especially in development mode, as you're building your application. You want to avoid having to continually update the Dockerfile to install necessary system-level dependencies when you add a new Python package. As you harden your application and Dockerfile(s) for production, you may want to explore using Alpine for the final image from a multi-stage build.