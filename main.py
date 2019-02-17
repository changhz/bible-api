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


arg_book = ''
arg_chpt = ''
arg_verses = ''
arg_version = 'zh_cuv'

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

src_path = "/Users/honzungchang/GitRepo/bible/json/"

filename = src_path + arg_version + '.json'

with open('./book_abbrevs.json') as f:
    book_abbrevs = json.load(f)
with open('./book_names.json') as f:
    book_names = json.load(f)

if arg_book == '':
    print(
        "Usage: bible --book=name [--chapter=1] [--verses=1,2,7,8-20] [--version=zh_cuv]")
    print("Please select a book:")
    for i, book in enumerate(book_names):
        sys.stdout.write(book + ' (' + book_abbrevs[i] + ')' + ' | ')
    print()
    sys.exit(0)


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

    if arg_chpt == '':
        print("Please select a chapter (1 to %s)" % len(chapters))
        return

    selected_book_name = book_names[ind]
    print("Book of %s chapter %s (%s)" %
          (selected_book_name, arg_chpt, arg_version))

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
