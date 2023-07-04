#!/usr/bin/env python
import argparse
import concurrent.futures
import re
import asyncio
import aiohttp
from lxml import html


async def extractor(url: str) -> set:
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


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='scheme://domain.tld/path')
    parser.add_argument('-f', '--file', type=str, help='URLs file path')
    parser.add_argument('-t', '--thread', type=int, default=4, help='maximum number of threads to use (default: 4)')

    args = parser.parse_args()
    url = args.url
    urls = args.file
    thread = args.thread

    keywords = set()
    if url:
        keywords = await extractor(url)
    elif urls:
        with open(urls, "r") as f:
            urls_list = [url.strip() for url in f.readlines()]
            with concurrent.futures.ThreadPoolExecutor(thread) as executor:
                tasks = [asyncio.create_task(extractor(url)) for url in urls_list]
                for coro in asyncio.as_completed(tasks):
                    result = await coro
                    keywords.update(result)

    for keyword in keywords:
        print(keyword)


if __name__ == '__main__':
    asyncio.run(main())
