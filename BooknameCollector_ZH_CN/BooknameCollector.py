# -*- coding: utf-8 -*-

import re, os, sys
from collections import OrderedDict

# Configure how many times the book should be mentioned if the book info. be printed
BOOK_MENTION_MIN_TIMES = 4

booknames = OrderedDict()
book_mention_times = []

fns = sys.argv[1:]

# Problme: Bookname mentioned more than once should be taken into consideration
for fn in fns:
    file = open(fn, encoding = 'utf-8')
    for line in file:
        for name in re.compile('《.*?》').findall(line):
            book_ori = booknames.get(name, ('', 0))
            booknames[name] = (book_ori[0] + '\n' + line, book_ori[1] + 1)
for key in booknames:
    book_mention_times.append(booknames[key][1])
print('# Book mentioned times: ')
print(list(reversed(sorted(book_mention_times))))
for key in booknames:
    if booknames[key][1] >= BOOK_MENTION_MIN_TIMES:
        print(key, '[{}]'.format(booknames[key][1]))
        print(booknames[key][0])
