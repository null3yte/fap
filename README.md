<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#examples">Examples</a>
</p>
<p align="center">FAP is a tool for collecting web keywords to create a custom wordlist for fuzzing any desired site.</p>

## Installation

```bash
git clone https://github.com/null3yte/fap.git
cd fap
python setup.py install
```

## Usage

```bash
fap -h
```

This will display help for the tool.

```
usage: fap.py [-h] [-u URL] [-f FILE] [-t THREAD]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     scheme://domain.tld/path
  -f FILE, --file FILE  URLs file path
  -t THREAD, --thread THREAD
                        maximum number of threads to use (default: 4)
```

### Examples

1. Extract keywords from a single URL:

```bash
fap -u https://www.google.com/
```

2. Extract keywords from multiple URLs

```bash
fap -f urls.txt -t 8
```
