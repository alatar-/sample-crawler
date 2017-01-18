# Sample crawler

## Pre

- Python 3.5
- requirements.txt

## Example usage

To crawl and store into `crawler.db` full offers catalog:

    python runner.py store

To crawl recent listings and detect which cars were sold (and notify sellers), executed every 10 minutes:

    python runner.py detect -s 10
