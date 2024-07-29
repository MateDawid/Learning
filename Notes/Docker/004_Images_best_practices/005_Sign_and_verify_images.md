# Sign and Verify Images

Source: https://testdriven.io/blog/docker-best-practices/#sign-and-verify-images

How do you know that the images used to run your production code have not been tampered with?

Tampering can come over the wire via man-in-the-middle (MITM) attacks or from the registry being compromised altogether.

Docker Content Trust (DCT) enables the signing and verifying of Docker images from remote registries.

To verify the integrity and authenticity of an image, set the following environment variable:

```dotenv
DOCKER_CONTENT_TRUST=1
```

Now, if you try to pull an image that hasn't been signed, you'll receive the following error:

```commandline
Error: remote trust data does not exist for docker.io/namespace/unsigned-image:
notary.docker.io does not have trust data for docker.io/namespace/unsigned-image
```

You can learn about signing images from the Signing Images with [Docker Content Trust documentation](https://docs.docker.com/engine/security/trust/#signing-images-with-docker-content-trust).