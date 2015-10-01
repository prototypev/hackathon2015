from __future__ import print_function

import httplib2
import argparse

from apiclient import discovery
from apiclient import errors

from oauth2client import file
from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets


try:
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


CLIENT_SECRET_FILE = 'client_secret.json'
CREDENTIALS_FILE = 'gmail-python.json'
APPLICATION_NAME = 'Dream Killer'
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


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
    query = 'label:inbox'
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        # The response may need to be paged, depending on the total number of messages that need to be returned
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError, error:
        print('An error occurred: %s' % error)

