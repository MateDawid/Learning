# Luigi parameters

Source: https://www.digitalocean.com/community/tutorials/how-to-build-a-data-processing-pipeline-using-luigi-in-python-on-ubuntu-20-04#step-5-downloading-the-books

```python
# word-frequency.py

class DownloadBooks(luigi.Task):
    """
    Download a specified list of books
    """
    FileID = luigi.IntParameter()

    REPLACE_LIST = """.,"';_[]:*-"""

    def requires(self):
        return GetTopBooks()

    def output(self):
        return luigi.LocalTarget("data/downloads/{}.txt".format(self.FileID))

    def run(self):
        with self.input().open("r") as i:
            URL = i.read().splitlines()[self.FileID]

            with self.output().open("w") as outfile:
                book_downloads = requests.get(URL)
                book_text = book_downloads.text

                for char in self.REPLACE_LIST:
                    book_text = book_text.replace(char, " ")

                book_text = book_text.lower()
                outfile.write(book_text)
```

In this task you introduce a Parameter; in this case, an integer parameter. Luigi parameters are inputs to your tasks that affect the execution of the pipeline. Here you introduce a parameter FileID to specify a line in your list of URLs to fetch.

```commandline
python -m luigi --module word-frequency DownloadBooks --FileID 2
```