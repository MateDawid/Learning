# Luigi config

Source: https://www.digitalocean.com/community/tutorials/how-to-build-a-data-processing-pipeline-using-luigi-in-python-on-ubuntu-20-04#step-7-defining-configuration-parameters

When you want to set parameters that are shared among tasks, you can create a Config() class. Other pipeline stages can reference the parameters defined in the Config() class; these are set by the pipeline when executing a job.

```python
class GlobalParams(luigi.Config):
    NumberBooks = luigi.IntParameter(default=10)
    NumberTopWords = luigi.IntParameter(default=500)

    
class TopWords(luigi.Task):
    """
    Aggregate the count results from the different files
    """

    def requires(self):
        requiredInputs = []
        for i in range(GlobalParams().NumberBooks):
            requiredInputs.append(CountWords(FileID=i))
        return requiredInputs

    def output(self):
        return luigi.LocalTarget("data/summary.txt")

    def run(self):
        total_count = Counter()
        for input in self.input():
            with input.open("rb") as infile:
                nextCounter = pickle.load(infile)
                total_count += nextCounter

        with self.output().open("w") as f:
            for item in total_count.most_common(GlobalParams().NumberTopWords):
                f.write("{0: <15}{1}\n".format(*item))
```

Config values may be overridden in command.

```commandline
python -m luigi --module word-frequency TopWords --GlobalParams-NumberBooks 15 --GlobalParams-NumberTopWords 750
```