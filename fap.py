#!/usr/bin/env python
import argparse
import re
import asyncio
import httpx
from lxml import html
from urllib.parse import urlparse, parse_qs


async def extractor(url: str) -> set:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        content = response.text
        tree = html.fromstring(content)

        keywords = set()
        if response.status_code == 200:
            keywords.update(tree.xpath('//*[@id]/@id'))
            keywords.update(tree.xpath('//*[@name]/@name'))

            for var in tree.xpath('//script[contains(text(), "var ")]'):
                vars_list = re.findall(r'var\s+(\w+)', var.text)
                keywords.update(vars_list)

            # Extract parameter names
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            param_names = query_params.keys()
            keywords.update(param_names)

        else:
            print(f"status code: {response.status_code}")

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
        keywords = await extractor(url)
    elif urls:
        with open(urls, "r") as f:
            urls_list = [url.strip() for url in f.readlines()]
            tasks = [extractor(url) for url in urls_list]
            results = await asyncio.gather(*tasks)
            for result in results:
                keywords.update(result)

    for keyword in keywords:
        print(keyword)


if __name__ == '__main__':
    asyncio.run(main())
