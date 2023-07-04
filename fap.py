#!/usr/bin/env python
import argparse
import re
import asyncio
import aiohttp
from lxml import html


async def single(url: str) -> set:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
            tree = html.fromstring(content)

            keywords = set()
            if response.status == 200:
                keywords.update(tree.xpath('//*[@id]/@id'))
                keywords.update(tree.xpath('//*[@name]/@name'))

                for var in tree.xpath('//script[contains(text(), "var ")]'):
                    vars_list = re.findall(r'var\s+(\w+)', var.text)
                    keywords.update(vars_list)
            else:
                print(f"status code: {response.status}")
            return keywords


async def mass(url: str) -> set:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
            tree = html.fromstring(content)

            keywords = set()
            if response.status == 200:
                for element in tree.xpath('//input[@name] | //select[@name]'):
                    keywords.add(element.get('name'))
                    keywords.add(element.get('id'))

                for var in tree.xpath('//script[contains(text(), "var ")]'):
                    vars_list = re.findall(r'var\s+(\w+)', var.text)
                    keywords.update(vars_list)
            return keywords


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='scheme://domain.tld/path')
    parser.add_argument('-f', '--file', type=str, help='URLs file path')

    args = parser.parse_args()
    url = args.url
    urls = args.file

    keywords = set()
    if url:
        keywords = await single(url)
    elif urls:
        async with aiohttp.ClientSession() as session:
            with open(urls, "r") as f:
                tasks = []
                for line in f:
                    tasks.append(mass(line.strip()))
                results = await asyncio.gather(*tasks)
                for result in results:
                    keywords.update(result)

    for keyword in keywords:
        print(keyword)


if __name__ == '__main__':
    asyncio.run(main())
