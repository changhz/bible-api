import sys
import json
import codecs

from pprint import pprint
from getopt import getopt
from getopt import error


def parse_arg_verses(s):
    ls = s.split(',')
    verses = []
    for x in ls:
        if x.isdigit():
            verses.append(int(x))
        else:
            x = x.split('-')
            x = [int(n) for n in x if n.isdigit()]
            if len(x) > 0:
                for n in range(x[0], x[1] + 1):
                    verses.append(n)
    return verses


arg_book = 'John'
arg_chpt = '1'
arg_verses = ''
arg_version = "zh_cuv"

arg_list = sys.argv[1:]
unix_options = "b:c:v:u:"
gnu_options = ["book=", "chapter=", "verses=", "version="]

try:
    arguments, values = getopt(arg_list, unix_options, gnu_options)
except error as err:
    # output error, and return with an error code
    print(str(err))
    sys.exit(2)

for k, v in arguments:
    if k in ('-b', '--book'):
        arg_book = v
    elif k in ('-c', '--chapter'):
        arg_chpt = v
    elif k in ('-v', '--verses'):
        arg_verses = v
    elif k in ('-u', '--version'):
        arg_version = v

verse_num_list = parse_arg_verses(arg_verses)

# pprint(verse_num_list)

print("Book of %s chapter %s (%s)" %
      (arg_book, arg_chpt, arg_version))

src_path = "/Users/honzungchang/GitRepo/bible/json/"

filename = src_path + arg_version + '.json'

with open('./book_abbrevs.json') as f:
    book_abbrevs = json.load(f)
with open('./book_names.json') as f:
    book_names = json.load(f)


def main():
    try:
        c = codecs.open(filename, 'r', 'utf-8-sig')
    except:
        print("Error: no such version '%s'" % arg_version)
        return
    bible = json.load(c)

    # for book in bible:
    #     pprint(book['abbrev'])

    ind = -1
    if arg_book in book_abbrevs:
        ind = book_abbrevs.index(arg_book)
    if arg_book in book_names:
        ind = book_names.index(arg_book)

    if ind == -1:
        print("Error: no such book '%s'" % arg_book)
        return

    book = bible[ind]  # keys: abbrev, chapters, name
    chapters = book['chapters']

    n_chapter = int(arg_chpt) - 1

    if n_chapter < 0 or n_chapter > len(chapters):
        print("Error: no such chapter %s" % arg_chpt)
        return

    verses = chapters[n_chapter]
    if len(verse_num_list) == 0:
        for n, s in enumerate(verses):
            print("%s\t%s" % (n, s))
    else:
        for n in verse_num_list:
            if n-1 >= 0 and n-1 <= len(verses):
                print("%s\t%s" % (n, verses[n - 1]))
    return


if __name__ == "__main__":
    main()
    pass
