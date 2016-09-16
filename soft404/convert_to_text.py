#!/usr/bin/env python
import argparse
import json
import gzip
import multiprocessing

import json_lines
import langdetect
from langdetect.lang_detect_exception import LangDetectException
import tldextract

from soft404.utils import cleaned_selector, selector_to_text, get_text_blocks


def convert_item(item):
    try:
        sel = cleaned_selector(item.pop('html'))
        text = selector_to_text(sel)
        text_item = {
            'url': item['url'],
            'domain': get_domain(item['url']),
            'text': text,
            'title': ' '.join(sel.xpath('/html/head/title//text()').extract()),
            'status': item['status'],
            'lang': get_lang(text),
        }
        body = sel.xpath('/html/body')
        if body:
            text_item['blocks'] = get_text_blocks(body[0].root)
    except Exception:
        return None
    else:
        return text_item


def get_domain(url):
    return tldextract.extract(url).registered_domain.lower()


def get_lang(text):
    try:
        return langdetect.detect_langs(text)[0].lang
    except LangDetectException:
        return ''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='Pages in .jl.gz')
    parser.add_argument(
        'out_prefix',
        help='Output prefix (two files are written: one with'
             'full data and one with meta: status, url, domain, lang)')
    args = parser.parse_args()

    with json_lines.open(args.infile, broken=True) as f:
        items_file = gzip.open(args.out_prefix + '.items.jl.gz', 'wt')
        meta_file = gzip.open(args.out_prefix + '.meta.jl.gz', 'wt')
        n_errors = 0
        with multiprocessing.Pool() as pool:
            for text_item in pool.imap_unordered(
                    convert_item, f, chunksize=500):
                if text_item is None:
                    n_errors += 1
                else:
                    items_file.write(json.dumps(text_item))
                    items_file.write('\n')
                    meta_file.write(json.dumps({key: text_item[key] for key in [
                        'url', 'domain', 'lang', 'status']}))
                    meta_file.write('\n')

    print('Number of errors: {}'.format(n_errors))


if __name__ == '__main__':
    main()