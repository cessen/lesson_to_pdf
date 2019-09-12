#!/usr/bin/env python3

import sys
import os
import subprocess

if __name__ == "__main__":
    md_filename = sys.argv[1]
    html_filename = md_filename.rsplit(".")[0] + ".html"
    pdf_filename = md_filename.rsplit(".")[0] + ".pdf"

    subprocess.Popen([
        "pandoc",
        "-s",
        "-M",
        "title:none",
        '--css=../plan.css',
        md_filename,
        "-o",
        html_filename,
    ]).wait()
    
    subprocess.Popen(
        [
            "wkhtmltopdf",
            "-s",
            "A4",
            html_filename,
            pdf_filename,
        ],
    ).wait()

    os.remove(html_filename)
