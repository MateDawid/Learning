# Luigi Scheduler

Source: https://www.digitalocean.com/community/tutorials/how-to-build-a-data-processing-pipeline-using-luigi-in-python-on-ubuntu-20-04#step-4-running-the-luigi-scheduler

So far, you have been running Luigi using the --local-scheduler tag to run your jobs locally without allocating work to a central scheduler. This is useful for development, but for production usage it is recommended to use the Luigi scheduler. The Luigi scheduler provides:

* A central point to execute your tasks.
* Visualization of the execution of your tasks.

To access the Luigi scheduler interface, you need to enable access to port 8082.

To run the scheduler execute the following command:
```commandline
luigid --port 8082 --background
```

Open a browser to access the Luigi interface. This will either be at http://localhost:8082/

By default, Luigi tasks run using the Luigi scheduler. To run one of your previous tasks using the Luigi scheduler omit the --local-scheduler argument from the command.

```commandline
python -m luigi --module word-frequency GetTopBooks
```