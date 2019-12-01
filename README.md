# Print Address

This program can be used to turn a TSV document containing mailing addresses into
a PDF file containing a table of these addresses. The format of the table can be
modified to match your label paper.

Example usage:
```bash
python print_address --width=1.5 --font-size=7 ~/Documents/addresses.tsv -o out.pdf
```

The input is a tab-separated file, where each line contains an address.
Most spreadsheet programs will export to this format. Tabs within
a line will be used as newlines in the output document.

```
print address [-h] [-o OUT] [--width WIDTH] [--height HEIGHT]
                     [--page-width PAGE_WIDTH] [--page-height PAGE_HEIGHT]
                     [--font-size FONT_SIZE] [--margin MARGIN] [--grid]
                     [--repeat REPEAT]
                     tsvfile

positional arguments:
  tsvfile               TSV file to parse.


optional arguments:
  -h, --help            show this help message and exit
  -o OUT, --out OUT     Output PDF file.
  --width WIDTH         Width of each cell
  --height HEIGHT       Height of each cell
  --page-width PAGE_WIDTH
                        Width of page
  --page-height PAGE_HEIGHT
                        Height of page
  --font-size FONT_SIZE
                        Font size
  --margin MARGIN       Margin of page
  --grid                Display grid between entries
  --repeat REPEAT       Number of times to repeat addresses
  ```
