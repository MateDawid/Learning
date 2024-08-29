# Lint and Scan Your Dockerfiles and Images

Source: https://testdriven.io/blog/docker-best-practices/#lint-and-scan-your-dockerfiles-and-images

Linting is the process of checking your source code for programmatic and stylistic errors and bad practices that could lead to potential flaws. Just like with programming languages, static files can also be linted. With your Dockerfiles specifically, linters can help ensure they are maintainable, avoid deprecated syntax, and adhere to best practices. Linting your images should be a standard part of your CI pipelines.

Hadolint is the most popular Dockerfile linter:

```commandline
$ hadolint Dockerfile

Dockerfile:1 DL3006 warning: Always tag the version of an image explicitly
Dockerfile:7 DL3042 warning: Avoid the use of cache directory with pip. Use `pip install --no-cache-dir <package>`
Dockerfile:9 DL3059 info: Multiple consecutive `RUN` instructions. Consider consolidation.
Dockerfile:17 DL3025 warning: Use arguments JSON notation for CMD and ENTRYPOINT arguments
```

You can see it in action online at https://hadolint.github.io/hadolint/. There's also a VS Code Extension.

You can couple linting your Dockerfiles with scanning images and containers for vulnerabilities.

