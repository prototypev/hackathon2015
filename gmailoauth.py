from __future__ import print_function

import httplib2
import argparse
import re
import os

from apiclient import discovery
from apiclient import errors

from oauth2client import file
from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets

from email_object import Email


try:
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


CLIENT_SECRET_FILE = 'client_secret.json'
CREDENTIALS_FILE = 'gmail-python.json'
APPLICATION_NAME = 'Dream Killer'
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def revoke_credentials():
    credentials = get_credentials()
    credentials.revoke(httplib2.Http())
    print('Credentials revoked')


def get_credentials():
    store = file.Storage(CREDENTIALS_FILE)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + CREDENTIALS_FILE)
    return credentials


def crawl_inbox():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    user_id = 'me'
    query = 'label:inbox after:2010/06/01 before:2010/06/15'
    emails = []
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        bare_messages = []
        if 'messages' in response:
            bare_messages.extend(response['messages'])

        # The response may need to be paged, depending on the total number of messages that need to be returned
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            bare_messages.extend(response['messages'])

        for bareMessage in bare_messages:
            message_id = bareMessage.get('id')
            message = service.users().messages().get(userId=user_id, id=message_id).execute()
            email = parse_email(message)
            print(email)
            emails.append(email)
    except errors.HttpError, error:
        print('An error occurred: %s' % error)

    return emails


def parse_email(message):
    message_id = message.get('id')
    email = Email(message_id)
    email.date = message.get('internalDate')

    payload = message.get('payload')
    headers = payload.get('headers')

    for header in headers:
        header_name = header.get('name')
        header_value = header.get('value')

        if header_name == 'From':
            email.from_email = extract_email_and_name(header_value)
        elif header_name == 'Delivered-To':
            email.to_email = extract_email_and_name(header_value)
        elif header_name == 'Cc':
            email.cc_email = extract_email_and_name(header_value)

    return email


def extract_email_and_name(value):
    # TODO
    return value
