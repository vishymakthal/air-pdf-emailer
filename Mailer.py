from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json
import datetime

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors


RAW_DATA = [[94, datetime.datetime(2018, 9, 27, 15, 37, 3)], [93, datetime.datetime(2018, 9, 27, 15, 1, 57)], [-1, datetime.datetime(2018, 9, 27, 15, 22, 2)], [-1, datetime.datetime(2018, 9, 27, 15, 57, 9)], [93, datetime.datetime(2018, 9, 27, 15, 32, 4)], [-1, datetime.datetime(2018, 9, 27, 15, 17, 1)], [93, datetime.datetime(2018, 9, 27, 15, 26, 59)], [-1, datetime.datetime(2018, 9, 27, 15, 6, 57)], [101, datetime.datetime(2018, 9, 27, 15, 52, 5)], [101, datetime.datetime(2018, 9, 27, 15, 47, 5)], [116, datetime.datetime(2018, 9, 27, 15, 42, 3)], [94, datetime.datetime(2018, 9, 27, 15, 11, 59)], [97, datetime.datetime(2018, 9, 27, 16, 17, 8)], [113, datetime.datetime(2018, 9, 27, 16, 57, 15)], [153, datetime.datetime(2018, 9, 27, 16, 7, 9)], [105, datetime.datetime(2018, 9, 27, 16, 27, 9)], [142, datetime.datetime(2018, 9, 27, 17, 2, 14)], [162, datetime.datetime(2018, 9, 27, 16, 47, 11)], [129, datetime.datetime(2018, 9, 27, 16, 42, 10)], [-1, datetime.datetime(2018, 9, 27, 21, 43, 3)], [120, datetime.datetime(2018, 9, 27, 17, 17, 17)], [153, datetime.datetime(2018, 9, 27, 16, 52, 12)], [116, datetime.datetime(2018, 9, 27, 16, 32, 9)], [119, datetime.datetime(2018, 9, 27, 20, 52, 55)], [160, datetime.datetime(2018, 9, 27, 16, 12, 9)], [116, datetime.datetime(2018, 9, 27, 16, 37, 10)], [147, datetime.datetime(2018, 9, 27, 21, 28, 2)], [111, datetime.datetime(2018, 9, 27, 21, 7, 58)], [-1, datetime.datetime(2018, 9, 27, 20, 42, 59)], [-1, datetime.datetime(2018, 9, 27, 21, 33, 3)], [-1, datetime.datetime(2018, 9, 27, 21, 38, 3)], [186, datetime.datetime(2018, 9, 27, 21, 48, 5)], [117, datetime.datetime(2018, 9, 27, 16, 22, 9)], [115, datetime.datetime(2018, 9, 27, 21, 2, 59)], [-1, datetime.datetime(2018, 9, 27, 22, 18, 9)], [-1, datetime.datetime(2018, 9, 27, 22, 3, 6)], [132, datetime.datetime(2018, 9, 27, 22, 48, 16)], [-1, datetime.datetime(2018, 9, 27, 22, 13, 8)], [123, datetime.datetime(2018, 9, 27, 16, 2, 8)], [-1, datetime.datetime(2018, 9, 27, 21, 12, 59)], [131, datetime.datetime(2018, 9, 27, 23, 28, 22)], [110, datetime.datetime(2018, 9, 27, 22, 38, 13)], [125, datetime.datetime(2018, 9, 27, 22, 43, 15)], [124, datetime.datetime(2018, 9, 27, 23, 8, 19)], [136, datetime.datetime(2018, 9, 27, 17, 7, 15)], [122, datetime.datetime(2018, 9, 27, 20, 47, 55)], [120, datetime.datetime(2018, 9, 27, 20, 57, 56)], [121, datetime.datetime(2018, 9, 27, 17, 12, 18)], [114, datetime.datetime(2018, 9, 27, 22, 33, 10)], [93, datetime.datetime(2018, 9, 27, 23, 43, 25)], [90, datetime.datetime(2018, 9, 27, 23, 38, 25)], [185, datetime.datetime(2018, 9, 27, 23, 13, 20)], [-1, datetime.datetime(2018, 9, 27, 21, 58, 7)], [194, datetime.datetime(2018, 9, 27, 23, 33, 24)], [155, datetime.datetime(2018, 9, 27, 23, 23, 21)], [-1, datetime.datetime(2018, 9, 27, 22, 28, 9)], [109, datetime.datetime(2018, 9, 27, 21, 18)], [-1, datetime.datetime(2018, 9, 27, 22, 23, 8)], [127, datetime.datetime(2018, 9, 27, 22, 58, 17)], [117, datetime.datetime(2018, 9, 27, 23, 3, 17)], [-1, datetime.datetime(2018, 9, 27, 22, 8, 8)], [93, datetime.datetime(2018, 9, 27, 23, 48, 26)], [90, datetime.datetime(2018, 9, 27, 23, 58, 30)], [166, datetime.datetime(2018, 9, 27, 21, 23, 3)], [176, datetime.datetime(2018, 9, 27, 23, 18, 21)], [93, datetime.datetime(2018, 9, 27, 23, 53, 28)], [122, datetime.datetime(2018, 9, 27, 22, 53, 17)], [200, datetime.datetime(2018, 9, 27, 21, 53, 7)]]

def SendMessage(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """

  msgRoot = MIMEMultipart('related')
  msgRoot['subject'] = subject
  msgRoot['from'] = sender
  msgRoot['to'] = to

  msgAlternative = MIMEMultipart('alternative')
  msgRoot.attach(msgAlternative)

  msgText = MIMEText(message_text, 'html')
  msgAlternative.attach(msgText)
  return {'raw': base64.urlsafe_b64encode(msgRoot.as_string().encode('ASCII')).decode()}


SCOPES = 'https://mail.google.com/'

if __name__ == '__main__':


    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


    user_id = 'vishy787@gmail.com'

    message ='''

        <html><h3> AIR-FC-Report (''' + str(datetime.date.today()) + ''') </h3>

            <h4> Raw </h4>
            <table>
            <tr>
                <td>Fish Count</td><td>Timestamp</td>
            </tr>
            <tbody>'''

    for dl in RAW_DATA:
        line = "<tr>"

        line += '<td>{}</td>'.format(dl[0])
        line += '<td>{}</td>'.format(dl[1])
        line += '</tr>'
        message += line

    message += "</tbody></table></html>"

    msg =CreateMessage(user_id, 'ppauan@ncsu.edu', '[TEST] AIR Fish Count/Density', message)
    SendMessage(service, user_id, msg)
