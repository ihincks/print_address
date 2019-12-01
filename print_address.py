#!python3

import argparse
import csv

import reportlab
import reportlab.lib as rll
import reportlab.platypus
from reportlab.lib.pagesizes import letter, inch


class RowData:
    def __init__(self, *, n_cols):
        self.n_cols = n_cols
        self.rows = [[]]

    def add(self, entry):
        row = self.rows[-1]
        if len(row) == self.n_cols:
            row = []
            self.rows.append(row)
        row.append(entry.format())


class Entry:
    def __init__(self, lines, style):
        self.lines = lines
        self.style = style

    def format(self):
        lines = "<br/>".join(x.strip() for x in self.lines)
        return reportlab.platypus.Paragraph(lines, self.style)

parser = argparse.ArgumentParser(prog="print address")
parser.add_argument("tsvfile", help="TSV to parse.")
parser.add_argument("-o", "--out", default="addresses.pdf", help="Output PDF file.")

parser.add_argument("--width", default=2, help="Width of each cell")
parser.add_argument("--height", default=0.75, help="Height of each cell")
parser.add_argument("--page-width", default=8.5, help="Width of page")
parser.add_argument("--page-height", default=11, help="Height of page")
parser.add_argument("--font-size", default=8, help="Font size")
parser.add_argument("--margin", default=0.25, help="Margin of page")
parser.add_argument("--grid", action="store_true", help="Grid between entries")
parser.add_argument("--repeat", default=1, help="Number of times to repeat addresses")


if __name__ == "__main__":
    args = parser.parse_args()
    n_cols = int((args.page_width - 2 * args.margin) // args.width)

    # define style of each entry
    entry_style = rll.styles.ParagraphStyle(
        "small",
        parent=rll.styles.getSampleStyleSheet()["Normal"],
        fontSize=args.font_size,
        leading=args.font_size * 1.05,
        alignment=rll.enums.TA_CENTER
    )

    # parse and store data
    data = RowData(n_cols=n_cols)
    with open(args.tsvfile, "r") as f:
        for row in csv.reader(f, delimiter="\t", quotechar='"'):
            valid = row[0].lower() != "name"
            valid &= len(row[1]) > 0
            if valid:
                for _ in range(int(args.repeat)):
                    data.add(Entry(row, entry_style))

    # write the table
    style = [
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    if args.grid:
        style.append(("INNERGRID", (0, 0), (-1, -1), 0.1, rll.colors.black))
    table = reportlab.platypus.Table(
        data.rows,
        colWidths=args.width * inch,
        rowHeights=args.height * inch,
        style=reportlab.platypus.TableStyle(style),
    )

    # generate pdf
    doc = reportlab.platypus.SimpleDocTemplate(
        args.out,
        pagesize=(args.page_width * inch, args.page_height * inch),
        leftMargin=args.margin * inch,
        rightMargin=args.margin * inch,
        topMargin=args.margin * inch,
        bottomMargin=args.margin * inch,
    )
    doc.build([table])
