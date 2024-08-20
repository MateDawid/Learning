# Secure Communication with TLS

Source: https://testdriven.io/blog/docker-best-practices/#secure-communication-with-tls

When a Docker daemon is exposed to the network or accessed over a network, securing the communication channel is crucial to prevent unauthorized access and ensure the integrity and confidentiality of the data being transmitted. Using TLS (Transport Layer Security) helps in encrypting the communication between the Docker client and the Docker daemon, making it significantly more secure.

To set up TLS for Docker, you'll need to generate SSL certificates: a CA (Certificate Authority) certificate, a server certificate for the Docker daemon, and a client certificate for the Docker client. These certificates are used to encrypt the communication and authenticate the client and server to each other.