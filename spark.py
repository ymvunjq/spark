#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
spark
https://github.com/ymvunjq/spark

Usefull to graph some data

    $ spark.py 1 2 3 4 5 6
     _▁▃▄▆█

    $ spark.py -s 10 -H 1 3 7 10 2 0
    █ 1
    ███ 3
    ███████ 7
    ██████████ 10
    ██ 2
    ▏ 0

    $ du -bs * | awk -F'\t' '{print $2":"$1}' | spark.py -H -s 10
    file_10k █▉ 10240
     file_1k ▏ 1024
    file_25k ████▉ 25600
     file_4k ▋ 4096
    file_50k ██████████ 51200


Inspired by https://github.com/holman/spark with few more things
"""

# Depending on font used, sprites can be bad displayed
# Feel free to adapt vertical or horizontal sprites for your font
# With DejaVu Sans Mono:style=regular:pixelsize=11, sprites are perfectly displayed

# Vertical sprites
spritev = list(u'_▁▂▃▄▅▆▇█')

# Horizontal sprites
spriteh = list(u"▏" \
               u"▎" \
               u"▍" \
               u"▌" \
               u"▋" \
               u"▊" \
               u"▉" \
               u"█")


def scaled(numbers,scale,start_zero=False):
    """ Return scaled numbers : lowest number will be 0, highest number will be scale
        if start_zero is set to true, then lowest value will be 0 (except is lowest number
        is lower than 0) """
    if len(numbers) == 0:
        return []

    if start_zero:
        min_value = min(0,min(numbers))
    else:
        min_value = min(numbers)
    max_value = max(numbers)
    value_scale = max_value - min_value

    if value_scale == 0:
        return [0]*len(numbers)

    return map(lambda x: int(((x-min_value)*(float(scale)-1.0))/value_scale),numbers)

def spark_values(numbers,ln,char=1,start_zero=False):
    """ Return matrix of scaled values """
    out = []
    sc = scaled(numbers,ln*char,start_zero)
    for i in xrange(char):
        l = []
        for n in sc:
            if n/ln == i:
                l.append(n%ln)
            elif n/ln > i:
                l.append(ln-1)
            else:
                l.append(None)
        out.append(l)
    return out

def spark(numbers,horizontal=True,char=1,start_zero=False):
    """ Return array of sprites to display """
    numbers = map(float,numbers)
    if horizontal:
        sp = spark_values(numbers,len(spriteh),char,start_zero)
        return ["".join([spriteh[x] if not x is None else "" for x in l]) for l in zip(*sp)]
    else:
        sp = spark_values(numbers,len(spritev),char,zero)
        return list(reversed(["".join([spritev[x] if not x is None else " " for x in l]) for l in sp]))


if __name__ == "__main__":
    import sys
    import re
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("data",metavar="INTEGERS",nargs="*")
    parser.add_argument("--horizontal","-H",action="store_true")
    parser.add_argument("--size","-s",metavar="SIZE",type=int,default=1)
    parser.add_argument("--regex","-r",metavar="REGEXP",default=None)
    parser.add_argument("--no-title",action="store_true",help="Do not display title in horizontal display")
    parser.add_argument("--no-value",action="store_true",help="Do not display value in horizontal display")
    parser.add_argument("-z","--zero",action="store_true",help="Start at 0 instead of lowest numbers value")
    args = parser.parse_args()

    numbers = []
    title = None

    if len(args.data) > 0:
        numbers = args.data
    else:
        if args.regex is None:
            v = sys.stdin.readlines()
            if len(v) == 1:
                v = v[0].split(" ")
            if len(v) > 0 and ":" in v[0]:
                title = []
                for e in v:
                    try:
                        name,value = e.split(":")
                    except ValueError:
                        print "Bad input value"
                        sys.exit(0)
                    numbers.append(value)
                    title.append(name)
            else:
                numbers = v
        else:
            pattern = re.compile(args.regex)
            title = []
            for v in sys.stdin.readlines():
                m = pattern.search(v)
                numbers.append(m.group("value"))
                title.append(m.group("name"))

    if not title is None:
        smax = len(max(title,key=len))

    s = u''
    sp = spark(numbers,args.horizontal,args.size,args.zero)
    for i in xrange(len(sp)):
        if args.horizontal and not title is None and not args.no_title:
            s = s + title[i].rjust(smax," ") + " "
        s = s + sp[i]
        if args.horizontal and not args.no_value:
            s = s + " " + str(numbers[i]).rstrip("\n")
        s = s + "\n"

    # Important when pipe to a program
    print s.rstrip("\n").encode("utf-8")
