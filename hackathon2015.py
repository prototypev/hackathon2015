from flask import Flask
from flask import make_response
from StringIO import StringIO
import csv

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/csv')
def download_csv():
    csvList = "1,2,3,4"
    si = StringIO()
    cw = csv.writer(si)
    cw.writerows(csvList)
    print(cw)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


if __name__ == '__main__':
    app.run()
