import sys
import json
import codecs
import os

from pprint import pprint
from getopt import getopt
from getopt import error

# cwd = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))


def parse_arg_verses(s):
    ls = s.split(',')
    verses = []
    for x in ls:
        if x.isdigit():
            verses.append(int(x))
        else:
            x = x.split('-')
            if x[0].isdigit() and x[1].isdigit():
                x = [int(n) for n in x]
                for n in range(x[0], x[1] + 1):
                    verses.append(n)
            elif x[0].isdigit() and not x[1].isdigit():
                verses.append(int(x[0]))
    return verses


def print_verse(n, s, l):
    if l == 0:
        sys.stdout.write("[%s] %s" % (n, s))
    else:
        print("[%s] %s" % (n, s))
        print()


arg_l = 0
arg_b = 0
arg_book = ''
arg_chpt = ''
arg_version = 'zh_cuv'

arg_list = sys.argv[1:]
unix_options = "lbv:"
gnu_options = ["list", "books", "version="]

try:
    arguments, values = getopt(arg_list, unix_options, gnu_options)

    if len(values) > 0:
        arg_book = values[0]
    if len(values) > 1:
        arg_chpt = values[1]

except error as err:
    print(str(err))
    sys.exit(2)

for k, v in arguments:
    if k in ('-l', '--list'):
        arg_l = 1
    if k in ('-b', '--books'):
        arg_b = 1
    elif k in ('-v', '--version'):
        arg_version = v

with open(dir_path + '/book_abbrevs.json') as f:
    book_abbrevs = json.load(f)
with open(dir_path + '/book_names.json') as f:
    book_names = json.load(f)

if arg_b == 1:
    for i, book in enumerate(book_names):
        # sys.stdout.write(book + ' (' + book_abbrevs[i] + ')' + ' | ')
        print(str(i+1) + ' ------- ' + book + ' (' + book_abbrevs[i] + ')')
    print()
    sys.exit(0)

if arg_book == '':
    print(
        "Usage: bible [--list] [--books] [-v version] book chapter:verses")
    sys.exit(0)

src_path = dir_path + "/_data"

filename = src_path + '/' + arg_version + '.json'

try:
    c = codecs.open(filename, 'r', 'utf-8-sig')
except:
    print("Error: no such version '%s'" % arg_version)
    sys.exit(2)

bible = json.load(c)

ind = -1
if arg_book in book_abbrevs:
    ind = book_abbrevs.index(arg_book)
if arg_book in book_names:
    ind = book_names.index(arg_book)

if ind == -1:
    print("Error: no such book '%s'" % arg_book)
    sys.exit(2)

book = bible[ind]  # keys: abbrev, chapters, name
chapters = book['chapters']

if arg_chpt == '':
    print("Please select a chapter (1 to %s)" % len(chapters))
    sys.exit(0)

verse_num_list = []

chpt = arg_chpt.split(':')
if len(chpt) > 1:
    verse_num_list = parse_arg_verses(chpt[1])

selected_book_name = book_names[ind]
# print("Book of %s (%s)\nChapter %s" %
#       (selected_book_name, arg_version, chpt[0]))
# print()

if not chpt[0].isdigit():
    print("Error: invalid chapter")
    sys.exit(1)

n_chapter = int(chpt[0]) - 1

if n_chapter < 0 or n_chapter > len(chapters):
    print("Error: no such chapter %s" % chpt[0])
    sys.exit(2)

verses = chapters[n_chapter]
if len(verse_num_list) == 0:
    for n, s in enumerate(verses):
        print_verse(n+1, s, arg_l)
    print()
else:
    for n in verse_num_list:
        if n-1 >= 0 and n-1 < len(verses):
            print_verse(n, verses[n-1], arg_l)
    print()


if __name__ == "__main__":
    pass
