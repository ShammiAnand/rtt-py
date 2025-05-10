# rtt

`rtt` is a cli application which allows you to convert a repository of code/files
and webpages into flat files (both `txt` and `md` formats are supported) and
interact with LLMs all using one CLI

## Installation

```bash
pip install rtt-py
```

## Usage

```bash

rtt-py --help

rtt-py query https://ssi.inc --type url --query "what does this company do?"

rtt-py query /path/to/repo --type dir --query "what does this repo do?"

rtt-py process /path/to/repo --type dir  # process the repo and save it to a flat file

rtt-py process https://ssi.inc --type url  # process the url and save it to a flat file


```

## Author

[@shammianand](https://www.github.com/shammianand)
