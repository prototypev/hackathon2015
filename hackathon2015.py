from flask import Flask
from flask import make_response
from StringIO import StringIO
from email_object import Email
import csv
import mongo_presistence

import gmailoauth

app = Flask(__name__)
db = mongo_presistence.get_db()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/crawl')
def crawl():
    messages = gmailoauth.crawl_inbox()
    return str(len(messages)) + ' emails crawled'


@app.route('/csv')
def download_csv():
    si = generate_csv_as_stringio(load_csv())
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


def generate_csv_as_stringio(emails):
    si = StringIO()
    for e in emails:
        si.write(str(e))
        si.write("\n")
    return si


def load_csv():
    emails = []
    with open('EMAIL.CSV', 'rb') as csvfile:
        reader = csv.reader(csvfile, skipinitialspace=True)
        for row in reader:
            emails.append(Email(row[7], row[8], row[9], row[5], row[10]))
    return emails

if __name__ == '__main__':
    app.debug = True
    app.run()
