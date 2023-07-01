#!/usr/bin/env python
import argparse
import re
import requests
from bs4 import BeautifulSoup
import sys

def single(url: str) -> set:
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')

    keywords = set()
    if response.status_code == 200:
        for tag in soup.find_all(re.compile(r'.*'), {'id': True}):
            keywords.add(tag['id'])

        for tag in soup.find_all(re.compile(r'.*'), {'name': True}):
            keywords.add(tag['name'])

        for var in soup.find_all('script', string=re.compile(r'var\s+\w+')):
            vars_list = re.findall(r'var\s+(\w+)', var.text)
            keywords.update(vars_list)
    else:
        print(f"status code: {response.status_code}")
    return keywords


def mass(url: str) -> set:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    keywords = set()

    if response.status_code == 200:
        for element in soup.find_all(['input', 'select']):
            if element.get('name'):
                keywords.add(element['name'])
            if element.get('id'):
                keywords.add(element['id'])

        script_tags = soup.find_all('script', string=re.compile(r'var\s+\w+'))
        for tag in script_tags:
            variables = re.findall(r'var\s+(\w+)', tag.string)
            keywords.update(variables)
    else:
        print(f"status code {response.status_code}: {url}")
        sys.exit(0)
    return keywords


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='scheme://domain.tld/path')
    parser.add_argument('-f', '--file', type=str, help='URLs file path')

    args = parser.parse_args()
    url = args.url
    urls = args.file

    if url:
        for keyword in single(url):
            print(keyword)
    elif urls:
        keywords = set()
        with open(urls, "r") as f:
            for line in f:
                url_keywords = mass(line.strip())
                for keyword in url_keywords:
                    keywords.add(keyword)
        for keyword in keywords:
            print(keyword)


if __name__ == '__main__':
    main()
