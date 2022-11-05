import csv
from pathlib import Path

import openpyxl


def excel2csv(filename: Path, outdir: Path = '.') -> None:
    """ Create one csv file for each sheet in the workbook.

    Args:
        filename: excel filename to convert
        outdir: output directory
    """

    wb = openpyxl.load_workbook(str(filename))

    if not outdir.exists():
        outdir.mkdir(parents=True)

    for iws in wb.sheetnames:
        ws = wb[iws]
        fout = outdir / '{}.csv'.format(iws)
        with open(str(fout), newline='', mode='w') as csvfile:
            writer = csv.writer(csvfile)
            for row in ws.rows:
                writer.writerow([cell.value for cell in row])

    wb.close()


if __name__ == '__main__':
    input = Path('examples/iris-dataset.xlsx')
    outputs = Path('csvs')
    excel2csv(input, outputs)
