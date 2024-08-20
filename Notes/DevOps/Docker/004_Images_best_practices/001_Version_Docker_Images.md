# Version Docker Images

Source: https://testdriven.io/blog/docker-best-practices/#version-docker-images

Whenever possible, avoid using the latest tag.

If you rely on the latest tag (which isn't really a "tag" since it's applied by default when an image isn't explicitly tagged), you can't tell which version of your code is running based on the image tag. It makes it challenging to do rollbacks and makes it easy to overwrite it (either accidentally or maliciously). Tags, like your infrastructure and deployments, should be immutable.

Regardless of how you treat your internal images, you should never use the latest tag for base images since you could inadvertently deploy a new version with breaking changes to production.

For internal images, use descriptive tags to make it easier to tell which version of the code is running, handle rollbacks, and avoid naming collisions.

For example, you can use the following descriptors to make up a tag:

1. Timestamps
2. Docker image IDs
3. Git commit hashes
4. Semantic version

For example:
```commandline
docker build -t web-prod-a072c4e5d94b5a769225f621f08af3d4bf820a07-0.1.4 .
```

Here, we used the following to form the tag:

1. Project name: web
2. Environment name: prod
3. Git commit hash: a072c4e5d94b5a769225f621f08af3d4bf820a07
4. Semantic version: 0.1.4

It's essential to pick a tagging scheme and be consistent with it. Since commit hashes make it easy to tie an image tag back to the code quickly, it's highly recommended to include them in your tagging scheme.