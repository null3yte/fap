<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a>
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
usage: fap [-h] [-u URL] [-f FILE]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     scheme://domain.tld/path
  -f FILE, --file FILE  URLs file path
```
