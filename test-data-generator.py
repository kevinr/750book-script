#!/usr/bin/env python

import sys, lipsum, random, optparse
from datetime import datetime, timedelta

lipgen = lipsum.Generator()
def do_lorem(words):
    global lipgen

    my_words = 0
    lipsum_block = ''
    while my_words < words:
        if my_words == 0:
            # header prints its own newline
            lipsum_para = lipgen.generate_paragraph(start_with_lorem=True)
        else:
            # subsequent paras get an empty line
            lipsum_block += "\n"
            lipsum_para = lipgen.generate_paragraph(start_with_lorem=False)

        lipsum_words_list = lipsum_para.split(' ')
        lipsum_words = len(lipsum_words_list)
        if lipsum_words + my_words > words:
            new_words = words - my_words
            lipsum_block += ' '.join(lipsum_words_list[:new_words])
            lipsum_block += "...\n"
            my_words += new_words
        else:
            lipsum_block += lipsum_para + "\n"
            my_words += lipsum_words
    
    return lipsum_block


# generate_day(DateTime)
def generate_day(date):
    words = int(random.random() * 2500)
    minutes = random.random() * 1440    # minutes in a day = 24 * 60
    day_block = ''
    # no blank lines between entries
    day_block += "##### ENTRY ##### %s, num_words:%d, num_minutes:%f\n" % (date.strftime('%Y-%m-%d'), words, minutes)
    day_block += do_lorem(words)
    return day_block


def main():
    # TODO other options: --missed (# of missed days in period)
    # TODO other options: --unfinished (# of started but unfinished days in period)
    # TODO other options: mean+dev of # words
    # TODO other options: mean+dev of # paras (test single-para)
    # TODO other options: mean+dev of times taken
    # TODO other options: include weirdnesses (??)
    # TODO other options: time can be in expn notation, eg. num_minutes:2.74976e-06
    # TODO other options: include Unicode (!!)
    usage = "Usage: %prog --from DATE [--to DATE]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-1', '--from', help='beginning of range, inclusive (required)', metavar='YYYY-MM-DD')
    parser.add_option('-2', '--to', help='end of range, inclusive', metavar='YYYY-MM-DD')
    parser.add_option('-o', '--output', help='output to file', metavar='FILE')

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()

    output_file = getattr(options, 'output')
    if not output_file:
        output = sys.stdout
    else:
        output = open(output_file, 'w')

    from_str = getattr(options, 'from')
    if not from_str:
        sys.stderr.write("--from option is required\n")
        parser.print_help()
        sys.exit(1)

    from_date = datetime.strptime(from_str, '%Y-%m-%d')
    to_str = getattr(options, 'to')
    to_date = None
    if to_str:
        to_date = datetime.strptime(to_str, '%Y-%m-%d')
    else:
        to_date = from_date

    day = timedelta(days=1)
    while from_date <= to_date:
        output.write(generate_day(from_date))
        from_date += day


if __name__ == '__main__': main()
