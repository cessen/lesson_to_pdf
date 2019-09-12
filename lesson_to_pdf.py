#!/usr/bin/env python3

import sys
import os
import subprocess
import string
import random


CSS_STYLE = """
body {
    font-family: sans-serif;
    margin: 0.5cm 1cm 0.5cm 1cm;
    font-size: 12pt;
}

header {
    display: none;
}

h1 {
    margin-top: 0;
    margin-bottom: 1.2em;
    font-size: 2em;
    text-align: center;
}

h2 {
    font-size: 1.4em;
    margin-top: 2em;
}

hr {
    display: none;
}

div#header {
    display: flex;
    padding: 0.5em 0.5em 0.5em 0.5em;
    border-top: 2px solid #AAA;
    border-bottom: 2px solid #AAA;
}

div#header h2 {
    margin-top: 0.5em;
    margin-left: 0.5em;
    margin-right: 0.5em;
}

div#header div {
    width: 50%;
    padding: 0;
    margin: 0;
}

li {
    margin-top: 0.5em;
    margin-bottom: 0em;
}
"""


if __name__ == "__main__":
    for md_filename in sys.argv[1:]:
        if not md_filename.endswith(".md"):
            print("Warning: '{}' doesn't appear to be a markdown file. Skipping.".format(md_filename))
            continue
        else:
            print("Processing '{}'".format(md_filename))

        pdf_filename = md_filename.rsplit(".")[0] + ".pdf"
        tmp_filename_base = ''.join(
            random.choices(
                string.ascii_lowercase + string.ascii_uppercase + string.digits,
                k=16)
            )
        tmp_md_filename = tmp_filename_base + ".md"
        tmp_html_filename = tmp_filename_base + ".html"

        # Create a modified md file
        with open(tmp_md_filename, 'w') as mod_md_file:
            with open(md_filename) as md_file:
                state = 0
                for line in md_file:
                    if line.startswith("---") and state == 0:
                        mod_md_file.write('<div id="header"><div>\n')
                        state += 1
                    elif line.startswith("## ") and state == 1:
                        mod_md_file.write(line)
                        state +=1
                    elif line.startswith("## ") and state == 2:
                        mod_md_file.write("</div><div>\n")
                        mod_md_file.write(line)
                        state +=1
                    elif line.startswith("---") and state == 3:
                        mod_md_file.write('</div></div>\n')
                        state += 1
                    else:
                        mod_md_file.write(line)
                if state != 4:
                    print("Error!  File does not follow the lesson plan format.")
                    exit()


        # Generate the html
        subprocess.Popen([
            "pandoc",
            tmp_md_filename,
            "-o",
            tmp_html_filename,
        ]).wait()

        # Take the output html and turn it into a proper html file with our css.
        html_content = """
        <html>
        <head>
        <meta charset="utf-8" />
        <title>Untitled</title>
        <style type="text/css">{}</style>
        </head>
        <body>
        {}
        </body>
        """
        with open(tmp_html_filename) as html_file:
            html_file_contents = html_file.read()
            html_content = html_content.format(CSS_STYLE, html_file_contents)
        with open(tmp_html_filename, 'w') as html_file:
            html_file.write(html_content)
        
        # Generate the pdf
        subprocess.Popen(
            [
                "wkhtmltopdf",
                "-s",
                "A4",
                tmp_html_filename,
                pdf_filename,
            ],
        ).wait()

        os.remove(tmp_md_filename)
        os.remove(tmp_html_filename)
