#!/usr/bin/env python

# takes as input one or more 750 Words export file(s), outputs a LaTeX file on stdout
# usage: 750book-latex.py INPUT[..]

from mako.template import Template
from datetime import datetime
import sys, re, calendar, math


# based off http://stackoverflow.com/questions/2541616/how-to-escape-strip-special-characters-in-the-latex-document/5422751#5422751
latex_substitutions = {
    "#": "\\#",
    "$": "\\$",
    "%": "\\%",
    "&": "\\&",
    "~": "\\~{}",
    "_": "\\_",
    "^": "\\^{}",
    "\\":"\\textbackslash ",
    "{": "\\{",
    "}": "\\}",
}
latex_re = re.compile("([\^\%~\\\\#\$%&_\{\}])")

def sanitize_latex(s):
    global latex_substitutions, latex_re
    return latex_re.sub(lambda m: latex_substitutions[m.group(1)], s)


def main():

    global template

    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s INPUT[..] OUTPUT" % (sys.argv[0]))
        sys.exit(1)

    inputs = sys.argv[1:]
    # XXX TODO output to last arg is bad, runs risk of stomping on things; use getopt!
    # XXX TODO output to other than STDOUT
    output = sys.stdout

    # apparently sometimes the export doesn't include values for num_minutes
    raw_entry_header_re = re.compile('##### ENTRY ##### ([-\d]+), num_words:(\d+), num_minutes:([.\d]+)?')
    raw_entries = []
    for filename in inputs:
        f = open(filename)
        raw_entry = None
        for raw_l in f:
            # FORCE UTF-8
            # XXX TODO given that I'm forcing this, do I want to switch to xetex?
            l = unicode(raw_l, 'utf-8')
            match = raw_entry_header_re.match(l)
            if match:
                if raw_entry:
                    raw_entry['text'] = sanitize_latex(raw_entry['text'])
                    raw_entries.append(raw_entry)
                # match.groups() doesn't include match.group(0)
                # 0 means the time to 750 went unrecorded, ie. you didn't hit 750 words
                time = len(match.groups()) > 2 and match.group(3) or 0
                raw_entry = { 'date': match.group(1), 'words': match.group(2), 'time': time, 'text': '' }
            else:
                if raw_entry:
                    raw_entry['text'] += l
                else:
                    sys.stderr.write("Unexpected leading data; file corrupt.\n")
                    sys.exit(1)

    entries = process_raw_entries(raw_entries)

    data = { 'title': "750 Words Morning Pages",
            'author': "Kevin Riggle",
            'date_string': 'June 2011 - August 2011',
            'entries': entries,
    }

    compiled_template = Template(template)
    # another place to force UTF-8
    output.write(compiled_template.render_unicode(**data).encode('utf-8'))


class Year(list):
    def __init__(self, year, months):
        list.__init__(self, months)
        self._year = year

    def __str__(self):
        return self._year

class Month(list):
    def __init__(self, month, entries):
        list.__init__(self, entries)
        self._month = month

    def __str__(self):
        return self._month

def process_raw_entries(raw_entries):
    # first level is decimal year, second is decimal month, third is list of entries
    working_entries = {}
    for raw_entry in raw_entries:
        working_entry = {}
        working_entry['text'] = raw_entry['text']
        working_entry['words'] = raw_entry['words']

        # parsed_date gets used later on, it's not just wanking
        parsed_date = datetime.strptime(raw_entry['date'], '%Y-%m-%d')
        working_entry['date'] = parsed_date.strftime('%A, %B %d, %Y')
        # stash parsed_date for sorting
        working_entry['parsed_date'] = parsed_date

        parsed_time = float(raw_entry['time'])  #really a duration, but datetime.timedelta is overkill
        hours = int(parsed_time / 60)
        minutes = int(math.ceil( parsed_time - (hours * 60) ))
        # 0 means the time to 750 went unrecorded, ie. you didn't hit 750 words
        if parsed_time == 0:
            working_entry['time'] = 'unrecorded'
        elif hours == 1:
            working_entry['time'] = "1 hour, %d minutes" % (minutes,)
        elif hours > 1:
            working_entry['time'] = "%d hours, %d minutes" % (hours, minutes)
        else:
            working_entry['time'] = "%d minutes" % (minutes,)

        year = parsed_date.year
        month = parsed_date.month
        if not year in working_entries:
            working_entries[year] = {}
        if not month in working_entries[year]:
            working_entries[year][month] = []
        working_entries[year][month].append(working_entry)

    # though we might, it's better not to trust input order, so we sort everything ourselves
    working_years = working_entries.keys()
    working_years.sort()
    years = []
    for working_year in working_years:
        formatted_year = "%d" % (working_year,)
        working_months = working_entries[working_year].keys()
        working_months.sort()
        months = []
        for working_month in working_months:
            formatted_month = "%s %d" % (calendar.month_name[working_month], working_year)
            entries = working_entries[working_year][working_month]
            entries.sort(key=lambda x: x['parsed_date'])
            months.append(Month(formatted_month, entries))

        years.append(Year(formatted_year, months))

    return years



template = """%%% LaTeX autogenerated by 750book-latex.py; do not hand-modify!

%% memoir class in 10 points, statement paper size (aka digest size, 8.5in x 5.5in)
\documentclass[10pt,statementpaper]{memoir}

%% frobs to provide
%% Title:, Author:
%% when given multiple files, output: single file, one file per year, one file per month
%% include statistics?
%% optimize for: screen, print
%% font size: normal, large
%% ?? attitude: informal, formal  (I'd prefer to get this Just Right)
%% font: serif, sans-serif


\\parindent0pt  \\parskip10pt             %% make block paragraphs (same 10pt as font size)
\\OnehalfSpacing                        %% a bit of extra leading between lines for readability and 750-consistency
\\raggedright                            %% do not right justify
\\renewcommand{\\familydefault}{\\sfdefault}    %% use sans-serif fonts
\\renewcommand{\\sfdefault}{phv}                %% specifically, Helvetica, since 750 Words uses it

\\setsecnumdepth{none}

\\pagestyle{headings}
\\nouppercaseheads
%% XXX TODO add the author's name to the recto heading
%% XXX TODO move the page number to the footer on all pages

\\renewcommand{\\cftchapterdotsep}{\\cftdotsep}

%% XXX TODO redefine epigraph so I don't need to use the source field
%%\\setlength{\\epigraphrule}{0pt}          %% no rule separating the (nonexistent) epigraph source


\\title{${title}}
\\author{${author}}
\date{${date_string}}

\\begin{document}                        %% End of preamble, start of text.

%%% title page
\pagestyle{empty}
%% center relative to page rather than typeblock
\calccentering{\\unitlength}
\\begin{adjustwidth*}{\\unitlength}{-\\unitlength}
    \\null\\vfil     %% vertically center the title
    {\\begin{center}\\Huge \\bfseries \\thetitle \\par\\end{center}\\vskip 0.5em}
    {\\begin{center} 
        \\huge \\bfseries \\lineskip 0.5em%% 
        \\begin{tabular}[t]{c} \\theauthor \\end{tabular}\\par\\end{center}}
    {\\begin{center}\\huge \\bfseries \\thedate \\par\\end{center}}
    \\vfil
\end{adjustwidth*}
\cleardoublepage

\\frontmatter                            %% only in book class (roman page #s)
%%% table of contents
\\tableofcontents*                       %% Print table of contents

%%% entries
\mainmatter                             %% only in book class (arabic page #s)

% for year in entries:
## only print the year when there are multiple years in the book
${len(entries) == 1 and '%%' or ''}\\book{${year}}

%   for month in year:
## always print the month, even when there's only one month in the book
\\part{${month}}

%       for entry in month:
\chapter{${entry['date']}}
${entry['text']}
\epigraph{}{Words: ${entry['words']} \\\\ Total time: ${entry['time']}}
%       endfor

%   endfor
% endfor
 
\end{document}                          %% The required last line
"""


if __name__ == '__main__': main()
