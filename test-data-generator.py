#!/usr/bin/env python

import sys, lipsum, random, optparse
from datetime import datetime

lipgen = lipsum.Generator()
def do_lorem(words):
    global lipgen

    my_words = 0
    lipsum_block = ''
    while my_words < words:
        if words == 0:
            lipsum_para = lipgen.generate_paragraph(start_with_lorem=True)
        else:
            lipsum_para = lipgen.generate_paragraph(start_with_lorem=False)

        lipsum_words_list = lipsum_para.split(' ')
        lipsum_words = len(lipsum_words_list)
        if lipsum_words + my_words > words:
            new_words = words - my_words
            lipsum_block += "\n"
            lipsum_block += ' '.join(lipsum_words_list[:new_words])
            lipsum_block += '...'
            my_words += new_words
        else:
            lipsum_block += "\n"
            lipsum_block += lipsum_para
            my_words += lipsum_words
    
    return lipsum_block


# generate_day(DateTime)
def generate_day(date):
    words = int(random.random() * 5000)
    minutes = random.random() * 1440    # minutes in a day = 24 * 60
    day_block = ''
    # no blank lines between entries
    day_block += "##### ENTRY ##### %s, num_words:%d, num_minutes:%f" % (date.isoformat(), words, minutes)
    day_block += do_lorem(words)
    return day_block


def main():
    # TODO other options: --missed (# of missed days in period)
    # TODO other options: --unfinished (# of started but unfinished days in period)
    # TODO other options: mean+dev of # words
    # TODO other options: mean+dev of # paras (test single-para)
    # TODO other options: mean+dev of times taken
    # TODO other options: include weirdnesses (??)
    # TODO other options: include Unicode (!!)
    # TODO other options: DUH output to file; no input files, so any remaining arg is output?
    from_str = None
    to_str = None
    usage = "Usage: %prog --from DATE [--to DATE]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-1', '--from', dest=from_str, help='beginning of range, inclusive', metavar='YYYY-MM-DD')
    parser.add_option('-2', '--to', dest=to_str, help='end of range, inclusive', metavar='YYYY-MM-DD')

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    print options

    if not 'from' in options:
        sys.stderr.write("--from option is required\n")
        parser.print_help()
        sys.exit(1)

    from_date = datetime.strptime(from_str, '%Y-%m-%d')
    to_date = None
    if 'to' in options:
        to_date = datetime.strptime(to_str, '%Y-%m-%d')
    # XXX TODO DateTime implements inc, right? ^^;;
    #while (++$from != $to):
        #generate_day(from_date)


if __name__ == '__main__': main()
