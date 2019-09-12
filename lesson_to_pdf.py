#!/usr/bin/env python3

import sys
import os
import subprocess
import string
import random


if __name__ == "__main__":
    md_filename = sys.argv[1]
    html_filename = md_filename.rsplit(".")[0] + ".html"
    pdf_filename = md_filename.rsplit(".")[0] + ".pdf"
    tmp_md_filename = ''.join(
        random.choices(
            string.ascii_lowercase + string.ascii_uppercase + string.digits,
            k=16)
        ) + ".md"

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
        "-s",
        "-M",
        "title:none",
        '--css=../plan.css',
        tmp_md_filename,
        "-o",
        html_filename,
    ]).wait()
    
    # Generate the pdf
    subprocess.Popen(
        [
            "wkhtmltopdf",
            "-s",
            "A4",
            html_filename,
            pdf_filename,
        ],
    ).wait()

    os.remove(tmp_md_filename)
    os.remove(html_filename)
