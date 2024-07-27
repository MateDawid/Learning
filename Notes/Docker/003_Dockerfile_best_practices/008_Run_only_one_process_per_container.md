# Run Only One Process Per Container

Source: https://testdriven.io/blog/docker-best-practices/#run-only-one-process-per-container

Why is it recommended to run only one process per container?

Let's assume your application stack consists of a two web servers and a database. While you could easily run all three from a single container, you should run each in a separate container to make it easier to reuse and scale each of the individual services.

1. Scaling - With each service in a separate container, you can scale one of your web servers horizontally as needed to handle more traffic.
2. Reusability - Perhaps you have another service that needs a containerized database. You can simply reuse the same database container without bringing two unnecessary services along with it.
3. Logging - Coupling containers makes logging much more complex. We'll address this in further detail later in this article.
4. Portability and Predictability - It's much easier to make security patches or debug an issue when there's less surface area to work with.