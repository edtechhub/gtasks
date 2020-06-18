from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']


class GTaskWrapper:
    def __init__(self):
        """Shows basic usage of the Tasks API.
        Prints the title and ID of the first 10 task lists.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('tasks', 'v1', credentials=creds)

    def get_lists(self):
        # Call the Tasks API
        results = self.service.tasklists().list(
            maxResults=100).execute()
        all_lists = results.get('items', [])
        while 'nextPageToken' in results:
            results = self.service.tasklists().list(
                pageToken=results['nextPageToken'], maxResults=100).execute()
            all_lists += results.get('items', [])
        return all_lists

    def get_tasks(self, list_id, include_hidden):
        results = self.service.tasks().list(maxResults=100, tasklist=list_id,
                                            showHidden=include_hidden).execute()
        all_tasks = results.get('items', [])
        while 'nextPageToken' in results:
            results = self.service.tasks().list(
                pageToken=results['nextPageToken'], maxResults=100, tasklist=list_id, showHidden=include_hidden).execute()
            all_tasks += results.get('items', [])
        return all_tasks
