import json
import codecs
from pprint import pprint

ver = "zh_cuv"

src_path = "/Users/honzungchang/GitRepo/bible/json/"

filename = src_path + ver + '.json'

with open('./book_abbrevs.json') as f:
    book_abbrevs = json.load(f)
with open('./book_names.json') as f:
    book_names = json.load(f)


def main():
    c = codecs.open(filename, 'r', 'utf-8-sig')
    bible = json.load(c)

    # for book in bible:
    #     pprint(book['abbrev'])

    book = bible[book_abbrevs.index('gn')]  # keys: abbrev, chapters, name
    chapters = book['chapters']
    pprint(chapters[0][1])
    return


if __name__ == "__main__":
    main()
    pass
