from flask import Flask
from flask import make_response
from flask import render_template
from StringIO import StringIO
from email_object import Email
import csv
import mongo_presistence

import gmailoauth

app = Flask(__name__)
db = mongo_presistence.get_db()


@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/doOauth')
def do_oauth():
    gmailoauth.get_credentials()
    return 'OAuth done'


@app.route('/revokeOauth')
def revoke_oauth():
    gmailoauth.revoke_credentials()
    return 'OAuth revoked'


@app.route('/crawl')
def crawl():
    emails = gmailoauth.crawl_inbox()

    mongo_presistence.delete_emails(db)
    for email in emails:
        json = email.to_json()
        mongo_presistence.insert_email(db, json)

    return str(len(emails)) + ' emails crawled'


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
        try:
            si.write(str(e))
            si.write("\n")
        except Exception as e:
            print e
    return si


def load_csv():
    emails = mongo_presistence.get_email_collection(db).find()
    result = []
    for email in emails:
        print email
        try:
            result.append(email['from_email'] + ',' + email['to_email'] + ',' + email['date'])
        except Exception as e:
            print e

    # emails = []
    # with open('EMAIL.CSV', 'rb') as csvfile:
    #     reader = csv.reader(csvfile, skipinitialspace=True)
    #     for row in reader:
    #         emails.append(Email(row[7], row[8], row[9], row[5], row[10]))
    return result


if __name__ == '__main__':
    app.debug = True
    app.run()
