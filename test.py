__author__ = 'sen.li'

from flask import Flask
from StringIO import StringIO
import csv


def generate_csv():
    csvList = "1,2,3,4"
    si = StringIO()
    cw = csv.writer(si)
    cw.writerows(csvList)
    print(cw)
    output = Flask.make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


if __name__ == '__main__':
    generate_csv()