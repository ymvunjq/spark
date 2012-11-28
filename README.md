spark
=====

Inspired by https://github.com/holman/spark, with few more functionalities I needed.

## Usage

Data can be passed in command line :

    $ spark.py 1 2 3 4 5 6
    _▁▃▄▆█

Or with standard input :

    $ echo 0 10 20 30 40 50 | spark.py
    _▁▃▄▆█

By default vertical display is used, but with `-H` option, horizontal display can be selected.

    $ spark.py -H 1 3 7 10 2 0
    ▏ 1
    ▍ 3
    ▋ 7
    █ 10
    ▎ 2
    ▏ 0


Number of characters used to display data can be choosen with `-s` option.

    $ spark.py -s 10 -H 1 3 7 10 2 0
    █ 1
    ███ 3
    ███████ 7
    ██████████ 10
    ██ 2
    ▏ 0

Or in vertical

    $ spark.py -s 10 1 3 7 10 2 0
       █  
       █  
       █  
      ██  
      ██  
      ██  
      ██  
     ███  
     ████ 
    █████_


If input contains a `:` first part is considered as name and the other as size.

    $ du -bs * | awk -F'\t' '{print $2":"$1}' | spark -H -s 10
    file_10k █▉ 10240
     file_1k ▏ 1024
    file_25k ████▉ 25600
     file_4k ▋ 4096
    file_50k ██████████ 51200


The same output can be generated with a python regular expression

    $ du -bs * | spark -H -s 10 -r "(?P<value>\d+)\s+(?P<name>.*)"
    file_10k █▉ 10240
     file_1k ▏ 1024
    file_25k ████▉ 25600
     file_4k ▋ 4096
    file_50k ██████████ 51200
    
## Bad Display

Depending on the font you are using, graph can be perfect or ugly... On github Readme vertical graph are ugly. My .Xdefault contains `URxvt*font: xft:DejaVu Sans Mono:style=regular:pixelsize=11` and graph are nice.
You can change `spritev` and `spriteh` variables in code to adapt sprites to your font configuration.