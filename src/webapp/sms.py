import sys
import requests
import urllib

apikey = '9c0d87167d2ee052f140769728452a78'
sendername = 'Stephen Nacion'


def send_message(message, number):
    print('Sending Message...')
    params = (
        ('apikey', apikey),
        ('sendername', sendername),
        ('message', message),
        ('number', number)
    )
    path = 'https://semaphore.co/api/v4/messages?' + \
        urllib.parse.urlencode(params)
    requests.post(path)
    print('Message Sent!')


if __name__ == '__main__':
    message = sys.argv[1]
    number = sys.argv[2]
    send_message(message, number)
